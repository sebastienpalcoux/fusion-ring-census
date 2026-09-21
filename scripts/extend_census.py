#!/usr/bin/env python3
"""Advance a whole-rank census within one finite, shared wall-clock budget.

Only complete, independently checked candidates with the existing count prefix
enter best/. Released datasets are never modified. No interrupted search resumes.
"""
from __future__ import annotations
import argparse
import csv
import json
import math
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
CAP = {3: 1000, 4: 1000, 5: 32, 6: 15, 7: 15, 8: 15}
MAX_SECONDS = 4200
CLEANUP_MARGIN = 3.0


def write_json(path, value):
    temp = path.with_suffix(path.suffix + '.next')
    temp.write_text(json.dumps(value, indent=2) + '\n')
    temp.replace(path)


def stop_group(p, deadline):
    """Terminate the entire child group; never give a retry a fresh budget."""
    try:
        if os.name == 'posix':
            os.killpg(p.pid, signal.SIGTERM)
        else:
            p.terminate()
    except ProcessLookupError:
        pass
    try:
        p.wait(timeout=max(0, min(2, deadline - time.monotonic())))
    except subprocess.TimeoutExpired:
        try:
            if os.name == 'posix':
                os.killpg(p.pid, signal.SIGKILL)
            else:
                p.kill()
        except ProcessLookupError:
            pass
        p.wait()
    finally:
        # A compiler can exit while one of its children is still alive. Reaping
        # only the Python parent is not enough to enforce the numerical budget.
        if os.name == 'posix':
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass


