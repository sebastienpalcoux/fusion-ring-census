#!/usr/bin/env python3
"""End-to-end small complete censuses at every supported rank."""
from __future__ import annotations
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 out=a.out.resolve();out.mkdir(parents=True,exist_ok=True);start=time.monotonic();records=[]
 # These prefixes are independently checked against the shipped, larger release.
 manifest=json.loads((ROOT/'results/census.json').read_text())
 for rank,bound in [(3,2),(4,2),(5,2),(6,2),(7,1),(8,1)]:
  target=out/f'rank{rank}';cmd=[sys.executable,str(ROOT/'code/run_census.py'),'--rank',str(rank),'--bound',str(bound),'--seconds','90','--threads','2','--verify','--build-dir',str(out/'build-cache'),'--out',str(target)]
  subprocess.run(cmd,check=True,timeout=180)
  run=json.loads((target/'run.json').read_text());expect={str(m):manifest['ranks'][str(rank)]['counts'][str(m)] for m in range(1,bound+1)}
  if not(run.get('complete') is True and run.get('verified') is True and run['counts']==expect):raise RuntimeError(f'rank {rank}: incorrect census or verification status')
  records.append({'rank':rank,'bound':bound,'classes':run['classes'],'complete':True,'verified':True,'enumeration_seconds':run['enumeration_seconds']})
  print(f'PASS rank {rank}: {run["classes"]} classes',flush=True)
 report={'all_passed':True,'elapsed_seconds':time.monotonic()-start,'runs':records}
 (out/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
