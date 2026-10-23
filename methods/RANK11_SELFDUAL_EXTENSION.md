# Self-dual enumeration through rank 11

The self-dual engine uses `N = rank - 2`. Its templates now cover `N=2,...,9`
and multiplicity bounds `1,...,15`. The identities in `SELFDUAL_PROOF.md`
are uniform in `N`; the extension requires implementation and resource
checks, not an additional mathematical hypothesis. The examples below are
bounded fusion-ring enumerations, not assertions of categorifiability.

## Earlier contraction tests at multiplicity one

For a completed row `i` of `Q` and a partially assigned row `j`, put

```
z = u_i u_j + sum_k Q_ik Q_kj.
```

At multiplicity one, each unknown summand is either identically zero or an
independent binary variable: `Q_ik` is known and lies in `{0,1}`. Hence the
possible values of `z` form the exact interval `[L,L+t]`, where `L` is the
known contribution and `t` counts unknown terms whose known coefficient is
one. The unknown entries are distinct entries of row `j`; the diagonal is
already assigned. The existing contraction identity requires

```
z - a Q_ij = sum_k u_k T_ijk.
```

The existing `dot_masks` test this condition using bounded tail coefficients.
Taking the bitwise union of those masks over `[L,L+t]` is therefore a
necessary condition at the partial assignment. This union is cached. A
changed edge affects contractions with the completed rows; when another
row becomes complete, all its partners are checked. The optimization is
enabled for ranks 10 and 11 at multiplicity one. Higher bounds retain the
previous complete-row path.

`audits/audit_partial_dot.cpp` independently enumerates all unknown entries
in each tested row and checks equality with this interval union, for every
input mask. It covers `N=7,8,9`, both unit weights `C=1,2`, every sorted
binary `u`, every edge-prefix length and every completed-row partner in
three seeded random matrices per `u`: 80,928 cases and 1,109,232 binary
completions.

## Bounded-memory canonical first matrices

The already assigned pairs `(u_i,Q_ii)` partition the tail vertices into
ordered color classes. The allowed relabelings preserve each class.
For groups of order at most 4096, the existing full stabilizer test is used.
For larger groups, the engine stores transpositions within classes and
products of two such transpositions. These give necessary partial
lexicographic inequalities. A separate exact test is applied to each
completed matrix, so the subset of partial tests does not change the
accepted matrices.

The exact test uses ordered partition refinement. After the previous rows
have matched the reference matrix, the current ordered cells describe the
remaining freedom. Choose the next vertex from the first cell. Within each
remaining cell, sorting adjacency to that vertex minimizes the next row
without changing earlier rows or colors. If this least row is smaller than
the reference, the matrix is not canonical; if larger, discard this choice.
If equal, recurse on the split cells. This is exhaustive by induction on the
row number. Cells are split separately and their order is retained.

Two candidates in one cell can be identified only when their adjacency
values agree at every other vertex. Their diagonals and colors agree, so
their transposition is an automorphism fixing the chosen prefix; skipping
one is exact.

At `N=9`, a full one-color stabilizer has `9! = 362880` permutations. The
large-group path stores at most `36 + binomial(36,2) = 666` maps, each of
length 36, instead of 362880 such maps. The exact refinement search still
has exponential worst-case time; this change removes factorial storage,
not the intrinsic complexity of enumeration. Partial pruning can be weaker
with the subset, which is why small groups keep their full stabilizer.

`audits/audit_graph_canonicality.cpp` checks the actual C++ implementation
against explicit color-preserving permutations and checks every partial
prefix of each brute-force canonical matrix. The initial audit covered
5,724 matrices, 15,715,269 permutations and 64,044 prefixes for `N=2,...,9`
and `M=1,2,3`, including highly symmetric graph families. An independent
Python implementation additionally exhausted all binary graphs through
five vertices with every contiguous color partition and checked weighted
examples through eight vertices.

## Integer and indexing bounds

For `N <= 9`, `M <= 15` and `C in {1,2}`:

- Domain masks use shifts by at most 16; all arrays of length 16 are indexed
  by coefficients in `0,...,M`.
- `norm_length <= 2026` and `dot_length <= 2251`. The largest row-mask
  allocation has 2,625,696 entries; the largest dot-mask allocation has
  1,296,576 entries. Their index arithmetic fits signed 32-bit integers.
- `qnorm`, `qu` and `unorm` are at most 2025. Each witness coefficient has
  absolute value at most 450. A conservative bound for a witness residual,
  including all later edge updates, is below 450,000; cumulative interval
  bounds are at most 243,000 in absolute value. Signed 32-bit arithmetic
  suffices for these fields.
- For the modular filters (`P=17` or `257`), stored residues are at most
  `P-1`. The largest elementary sums in the displayed Krylov and elimination
  expressions remain below two million in absolute value. The positive
  offsets used before modular subtraction remain sufficient at `N=9`.
- The fourth-degree pair-mask identities already use signed 64-bit
  arithmetic; substituting the above bounds leaves a wide margin.
- The weighted folding branch changes `C=1` to `C=2` and cannot recursively
  create a larger weight: its trigger explicitly requires `C==1`.

These are arithmetic support limits, not a promise that a large-bound
rank-11 search will finish quickly. Complete performance examples recorded
for the extension use multiplicity one. The extended direct-moment audit
checks 160,000 seeded cases through `N=9` and bounds through 15, in addition
to the analytic bounds above.

## Compilation and output

Defining `CENSUS_SELFDUAL_RANK` compiles the requested top-level rank dispatch;
the default value zero retains all ranks for audits. Lower-rank completion systems
needed by the weighted folding path remain available. The driver can cache
rank-specific binaries. The output stream is explicitly flushed and checked
before success is returned.

Weighted unfolding calls the completion solver's exact `canonicalize`
method. It no longer assumes that the solver materializes every permutation.

## Recorded checks

The complete rank-10 multiplicity-one self-dual stratum contains 53 outputs
in the recorded runs. The full-stabilizer variant, the variant with early
partial-dot checks disabled and the final hybrid variant gave exactly the
same sorted parameter set, with SHA-256

```
c90d994e45c7b98c282afa5a7a87f5ae51846ce222904e388b2e0ef9de91d0d1
```

They each reached 2,803,959 complete first matrices and 84,435 singular
completion branches. The evidence is in
`benchmarks/evidence/rank11_extension/selfdual/`. These runs shared CPU
resources with other tasks; their wall times are not a controlled speed
comparison. The bounded-memory improvement above is exact. Independent
tensor verification of whole-rank outputs is a separate driver stage.

To rerun the new finite checks:

```
python3 audits/run_rank11_selfdual_audits.py
```
