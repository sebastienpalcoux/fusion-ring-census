# What is enumerated, and why the searches are exhaustive

## 1. Definitions and scope

A record is the full ordered tensor `N[i][j][k]` in a distinguished basis
`b[0],...,b[r-1]`, with `b[0]` the unit. All entries are nonnegative integers.
We require associativity, `N[0][j][k]=N[j][0][k]=delta[j,k]`, and an
involution `i -> i*` fixing 0 such that

    N[i][j][0] = delta[i*,j],
    N[i][j][k] = N[i*][k][j] = N[k][j*][i].

These reciprocity identities also imply that duality is an anti-involution.
No categorification, integrality of Frobenius--Perron dimensions, or
commutativity condition is added. Multiplicity is the maximum entry of the
FULL tensor, so it is at least one. An isomorphism is a simultaneous
permutation of all three indices, fixing 0. Ring anti-isomorphisms are not
silently identified with isomorphisms.

The general algorithm treats every involution type: p disjoint pairs among
r-1 nonunit basis elements, for p=0,...,floor((r-1)/2). Different types
cannot be isomorphic. A full census is certified only when every type has
completed. Time-limited incomplete searches do not supply full census terms.

## 2. A baseline exhaustive finite-domain algorithm

`build_system.py` partitions nonunit triples into orbits under the two
reciprocity operations `(i,j,k)->(i*,k,j)` and `(i,j,k)->(k,j*,i)`.
Give each orbit an independent variable in {0,...,M}. All other tensor
entries are fixed by the unit and the involution. Substitute into every
associativity identity

    sum_s N[i][j][s] N[s][k][l]
       = sum_s N[j][k][s] N[i][s][l].

Identities involving the unit, or with output index 0, already follow from
the imposed unit and reciprocity rules. The builder explicitly generates
all remaining identities (all four indices nonunit). It removes zero
polynomials and equal polynomials differing only by sign. This is an
exhaustive parameterization, not a random search or a reconstruction from
an existing database.

The finite-domain solver applies only necessary conditions:

* Interval evaluation of a polynomial may reject a domain only if zero
  lies outside the resulting enclosing interval.
* With at most two unfixed variables in an equation, all values in their
  current finite domains are examined and unsupported values removed.
* Equations linear in the remaining variables are reduced modulo 257.
  An inconsistent modular system rejects the branch. One- and two-variable
  consequences retain precisely their supported domain values. A singular
  modular system is not grounds for rejection.
* Lexicographic comparisons with involution-preserving basis permutations
  retain the lexicographically least orbit representative. A partial
  comparison stops at the first undetermined comparison; it does not infer
  a later strict comparison past an unresolved earlier coordinate.

Finally the first unfixed variable is assigned each remaining value, and
all integer associativity equations are tested at a leaf. Thus induction
on the number of unfixed variables proves exhaustiveness. The imposed
lexicographic inequalities give exactly one output per based-isomorphism
class. The parallel program partitions a fixed prefix into every possible
bounded assignment; these subtrees are disjoint and their union is the
whole search. It reports completion only after all prefixes finish.

## 3. Why specialization to commutative rings is safe at ranks four and five

The complex algebra of a fusion ring is a finite-dimensional semisimple
*-algebra, because the coefficient-of-unit trace gives the positive
inner product making the distinguished basis orthonormal. It has the
one-dimensional Frobenius--Perron representation. A noncommutative
semisimple algebra with a one-dimensional representation has dimension
at least five. In dimension five it must be C direct-sum M_2(C).

In the latter case the unique one-dimensional character is Galois
invariant; its values are rational algebraic integers and therefore
positive integers. Its formal codegree D is the sum of the squares of
these five integers, so D>=5. The formal-codegree identity
`sum_E dim(E)/f_E = 1` would give, for the other irreducible representation,

    f = 2D/(D-1) = 2 + 2/(D-1).

Formal codegrees are algebraic integers, whereas this rational number is
not an integer for D>=5. This contradiction proves commutativity. The
standard formal-codegree facts are used only in this low-rank justification;
the rank-six/seven algorithms do not assume commutativity. The same
argument and the full older specialized derivations are retained in
`rank5_specialized_derivation.tex`.

## 4. Fast self-dual parameterization

In the self-dual type, the reciprocity identities make the nonunit tensor
fully symmetric. Put r=N+2 (N=2,...,6 here), choose one nonunit basis element,
and write its fusion matrix as

    A = [ 0  1  0 ]
        [ 1  a  u^t ]
        [ 0  u  Q ],

