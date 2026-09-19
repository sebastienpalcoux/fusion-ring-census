#!/usr/bin/env python3
"""Export complete rank-3--8 parameter runs as Vercleyen-style tensors.

Standard-library Python only. This lossless exporter is NOT the independent
axiom verifier. For ranks 6/7/8, --systems contains systemRsd.txt.json and
rankR_pairsP.txt.json. Rank-5 systems are census_system{0,2,4}.json.
"""
from __future__ import annotations
import argparse
import gzip
import itertools
import json
import sys
from functools import lru_cache
from pathlib import Path


def text_file(path: Path, mode: str):
    return gzip.open(path, mode+'t', encoding='utf-8') if path.suffix == '.gz' else path.open(mode, encoding='utf-8')


def rank4_tensor(tag: str, v: list[int]):
    unit = [[int(i == j) for j in range(4)] for i in range(4)]
    if tag == 'S' and len(v) == 10:
        a,b,c,d,e,f,g,h,i,j = v
        return [unit,[[0,1,0,0],[1,a,b,c],[0,b,d,e],[0,c,e,f]],
                [[0,0,1,0],[0,b,d,e],[1,d,g,h],[0,e,h,i]],
                [[0,0,0,1],[0,c,e,f],[0,e,h,i],[1,f,i,j]]]
    if tag == 'N' and len(v) == 6:
        a,b,c,d,e,f = v
        x = [[0,1,0,0],[1,a,b,b],[0,b,c,d],[0,b,d,c]]
        y = [[0,0,1,0],[0,b,c,d],[0,d,e,f],[1,c,e,e]]
        return [unit,x,y,[list(row) for row in zip(*y)]]
    raise ValueError('invalid rank-four record')


@lru_cache(maxsize=None)
def maps(rank: int, tag: str, directory: str):
    root = Path(directory)
    if rank == 5:
        ty = {'S':0,'N2':2,'N4':4}[tag]
        data = json.loads((root/f'census_system{ty}.json').read_text())
        dual = data['dual']
        # These older systems parametrize the symmetric cubic form
        # t_ijk = N_ij^{k*}, NOT the ordered multiplication tensor itself.
        orbits = [sorted({(i,j,dual[k]) for t in orb for i,j,k in itertools.permutations(t)})
                  for orb in data['orbits']]
    else:
        p = int(tag)
        name = f'system{rank}sd.txt.json' if p == 0 else f'rank{rank}_pairs{p}.txt.json'
        data = json.loads((root/name).read_text())
        if data['rank'] != rank or data['pairs'] != p:
            raise ValueError('wrong system metadata')
        dual, orbits = data['dual'], data['orbits']
    owner = {}
    for a, orb in enumerate(orbits):
        for t in orb:
            t = tuple(t)
            if t in owner and owner[t] != a:
                raise ValueError('inconsistent orbit definitions')
            owner[t] = a
    if len(owner) != (rank-1)**3:
        raise ValueError('nonunit tensor orbits are incomplete')
    return dual, orbits


def tensor(rank: int, line: str, systems: Path):
    tag, *words = line.split()
    v = list(map(int, words))
    if any(x < 0 for x in v):
        raise ValueError('negative coefficient')
    if rank == 3:
        if tag == 'C3' and not v:
            return [[[int((i+j)%3 == k) for k in range(3)] for j in range(3)] for i in range(3)]
        if tag != 'S' or len(v) != 4:
            raise ValueError('invalid rank-three record')
        k,l,m,n = v
        return [[[1,0,0],[0,1,0],[0,0,1]], [[0,1,0],[1,m,k],[0,k,l]], [[0,0,1],[0,k,l],[1,l,n]]]
    if rank == 4:
        return rank4_tensor(tag, v)
    dual, orbits = maps(rank, tag, str(systems.resolve()))
    if len(v) != len(orbits):
        raise ValueError('incorrect parameter count')
    n = rank
    out = [[[int(j == k) if i == 0 else int(i == k) if j == 0 else
             int(dual[i] == j) if k == 0 else 0
             for k in range(n)] for j in range(n)] for i in range(n)]
    for orb, x in zip(orbits, v):
        for i,j,k in orb:
            out[i][j][k] = x
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rank', type=int, choices=(3,4,5,6,7,8), required=True)
    ap.add_argument('--input', type=Path, nargs='+', required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--systems', type=Path, default=Path('.'))
    args = ap.parse_args()
    if args.output.exists():
        ap.error('output already exists; choose a new path')
    count = 0
    try:
        with text_file(args.output, 'w') as dst:
            for path in args.input:
                with text_file(path, 'r') as src:
                    for no,line in enumerate(src, 1):
                        if not line.strip():
                            continue
                        try:
                            out = tensor(args.rank, line, args.systems)
                        except (ValueError,KeyError,IndexError) as exc:
                            raise ValueError(f'{path}, line {no}: {exc}') from exc
                        dst.write(json.dumps(out,separators=(',',':')).replace('[','{').replace(']','}')+'\n')
                        count += 1
        if not count:
            raise ValueError('no records')
    except (OSError,ValueError) as exc:
        print(f'ERROR: {exc}. Any partial output is invalid.',file=sys.stderr)
        return 1
    print(f'Exported {count} rank-{args.rank} tensors.',file=sys.stderr)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
