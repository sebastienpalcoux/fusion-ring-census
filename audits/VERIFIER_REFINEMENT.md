# Exact individualization/refinement in the independent verifier

The default mode of `code/verify_tables.cpp` now computes an exact canonical
tensor by individualization and refinement. `--exhaustive` retains the separate
reference algorithm that visits every unit-fixing permutation. The two modes
can choose different canonical tensors; they determine the same isomorphism
classes. The reported mode is `individualization-refinement (exact)`.

## Why the reduction is exact

Start with the unit as a singleton and partition nonunit elements by the
existing integer signature: self-duality, the diagonal coefficient, a sorted
multiplication slice, and sorted joint diagonal data. Sort the signature keys
lexicographically, so the order of the cells is preserved by any based-ring
isomorphism.

Given an ordered partition with colors `c`, refine each nonsingleton cell using
the dual's color and the sorted multiset, over all ordered pairs `(j,k)`, of

```
(c(j), c(k), N[i,j,k], N[j,i,k], N[j,k,i]).
```

Every quantity is exact. An isomorphism preserving the current cells preserves
this multiset. Splits therefore preserve all possible isomorphisms. Repeat
until no cell splits. A singleton partition gives a unit-fixing ordering and
the corresponding full multiplication tensor.

Otherwise choose the first cell of minimum size greater than one. For each
vertex in it, create an ordered singleton followed by the remaining cell and
recurse. This branching rule is invariant under an isomorphism. Thus an
isomorphism induces a bijection between the two search trees and their leaf
tensors. Taking the least full tensor at a leaf gives identical keys for
isomorphic rings. Conversely, equality of the full tensor keys supplies an
explicit based-ring isomorphism.

One additional pruning rule skips a vertex only when swapping it with a
previously visited vertex is an automorphism. The program checks this swap
against every original tensor entry. Both vertices lie in the chosen cell, so
the swap preserves the current partition and fixes all earlier singled-out
vertices. The two subtrees are therefore equivalent. Signature equality alone
never triggers this pruning.

Hash values accelerate lookups, but full integer-vector equality decides.
For every duplicate, the source-to-representative permutation is checked
against the original tensors. Unit, duality, Frobenius reciprocity, full
associativity, and multiplicity counts retain the existing checks.

## Validation and measured performance

`tests/test_verifier_refinement.py` compares the class partitions and source
representatives with exhaustive verification on twelve known rings of ranks
3 through 8, including noncommutative group rings, random unit-fixing
relabellings, and literal repeats. It also verifies six distinct known rings
of ranks 9 through 11 and their relabellings, including the cyclic groups of
orders 9, 10, and 11, the group of order 9 and exponent 3, the dihedral group of
order 10, and the product of two Ising fusion rings. Every returned witness is
checked again independently in Python.

The complete rank-nine multiplicity-one output (142 rings) was also compared
with exhaustive verification. An adversarial fixture adds one deterministic
random relabelling of each ring and 21 literal repetitions. Both modes return
142 classes from 305 records, with 163 duplicates and identical class
partitions and source representatives.

In one measured run, including axiom checks and I/O, the refined verifier took
0.168 seconds and visited 1,745 leaves; exhaustive verification took 1.892
seconds and visited 12,297,600 permutations. This is about an 11.2-fold speedup
for that fixture, not a claim about whole-census speed or every input. Machine
load affects timing. Inputs, hashes, platform, timings, and counters are saved
in `audits/evidence/verifier_refinement_benchmark.json` and the compressed
fixture `audits/evidence/rank9_verifier_adversarial.txt.gz`.

Run the independent regression tests with:

```bash
python3 -m unittest discover -s tests -p test_verifier_refinement.py -v
```

Worst-case search remains exponential. Refinement reduces the search without
changing what qualifies as a based-ring isomorphism.
