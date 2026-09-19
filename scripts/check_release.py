#!/usr/bin/env python3
"""Check release hashes/counts, optionally all tensor axioms and all relabellings."""
from __future__ import annotations
import argparse,csv,gzip,hashlib,json,os,shutil,subprocess,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--full',action='store_true')
    ap.add_argument('--out',type=Path);a=ap.parse_args()
    data=json.loads((ROOT/'results/census.json').read_text());report={'full_axiom_check':a.full,'ranks':{}}
    t0=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='fusion-verify-') as tmp:
        tmp=Path(tmp);exe=tmp/'verify'
        if a.full:subprocess.run([os.environ.get('CXX','g++'),'-O3','-std=c++17',str(ROOT/'code/verify_tables.cpp'),'-o',str(exe)],check=True)
        for r,item in sorted(data['ranks'].items(),key=lambda x:int(x[0])):
            assert item['complete'] is True,(r,'uncertified release')
            assert sorted(map(int,item['counts']))==list(range(1,item['bound']+1)),(r,'count gaps')
            assert sum(item['counts'].values())==item['classes'],(r,'incorrect total')
            if r=='3':assert item['bound']<=1000
            table=ROOT/item['tables'];assert sha256(table)==item['tables_gz_sha256'],(r,'compressed checksum mismatch')
            h=hashlib.sha256();lines=0
            with gzip.open(table,'rb') as f:
                for line in f:
                    h.update(line);lines+=bool(line.strip())
            assert lines==item['classes'],(r,'record count mismatch')
            assert h.hexdigest()==item['tables_uncompressed_sha256'],(r,'uncompressed checksum mismatch')
            rec={'rank':int(r),'bound':item['bound'],'classes':lines,'hashes_verified':True}
            if a.full:
                plain=tmp/f'rank{r}.txt'
                with gzip.open(table,'rb') as src,plain.open('wb') as dst:shutil.copyfileobj(src,dst)
                out=tmp/f'check{r}'
                subprocess.run([str(exe),str(plain),str(out),'--exhaustive'],check=True,stdout=subprocess.DEVNULL)
                check=json.loads((out/'summary.json').read_text())
                assert check['duplicates']==0 and check['distinct_rings']==lines,(r,'bad independent audit')
                counts={}
                with (out/'counts.csv').open() as f:
                    for row in csv.DictReader(f):
                        assert int(row['rank'])==int(r)
                        counts[row['multiplicity']]=int(row['distinct_rings'])
                assert counts==item['counts'],(r,'count mismatch against independent verifier')
                rec['independent_verification']=check
                plain.unlink()
            report['ranks'][r]=rec;print(f'Rank {r}, through {item["bound"]}: {lines:,} records OK',flush=True)
    report['total_classes']=sum(x['classes'] for x in report['ranks'].values());report['elapsed_seconds']=time.monotonic()-t0
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    return 0
if __name__=='__main__':raise SystemExit(main())
