#!/usr/bin/env python3
"""Advance a whole-rank census inside one shared wall-clock budget.

Only a normally completed, independently verified whole-rank attempt can become
``best/``. Timeouts never supply OEIS terms, even when some duality types finished.
This script never commits, publishes, or changes the checked-in baseline.
"""
from __future__ import annotations
import argparse, json, os, shutil, signal, subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CAP={3:1000,4:1000,5:32,6:15,7:15,8:15}
START={3:1000,4:160,5:19,6:7,7:4,8:2}

def stop_group(p: subprocess.Popen) -> None:
    if p.poll() is not None:return
    if os.name=='posix':os.killpg(p.pid,signal.SIGTERM)
    else:p.terminate()
    try:p.wait(timeout=2)
    except subprocess.TimeoutExpired:
        if os.name=='posix':os.killpg(p.pid,signal.SIGKILL)
        else:p.kill()
        p.wait()

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rank',type=int,choices=range(3,9),required=True)
    ap.add_argument('--seconds',type=float,default=1100)
    ap.add_argument('--threads',type=int,default=4)
    ap.add_argument('--start-bound',type=int)
    ap.add_argument('--step',type=int)
    ap.add_argument('--max-bound',type=int)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args()
    if not 0<a.seconds<=1200:ap.error('shared wall-clock budget must be at most 1200 seconds')
    if not 1<=a.threads<=64:ap.error('threads must be between 1 and 64')
    start=a.start_bound or START[a.rank];step=a.step or (16 if a.rank==4 else 1)
    maximum=a.max_bound or CAP[a.rank]
    if not 1<=start<=maximum<=CAP[a.rank] or step<1:ap.error('invalid bound/step')
    if a.rank==3 and maximum>1000:ap.error('rank three stops at 1000')
    out=a.out.resolve()
    if out.exists() and any(out.iterdir()):ap.error('output must be absent or empty')
    out.mkdir(parents=True,exist_ok=True)
    began=time.monotonic();deadline=began+a.seconds
    report={'rank':a.rank,'budget_seconds':a.seconds,'timing':'shared wall clock including compilation, export and verification',
            'github_run_id':os.environ.get('GITHUB_RUN_ID'),'github_sha':os.environ.get('GITHUB_SHA'),
            'attempts':[],'best_verified_bound':None,'partial_counts_published':False}
    try:
        for bound in range(start,maximum+1,step):
            remaining=deadline-time.monotonic()
            if remaining<=2:break
            attempt=out/f'attempt_M{bound}';log=out/f'attempt_M{bound}.log'
            cmd=[sys.executable,str(ROOT/'code/run_census.py'),'--rank',str(a.rank),'--bound',str(bound),
                 '--seconds',str(max(.01,remaining*.90)),'--threads',str(a.threads),'--verify',
                 '--build-dir',str(out/'build-cache'),'--out',str(attempt)]
            st=time.monotonic()
            with log.open('w') as f:
                p=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=os.name=='posix')
                try:rc=p.wait(timeout=max(.01,deadline-time.monotonic()))
                except subprocess.TimeoutExpired:stop_group(p);rc=124
            item={'bound':bound,'elapsed_seconds':time.monotonic()-st,'returncode':rc,'complete':False}
            state=json.loads((attempt/'run.json').read_text()) if (attempt/'run.json').exists() else {}
            if rc==0 and state.get('complete') is True and state.get('verified') is True:
                item['complete']=True;item['classes']=state['classes']
                best=out/'best';temp=out/'best-next';temp.mkdir()
                for filename in ('run.json','counts.csv','parameters.txt.gz','FusionRingMultiplicationTables.txt.gz'):
                    shutil.copy2(attempt/filename,temp/filename)
                shutil.copytree(attempt/'independent_check',temp/'independent_check')
                if best.exists():shutil.rmtree(best)
                temp.rename(best)
                report['best_verified_bound']=bound
            report['attempts'].append(item)
            # Retain logs and machine-readable status, not partial mathematical data.
            if attempt.exists():
                if (attempt/'run.json').exists():shutil.copy2(attempt/'run.json',out/f'attempt_M{bound}.json')
                shutil.rmtree(attempt)
            report['elapsed_seconds']=time.monotonic()-began
            (out/'frontier.json').write_text(json.dumps(report,indent=2)+'\n')
            print(json.dumps(item),flush=True)
            if not item['complete']:break
            if a.rank==3:break
    finally:
        report['elapsed_seconds']=time.monotonic()-began
        (out/'frontier.json').write_text(json.dumps(report,indent=2)+'\n')
        summary=['# Whole-rank search result','',f"Rank: {a.rank}. Shared wall time: {report['elapsed_seconds']:.2f} s.",'',
                 f"Largest newly completed and verified bound: {report['best_verified_bound'] or 'none'}.",'',
                 'The checked-in baseline is unchanged. No partial-stratum counts are released.','']
        (out/'SUMMARY.md').write_text('\n'.join(summary))
        if os.environ.get('GITHUB_STEP_SUMMARY'):
            with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:f.write('\n'.join(summary))
    return 0
if __name__=='__main__':raise SystemExit(main())
