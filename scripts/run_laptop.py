#!/usr/bin/env python3
"""Complete one whole-rank census locally with no time limit; package only verified results."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CAP = {3: 1000, 4: 1000, 5: 32, 6: 15, 7: 15, 8: 15}


def package_result(out, archive, rank, bound, baseline):
    state = json.loads((out/'run.json').read_text())
    required = (['all'] if rank <= 4 else ['nonselfdual', 'selfdual'] if rank == 5
                else [f'pairs{p}' for p in range(1, (rank-1)//2+1)] + ['selfdual'])
    if not (state.get('complete') is True and state.get('verified') is True
            and state.get('rank') == rank and state.get('bound') == bound
            and state.get('existing_prefix_checked_through') == min(bound, baseline['bound'])
            and [r['name'] for r in state['runs']] == required
            and all(r.get('returncode') == 0 for r in state['runs'])):
        raise ValueError('driver did not certify a complete whole-rank result')
    counts = state['counts']
    if (set(counts) != set(map(str, range(1, bound+1)))
            or any(type(v) is not int or v < 0 for v in counts.values())
            or sum(counts.values()) != state['classes']
            or any(counts[str(m)] != baseline['counts'][str(m)] for m in range(1, min(bound, baseline['bound'])+1))):
        raise ValueError('counts or released prefix mismatch')
    evidence = {'baseline': baseline, 'source': json.loads((ROOT/'SOURCE.json').read_text())
                if (ROOT/'SOURCE.json').exists() else {'code_sha256': state['code_sha256']}}
    (out/'laptop_provenance.json').write_text(json.dumps(evidence, indent=2, allow_nan=False)+'\n')
    # Explicit allowlist excludes partial outputs, compiler products and duplicate tensors.
    files = [out/name for name in ('run.json','counts.csv','parameters.txt.gz',
             'FusionRingMultiplicationTables.txt.gz','laptop_provenance.json')]
    files += sorted((out/'logs').glob('*.log'))
    files += sorted(p for p in (out/'independent_check').iterdir() if p.suffix in ('.json','.csv'))
    staged = archive.with_suffix('.zip.next')
    with zipfile.ZipFile(staged, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        root = f'rank{rank}_M{bound}_verified/'
        for p in files:
            z.write(p, root+str(p.relative_to(out)))
        z.writestr(root+'SHA256SUMS', ''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(out))+'\n' for p in files))
    staged.replace(archive)
    return state


def main():
    available = len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else os.cpu_count() or 1
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rank', type=int, choices=range(3,9), required=True)
    ap.add_argument('--bound', '--mult', type=int, required=True)
    ap.add_argument('--threads', type=int, default=min(64, available))
    ap.add_argument('--output-dir', type=Path, default=ROOT/'runs')
    a = ap.parse_args()
    if os.environ.get('GITHUB_ACTIONS'):
        ap.error('unlimited execution is for your laptop, not GitHub Actions')
    if not 1 <= a.bound <= CAP[a.rank] or not 1 <= a.threads <= 64:
        ap.error(f'rank {a.rank} bound must be 1..{CAP[a.rank]}; threads must be 1..64')
    baseline = json.loads((ROOT/'results/census.json').read_text())['ranks'][str(a.rank)]
    if not (baseline.get('complete') is True and baseline.get('verified') is True):
        ap.error('baseline is not certified')
    out = a.output_dir.resolve()/f'rank{a.rank}_M{a.bound}'
    archive = a.output_dir.resolve()/f'rank{a.rank}_multiplicity{a.bound}_verified.zip'
    if out.exists() or archive.exists():
        ap.error('output already exists; preserve it and choose a fresh --output-dir; checkpoint resume is not implemented')
    # Standalone packages carry an inventory; a repository checkout uses its Git history.
    if (ROOT/'SHA256SUMS').exists():
        for line in (ROOT/'SHA256SUMS').read_text().splitlines():
            expected, name = line.split('  ',1)
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
                ap.error('package checksum mismatch: '+name)
    command = [sys.executable, str(ROOT/'code/run_census.py'), '--rank', str(a.rank),
               '--bound', str(a.bound), '--local-unlimited', '--threads', str(a.threads),
               '--verify', '--out', str(out)]
    print(f'Rank {a.rank} through {a.bound}; {a.threads} threads; NO clock limit. Keep the laptop awake.', flush=True)
    print(f'Progress and logs: {out}', flush=True)
    try:
        result = subprocess.run(command, cwd=ROOT)
    except KeyboardInterrupt:
        print('\nInterrupted. No verified archive produced; this search cannot resume.', file=sys.stderr)
        return 130
    if result.returncode:
        print('No certified archive produced. Inspect run.json and logs.', file=sys.stderr)
        return result.returncode
    state = package_result(out, archive, a.rank, a.bound, baseline)
    print(f'COMPLETE AND INDEPENDENTLY VERIFIED: {state["classes"]:,} classes through {a.bound}.')
    print(f'Exact multiplicity {a.bound}: {state["counts"][str(a.bound)]:,}. Return: {archive}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
