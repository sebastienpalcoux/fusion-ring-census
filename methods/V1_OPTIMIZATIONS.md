# Optimizations and completeness

The equation systems, parameter orders, isomorphism convention, and independent
tensor verifier are unchanged. The new search uses the same finite domain
`0,...,M` and no categorifiability filter. This note supplements the original
coverage arguments under `methods/`; its description of parallel partitioning
supersedes the old fixed-prefix paragraph.

## 1. Stronger general associativity propagation

After substituting fixed variables into an associativity equation, combine
all linear coefficients belonging to each remaining variable. Write the
resulting polynomial as a constant plus linear and quadratic monomials.
Compute an enclosing interval `[L,H]` by adding each term's bounds over the
current nonnegative domains.

For an unfixed variable `v`, separately accumulate the bounds `[Lv,Hv]` of
**precisely the terms incident to v**. They are part of the same sums defining
`L,H`. Thus `[L-Lv,H-Hv]` encloses the sum of the other terms. This is removal
of constituent bounds, not generic interval subtraction.

The incident polynomial has the form `q*v*v + v*B`, where `B` is a linear
expression in the other variables and has bounds `[Bl,Bh]`. A candidate value
`v=z >= 0` therefore can satisfy the equation only if zero belongs to

```
[L-Lv + q*z*z + z*Bl, H-Hv + q*z*z + z*Bh].
```

Delete a value only when this necessary condition fails. Correlations between
other variables can make the interval too broad, never too narrow. All bounds
for one equation use its pre-update domains; subsequent reductions only shrink
those domains, so reusing these bounds is safe. Equations affected by any
reduction return to the propagation queue. Search still branches exhaustively
on the first unfixed variable.

With at most two remaining unknowns, the code collects the six coefficients
of `c + lx*x + ly*y + xx*x*x + xy*x*y + yy*y*y` once. It checks exact supports,
solving a linear equation in `y` directly where possible. This gives exactly
the same domain reductions as testing all original monomials for every pair.

Scratch arrays are reused within one worker. Propagation returns before any
recursive search, so no live recursive scratch state is overwritten. Sparse
symmetry maps omit only coordinates fixed by the permutation; their order is
unchanged. Modular Gaussian elimination uses a flat reusable buffer and the
same prime 257 and necessary congruences as before.

## 2. Propagated frontier for non-self-dual searches

The old parallel kernel enumerated every raw prefix of a fixed length. The new
kernel begins with the full domain box, propagates it, and repeatedly splits
one surviving box into all values of its first unfixed variable until it has
a bounded work queue. Failed children are discarded by necessary conditions.
Completed assignments remain jobs and are not emitted during queue creation.

Each split partitions its parent exactly; all retained boxes are disjoint and
cover its solutions. Each worker exhausts one box using the same solver. All
involution types use this scheduler. A one-thread run directly searches the
root, avoiding frontier construction. Completion is reported only after every
job completes normally. The last internal C++ CLI argument now denotes a
**target number of frontier jobs**, not a raw prefix length; the Python
launcher supplies it automatically.

## 3. Stronger self-dual row and dot-product masks

For the original self-dual first-matrix parameterization `(a,u,Q)`, tail
associativity implies

```
(Q*Q + u*u^t - C*I - a*Q)[i,j] = sum_k u[k] * T[i,j,k].
```

Here `C=1` normally and `C=2` in the inherited weighted folding. The established
canonical convention gives lower bound `b=min(u)` on mixed repeated tail
coefficients and zero on the remaining coefficients; all have upper bound M.
A bounded-sum dynamic program computes exactly the attainable values of the
right side. For a partially specified row of Q, a second dynamic program
accounts for sums of the remaining squares `0^2,...,M^2`. A row or dot-product
candidate is discarded only when the necessary value cannot occur. Shared
coefficients and stronger correlations are deliberately relaxed, preserving
completeness. All matrices still undergo the modular reconstruction or the
exhaustive singular fallback, followed by exact verification.

## 4. Symmetry and scalar moments

The pairs `(u[i],Q[i,i])` are already sorted. Their stabilizer is precisely the
product of permutations of equal-pair blocks. Generating those block
permutations directly gives the same edge comparisons without testing every
permutation first. Comparisons begin at the first moved coordinate.

In the modular first-row filter, let `V_t=Q^t*u`, `m_t=u^t*V_t`, and
`w_t=(Q^t)[0,0]`. Unrolling the existing recurrence gives its constant component

```
h_k = w_(k+2) - C*w_k
      + sum_(t=0..k) V_t[0]*V_(k-t)[0]
      - sum_(t=0..k-1) m_t*w_(k-t),
```

and its coefficient of `a` is `-w_(k+1)`. Symmetry yields
`w_(s+t)=(Q^s*e0)^t*(Q^t*e0)`, reducing the number of matrix-vector products.
These are identities over the integers and hence over both existing prime
fields. Singular reductions still go to exhaustive completion. Within the
retained bounds (`N<=6`, `M<=15`, `C<=2`, primes 17/257), the added offsets keep
modular numerators nonnegative and all intermediate integers fit signed 32-bit
storage; no floating-point arithmetic decides any mathematical condition.

## 5. Parallel self-dual work distribution

For multiple threads, each original sorted-u job is partitioned by its first
one or two diagonal entries, respecting the same ordering within equal-u
blocks. Every previously admissible diagonal belongs to exactly one job. This
also assigns the folded invertible case to one job. Masks are cached only when
u and the worker's unchanged M/C agree. Serial runs retain the original u
partition. This improves load balance without altering output or mathematical
pruning.

## Validation and limits

See `BENCHMARKS.md` and `benchmarks/evidence/`. Comparison is by exact sorted
parameter sets, not just counts. Complete whole-rank runs additionally use the
unchanged verifier to check unit, duality, reciprocity, all integer
associativity identities, and isomorphisms under every unit-fixing permutation.
The original packaged count prefix is independently checked.

These tests support the implementation; completeness depends on the coverage
arguments and normally completed exhaustive searches. An interrupted or timed
out run is not a census. Some small strata incur extra propagation overhead;
not every workload improves. No claim is made that rank 7 bound 5 or rank 8
bound 3 has become a short laptop calculation. Checkpoint/resume is not added.
