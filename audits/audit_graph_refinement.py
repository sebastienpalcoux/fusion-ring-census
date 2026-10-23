#!/usr/bin/env python3
"""Independent exact audit of lexicographic colored-graph refinement."""
from itertools import permutations, product
import json
from pathlib import Path
import random
import time

rng = random.Random(20261023)
checks = 0
permutations_checked = 0

def partitions(n):
    for cuts in range(1 << (n - 1)):
        out, start = [], 0
        for i in range(n - 1):
            if cuts >> i & 1:
                out.append(tuple(range(start, i + 1)))
                start = i + 1
        out.append(tuple(range(start, n)))
        yield tuple(out)

def is_canonical(Q, cells, twins=True):
    n = len(Q)
    def visit(cells, row):
        if not cells:
            return True
        considered = []
        for v in cells[0]:
            if twins and any(all(Q[v][k] == Q[w][k]
                                 for k in range(n) if k not in (v, w))
                             for w in considered):
                continue
            considered.append(v)
            remaining = (tuple(w for w in cells[0] if w != v),) + cells[1:]
            refined, row_values = [], []
            for cell in remaining:
                for value in sorted({Q[v][w] for w in cell}):
                    part = tuple(w for w in cell if Q[v][w] == value)
                    refined.append(part)
                    row_values.extend([value] * len(part))
            reference = list(Q[row][row + 1:])
            if row_values < reference:
                return False
            if row_values == reference and not visit(tuple(refined), row + 1):
                return False
        return True
    return visit(cells, 0)

def brute(Q, cells):
    global permutations_checked
    n = len(Q)
    best, best_p = None, None
    for blocks in product(*(tuple(permutations(cell)) for cell in cells)):
        p = sum(blocks, ())
        key = tuple(Q[p[i]][p[j]] for i in range(n) for j in range(i + 1, n))
        permutations_checked += 1
        if best is None or key < best:
            best, best_p = key, p
    return best, best_p

def check(Q, cells):
    global checks
    n = len(Q)
    expected, p = brute(Q, cells)
    key = tuple(Q[i][j] for i in range(n) for j in range(i + 1, n))
    canonical_Q = tuple(tuple(Q[p[i]][p[j]] for j in range(n)) for i in range(n))
    for twins in (False, True):
        assert is_canonical(Q, cells, twins) == (key == expected), (Q, cells, twins)
        assert is_canonical(canonical_Q, cells, twins), (canonical_Q, cells, twins)
        checks += 2

def matrix(n, values):
    Q = [[0] * n for _ in range(n)]
    for (i, j), x in zip(((i, j) for i in range(n) for j in range(i + 1, n)), values):
        Q[i][j] = Q[j][i] = x
    return tuple(map(tuple, Q))

started = time.monotonic()
for n in range(2, 6):
    edges = n * (n - 1) // 2
    for bits in range(1 << edges):
        Q = matrix(n, [(bits >> k) & 1 for k in range(edges)])
        for cells in partitions(n):
            check(Q, cells)
    print(f'PASS exhaustive binary n={n}; checks={checks}', flush=True)

for n, trials in ((6, 250), (7, 50), (8, 12)):
    choices = tuple(partitions(n))
    for t in range(trials):
        Q = matrix(n, [rng.randrange(4) for _ in range(n * (n - 1) // 2)])
        # Half the cases use the largest possible permutation group.
        cells = (tuple(range(n)),) if t % 2 == 0 else rng.choice(choices)
        check(Q, cells)
    print(f'PASS random weighted n={n}; checks={checks}', flush=True)

report = {'status': 'PASS', 'predicate_checks': checks,
          'brute_force_permutations': permutations_checked, 'seed': 20261023,
          'exhaustive_binary_vertices': [2, 3, 4, 5],
          'all_contiguous_color_partitions': True,
          'weighted_random_cases': {'6': 250, '7': 50, '8': 12},
          'twin_skipping_checked': True,
          'canonicalized_inputs_checked': True,
          'elapsed_seconds': time.monotonic() - started}
Path(__file__).with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
