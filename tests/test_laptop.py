"""Mock numerical subprocesses: laptop scope, completeness, prefix and packaging gates."""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec=importlib.util.spec_from_file_location(name, ROOT/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod
runner=load('local_runner','code/run_census.py')
launcher=load('local_launcher','scripts/run_laptop.py')

class LaptopTests(unittest.TestCase):
    def test_all_ranks_without_python_or_cpp_clock_limits(self):
        for rank in range(3,9):
            with self.subTest(rank=rank), tempfile.TemporaryDirectory() as td:
                commands=[]
                def fake(cmd, **kw):
                    if '-o' in cmd:
                        Path(cmd[cmd.index('-o')+1]).write_text('mock');return subprocess.CompletedProcess(cmd,0)
                    commands.append((cmd,kw))
                    raise subprocess.TimeoutExpired(cmd,None)
                argv=['driver','--rank',str(rank),'--bound','2','--local-unlimited','--verify','--out',td+'/out']
                with patch.dict(os.environ,{},clear=True), patch.object(sys,'argv',argv), patch.object(runner.subprocess,'run',side_effect=fake), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(runner.main(),3)
                self.assertIsNone(commands[0][1]['timeout'])
                if rank>=6:self.assertIn('inf',commands[0][0])
                state=json.loads(Path(td+'/out/run.json').read_text(),parse_constant=lambda s:self.fail('Nonstandard JSON: '+s))
                self.assertIsNone(state['enumeration_budget_seconds']);self.assertFalse(state['complete'])
                self.assertFalse(list(Path(td).rglob('*.zip')))

    def test_budget_combinations_caps_and_github_are_rejected(self):
        base=['driver','--rank','6','--bound','8','--local-unlimited','--verify','--out','unused']
        for extra in (['--seconds','100'],['--deadline','100'],['--rank6-m7-max'],['--rank','3','--bound','1001'],['--rank','5','--bound','33'],['--rank','7','--bound','16']):
            with self.subTest(extra=extra), patch.dict(os.environ,{},clear=True), patch.object(sys,'argv',base+extra), patch.object(runner.subprocess,'run') as run, contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):runner.main()
            run.assert_not_called()
        with patch.dict(os.environ,{'GITHUB_ACTIONS':'true'}), patch.object(sys,'argv',base), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):runner.main()
        with patch.dict(os.environ,{},clear=True), patch.object(sys,'argv',[x for x in base if x!='--verify']), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):runner.main()

    def test_prefix_every_rank_and_shorter_reproduction(self):
        data=json.loads((ROOT/'results/census.json').read_text())
        for rank in range(3,9):
            baseline=data['ranks'][str(rank)];counts=dict(baseline['counts']);bound=baseline['bound']
            self.assertEqual(runner.check_local_prefix(rank,bound,counts),bound)
            self.assertEqual(runner.check_local_prefix(rank,1,{'1':counts['1']}),1)
            counts['1']+=1
            with self.assertRaisesRegex(ValueError,'prefix mismatch'):runner.check_local_prefix(rank,bound,counts)

    def test_parallel_partition_stays_within_job_cap(self):
        for bound in range(1,16):
            depth=runner.parallel_depth(bound)
            self.assertLessEqual((bound+1)**depth,2000000)
            self.assertEqual(depth,6 if bound<=10 else 5)

    def test_launcher_all_ranks_pass_correct_bound_and_verification(self):
        for rank in range(3,9):
            with self.subTest(rank=rank), tempfile.TemporaryDirectory() as td:
                args=['launcher','--rank',str(rank),'--mult','2','--threads','3','--output-dir',td]
                with patch.dict(os.environ,{},clear=True),patch.object(sys,'argv',args),patch.object(launcher.subprocess,'run',return_value=subprocess.CompletedProcess([],3)) as run,contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(launcher.main(),3)
                cmd=run.call_args.args[0];self.assertEqual(cmd[cmd.index('--rank')+1],str(rank));self.assertIn('--verify',cmd);self.assertIn('--local-unlimited',cmd)
                self.assertFalse(list(Path(td).glob('*.zip')))

    def test_packaging_rejects_incomplete_and_prefix_mismatch(self):
        baseline={'bound':1,'counts':{'1':39}}
        for complete, count in ((False,39),(True,40)):
            with tempfile.TemporaryDirectory() as td:
                p=Path(td);state={'rank':6,'bound':1,'complete':complete,'verified':True,'existing_prefix_checked_through':1,'runs':[{'name':n,'returncode':0} for n in ('pairs1','pairs2','selfdual')],'counts':{'1':count},'classes':count}
                (p/'run.json').write_text(json.dumps(state))
                with self.assertRaises(ValueError):launcher.package_result(p,p/'result.zip',6,1,baseline)
                self.assertFalse((p/'result.zip').exists())

    def test_success_archive_excludes_partial_and_compiler_files(self):
        import zipfile
        with tempfile.TemporaryDirectory() as td:
            p=Path(td);out=p/'out';out.mkdir()
            state={'rank':3,'bound':1,'complete':True,'verified':True,'existing_prefix_checked_through':1,'runs':[{'name':'all','returncode':0}],'counts':{'1':2},'classes':2,'code_sha256':'mock'}
            (out/'run.json').write_text(json.dumps(state))
            for n in ('counts.csv','parameters.txt.gz','FusionRingMultiplicationTables.txt.gz'):(out/n).write_text('mock')
            for n in ('logs','build','diagnostics','independent_check'):(out/n).mkdir()
            (out/'build/executable').write_text('exclude');(out/'diagnostics/partial.txt').write_text('exclude')
            (out/'independent_check/tables.deduplicated').write_text('exclude');(out/'independent_check/summary.json').write_text('{}')
            launcher.package_result(out,p/'result.zip',3,1,{'bound':1,'counts':{'1':2}})
            with zipfile.ZipFile(p/'result.zip') as z:
                names=z.namelist();self.assertTrue(any(x.endswith('SHA256SUMS') for x in names));self.assertFalse(any('partial' in x or 'deduplicated' in x or 'executable' in x for x in names))

if __name__=='__main__':unittest.main()
