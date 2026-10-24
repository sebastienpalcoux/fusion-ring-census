# R8_3_3472: exclusion and focused research history

Updated 22 October 2026. **R8_3_3472 has no complex fusion categorification.**
The completed computer-assisted proof supersedes the earlier necessary
restrictions and scoped construction obstruction recorded below. Its scope
includes arbitrary complex fusion categories.

## Classification and publication provenance

The previous classification snapshot
[`7b98ab97ac2391997f41d4a05f3b70e9d792fd48`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/7b98ab97ac2391997f41d4a05f3b70e9d792fd48)
had ledger SHA-256
`edac9d5685ed86acfff16d620598d76324430559cab58d9bf24d59074927d067`.
It recorded this case as unresolved. The current classification adds the
general exclusion, with canonical evidence in
[`evidence/r3472_exclusion_20261022/`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/r3472_exclusion_20261022).
The generated census overview records the publication revision for its current
classification totals; historical snapshot claims retain their original pins.

| Scope | General exclusions | Unitary models | Unresolved | Supplied rings |
|---|---:|---:|---:|---:|
| Rank 8, exact multiplicity 3 | 3,507 | 16 | 4 | 3,527 |
| Rank 8, multiplicity at most 3 | 4,403 | 93 | 4 | 4,500 |

The four unresolved rank-eight rings are `R8_3_928`, `R8_3_941`,
`R8_3_1154`, and `R8_3_1768`. Together with `R6_4_155` and `R6_8_1660`,
six cases remained open at ranks at most eight at this historical checkpoint. This excludes the later rank-ten and rank-nine continuations. The [24 October audit correction](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/audit_20261024/README.md) restores R8_3_436 to generally unresolved, giving seven open cases at ranks at most eight, with its unitary exclusion retained. No census tensor,
enumeration result, completeness qualification, or manifest count changes.

## Completed exclusion

Sphericalization and Galois transport reduce any hypothetical complex
categorification to the pseudo-unitary case. Exact induction, Galois
constraints and distinguished modular identities enumerate all 372 labelled
low center frames and exclude all but the equivalent frames 42, 117 and 304.
Their surviving restrictions force the relevant twist moments.

Cauchy's theorem and modular Galois symmetry reduce every possible remaining
twist to one of 424 weighted square-orbit types; this domain is complete and
does not assume an arbitrary twist-order cutoff. Cyclic-rotation identities
at orders 4, 5, 7, 8, 10, 16 and 20, together with indicator field membership,
give 628 necessary equations in 572 integer variables. A certificate of
1,648 exact integer-bound deductions followed by a rational separating
inequality proves the system impossible. The resulting exclusion covers all
center frames and hence all complex categorifications.

The [complete proof record](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/r3472_exclusion_20261022/README.md)
includes the mathematical reduction, exhaustive coverage audits, two portable
checkers using exact rational arithmetic, and a separately checked VIPR
infeasibility certificate. From the canonical evidence directory, run:

```sh
python3 verification/check.py
```

The terminal checker uses Python's standard library and no optimization
solver. It certifies the integer contradiction; the mathematical reduction
and coverage audits establish why that system is necessary.

## Earlier focused research

The following sections preserve the restrictions developed before the final
exclusion. Their feasible data satisfied weaker necessary systems, so they
do not contradict the complete proof. The
[focused evidence directory](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/r3472_focus_20261022)
retains those intermediate calculations and scoped construction analyses.

### All Morita partners: one or seven invertibles

For every hypothetical complex fusion category with the `R8_3_3472`
Grothendieck ring, every Morita partner has exactly **one or seven**
invertible simple objects. This result is not restricted to the two
previously identified rank-two based modules, nor does it assume that
either module has a categorical realization.

The proof descends every Morita partner's Frobenius--Perron dimensions to
the common global-dimension field, using the absence of nontrivial
central invertibles. Galois orthogonality and strong Lagrange divisibility
first leave invertible counts 1, 2, 5, and 7. Orbit parity excludes 2.
The 5-invertible case has four finite dimension profiles; fusion
reciprocity and rank-two/formal-codegree obstructions exclude all four.

In the 7-invertible case the dimension profile is forced to be
`1^7, (7 + 5 sqrt(2))^7`. The corresponding based fusion ring must be one
of two explicit rank-14 tensors. With indices modulo 7 and `a = +1` or
`a = -1`, their rules are

