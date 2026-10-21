# Deeper optimizations and completeness (v2)

The equation systems, output parameter order, canonical isomorphism convention,
exporter, and independent verifier are unchanged. No categorifiability
assumptions, known solutions, or rank-specific census facts prune the search.
This package retains the first optimization pass documented in
`methods/V1_OPTIMIZATIONS.md`, and adds the following changes.

## Self-dual enumeration

1. **Canonical generator rows.** Before constructing a multiplication matrix,
   exact reachable-sum masks now incorporate the necessary lexicographic order
   of the sorted mixed coefficients for every possible distinguished generator.
   Equal-weight permutations are collapsed when constructing these masks.
2. **Bounded integer witnesses.** After the first row is known, enumerate the
   bounded symmetric-tensor row witnesses permitted by its first associativity
   contraction. A second contraction is linear in the remaining matrix entries;
   intervals and divisibility remove impossible witnesses during descent.
3. **Joint final-entry constraints.** A third contraction gives a quadratic
   identity. Its intersection with the linear identity produces exact support
   masks for the final two off-diagonal entries and the coefficient `a`.
   Degenerate linear equations are handled by exhaustive bounded enumeration.
4. **Shared polynomial work.** Precomputed coefficient vectors turn repeated
   matrix-vector products for each witness into short dot products. All these
   calculations use integer arithmetic; the quadratic coefficients use `int64_t`.
5. **Safe resource bounds.** A zero `u` vector is collapsed algebraically in
   these filters. If 4,096 stored witnesses or 200,000 witness-construction visits
   would be exceeded, witness pruning is disabled for that branch and the
   complete prior search path is used. Partial witness lists are never used to
   exclude solutions. The final completion solver still determines the real
   tensor entries in the zero-vector case.

`methods/SELFDUAL_PROOF.md` derives the identities, proves the necessary
canonical condition, and explains singular and fallback cases. Neither
invertibility nor spectral simplicity is required for these new filters.

## General completion solver

1. Remove the old prefix gate before modular Gaussian elimination: every
   equation that is linear after current singleton substitutions is usable
   immediately. Equations that remain nonlinear are conservatively omitted.
2. For each reduced row with two or three free variables, enumerate those
   variables' actual bounded domains, solve for the pivot modulo 257, and
   intersect every variable with its exact support projection. The supported
   coefficient bound is below 257, so pivot residues identify bounded values
   uniquely. Later domain reductions do not invalidate the row equations.
3. For a quadratic equation with exactly three unfixed variables, collect its
   coefficients once, enumerate two domains, and solve or enumerate the third
   exactly. Early exit is allowed only after every current value has a witness.

`methods/GAUSSIAN_AUDIT.md` gives the detailed preservation arguments and audit
results. Search branching, output canonicalization, and exhaustive completion
remain in place.

## Experimental decisions

Several alternatives were implemented and rejected after testing: switching
all self-dual work to generic constraint search, extra partial dot-product
filters, putting the smaller prime first, changing to a largest-weight pivot,
grouping three final edges, joint Gaussian-table propagation, and alternative
branching and queue policies. The package includes the selected implementations
only. The largest reductions come from avoiding impossible matrix completions,
not changing the compiler flags or omitting duality types.

## Limits of the evidence

`BENCHMARKS.md` reports completed computations and exact sorted parameter-set
comparisons. Whole-rank integration runs also use the unchanged independent
full-tensor and isomorphism verifier. The included randomized/exhaustive local
audits test the newly introduced pruning conditions separately.

These are substantial optimizations, not a proof that any particular unexplored
large census will finish on a laptop. Speedups vary by rank, bound, and duality
type. The mathematical preservation arguments accompany finite implementation
tests; neither can guarantee the absence of every possible software defect.
