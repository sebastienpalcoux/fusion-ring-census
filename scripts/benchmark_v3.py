#!/usr/bin/env python3
"""Compare v3 and retained v2 algorithms using exact output sets (ranks 6--9).

Compilation and explicit reference-system generation are excluded from timing.
Each kernel receives the same thread count and time allowance. A timeout or
output mismatch fails the benchmark; it is never reported as a speedup.
"""
import argparse
import hashlib
import json
import os
import shutil
from pathlib import Path
import statistics
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'code'))
from build_system import system, write_system
from build_selfdual_system import reordered


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rank', type=int, choices=range(6,10), default=9)
    ap.add_argument('--bound', type=int, default=1)
    ap.add_argument('--threads', type=int, default=2)
    ap.add_argument('--repeats', type=int, default=3)
    ap.add_argument('--seconds', type=float, default=120)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    if not 1 <= a.bound <= (1 if a.rank == 9 else 15):
        ap.error('reference rank 9 supports bound 1; other reference bounds are 1..15')
    if not 1 <= a.threads <= 64 or a.repeats < 1 or a.seconds <= 0:
        ap.error('positive repeats/seconds and threads 1..64 required')
    if a.out.exists():
        ap.error('--out must be a new directory')
    a.out = a.out.resolve(); a.out.mkdir(parents=True)
    report = {'rank':a.rank, 'bound':a.bound, 'threads':a.threads, 'repeats':a.repeats,
              'complete':False, 'compilation_excluded':True, 'cases':[]}
    try:
        ref = a.out/'reference_systems'; ref.mkdir()
        # The self-dual engine folds involution branches into lower ranks.
        for rank in range(4,a.rank):
            for suffix in ('.txt','.txt.json'):
                name=f'system{rank}sd{suffix}'
                shutil.copy2(ROOT/'systems'/name,ref/name)
        for pairs in range((a.rank-1)//2+1):
            data = reordered(a.rank,compact=False) if pairs == 0 else system(a.rank,pairs,compact=False)
            name = f'system{a.rank}sd.txt' if pairs == 0 else f'rank{a.rank}_pairs{pairs}.txt'
            write_system(data,ref/name)
        binaries={}
        for version, source in [('v2',ROOT/'benchmarks/reference/v2_rank9/code'),('v3',ROOT/'code')]:
            for kind, filename in [('general','enumerate_parallel.cpp'),('selfdual','enumerate_selfdual_fast.cpp')]:
                binary=a.out/f'{version}_{kind}'
                flags=[f'-DCENSUS_SELFDUAL_RANK={a.rank}'] if version=='v3' and kind=='selfdual' else []
                command=[os.environ.get('CXX','g++'),'-O3','-std=c++17','-fopenmp',*flags,str(source/filename),'-o',str(binary)]
                subprocess.run(command,check=True,capture_output=True)
                binaries[version,kind]=binary
        for pairs in range(1,(a.rank-1)//2+1):
            report['cases'].append({'name':f'pairs{pairs}','pairs':pairs,'runs':[]})
        report['cases'].append({'name':'selfdual','pairs':0,'runs':[]})
        env=dict(os.environ,OMP_NUM_THREADS=str(a.threads))
        for case in report['cases']:
            expected=None
            for repeat in range(a.repeats):
                # Alternate order to reduce systematic warm-up/order bias.
                order=('v2','v3') if repeat%2==0 else ('v3','v2')
                for version in order:
                    pairs=case['pairs']; kind='general' if pairs else 'selfdual'
                    name=f'rank{a.rank}_pairs{pairs}.txt' if pairs else f'system{a.rank}sd.txt'
                    directory=ref if version=='v2' else ROOT/'systems'
                    command=[str(binaries[version,kind]),str(directory/name)]
                    if pairs:
                        command += [str(a.bound),str(a.seconds),str(a.threads),str(max(64,64*a.threads))]
                    else:
                        command += [str(a.rank),str(a.bound),str(a.seconds),str(a.threads)]
                    started=time.perf_counter()
                    run=subprocess.run(command,capture_output=True,env=env,timeout=a.seconds+30)
                    elapsed=time.perf_counter()-started
                    (a.out/f"{case['name']}_{version}_{repeat}.log").write_bytes(run.stderr)
                    if run.returncode:
                        raise RuntimeError(f"{case['name']} {version}: return code {run.returncode}; no speedup certified")
                    rows=sorted(run.stdout.splitlines())
                    if len(set(rows))!=len(rows):
                        raise RuntimeError(f"{case['name']} {version}: duplicate output")
                    if expected is None:expected=rows
                    elif rows!=expected:
                        raise RuntimeError(f"{case['name']}: exact parameter sets disagree")
                    case['runs'].append({'version':version,'repeat':repeat,'seconds':elapsed,
                                         'classes':len(rows),'sha256':hashlib.sha256(b'\n'.join(rows)).hexdigest()})
            case['v2_median_seconds']=statistics.median(r['seconds'] for r in case['runs'] if r['version']=='v2')
            case['v3_median_seconds']=statistics.median(r['seconds'] for r in case['runs'] if r['version']=='v3')
            case['speedup']=case['v2_median_seconds']/case['v3_median_seconds']
            print(f"{case['name']}: exact sets equal; {case['speedup']:.2f}x",flush=True)
        report['complete']=True
        report['v2_sum_medians']=sum(c['v2_median_seconds'] for c in report['cases'])
        report['v3_sum_medians']=sum(c['v3_median_seconds'] for c in report['cases'])
        report['kernel_total_speedup']=report['v2_sum_medians']/report['v3_sum_medians']
    except Exception as exc:
        report['error']=str(exc)
        raise
    finally:
        (a.out/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    return 0


if __name__=='__main__':
    raise SystemExit(main())

