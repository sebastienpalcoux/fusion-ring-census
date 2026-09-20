"""Budget/status regression tests: mock every numerical subprocess."""
import contextlib
import csv
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

frontier = load('campaign_frontier', 'scripts/extend_census.py')
runner = load('campaign_runner', 'code/run_census.py')

class CampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / 'campaign'
        # Historical budget tests use a fixed baseline, independent of later releases.
        fixture = Path(self.temp.name) / 'repository'
        (fixture/'results').mkdir(parents=True)
        data = json.loads((ROOT/'results/census.json').read_text())
        six = data['ranks']['6']
        six.update(bound=6, classes=5799, counts={str(k): v for k, v in enumerate([39,154,384,872,1582,2768],1)})
        (fixture/'results/census.json').write_text(json.dumps(data))
        root_patch = patch.object(frontier, 'ROOT', fixture)
        root_patch.start()
        self.addCleanup(root_patch.stop)
        self.now = 100.0
        self.commands = []
        self.environment = patch.dict(os.environ, {'GITHUB_RUN_ATTEMPT': '1'})
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def invoke(self, *args):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return frontier.main(['--rank', '6', '--seconds', '4200', '--threads', '2', '--out', str(self.out), *args])

    def fake_process(self, behaviors):
        owner = self
        class FakeProcess:
            def __init__(self, cmd, **kwargs):
                owner.commands.append(cmd)
                self.behavior = behaviors[len(owner.commands) - 1]
                self.pid = 12345
                self.path = Path(cmd[cmd.index('--out') + 1])
                bound = int(cmd[cmd.index('--bound') + 1])
                baseline = json.loads((frontier.ROOT / 'results/census.json').read_text())['ranks']['6']
                self.path.mkdir()
                (self.path / 'logs').mkdir()
                (self.path / 'logs/selfdual.log').write_text('mock per-duality evidence\n')
                (self.path / 'diagnostics').mkdir()
                (self.path / 'diagnostics/partial.parameters.txt').write_text('never upload')
                checkdir = self.path / 'independent_check'
                checkdir.mkdir()
                (checkdir / 'FusionRingMultiplicationTables.deduplicated').write_text('redundant/possibly partial tensor copy')
                state = {'rank': 6, 'bound': bound, 'phase': 'enumeration:selfdual', 'complete': False, 'verified': False}
                if self.behavior in ('complete', 'prefix_mismatch'):
                    counts = dict(baseline['counts'])
                    counts.update({str(m): 1 for m in range(baseline['bound'] + 1, bound + 1)})
                    if self.behavior == 'prefix_mismatch':
                        counts['1'] += 1
                    state.update(complete=True, verified=True, classes=sum(counts.values()), counts=counts,
                                 runs=[{'name': x, 'returncode': 0} for x in frontier.expected_strata(6)])
                    check = {'duplicates': 0, 'distinct_rings': state['classes'], 'input_records': state['classes'],
                             'associativity_checked': True, 'canonical_mode': 'all unit-fixing permutations'}
                    (checkdir / 'summary.json').write_text(json.dumps(check))
                    with (checkdir / 'counts.csv').open('w') as f:
                        f.write('rank,multiplicity,distinct_rings\n')
                        for k, v in counts.items():
                            f.write(f'6,{k},{v}\n')
                    for filename in ('counts.csv', 'parameters.txt.gz', 'FusionRingMultiplicationTables.txt.gz'):
                        (self.path / filename).write_text('mock candidate bytes; no mathematical computation')
                    # Real successful runs have already removed the partial-output directory.
                    import shutil
                    shutil.rmtree(self.path / 'diagnostics')
                elif self.behavior == 'timeout':
                    state.update(failure_kind='budget_exhausted', error='selfdual did not finish')
                elif self.behavior == 'error':
                    state.update(failure_kind='error', error='mock invalid tensor')
                if self.behavior != 'missing_report':
                    (self.path / 'run.json').write_text(json.dumps(state))
                kwargs['stdout'].write('mock child log\n')
            def wait(self, timeout=None):
                owner.now += 600
                if self.behavior == 'parent_timeout':
                    raise subprocess.TimeoutExpired(owner.commands[-1], timeout)
                return 0 if self.behavior in ('complete', 'prefix_mismatch') else (3 if self.behavior == 'timeout' else 1)
        return FakeProcess

    def run_mocked(self, behaviors, *args):
        with patch.object(frontier.time, 'monotonic', side_effect=lambda: self.now), \
             patch.object(frontier.subprocess, 'Popen', self.fake_process(behaviors)), \
             patch.object(frontier, 'stop_group') as stop:
            rc = self.invoke(*args)
            self.cleanup_calls = stop.call_count
        return rc, json.loads((self.out / 'frontier.json').read_text())

    def test_full_long_budget_and_next_baseline_bound(self):
        rc, report = self.run_mocked(['timeout'])
        self.assertEqual(rc, 0)
        self.assertEqual(report['starting_bound'], 7)
        self.assertEqual(report['outcome'], 'no_extension_within_budget')
        cmd = self.commands[0]
        self.assertGreater(float(cmd[cmd.index('--seconds') + 1]), 3600)
        self.assertLess(float(cmd[cmd.index('--seconds') + 1]), 4200)
        self.assertIn('--verify', cmd)
        self.assertFalse((self.out / 'best').exists())
        self.assertTrue((self.out / 'diagnostics/attempt_M7/logs/selfdual.log').is_file())
        self.assertFalse(list(self.out.rglob('*.deduplicated')))
        self.assertFalse(list(self.out.rglob('partial.parameters.txt')))

    def test_max_rank6_campaign_uses_nearly_six_hours_and_stops_at_seven(self):
        rc, report = self.run_mocked(['complete'], '--rank6-m7-max', '--seconds', '21300')
        self.assertEqual(rc, 0)
        self.assertEqual(report['campaign'], 'rank6-m7-max')
        self.assertEqual(report['best_verified_bound'], 7)
        self.assertEqual(report['max_bound'], 7)
        self.assertEqual(len(self.commands), 1)  # No multiplicity-eight search.
        cmd = self.commands[0]
        self.assertIn('--rank6-m7-max', cmd)
        self.assertEqual(float(cmd[cmd.index('--seconds') + 1]), 21177)
        self.assertEqual(float(cmd[cmd.index('--deadline') + 1]), 21397)

    def test_max_rank6_campaign_rejects_wrong_scope_and_unbounded_allowance(self):
        with patch.object(frontier.subprocess, 'Popen') as process:
            for args in (['--rank', '5'], ['--start-bound', '8'], ['--max-bound', '8'],
                         ['--seconds', '21301'], ['--seconds', 'nan'], ['--seconds', 'inf']):
                with self.subTest(args=args), self.assertRaises(SystemExit):
                    self.invoke('--rank6-m7-max', '--seconds', '21300', *args)
            process.assert_not_called()

    def test_next_attempt_uses_only_remaining_budget_and_retains_best(self):
        rc, report = self.run_mocked(['complete', 'timeout'])
        self.assertEqual(rc, 0)
        self.assertEqual(report['outcome'], 'verified_extension')
        self.assertEqual(report['best_verified_bound'], 7)
        first, second = self.commands
        self.assertEqual(first[first.index('--deadline') + 1], second[second.index('--deadline') + 1])
        self.assertLess(float(second[second.index('--seconds') + 1]), float(first[first.index('--seconds') + 1]))
        self.assertEqual(first[first.index('--build-dir') + 1], second[second.index('--build-dir') + 1])
        self.assertEqual(json.loads((self.out / 'best/run.json').read_text())['existing_prefix_checked_through'], 6)
        self.assertEqual(report['attempts'][1]['bound'], 8)
        self.assertFalse((self.out / 'attempt_M8').exists())

    def test_real_error_fails_but_keeps_prior_candidate(self):
        rc, report = self.run_mocked(['complete', 'error'])
        self.assertEqual(rc, 1)
        self.assertEqual(report['outcome'], 'error')
        self.assertEqual(report['best_verified_bound'], 7)
        self.assertTrue((self.out / 'best/run.json').exists())

    def test_prefix_mismatch_is_not_accepted(self):
        rc, report = self.run_mocked(['prefix_mismatch'])
        self.assertEqual(rc, 1)
        self.assertIn('existing-prefix', report['error'])
        self.assertFalse((self.out / 'best').exists())

    def test_missing_child_report_is_error(self):
        rc, report = self.run_mocked(['missing_report'])
        self.assertEqual(rc, 1)
        self.assertEqual(report['outcome'], 'error')

    def test_parent_deadline_terminates_process_group(self):
        rc, report = self.run_mocked(['parent_timeout'])
        self.assertEqual(self.cleanup_calls, 1)
        self.assertEqual(rc, 0)
        self.assertEqual(report['outcome'], 'no_extension_within_budget')
        self.assertEqual(report['attempts'][0]['returncode'], 124)

    def test_budget_validation_and_no_enumeration(self):
        with patch.object(frontier.subprocess, 'Popen') as process:
            for value in ('4201', 'nan', 'inf', '0', '-1'):
                with self.subTest(value=value), self.assertRaises(SystemExit):
                    self.invoke('--seconds', value)
            process.assert_not_called()

    def test_cleanup_kills_descendants_after_parent_exit(self):
        p = Mock(pid=12345)
        p.wait.return_value = 0
        with patch.object(frontier.os, 'killpg') as kill:
            frontier.stop_group(p, frontier.time.monotonic() + 2)
        self.assertEqual([c.args[1] for c in kill.call_args_list], [frontier.signal.SIGTERM, frontier.signal.SIGKILL])

    def test_expired_small_budget_never_starts_child(self):
        with patch.object(frontier.subprocess, 'Popen') as process:
            rc = self.invoke('--seconds', '0.05')
        self.assertEqual(rc, 0)
        process.assert_not_called()

    def test_no_automatic_retry_or_skipped_bound(self):
        with patch.object(frontier.subprocess, 'Popen') as process:
            with patch.dict(os.environ, {'GITHUB_RUN_ATTEMPT': '2'}), self.assertRaises(SystemExit):
                self.invoke()
            with self.assertRaises(SystemExit):
                self.invoke('--start-bound', '8')
            process.assert_not_called()

    def test_legitimate_stop_at_finite_bound_cap(self):
        rc, report = self.run_mocked(['complete'], '--max-bound', '7')
        self.assertEqual(rc, 0)
        self.assertEqual(report['stop_reason'], 'repository_bound_cap_reached')
        self.assertEqual(len(self.commands), 1)

    def test_rank3_remains_capped_and_cannot_take_long_budget(self):
        for args in (['--rank', '3', '--seconds', '4200'], ['--rank', '3', '--max-bound', '1001']):
            with self.assertRaises(SystemExit):
                self.invoke(*args)

