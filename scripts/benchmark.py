#!/usr/bin/env python3
"""Compare original, previous optimized, and new census engines on complete runs.
All versions use the same compiler flags and equation systems. Compilation is
excluded. Timed-out output is diagnostic only and never certifies a census.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import statistics
import subprocess
import time

ROOT=Path(__file__).resolve().parents[1]
CASES={
 'sd6m3':('selfdual',6,3,0), 'sd7m1':('selfdual',7,1,0),
 'sd7m2':('selfdual',7,2,0), 'sd7m3':('selfdual',7,3,0),
 'sd8m1':('selfdual',8,1,0), 'sd8m2':('selfdual',8,2,0),
 **{f'ns{r}p{p}m{m}':('nonselfdual',r,m,p)
    for r,m in [(6,2),(7,2),(7,3),(8,1),(8,2)] for p in range(1,(r-1)//2+1)}
}
DEFAULT=['sd7m2',*[f'ns7p{p}m2' for p in (1,2,3)],'sd8m1',*[f'ns8p{p}m1' for p in (1,2,3)]]
SOURCES={'selfdual':'enumerate_selfdual_fast.cpp','parallel':'enumerate_parallel.cpp','general':'enumerate_bounded.cpp'}

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--original-root',type=Path,default=ROOT/'benchmarks/reference/original')
 ap.add_argument('--previous-root',type=Path,default=ROOT/'benchmarks/reference/previous')
 ap.add_argument('--new-root',type=Path,default=ROOT)
 ap.add_argument('--systems',type=Path,default=ROOT/'systems')
 ap.add_argument('--released-root',type=Path,help='Optional checkout containing released parameters for an additional exact comparison')
 ap.add_argument('--work',type=Path,default=ROOT/'benchmark_runs')
 ap.add_argument('--cases',nargs='+',choices=CASES,default=DEFAULT)
 ap.add_argument('--repeats',type=int,default=3)
 ap.add_argument('--threads',type=int,default=1)
 ap.add_argument('--seconds',type=float,default=60)
 ap.add_argument('--compiler',default=os.environ.get('CXX','g++'))
 ap.add_argument('--versions',nargs='+',choices=('original','previous','new'),default=['original','previous','new'])
 a=ap.parse_args()
 if not 1<=a.threads<=64 or a.repeats<1 or not 0<a.seconds<86400:ap.error('invalid threads, repeats or timeout')
 a.work=a.work.resolve();a.work.mkdir(parents=True,exist_ok=True)
 roots={'original':a.original_root.resolve(),'previous':a.previous_root.resolve(),'new':a.new_root.resolve()}
 compiler=subprocess.check_output([a.compiler,'--version'],text=True).splitlines()[0]
 flags=['-O3','-std=c++17','-fopenmp']
 report={'compiler':compiler,'flags':flags,'platform':platform.platform(),'threads':a.threads,'repeats':a.repeats,'timeout_seconds':a.seconds,'cases':[],'source_hashes':{}}
 env=dict(os.environ,OMP_NUM_THREADS=str(a.threads),OMP_DYNAMIC='FALSE')
 def engine(v,c):
  kind,r,m,p=CASES[c]
  return 'selfdual' if kind=='selfdual' else 'general' if v=='original' and (r<7 or p!=1) else 'parallel'
 bins={}
 for v in a.versions:
  report['source_hashes'][v]={}
  for kind in sorted({engine(v,c) for c in a.cases}):
   src=roots[v]/'code'/SOURCES[kind];header=roots[v]/'code/completion_solver.hpp'
   digest=hashlib.sha256((compiler+json.dumps(flags)).encode()+src.read_bytes()+header.read_bytes()).hexdigest()
   binary=a.work/(v+'_'+kind);stamp=binary.with_suffix('.sha256')
   if not binary.exists() or not stamp.exists() or stamp.read_text()!=digest:
    subprocess.run([a.compiler,*flags,str(src),'-o',str(binary)],check=True);stamp.write_text(digest)
   bins[v,kind]=binary
   report['source_hashes'][v][src.name]=hashlib.sha256(src.read_bytes()).hexdigest()
   report['source_hashes'][v][header.name]=hashlib.sha256(header.read_bytes()).hexdigest()
 def save():
  (a.work/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
 def run(v,c,trial):
  _,r,m,p=CASES[c];kind=engine(v,c)
  system=a.systems.resolve()/(f'system{r}sd.txt' if not p else f'rank{r}_pairs{p}.txt')
  cmd=[str(bins[v,kind]),str(system)]
  if kind=='selfdual':cmd += [str(r),str(m),str(a.seconds),str(a.threads)]
  elif kind=='parallel':
   depth=6
   while (m+1)**depth>2000000:depth-=1
   cmd += [str(m),str(a.seconds),str(a.threads),str(depth if v=='original' else max(64,64*a.threads))]
  else:cmd += [str(m),str(a.seconds)]
  stem=a.work/f'{c}_{v}_{trial}';t=time.perf_counter()
  with stem.with_suffix('.params').open('wb') as out,stem.with_suffix('.log').open('wb') as log:
   try:rc=subprocess.run(cmd,stdout=out,stderr=log,env=env,timeout=a.seconds+5).returncode
   except subprocess.TimeoutExpired:rc=124
  wall=time.perf_counter()-t
  lines=sorted(stem.with_suffix('.params').read_bytes().splitlines())
  finals=[s for s in stem.with_suffix('.log').read_text().splitlines() if s.startswith(('FINAL','rank ')) and ' classes ' in s]
  s=finals[-1] if finals else '';match=re.search(r'\bseconds ([\d.eE+-]+)',s)
  return {'returncode':rc,'wall_seconds':wall,'enumeration_seconds':float(match[1]) if match else None,'rows':len(lines),'duplicates':len(lines)-len(set(lines)),'sorted_sha256':hashlib.sha256(b'\n'.join(lines)+(b'\n' if lines else b'')).hexdigest(),'command':cmd,'final':s}
 for c in a.cases:
  item={'case':c,'runs':{v:[] for v in a.versions}}
  for trial in range(a.repeats):
   order=a.versions[trial%len(a.versions):]+a.versions[:trial%len(a.versions)]
   for v in order:
    x=run(v,c,trial);item['runs'][v].append(x)
    print(f'{c} {v} trial {trial+1}: rc={x["returncode"]} enumeration={x["enumeration_seconds"]}s rows={x["rows"]}',flush=True)
  completed=[x for runs in item['runs'].values() for x in runs if x['returncode']==0]
  item['all_complete']=all(x['returncode']==0 for runs in item['runs'].values() for x in runs)
  item['completed_outputs_equal']=len({x['sorted_sha256'] for x in completed})<=1
  item['medians']={v:statistics.median(x['enumeration_seconds'] for x in runs) for v,runs in item['runs'].items() if all(x['returncode']==0 and x['enumeration_seconds'] is not None for x in runs)}
  item['speedups_vs_new']={v:t/item['medians']['new'] for v,t in item['medians'].items() if v!='new'} if 'new' in item['medians'] else {}
  if a.released_root and completed:
   import gzip
   _,r,m,p=CASES[c]
   manifest=json.loads((a.released_root/'results/census.json').read_text())
   if manifest['ranks'][str(r)]['bound']>=m:
    with gzip.open(a.released_root/f'results/rank{r}/parameters.txt.gz','rt') as f:
     expected=sorted(line.strip().encode() for line in f if int(line.split()[0])==p and max(map(int,line.split()[1:]))<=m)
    digest=hashlib.sha256(b'\n'.join(expected)+(b'\n' if expected else b'')).hexdigest()
    item['released_rows']=len(expected);item['released_outputs_equal']=all(x['sorted_sha256']==digest for x in completed)
  report['cases'].append(item);save()
  if not item['completed_outputs_equal'] or item.get('released_outputs_equal') is False or any(x['duplicates'] for x in completed):raise SystemExit('ERROR: output mismatch or duplicates')
 print(a.work/'comparison.json')
 return 0 if all(x['all_complete'] for x in report['cases']) else 3
if __name__=='__main__':raise SystemExit(main())
