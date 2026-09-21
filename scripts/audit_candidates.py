#!/usr/bin/env python3
"""Independently audit supplied whole-rank candidates without changing the release.

Run the full numerical audit on GitHub Actions or the user's own computer.
Input manifest entries are rank, bound, path and source_commit. A matching bound
is accepted only when both uncompressed data hashes equal the released hashes.
"""
import argparse,csv,gzip,hashlib,json,os,platform,re,shutil,subprocess,tempfile
from pathlib import Path
from extend_census import validate_candidate
ROOT=Path(__file__).resolve().parents[1]

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1<<20),b''):h.update(block)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('manifest',type=Path);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists():ap.error('audit output already exists')
 specs=json.loads(a.manifest.read_text());base=json.loads((ROOT/'results/census.json').read_text())
 if not isinstance(specs,list) or not specs or len({x['rank'] for x in specs})!=len(specs):ap.error('one candidate per rank required')
 a.out.mkdir(parents=True);summary=[]
 with tempfile.TemporaryDirectory(prefix='fusion-candidate-audit-') as td:
  td=Path(td);exe=td/'verify'
  subprocess.run([os.environ.get('CXX','g++'),'-O3','-std=c++17',str(ROOT/'code/verify_tables.cpp'),'-o',str(exe)],check=True)
  for spec in specs:
   r=spec['rank'];m=spec['bound'];p=(ROOT/spec['path']).resolve()
   if not p.is_relative_to(ROOT) or r not in range(3,9) or not 1<=m<={3:1000,4:1000,5:32,6:15,7:15,8:15}[r]:raise ValueError('candidate outside scope')
   state=json.loads((p/'run.json').read_text());old=base['ranks'][str(r)]
   if m<old['bound']:raise ValueError('candidate is below released bound')
   validate_candidate(p,state,old,r,m)
   if not re.fullmatch(r'[0-9a-f]{40}',spec['source_commit']):raise ValueError('full source commit required')
   inventory=p/'SHA256SUMS'
   for line in inventory.read_text().splitlines() if inventory.exists() else []:
    h,name=line.split('  ',1);f=(p/name).resolve()
    if not f.is_relative_to(p) or digest(f)!=h:raise ValueError('candidate file checksum mismatch')
   if (p/'laptop_provenance.json').exists():
    provenance=json.loads((p/'laptop_provenance.json').read_text())
    if provenance['source'].get('commit') and provenance['source']['commit']!=spec['source_commit']:raise ValueError('source commit mismatch')
   if state.get('github_sha') and state['github_sha']!=spec['source_commit']:raise ValueError('runner source commit mismatch')
   codehash=hashlib.sha256()
   paths=subprocess.check_output(['git','ls-tree','-r','--name-only',spec['source_commit'],'--','code'],cwd=ROOT,text=True).splitlines()
   if 'code/verify_tables.cpp' not in paths:raise ValueError('source revision lacks expected code tree')
   for name in sorted(paths):
    if Path(name).suffix in ('.cpp','.hpp','.py'):
     codehash.update(str(Path(name).relative_to('code')).encode());codehash.update(subprocess.check_output(['git','show',spec['source_commit']+':'+name],cwd=ROOT))
   if state['code_sha256']!=codehash.hexdigest():raise ValueError('enumeration source checksum mismatch')
   rd=td/f'rank{r}';rd.mkdir()
   for filename,kind in [('FusionRingMultiplicationTables.txt','tables'),('parameters.txt','parameters')]:
    with gzip.open(p/(filename+'.gz'),'rb') as src,(rd/filename).open('wb') as dst:shutil.copyfileobj(src,dst)
    actual=digest(rd/filename)
    if actual!=state[filename+'_sha256']:raise ValueError('uncompressed checksum mismatch')
    if m==old['bound'] and kind+'_uncompressed_sha256' in old and actual!=old[kind+'_uncompressed_sha256']:raise ValueError('equal-bound reproduction differs from release')
   output=a.out/f'rank{r}';output.mkdir()
   with (output/'verification.log').open('w') as log:
    subprocess.run([str(exe),str(rd/'FusionRingMultiplicationTables.txt'),str(output/'independent'),'--exhaustive'],check=True,stdout=log,stderr=subprocess.STDOUT)
   check=json.loads((output/'independent/summary.json').read_text())
   if not (check['input_records']==check['distinct_rings']==state['classes'] and check['duplicates']==0 and check['associativity_checked'] and check['canonical_mode']=='all unit-fixing permutations'):raise ValueError('independent audit mismatch')
   counts={str(k):0 for k in range(1,m+1)}
   for row in csv.DictReader((output/'independent/counts.csv').open()):
    if int(row['rank'])!=r or row['multiplicity'] not in counts:raise ValueError('unexpected tensor rank or multiplicity')
    counts[row['multiplicity']]=int(row['distinct_rings'])
   if counts!=state['counts']:raise ValueError('independent counts mismatch')
   (output/'independent/FusionRingMultiplicationTables.deduplicated').unlink(missing_ok=True)
   for f in (output/'independent').glob('*.deduplicated'):f.unlink()
   item={'rank':r,'bound':m,'classes':state['classes'],'counts':counts,'outcome':'verified_extension' if m>old['bound'] else 'verified_reproduction','previous_bound':old['bound'],'previous_classes':old['classes'],'source_commit':spec['source_commit'],'code_sha256':state['code_sha256'],'verification_commit':os.environ.get('GITHUB_SHA'),'verification_run_id':os.environ.get('GITHUB_RUN_ID'),'complete':True,'verified':True,'independent_verification':check,'tables_sha256':state['FusionRingMultiplicationTables.txt_sha256'],'parameters_sha256':state['parameters.txt_sha256']}
   (output/'audit.json').write_text(json.dumps(item,indent=2)+'\n');summary.append(item)
   print(f'Rank {r} through {m}: {item["outcome"]}, {state["classes"]:,} classes',flush=True)
 (a.out/'summary.json').write_text(json.dumps({'candidates':summary,'environment':{'python':platform.python_version(),'system':platform.platform(),'compiler':subprocess.check_output(['g++','--version'],text=True)}},indent=2)+'\n')
 if os.environ.get('GITHUB_STEP_SUMMARY'):
  with open(os.environ['GITHUB_STEP_SUMMARY'],'a') as f:
   for s in summary:f.write(f'- Rank {s["rank"]} through {s["bound"]}: **{s["outcome"]}**, {s["classes"]:,} classes.\n')
if __name__=='__main__':main()