class RunnerFailureTests(unittest.TestCase):
    def invoke(self, behavior, extra=()):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / 'attempt'
            commands = []
            def fake_run(cmd, **kwargs):
                commands.append(cmd)
                if behavior == 'compiler_error':
                    raise subprocess.CalledProcessError(2, cmd)
                if 'g++' == cmd[0]:
                    Path(cmd[cmd.index('-o') + 1]).write_text('mock executable')
                    return subprocess.CompletedProcess(cmd, 0)
                if behavior == 'timeout':
                    raise subprocess.TimeoutExpired(cmd, kwargs.get('timeout'))
                return subprocess.CompletedProcess(cmd, -9)
            argv = ['run_census.py', '--rank', '6', '--bound', '7', '--seconds', '3700', '--verify', '--out', str(out), *extra]
            with patch.object(sys, 'argv', argv), patch.object(runner.subprocess, 'run', side_effect=fake_run), \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                rc = runner.main()
            return rc, json.loads((out / 'run.json').read_text())

    def test_compile_error_is_distinct_from_timeout(self):
        rc, state = self.invoke('compiler_error')
        self.assertEqual(rc, 1)
        self.assertEqual(state['failure_kind'], 'error')
        self.assertTrue(state['phase'].startswith('compilation:'))
        self.assertFalse(state['verified'])

    def test_enumerator_timeout_is_normal_budget_exhaustion(self):
        rc, state = self.invoke('timeout')
        self.assertEqual(rc, 3)
        self.assertEqual(state['failure_kind'], 'budget_exhausted')
        self.assertTrue(state['runs'][0]['timeout'])
        self.assertGreater(state['runs'][0]['allowance_seconds'], 3600)

    def test_resource_kill_is_error(self):
        rc, state = self.invoke('resource_kill')
        self.assertEqual(rc, 1)
        self.assertEqual(state['failure_kind'], 'error')
        self.assertEqual(state['runs'][0]['returncode'], -9)

    def test_low_level_max_allowance_is_not_capped_at_4200(self):
        rc, state = self.invoke('timeout', ['--rank6-m7-max', '--seconds', '21177',
                                          '--deadline', str(runner.time.monotonic() + 21297)])
        self.assertEqual(rc, 3)
        self.assertEqual(state['failure_kind'], 'budget_exhausted')
        self.assertGreater(state['runs'][0]['allowance_seconds'], 21100)

    def test_low_level_max_requires_exact_scope_and_deadline(self):
        for extra in (['--rank6-m7-max'],
                      ['--rank6-m7-max', '--rank', '5', '--deadline', str(runner.time.monotonic()+100)],
                      ['--rank6-m7-max', '--bound', '8', '--deadline', str(runner.time.monotonic()+100)],
                      ['--rank6-m7-max', '--seconds', '21301', '--deadline', str(runner.time.monotonic()+100)],
                      ['--rank6-m7-max', '--deadline', str(runner.time.monotonic()+21400)]):
            with self.subTest(extra=extra), self.assertRaises(SystemExit):
                self.invoke('compiler_error', extra)

if __name__ == '__main__':
    unittest.main()
