#!/usr/bin/env python3
"""Compare the Diophantine enumerator with independent four-variable brute force."""
import argparse
import itertools
import subprocess
from collections import Counter
from pathlib import Path

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('executable', type=Path)
p.add_argument('--bound', type=int, default=16)
a = p.parse_args()
if not 1 <= a.bound <= 32:
    p.error('brute-force test bound must be 1..32')
seen = set()
for k,l,m,n in itertools.product(range(a.bound+1), repeat=4):
    if k*k+l*l == 1+l*m+k*n:
        seen.add(min((k,l,m,n),(l,k,n,m)))
expected = Counter(max(1,*v) for v in seen)
expected[1] += 1  # Z[C3]
out = subprocess.check_output([str(a.executable.resolve()),str(a.bound)],text=True)
actual = dict(tuple(map(int,line.split())) for line in out.splitlines())
if actual != {m:expected[m] for m in range(1,a.bound+1)}:
    raise RuntimeError('count mismatch against exhaustive four-parameter enumeration')
# Independently check the associativity of every small self-dual tensor.
for k,l,m,n in seen:
    N=[[[1,0,0],[0,1,0],[0,0,1]],[[0,1,0],[1,m,k],[0,k,l]],[[0,0,1],[0,k,l],[1,l,n]]]
    for i,j,k,l in itertools.product(range(3), repeat=4):
        if sum(N[i][j][s]*N[s][k][l] for s in range(3)) != sum(N[j][k][s]*N[i][s][l] for s in range(3)):
            raise RuntimeError('associativity failure')
print(f'Independent brute-force counts and tensor checks pass through {a.bound}.')
