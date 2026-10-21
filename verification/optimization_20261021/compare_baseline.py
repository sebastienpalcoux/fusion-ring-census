#!/usr/bin/env python3
"""Compare complete optimized and pre-optimization strata on eight small domains."""
import hashlib,json,os,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
BASELINE='476bc53e2a964934735d91c8422e06acfbea654a'
def run(cmd,timeout=180):
 st=time.monotonic();p=subprocess.run(list(map(str,cmd)),stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,timeout=timeout,text=True)
 return p,time.monotonic()-st
with tempfile.TemporaryDirectory(prefix='fusion-baseline-audit-') as td:
 work=Path(td);old=work/'old';old.mkdir();new=work/'new';new.mkdir()
 for name in ['completion_solver.hpp','enumerate_bounded.cpp','enumerate_parallel.cpp','enumerate_selfdual_fast.cpp']:
  (old/name).write_bytes(subprocess.check_output(['git','show',BASELINE+':code/'+name],cwd=ROOT))
  (new/name).write_bytes((ROOT/'code'/name).read_bytes())
 for folder in [old,new]:
  for src,exe in [('enumerate_selfdual_fast.cpp','sd'),('enumerate_bounded.cpp','general')]:run([os.environ.get('CXX','g++'),'-O3','-std=c++17','-fopenmp',folder/src,'-o',folder/exe])
 report={'status':'PASS','baseline_commit':BASELINE,'scope':'Eight complete strata; not a full rank-7 M5 or rank-8 M3 rerun.','comparisons':[]}
 for rank,bound in [(7,2),(8,1)]:
  for pairs in range(4):
   outputs=[];times=[];logs=[]
   for folder in [old,new]:
    if pairs:cmd=[folder/'general',ROOT/'systems'/f'rank{rank}_pairs{pairs}.txt',bound,150]
    else:cmd=[folder/'sd',ROOT/'systems'/f'system{rank}sd.txt',rank,bound,150,1]
    result,elapsed=run(cmd);outputs.append(sorted(result.stdout.splitlines()));times.append(elapsed);logs.append(result.stderr)
   if outputs[0]!=outputs[1]:raise RuntimeError(f'Output mismatch {rank} {bound} {pairs}')
   item={'rank':rank,'bound':bound,'dual_pairs':pairs,'classes':len(outputs[0]),'exact_sorted_parameter_match':True,'sorted_output_sha256':hashlib.sha256(('\n'.join(outputs[0])+'\n').encode()).hexdigest(),'baseline_seconds':times[0],'optimized_seconds':times[1],'baseline_log':logs[0],'optimized_log':logs[1]}
   report['comparisons'].append(item);print(json.dumps({k:v for k,v in item.items() if not k.endswith('_log')}),flush=True)
 (Path(__file__).parent/'baseline_comparison.json').write_text(json.dumps(report,indent=2)+'\n')
