#!/usr/bin/env python3
"""Concatenate complete released ranks into one original-format file."""
import argparse,gzip,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
a=argparse.ArgumentParser(description=__doc__);a.add_argument('output',type=Path);a.add_argument('--ranks',type=int,nargs='+',default=list(range(3,9)));o=a.parse_args()
if o.output.exists():a.error('output exists; choose a new filename')
d=json.loads((ROOT/'results/census.json').read_text());total=0
if len(set(o.ranks))!=len(o.ranks) or any(str(r) not in d['ranks'] for r in o.ranks):a.error('invalid or repeated rank')
with o.output.open('wb') as dst:
 for r in o.ranks:
  item=d['ranks'][str(r)]
  if item.get('complete') is not True:raise ValueError('uncertified rank')
  with gzip.open(ROOT/item['tables'],'rb') as src:shutil.copyfileobj(src,dst)
  total+=item['classes']
print(f'Wrote {total} full tensors to {o.output}')
