#!/usr/bin/env python3
"""Import a complete independently verified whole-rank artifact; never publish it.

Pass the extracted ``best/`` directory. Hashes, the entire existing count prefix,
and all tensor axioms and relabellings are rechecked before touching the manifest.
"""
from __future__ import annotations
import argparse,csv,gzip,hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def digest(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('artifact',type=Path);a=ap.parse_args()
    source=a.artifact.resolve();state=json.loads((source/'run.json').read_text())
    if not(state.get('complete') is True and state.get('verified') is True):
        ap.error('not a complete independently verified whole-rank artifact')
    r=state['rank'];m=state['bound'];caps={3:1000,4:1000,5:32,6:15,7:15,8:15}
    if type(r) is not int or r not in caps or type(m) is not int or not 1<=m<=caps[r]:
        ap.error('outside repository scope')
    counts=state['counts']
    if set(counts)!=set(map(str,range(1,m+1))) or any(type(v) is not int or v<0 for v in counts.values()):
        ap.error('invalid or noncontiguous exact-multiplicity counts')
    if sum(counts.values())!=state['classes']:ap.error('incorrect class total')
    data=json.loads((ROOT/'results/census.json').read_text());previous=data['ranks'][str(r)]
    if m<=previous['bound']:ap.error('artifact does not extend the checked-in bound')
    if any(counts.get(k)!=v for k,v in previous['counts'].items()):ap.error('existing-prefix count mismatch')
    provenance=ROOT/f'verification/imports/rank{r}_through{m}'
    if provenance.exists():ap.error('provenance destination exists; review it explicitly')
    with tempfile.TemporaryDirectory(prefix='fusion-import-') as temp:
        temp=Path(temp)
        for filename in ['FusionRingMultiplicationTables.txt','parameters.txt']:
            plain=temp/filename
            with gzip.open(source/(filename+'.gz'),'rb') as f,plain.open('wb') as g:shutil.copyfileobj(f,g)
            if digest(plain)!=state[filename+'_sha256']:ap.error(filename+': checksum mismatch')
        exe=temp/'verify'
        subprocess.run([os.environ.get('CXX','g++'),'-O3','-std=c++17',str(ROOT/'code/verify_tables.cpp'),'-o',str(exe)],check=True)
        subprocess.run([str(exe),str(temp/'FusionRingMultiplicationTables.txt'),str(temp/'check'),'--exhaustive'],check=True)
        check=json.loads((temp/'check/summary.json').read_text())
        if check['duplicates'] or check['distinct_rings']!=state['classes']:ap.error('independent audit failed')
        found={}
        with (temp/'check/counts.csv').open() as f:
            for row in csv.DictReader(f):
                if int(row['rank'])!=r:ap.error('tensor rank mismatch')
                found[row['multiplicity']]=int(row['distinct_rings'])
        if found!=counts:ap.error('independent count or multiplicity mismatch')
        prefix=f'results/rank{r}_through{m}'
        record={'rank':r,'bound':m,'complete':True,'verified':True,'classes':state['classes'],'counts':counts,
                'provenance':'Imported whole-rank artifact with fresh full independent verification; reports retained.'}
        for kind,filename,key in [('tables','FusionRingMultiplicationTables.txt.gz','FusionRingMultiplicationTables.txt_sha256'),('parameters','parameters.txt.gz','parameters.txt_sha256')]:
            target=ROOT/f'{prefix}_{kind}.txt.gz'
            if target.exists():ap.error('dataset destination exists; review it explicitly')
            shutil.copy2(source/filename,target)
            record[kind]=str(target.relative_to(ROOT));record[kind+'_gz_sha256']=digest(target)
            record[kind+'_uncompressed_sha256']=state[key]
        provenance.mkdir(parents=True,exist_ok=False)
        shutil.copy2(source/'run.json',provenance/'run.json')
        shutil.copytree(source/'independent_check',provenance/'artifact_independent_check')
        shutil.copytree(temp/'check',provenance/'fresh_independent_check')
    data['ranks'][str(r)]=record;data['total_classes']=sum(x['classes'] for x in data['ranks'].values())
    staged=ROOT/'results/census.json.next';staged.write_text(json.dumps(data,indent=2)+'\n')
    staged.replace(ROOT/'results/census.json')
    print('Local manifest updated. Refresh documentation, rebuild PDFs, inspect the diff, then commit explicitly.')
if __name__=='__main__':main()