where u has N coordinates and Q is symmetric of size N. The rest of the
nonunit tensor is a symmetric cubic tensor on N indices. Order the
parameters as: u; the diagonal of Q; the strict upper triangle of Q;
a; then the remaining symmetric cubic coefficients.

The lexicographically least full parameter vector in a based-isomorphism
class has nondecreasing u. Moreover b=u[0] is the minimum of all mixed
repeated-index coefficients t[i][i][j] (i!=j), since any such coefficient
can be moved to the first coordinate. Hence Q[i][i]>=b. If two consecutive
coordinates of u agree, their Q diagonal entries may be sorted. The
remaining permutations preserving both u and the Q diagonal act on the
strict upper triangle; partial lexicographic minimization under that
stabilizer is again a necessary condition for a global minimum. Final
canonicalization still tests the complete permutation group.

This explains why the much smaller first-matrix search covers every
self-dual isomorphism class. No simultaneous diagonalization or generic
spectral hypothesis is imposed.

## 5. Necessary contraction bounds

For a remaining multiplication matrix let R_i denote its N-by-N tail.
Commutation with A implies

    R_i u = (Q^2 + u u^t - I - a Q) e_i,
    R_i Q = Q R_i - (Q e_i)u^t + u(Q e_i)^t.

Let s=sum_j u[j], g=gcd_j u[j], and b=u[0]. Every scalar product of a row
of R_i with u lies in [0,M*s] and is divisible by g (or is zero if u=0).
The diagonal contraction has the stronger lower bound b*(s-u[i]), since
all but its fully diagonal cubic coefficient are mixed repeated-index
coefficients. The off-diagonal contraction indexed by i!=j has lower bound
b*(u[i]+u[j]). These give necessary intervals for a.

During an incomplete Q row, the unassigned sum of squares is bounded
between zero and the number of missing entries times M^2. Thus the interval
filter remains enclosing. Complete rows additionally impose the exact gcd
condition. The program caches the resulting allowed-a bitmasks; caching
changes neither the conditions nor the search space.

## 6. Krylov reconstruction over finite fields

Set V_k=Q^k u and K=[V_0,...,V_(N-1)]. Write

    H_0 = Q^2 + u u^t - I - a Q,
    H_(k+1) = Q H_k - (u^t V_k) Q + u V_(k+1)^t.

An induction using the two commutator equations above gives

    R_i V_k = H_k e_i.

Every H_k is affine in a. If K is invertible modulo a prime p>M, these
identities uniquely determine every entry of every R_i modulo p. Since a
permitted integer entry lies in [0,M], each residue determines at most one
entry. The program reconstructs just the independent symmetric cubic
entries; all original integer equations are then tested. A spurious modular
candidate therefore cannot be emitted.

A cheap preliminary test considers only the first row of R_0, solving
`K^t x = h_0 + a h_1`. This can eliminate an a before the full reconstruction.
The primes used are 257 and 17, so this general implementation restricts
M<=15. Failure of invertibility modulo either prime is not evidence that
there is no ring, even if the integer matrix is invertible.

## 7. Compatible singular systems are fully retained

Row reduction of the first-row system skips missing pivots. Every zero
row gives a necessary affine congruence on a. When the row-reduced system
has one or two free x coordinates, the program enumerates all their
bounded values and back-substitutes: it retains an a exactly when this
necessary scalar-row system has a bounded solution. The mixed-coefficient
lower bound b is imposed only on the non-diagonal entries of that row.
With more free coordinates it does not attempt this bounded enumeration.

If a survives and neither prime gives a nonsingular reconstruction, the
baseline exhaustive solver from Section 2 completes the fixed first
matrix for every remaining a. Thus rationally singular matrices, matrices
singular modulo one or both primes, and all zero-coefficient cases remain
covered. There is no division by a potentially zero determinant without
a separate exhaustive alternative.

## 8. Folding the fixed invertible element

The case u=0, a=0, Q=I says that the chosen element g satisfies g^2=1 and
fixes every other nonunit basis element X_i. Therefore

    X_i X_j = delta[i,j]*(1+g) + sum_k t[i,j,k] X_k.

All remaining associativity equations are those of a rank-(r-1) weighted
system, in which the coefficient of its unit in X_i^2 is 2 rather than 1.
This is only a computational auxiliary system, not a claimed fusion ring.
Its equations are obtained by multiplying the constant terms in the
ordinary self-dual associativity polynomials by 2. Equivalently, replace
I by 2I in the contraction and Krylov equations above. The same bounded
search and exhaustive fallback apply.

