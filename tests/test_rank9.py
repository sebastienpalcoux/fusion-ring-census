"""Rank-nine launch gates and exact known-ring fixtures (no census run)."""
import contextlib
import importlib.util
import io
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load('rank9_runner', 'code/run_census.py')
launcher = load('rank9_launcher', 'scripts/run_laptop.py')
exporter = load('rank9_exporter', 'code/export_tables.py')


class RankNineTests(unittest.TestCase):
    def test_truncated_enumerator_output_cannot_be_certified(self):
        with tempfile.TemporaryDirectory() as td:
            def fake(cmd, **kwargs):
                if '-o' in cmd:
                    Path(cmd[cmd.index('-o')+1]).write_text('mock')
                else:
                    kwargs['stderr'].write('FINAL bound 1 complete 1 jobs 1 / 1 classes 1 seconds 0 counts 1\n')
                    # Deliberately missing the one ring claimed by the engine.
                return subprocess.CompletedProcess(cmd,0)
            argv=['driver','--rank','9','--bound','1','--verify','--out',td+'/out']
            with patch.object(sys,'argv',argv),patch.object(runner.subprocess,'run',side_effect=fake), \
                    contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(runner.main(),1)
            state=json.loads(Path(td,'out/run.json').read_text())
            self.assertFalse(state['complete'])
            self.assertFalse(state['verified'])
            self.assertIn('output does not match enumerator totals',state['error'])
            self.assertNotIn('counts',state)

    def test_launcher_accepts_rank9_and_preserves_verification(self):
        # Hide only the distribution inventory: the release writer regenerates it
        # after edits; these tests do not weaken checksum checking in the launcher.
        exists = Path.exists
        def without_inventory(path):
            return False if path == ROOT / 'SHA256SUMS' else exists(path)
        with tempfile.TemporaryDirectory() as td:
            argv = ['launcher', '--rank', '9', '--bound', '1', '--threads', '2', '--output-dir', td]
            with patch.dict(os.environ, {}, clear=True), patch.object(sys, 'argv', argv), \
                    patch.object(Path, 'exists', without_inventory), \
                    patch.object(launcher.subprocess, 'run', return_value=subprocess.CompletedProcess([], 3)) as run, \
                    contextlib.redirect_stdout(io.StringIO()) as stdout, contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(launcher.main(), 3)
            cmd = run.call_args.args[0]
            self.assertEqual(cmd[cmd.index('--rank') + 1], '9')
            self.assertEqual(cmd[cmd.index('--bound') + 1], '1')
            self.assertIn('--verify', cmd)
            self.assertIn('--local-unlimited', cmd)
            self.assertNotIn('No released rank-9 baseline', stdout.getvalue())
            self.assertFalse(list(Path(td).rglob('*.zip')))

    def test_driver_plans_all_five_strata_and_timeout_is_incomplete(self):
        with tempfile.TemporaryDirectory() as td:
            commands = []
            def fake(cmd, **kwargs):
                if '-o' in cmd:
                    Path(cmd[cmd.index('-o') + 1]).write_text('mock')
                    return subprocess.CompletedProcess(cmd, 0)
                commands.append((cmd, kwargs))
                raise subprocess.TimeoutExpired(cmd, None)
            argv = ['driver', '--rank', '9', '--bound', '1', '--local-unlimited', '--verify', '--out', td + '/out']
            with patch.dict(os.environ, {}, clear=True), patch.object(sys, 'argv', argv), \
                    patch.object(runner.subprocess, 'run', side_effect=fake), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(runner.main(), 3)
            state = json.loads(Path(td, 'out/run.json').read_text())
            self.assertEqual(state['expected_strata'], ['pairs1', 'pairs2', 'pairs3', 'pairs4', 'selfdual'])
            self.assertFalse(state['complete'])
            self.assertFalse(state['verified'])
            self.assertNotIn('counts', state)
            self.assertIsNone(commands[0][1]['timeout'])
            self.assertIn('inf', commands[0][0])
            self.assertFalse(list(Path(td).rglob('*.zip')))

    def test_rank9_bound16_is_rejected_by_both_entry_points(self):
        for module, extra in ((launcher, []), (runner, ['--out', 'unused'])):
            with self.subTest(module=module.__name__), patch.dict(os.environ, {}, clear=True), \
                    patch.object(sys, 'argv', ['entry', '--rank', '9', '--bound', '16'] + extra), \
                    patch.object(module.subprocess, 'run') as run, contextlib.redirect_stderr(io.StringIO()), \
                    self.assertRaises(SystemExit):
                module.main()
            run.assert_not_called()

    def test_absent_baseline_is_allowed_only_for_new_supported_ranks(self):
        with patch.object(Path, 'read_text', return_value=json.dumps({'ranks': {}})):
            for rank in (9,10,11):
                self.assertEqual(runner.check_local_prefix(rank, 1, {'1': 123}), 0)
            with self.assertRaisesRegex(ValueError, 'baseline is missing'):
                runner.check_local_prefix(8, 1, {'1': 123})
        with self.assertRaisesRegex(ValueError, 'baseline is missing'):
            launcher.package_result(Path('unused'), Path('unused.zip'), 8, 1, None)

    def package_state(self):
        return {'rank': 9, 'bound': 1, 'complete': True, 'verified': True,
                'existing_prefix_checked_through': 0,
                'runs': [{'name': name, 'returncode': 0} for name in ('pairs1', 'pairs2', 'pairs3', 'pairs4', 'selfdual')],
                'counts': {'1': 2}, 'classes': 2, 'code_sha256': 'mock'}

    def test_packaging_rejects_missing_stratum_failed_run_and_false_prefix(self):
        cases = []
        missing = self.package_state(); missing['runs'].pop(3); cases.append(missing)
        failed = self.package_state(); failed['runs'][3]['returncode'] = 3; cases.append(failed)
        prefix = self.package_state(); prefix['existing_prefix_checked_through'] = 1; cases.append(prefix)
        incomplete = self.package_state(); incomplete['complete'] = False; cases.append(incomplete)
        unverified = self.package_state(); unverified['verified'] = False; cases.append(unverified)
        for index, state in enumerate(cases):
            with self.subTest(case=index), tempfile.TemporaryDirectory() as td:
                out = Path(td)
                (out / 'run.json').write_text(json.dumps(state))
                with self.assertRaises(ValueError):
                    launcher.package_result(out, out / 'result.zip', 9, 1, None)
                self.assertFalse((out / 'result.zip').exists())

    def test_packaging_records_no_baseline_without_inventing_counts(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td)
            (out / 'run.json').write_text(json.dumps(self.package_state()))
            for name in ('counts.csv', 'parameters.txt.gz', 'FusionRingMultiplicationTables.txt.gz'):
                (out / name).write_text('mock')
            (out / 'logs').mkdir(); (out / 'independent_check').mkdir()
            (out / 'independent_check/summary.json').write_text('{}')
            archive = out / 'result.zip'
            launcher.package_result(out, archive, 9, 1, None)
            with zipfile.ZipFile(archive) as z:
                provenance = json.loads(z.read('rank9_M1_verified/laptop_provenance.json'))
                self.assertIsNone(provenance['baseline'])
                self.assertEqual(provenance['baseline_status'], 'no released rank-9 baseline')
                self.assertIn('rank9_M1_verified/SHA256SUMS', z.namelist())

    def test_all_systems_cover_the_tensor_and_fit_engine_limits(self):
        for pairs in range(5):
            name = f'rank9_pairs{pairs}.txt' if pairs else 'system9sd.txt'
            with self.subTest(pairs=pairs):
                system = json.loads((ROOT / 'systems' / (name + '.json')).read_text())
                with (ROOT / 'systems' / name).open() as handle:
                    rank, p, nv, ne, np = map(int, handle.readline().split())
                self.assertEqual((rank, p), (9, pairs))
                self.assertEqual((nv, ne), (len(system['orbits']), len(system['equations'])))
                self.assertEqual(np, -1 if system.get('symmetry_format') else len(system['perms']))
                self.assertLessEqual(nv, 128)
                self.assertLessEqual(ne, 2048)
                triples = [tuple(t) for orbit in system['orbits'] for t in orbit]
                self.assertEqual(len(triples), 8**3)
                self.assertEqual(len(set(triples)), 8**3)
                self.assertEqual(sum(i != d for i, d in enumerate(system['dual'])), 2 * pairs)
                self.assertEqual(system['symmetry_order'], 2**pairs * math.factorial(pairs) * math.factorial(8 - 2*pairs))

    def test_rank10_and_11_systems_and_cyclic_export(self):
        for rank in (10, 11):
            expected = json.loads((ROOT/'results/census.json').read_text())['ranks'][str(rank)]['counts']['1']
            self.assertEqual(runner.check_local_prefix(rank, 1, {'1': expected}), 1)
            with self.assertRaisesRegex(ValueError, 'prefix mismatch'):
                runner.check_local_prefix(rank, 1, {'1': expected+1})
            for pairs in range((rank-1)//2 + 1):
                name = f'rank{rank}_pairs{pairs}.txt.json' if pairs else f'system{rank}sd.txt.json'
                system = json.loads((ROOT / 'systems' / name).read_text())
                self.assertEqual(system['symmetry_order'], 2**pairs * math.factorial(pairs) * math.factorial(rank-1-2*pairs))
                triples = [tuple(t) for orbit in system['orbits'] for t in orbit]
                self.assertEqual(len(triples), (rank-1)**3)
                self.assertEqual(len(set(triples)), (rank-1)**3)
            # Consecutive inverse pairs, followed by the involution for even n.
            pairs = (rank-1)//2
            labels = [0] + [v for i in range(1, pairs+1) for v in (i, rank-i)]
            if rank % 2 == 0:
                labels.append(rank//2)
            tensor = [[[int((labels[i]+labels[j]) % rank == labels[k]) for k in range(rank)] for j in range(rank)] for i in range(rank)]
            system = json.loads((ROOT / 'systems' / f'rank{rank}_pairs{pairs}.txt.json').read_text())
            values = []
            for orbit in system['orbits']:
                possible = {tensor[i][j][k] for i,j,k in orbit}
                self.assertEqual(len(possible), 1)
                values.append(possible.pop())
            value = lambda index: values[index] if index >= 0 else int(index == -1)
            for equation in system['equations']:
                self.assertEqual(sum(c * value(a) * value(b) for a,b,c in equation), 0)
            self.assertEqual(exporter.tensor(rank, str(pairs)+' '+' '.join(map(str,values)), ROOT/'systems'), tensor)

    def test_rank10_and_11_launcher_and_driver_acceptance(self):
        exists = Path.exists
        def without_inventory(path):
            return False if path == ROOT / 'SHA256SUMS' else exists(path)
        for rank in (10, 11):
            with self.subTest(rank=rank), tempfile.TemporaryDirectory() as td:
                argv = ['entry', '--rank', str(rank), '--bound', '1', '--output-dir', td]
                with patch.dict(os.environ, {}, clear=True), patch.object(sys, 'argv', argv), \
                        patch.object(Path, 'exists', without_inventory), \
                        patch.object(launcher.subprocess, 'run', return_value=subprocess.CompletedProcess([], 3)) as run, \
                        contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(launcher.main(), 3)
                self.assertEqual(run.call_args.args[0][run.call_args.args[0].index('--rank')+1], str(rank))
                def fake(cmd, **kwargs):
                    if '-o' in cmd:
                        Path(cmd[cmd.index('-o')+1]).write_text('mock')
                        return subprocess.CompletedProcess(cmd, 0)
                    raise subprocess.TimeoutExpired(cmd, None)
                argv = ['entry', '--rank', str(rank), '--bound', '1', '--local-unlimited', '--verify', '--out', td+'/out']
                with patch.dict(os.environ, {}, clear=True), patch.object(sys, 'argv', argv), \
                        patch.object(runner.subprocess, 'run', side_effect=fake), \
                        contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                    self.assertEqual(runner.main(), 3)
                state = json.loads(Path(td, 'out/run.json').read_text())
                self.assertEqual(state['expected_strata'], [f'pairs{p}' for p in range(1,(rank-1)//2+1)]+['selfdual'])
                self.assertFalse(state['complete'])

    def test_known_rank9_rings_export_exactly_and_satisfy_generated_equations(self):
        # Cyclic group of order nine, labelled so inverses are consecutive pairs.
        labels = [0, 1, 8, 2, 7, 3, 6, 4, 5]
        cyclic = [[[int((labels[i] + labels[j]) % 9 == labels[k]) for k in range(9)] for j in range(9)] for i in range(9)]
        # Ising fusion rules: 1 is the unit, g^2=1, gx=x, x^2=1+g.
        ising = [[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                 [[0, 1, 0], [1, 0, 0], [0, 0, 1]],
                 [[0, 0, 1], [0, 0, 1], [1, 1, 0]]]
        square = [[[ising[i//3][j//3][k//3] * ising[i%3][j%3][k%3] for k in range(9)] for j in range(9)] for i in range(9)]
        for pairs, tensor in ((4, cyclic), (0, square)):
            with self.subTest(pairs=pairs):
                name = f'rank9_pairs{pairs}.txt.json' if pairs else 'system9sd.txt.json'
                system = json.loads((ROOT / 'systems' / name).read_text())
                values = []
                for orbit in system['orbits']:
                    possible = {tensor[i][j][k] for i, j, k in orbit}
                    self.assertEqual(len(possible), 1)
                    values.append(possible.pop())
                value = lambda index: values[index] if index >= 0 else int(index == -1)
                for equation in system['equations']:
                    self.assertEqual(sum(c * value(a) * value(b) for a, b, c in equation), 0)
                line = str(pairs) + ' ' + ' '.join(map(str, values))
                self.assertEqual(exporter.tensor(9, line, ROOT / 'systems'), tensor)
                with tempfile.TemporaryDirectory() as td:
                    source, target = Path(td) / 'params.txt', Path(td) / 'tables.txt'
                    source.write_text(line + '\n')
                    argv = ['export', '--rank', '9', '--input', str(source), '--output', str(target), '--systems', str(ROOT / 'systems')]
                    with patch.object(sys, 'argv', argv), contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(exporter.main(), 0)
                    self.assertEqual(json.loads(target.read_text().replace('{', '[').replace('}', ']')), tensor)


if __name__ == '__main__':
    unittest.main()