```text
g_i g_j = g_(i+j)
g_i X_j = X_(i+j)
X_i g_j = X_(i+a*j)
X_i X_j = g_(i+a*j) + 2 sum_k X_k
```

The identity-action ring is commutative; the inversion-action ring is
not. Full tensor-axiom checks establish that both are based fusion rings.
They do not establish categorifiability or a Morita equivalence to
`R8_3_3472`.

For the second rank-two module branch, the necessary arithmetic dimension
multisets decrease from 400,477 to 272,349: 272,348 have one invertible,
and the only surviving seven-invertible multiset is the profile above.
The all-Morita theorem removes 124,228 two-invertible and 3,900
five-invertible multisets. These numbers count dimension data, not based
rings, category models, or categorical module realizations.

Prepared sources:
[Morita proof and exact finite checks](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/r3472_focus_20261022/morita),
[candidate tensors and construction analysis](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/r3472_focus_20261022/constructions),
and [independent mathematical review](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/main/evidence/r3472_focus_20261022/review).

### Radchenko--Wheeler construction route

Obtaining the required global dimension `700 + 490 sqrt(2)` by direct
ordinary de-equivariantization of a Radchenko--Wheeler near-group parent
of order `N = 196` is obstructed, even after tensoring the parent with an
arbitrary pointed fusion category. The proof applies
to all corresponding `SL(2,Z)` inputs, including noncyclic parents.

The obstruction uses a necessary central half-braiding formula, its
two-primary quadratic form, and a bound on isotropic subgroups after
pointed stabilization. It does not assume unitarity. The required
Tannakian subgroup is too large. Passing to a Morita partner after such
a quotient cannot fix this dimension obstruction.

This statement does **not** exclude arbitrary near-group categories,
a nontrivial Morita change before quotienting, generalized-Haagerup
parents, or arbitrary chains of category constructions. It is not a
general exclusion of `R8_3_3472`.

Prepared source:
[construction obstruction and its exact checks](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/r3472_focus_20261022/constructions/CONSTRUCTIONS.md).

### Maximal third indicators

In the canonical spherical structure of every pseudo-unitary
categorification, the third Frobenius--Schur indicator is 1 on the unit
and **2 on each of the seven nonunit simples**. Equivalently, the
order-three rotation is the identity on each two-dimensional space
`Hom(1, X_i^3)`, for `i > 0`.

The existing sphericality and pseudo-unitary Galois reduction permits
application to a pseudo-unitary Galois form of any hypothetical complex
categorification. The new calculation does not independently establish
that reduction. The already certified phase relaxation satisfies these
third-indicator values, so this result supplies a necessary associator
constraint without eliminating that feasible point.

Prepared source:
[third-indicator proof and source-bound exact verification](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/r3472_focus_20261022/independent/THIRD_INDICATORS.md).

### Exact integer center relaxation

The stronger center relaxation with 3,347 equations and 13,242 variables
had an exact **nonnegative integer point** satisfying every equation
and propagated bound. Its sole fractional coordinate in the earlier
rational witness is removed using the exact column identity
`column 13024 = 100 * column 12917`: the coefficient `49/50` becomes
the integer coefficient 98 on column 12917.

This system includes Gram, distinguished-S, cubic Verlinde, Galois
balance, FP bounds, and unit-product constraints. It has no twist-phase
variables. A linked exact rational extension now satisfies the indicator
and rotation moments through order four: 80 equations, 391 variables, and
40 positive entries. Its complete 37-type relative-trace domain has no
categorical twist-order cutoff. This extension does not impose complete
complex STS equations or actual twist assignments. The combined necessary
data supply neither a modular datum nor a category.

Prepared source:
[exact integer witness](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/r3472_focus_20261022/center/integer_witness.json)
and [compatible indicator/rotation extension](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/r3472_focus_20261022/independent/phase_certificate.json).

## Census mirrors and reproduction

The current exclusion summary is generated from
`scripts/build_manuscripts.py:rank8_r3472_focus_addendum` into the README,
rank-eight mathematical companion, and census website. To regenerate:

```sh
python3 scripts/build_manuscripts.py --ranks 8 --compile --sync-readme
python3 scripts/build_site.py
python3 scripts/check_release.py --ranks 8
```

These commands build the census mirrors and check the released tensor
hashes/counts; they do not rerun category proofs or the census enumeration.
The companion evidence contains the separately scoped proof verifiers.
