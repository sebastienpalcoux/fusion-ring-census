#!/usr/bin/env python3
"""Independently verify all released tensors and optional source-file containment.

The C++ verifier checks full tensor axioms and ALL unit-fixing permutations.
New records are supplied first, followed by source records inside each release
bound. Every new record must be retained, and every appended old record must
be isomorphic to an earlier new record. No source file is needed for enumeration.
"""
from __future__ import annotations
import argparse
import collections
import csv
import gzip
import hashlib
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--database',type=Path,help='optional original ancillary file (plain text)')
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--compiler',default='g++')
    a=ap.parse_args()
    if a.out.exists() and any(a.out.iterdir()):
        ap.error('output directory must be empty or absent')
    a.out.mkdir(parents=True,exist_ok=True)
    release=json.loads((ROOT/'results/census.json').read_text())
    old=collections.defaultdict(list)
    source_hash=None
    if a.database:
        source_hash=hashlib.sha256(a.database.read_bytes()).hexdigest()
        with a.database.open() as src:
            for no,line in enumerate(src,1):
                if not line.strip():continue
                t=json.loads(line.replace('{','[').replace('}',']'))
                r=len(t)
                if str(r) not in release['ranks']:continue
                m=max(x for mat in t for row in mat for x in row)
                if m<=release['ranks'][str(r)]['bound']:
                    old[r].append((no,m,line.rstrip('\n')+'\n'))
    summary={}
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td);exe=tmp/'verify_tables'
        subprocess.run([a.compiler,'-O3','-std=c++17',str(ROOT/'code/verify_tables.cpp'),'-o',str(exe)],check=True)
        for rank,info in release['ranks'].items():
            r=int(rank);start=time.monotonic();path=tmp/f'rank{r}.txt'
            with gzip.open(ROOT/info['tables'],'rb') as src,path.open('wb') as dst:
                shutil.copyfileobj(src,dst)
            new_count=info['classes']
            with path.open('a') as dst:
                for no,m,line in old[r]:dst.write(line)
            out=a.out/f'rank{r}_raw_check'
            subprocess.run([str(exe),str(path),str(out),'--exhaustive'],check=True)
            raw=json.loads((out/'summary.json').read_text())
            emitted=0;new_duplicates=0;source_missing=[];old_reps={};old_counts=collections.Counter()
            with (out/'line_map.csv').open() as f:
                for row in csv.DictReader(f):
                    n=int(row['source_line'])
                    if n<=new_count:
                        emitted+=1
                        new_duplicates+=row['kind']!='retained'
                    else:
                        no,m,_=old[r][n-new_count-1]
                        if row['kind']=='retained':source_missing.append(no)
                        rep=int(row['representative_source_line'])
                        old_reps[rep]=m
                        old_counts[m]+=1
            if emitted!=new_count or new_duplicates or source_missing or raw['distinct_rings']!=new_count:
                raise RuntimeError(f'rank {r}: output duplicate or source containment failure')
            with (out/'counts.csv').open() as f:
                verified_counts={row['multiplicity']:int(row['distinct_rings']) for row in csv.DictReader(f)}
            if verified_counts!=info['counts']:
                raise RuntimeError(f'rank {r}: count discrepancy')
            checked={'rank':r,'bound':info['bound'],'complete_enumeration_records':emitted,
                'generated_duplicate_classes':new_duplicates,'all_fusion_axioms_checked':raw['associativity_checked'],
                'canonical_mode':raw['canonical_mode'],'permutations_examined':raw['permutations_examined'],
                'reference_records_in_bound':len(old[r]),'reference_distinct_classes_in_bound':len(old_reps),
                'reference_source_lines_missing':source_missing,'reference_sha256':source_hash,
                'new_classes_not_in_reference':new_count-len(old_reps) if a.database else None,
                'verified_counts':verified_counts,'raw_verifier_seconds':raw['elapsed_seconds'],
                'total_check_seconds':time.monotonic()-start}
            (a.out/f'rank{r}.json').write_text(json.dumps(checked,indent=2)+'\n')
            if a.database:
                with (a.out/f'rank{r}_source_witnesses.csv').open('w') as dst:
                    dst.write('original_source_line,new_release_line,multiplicity,permutation_source_to_release\n')
                    with (out/'line_map.csv').open() as f:
                        for row in csv.DictReader(f):
                            n=int(row['source_line'])
                            if n>new_count:
                                no,m,_=old[r][n-new_count-1]
                                dst.write(f"{no},{row['representative_source_line']},{m},{row['permutation_source_to_representative']}\n")
            # The original new-only database is unchanged. Remove redundant full
            # tensor copies from the raw check, but retain the actual summary.
            (out/'FusionRingMultiplicationTables.deduplicated').unlink()
            for name in ['line_map.csv','duplicates.csv']:
                src=out/name
                with src.open('rb') as f,gzip.GzipFile(filename=str(src)+'.gz',mode='wb',mtime=0) as dst:
                    shutil.copyfileobj(f,dst)
                src.unlink()
            path.unlink()
            summary[rank]=checked
    (a.out/'verification_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