def expected_strata(rank):
    if rank <= 4:
        return ['all']
    if rank == 5:
        return ['nonselfdual', 'selfdual']
    return [f'pairs{p}' for p in range(1, (rank - 1) // 2 + 1)] + ['selfdual']


def validate_candidate(path, state, previous, rank, bound):
    if not (state.get('complete') is True and state.get('verified') is True):
        raise ValueError('child did not certify a complete independently verified result')
    if state.get('rank') != rank or state.get('bound') != bound:
        raise ValueError('candidate rank or bound mismatch')
    runs = state.get('runs', [])
    if [r['name'] for r in runs] != expected_strata(rank) or any(r.get('returncode') != 0 for r in runs):
        raise ValueError('not every required duality stratum completed normally')
    counts = state['counts']
    if set(counts) != set(map(str, range(1, bound + 1))) or any(type(v) is not int or v < 0 for v in counts.values()):
        raise ValueError('invalid exact-multiplicity counts')
    if sum(counts.values()) != state['classes']:
        raise ValueError('class total mismatch')
    if any(counts.get(k) != v for k, v in previous['counts'].items()):
        raise ValueError('existing-prefix count mismatch')
    check = json.loads((path / 'independent_check/summary.json').read_text())
    if (check.get('duplicates') != 0 or check.get('distinct_rings') != state['classes']
            or check.get('input_records') != state['classes']
            or check.get('associativity_checked') is not True
            or check.get('canonical_mode') != 'all unit-fixing permutations'):
        raise ValueError('independent exhaustive tensor/isomorphism verification mismatch')
    actual = {str(m): 0 for m in range(1, bound + 1)}
    with (path / 'independent_check/counts.csv').open() as f:
        seen = set()
        for row in csv.DictReader(f):
            key = row['multiplicity']
            if int(row['rank']) != rank or key not in actual or key in seen:
                raise ValueError('invalid independent count row')
            seen.add(key)
            actual[key] = int(row['distinct_rings'])
    if actual != counts:
        raise ValueError('independent count mismatch')
    for name in ('counts.csv', 'parameters.txt.gz', 'FusionRingMultiplicationTables.txt.gz'):
        if not (path / name).is_file():
            raise ValueError('missing candidate file: ' + name)


def preserve_diagnostics(attempt, destination):
    """Move only reports and logs; raw/partial tensor output is never uploaded."""
    destination.mkdir(parents=True, exist_ok=True)
    for name in ('run.json', 'logs', 'independent_check'):
        source = attempt / name
        if source.exists():
            if name == 'independent_check':
                target = destination / name
                target.mkdir(exist_ok=True)
                for p in source.iterdir():
                    if p.is_file() and p.suffix in ('.csv', '.json'):
                        shutil.copy2(p, target / p.name)
            elif source.is_dir():
                shutil.copytree(source, destination / name, dirs_exist_ok=True)
            else:
                shutil.copy2(source, destination / name)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rank', type=int, choices=range(3, 9), required=True)
    ap.add_argument('--seconds', type=float, default=1100)
    ap.add_argument('--threads', type=int, default=min(64, len(os.sched_getaffinity(0))) if hasattr(os, 'sched_getaffinity') else min(64, os.cpu_count() or 1))
    ap.add_argument('--start-bound', type=int)
    ap.add_argument('--step', type=int)
    ap.add_argument('--max-bound', type=int)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args(argv)
    limit = MAX_SECONDS if a.rank >= 5 else 1200
    if not math.isfinite(a.seconds) or not 0 < a.seconds <= limit:
        ap.error(f'shared wall-clock budget must be finite and at most {limit} seconds')
    if not 1 <= a.threads <= 64:
        ap.error('threads must be between 1 and 64')
    baseline = json.loads((ROOT / 'results/census.json').read_text())['ranks'][str(a.rank)]
    if not (baseline.get('complete') is True and baseline.get('verified') is True):
        ap.error('released baseline is not complete and independently verified')
    start = a.start_bound if a.start_bound is not None else ({3: 1000, 4: 160}.get(a.rank, baseline['bound'] + 1))
    step = a.step if a.step is not None else (16 if a.rank == 4 else 1)
    maximum = a.max_bound if a.max_bound is not None else CAP[a.rank]
    if not 1 <= start <= maximum <= CAP[a.rank] or step < 1:
        ap.error('invalid bound/step or repository cap reached')
    if a.rank >= 5 and (start != baseline['bound'] + 1 or step != 1):
        ap.error('ranks 5–8 must start at the next unfinished bound and advance by one')
    if os.environ.get('GITHUB_RUN_ATTEMPT', '1') != '1':
        ap.error('automatic reruns are disabled; a new campaign requires separate authorization')
    out = a.out.resolve()
    if out.exists() and any(out.iterdir()):
        ap.error('output must be absent or empty; no checkpoint resume is implemented')
    out.mkdir(parents=True, exist_ok=True)
    began = time.monotonic()
    deadline = began + a.seconds
    execution_deadline = deadline - CLEANUP_MARGIN
    report = {
        'rank': a.rank, 'budget_seconds': a.seconds, 'threads': a.threads,
        'campaign': 'standard',
        'timing': 'one shared wall clock: compilation, enumeration, export, compression, verification and candidate acceptance',
        'github_run_id': os.environ.get('GITHUB_RUN_ID'), 'github_sha': os.environ.get('GITHUB_SHA'),
        'github_run_attempt': os.environ.get('GITHUB_RUN_ATTEMPT'),
        'baseline_bound': baseline['bound'], 'baseline_classes': baseline['classes'],
        'starting_bound': start, 'max_bound': maximum, 'attempts': [],
        'best_verified_bound': None, 'partial_counts_published': False,
        'outcome': 'no_extension_within_budget', 'stop_reason': 'budget_exhausted',
    }
    previous = baseline
    exit_code = 0
    attempt = None
    item = None
    try:
        for bound in range(start, maximum + 1, step):
            remaining = execution_deadline - time.monotonic()
            if remaining <= 2:
                report['stop_reason'] = 'budget_exhausted'
                break
            attempt = out / f'attempt_M{bound}'
            enumeration_seconds = remaining * .90
            if enumeration_seconds <= 0:
                break
            command = [sys.executable, str(ROOT / 'code/run_census.py'), '--rank', str(a.rank),
                       '--bound', str(bound), '--seconds', str(enumeration_seconds),
                       '--deadline', str(execution_deadline), '--threads', str(a.threads), '--verify',
                       '--build-dir', str(out / 'build-cache'), '--out', str(attempt)]
            item = {'bound': bound, 'command': command, 'remaining_seconds_at_start': remaining,
                    'complete': False, 'started_elapsed_seconds': time.monotonic() - began}
            report['attempts'].append(item)
            write_json(out / 'frontier.json', report)
            started = time.monotonic()
            timed_out = False
            with (out / f'attempt_M{bound}.log').open('w') as log:
                p = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT, start_new_session=os.name == 'posix')
                try:
                    rc = p.wait(timeout=max(.001, execution_deadline - time.monotonic()))
                except subprocess.TimeoutExpired:
                    stop_group(p, deadline)
                    rc = 124
                    timed_out = True
                else:
                    # Remove any surviving descendants even if the child driver
                    # reported its own deadline or a compiler/resource failure.
                    stop_group(p, deadline)
            item.update(returncode=rc, elapsed_seconds=time.monotonic() - started)
            state = json.loads((attempt / 'run.json').read_text()) if (attempt / 'run.json').exists() else {}
            if timed_out:
                item.update(outcome='budget_exhausted', error='shared driver deadline reached', phase=state.get('phase'))
            elif rc == 3 and state.get('failure_kind') == 'budget_exhausted':
                item.update(outcome='budget_exhausted', error=state.get('error'), phase=state.get('phase'))
            elif rc != 0:
                raise RuntimeError(f"child failed (exit {rc}): {state.get('error', 'missing final run report; inspect logs')}")
            else:
                validate_candidate(attempt, state, previous, a.rank, bound)
                if time.monotonic() >= execution_deadline:
                    item.update(outcome='budget_exhausted', error='deadline reached before candidate acceptance')
                else:
                    state['existing_prefix_checked_through'] = previous['bound']
                    state['github_sha'] = report['github_sha']
                    state['github_run_id'] = report['github_run_id']
                    write_json(attempt / 'run.json', state)
                    # The canonical tensor copy is redundant; retain the compressed
                    # original plus every verifier report, not two tensor collections.
                    (attempt / 'independent_check/FusionRingMultiplicationTables.deduplicated').unlink(missing_ok=True)
                    # Preserve diagnostics before any attempt cleanup, including on success.
                    preserve_diagnostics(attempt, out / 'diagnostics' / f'attempt_M{bound}')
                    if time.monotonic() >= execution_deadline:
                        raise TimeoutError('shared deadline reached before retaining the candidate')
                    best = out / 'best'
                    old = out / 'previous-best'
                    if best.exists():
                        best.rename(old)
                    try:
                        attempt.rename(best)
                    except Exception:
                        if old.exists():
                            old.rename(best)
                        raise
                    report['best_verified_bound'] = bound
                    report['outcome'] = 'verified_extension' if bound > baseline['bound'] else 'no_extension_within_budget'
                    item.update(complete=True, classes=state['classes'], outcome='verified_extension' if bound > baseline['bound'] else 'verified_baseline')
                    previous = state
                    if old.exists():
                        shutil.rmtree(old)
            if attempt.exists():
                preserve_diagnostics(attempt, out / 'diagnostics' / f'attempt_M{bound}')
                shutil.rmtree(attempt)
            report['elapsed_seconds'] = time.monotonic() - began
            write_json(out / 'frontier.json', report)
            print(json.dumps(item), flush=True)
            if not item['complete']:
                report['stop_reason'] = 'budget_exhausted'
                break
            report['stop_reason'] = 'repository_bound_cap_reached'
            if a.rank == 3:
                break
    except TimeoutError as exc:
        report['stop_reason'] = 'budget_exhausted'
        if item is not None:
            item.update(outcome='budget_exhausted', error=str(exc))
        if attempt is not None and attempt.exists():
            preserve_diagnostics(attempt, out / 'diagnostics' / attempt.name)
            shutil.rmtree(attempt)
    except Exception as exc:
        exit_code = 1
        report.update(outcome='error', stop_reason='error', error=f'{type(exc).__name__}: {exc}')
        if item is not None:
            item.update(outcome='error', error=report['error'])
        traceback.print_exc()
        if attempt is not None and attempt.exists():
            preserve_diagnostics(attempt, out / 'diagnostics' / attempt.name)
            shutil.rmtree(attempt)
    finally:
        report['elapsed_seconds'] = time.monotonic() - began
        write_json(out / 'frontier.json', report)
        summary = ['# Whole-rank campaign result', '', f'Rank: {a.rank}. Outcome: **{report["outcome"]}**.', '',
                   f'Released bound: {baseline["bound"]}. New verified bound: {report["best_verified_bound"] or "none"}.', '',
                   f'Shared driver wall time: {report["elapsed_seconds"]:.2f} / {a.seconds:g} seconds.', '',
                   f'Stop reason: {report["stop_reason"]}.', '',
                   'The checked-in baseline is unchanged. Partial-stratum counts are diagnostic only; no incomplete tensors are uploaded.', '']
        if report.get('error'):
            summary += ['Error: ' + report['error'], '']
        (out / 'SUMMARY.md').write_text('\n'.join(summary))
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as f:
                f.write('\n'.join(summary))
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