There is no second invertible element h outside {1,g}: the equality gh=h
would imply g=1 after multiplication by h^{-1}. Thus the distinguished
pair {1,g} is intrinsic. Enumerating the smaller weighted tensor up to
permutations of the X_i is therefore sufficient and introduces no hidden
identifications. Each output is unfolded, minimized under all original
basis permutations, and tested against all original integer equations
before being emitted. This optimization is applied only to unit weight 1;
weighted searches themselves continue with the ordinary exhaustive
singular fallback, rather than unproved repeated folding.

## 9. Rank-four and rank-five specialized implementations

Rank four uses the complete six-equation symmetric tensor elimination and
the six-parameter nonself-dual elimination in `rank4_completeness.tex`.
All zero branches are included. The parallelization only distributes
outer-loop values; all output and count updates are protected.

Rank five uses the complete Krylov-rank 3/2/1/0 case division and the two
nonself-dual reductions in `rank5_specialized_derivation.tex`. Its new
speedup is a necessary modular test on two affine reconstructed coefficients
`(A+B*a)/D`, with p=257. For D invertible modulo p, precomputed bitmasks
retain only a in [0,M] whose two coefficient residues are also in [0,M].
Every survivor still undergoes the original exact divisibility, bounds,
and complete integer associativity tests. If D is zero modulo p, the
original exact gcd/congruence algorithm is used. The integer-singular
branches of the original specialized algorithm are unchanged. Its bound
restriction M<=32 is retained.

The supplied rank-five orbit files encode the symmetric form
`t[i,j,k]=N[i][j][k*]`. The exporter expands all permutations of each listed
triple and then applies the dual to the output index. This is different
from the already-expanded ordered tensor orbits of the general program.
Confusing these conventions would give incorrect exported tables.

## 10. Completeness versus independent verification

The arguments above prove exhaustive coverage of a bounded search when
it terminates normally. The independent verifier addresses the separate
soundness and uniqueness questions: for every exported full tensor it
checks all fusion-ring axioms, including all associativity equations, and
canonicalizes over every unit-fixing permutation. It shares no generated
associativity polynomial list and no canonical parameter ordering with
the enumerators.

Comparison with the old ancillary file is a further regression check and
measures enlargement; it is NOT the reason for asserting completeness.
The old file is never read by an enumerator. Passing all output checks
alone would not prove that a generator omitted no rings: that is why the
complete case analysis, all singular fallbacks, execution completion flags,
and cross-checks of the new optimizations are supplied separately.

## 11. Arithmetic, timing, and reproducibility

The general generator permits ranks 4--8 and M<=15. Its cached integer
bounds and finite-field products fit signed 32-bit integers, and exact
polynomial evaluations use 64-bit integers. Rank four permits M<=1000,
uses 64-bit integer polynomials and 128-bit modular products. Rank five
retains its original M<=32 restriction and exact integer arithmetic.

Run records report elapsed wall time rather than summed CPU time. Current
source identity, compilation and enumeration timings, completion status, and
independent verification are indexed by rank in `verification/README.md`.
A finite campaign shares one deadline across all phases and all attempts;
unlimited local runs retain the same mathematical scope and verification gates.

OpenMP can change raw output order. The release parameter files are sorted
lexicographically by (tag, integer parameter vector), and the exporter
preserves that order. Reproduced records therefore have a deterministic
release order, independent of thread scheduling. A timeout prevents the
runner from issuing `complete: true` or publishing full census counts.

## References

V. Ostrik, *On formal codegrees of fusion categories*, Mathematical Research
Letters 16 (2009), 895--901; arXiv:0810.3242. This supplies the algebraic
integrality and trace identities used in the rank-five commutativity argument.

G. Vercleyen and J. Slingerland, *On Low Rank Fusion Rings*, Journal of
Mathematical Physics 64 (2023), 091703; arXiv:2205.15637v4. The original
ancillary database is used only for comparison, with its exact checksum in
`audit/source.json`.

The earlier Dong--Palcoux rank-four and rank-five census derivations are
retained as the accompanying TeX excerpts. They are provenance for the
specialized code, not a reference to an asserted published article.

## Workspace bounds at rank eight

Rank eight includes every duality type without imposing commutativity. Its self-dual system has
84 variables and 231 nonzero associativity equations. Modular matrix storage is
sized from the actual variable/equation counts instead of historical fixed
80/200 buffers. The same necessary-condition and singular-completion arguments
apply; merely changing a rank flag would not have been safe. Current whole-rank evidence is indexed in `verification/README.md`.
