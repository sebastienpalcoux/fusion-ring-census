# Exact pruning for the self-dual enumeration

This note proves that the new tests preserve every canonical solution of the
bounded associativity system. They use only the based-ring equations and
basis relabeling. No categorifiability, integrality of dimensions, spectral
simplicity, or irreducibility assumption is used.

## Notation and identities

Write the rank as `r=N+2`. Besides the unit and a distinguished nonunit object
`x`, index the other objects by `0,...,N-1` (these are **tail indices**, so tail
index 0 does not denote the unit). Set

- `a=N_xx^x`, `u_i=N_xx^i`, and `Q_ij=N_xi^j`;
- `T_ijk=N_ij^k`, and `(T_i)_jk=T_ijk`.

In the self-dual case Frobenius reciprocity makes `Q` symmetric and `T`
fully symmetric. Every free coefficient is an integer in `[0,M]`.
The existing canonical parameter order begins with the nondecreasing vector
`u`; put `b=min(u)`. It follows that every mixed coefficient `T_iik`, `i!=k`,
and every `Q_ii`, is at least `b`.

Let `C=1` for ordinary fusion-ring equations. The pre-existing folded branch
uses the same reduced equations with the constant unit contribution changed
to `C=2`. The arguments below apply to either constant. Associativity gives

```
T_i u = (Q^2 - a Q - C I)e_i + u_i u,
Q T_i - T_i Q = (Qe_i)u^t - u(Qe_i)^t.                 (1)
```

Here vectors are columns and `t` on a matrix denotes transpose. In particular,

```
sum_k u_k T_iik = u_i^2 + sum_k Q_ik^2 - C - a Q_ii.  (2)
```

## Canonical generator rows and exact reachable sums

For every tail generator `i`, a canonical table must satisfy

```
sort(Q_ii, (T_iik)_{k!=i}) >= u                       (3)
```

in **lexicographic order**. To prove this, relabel `i` as the distinguished
object and sort the remaining objects by their new mixed coefficients.
The first block of the resulting parameter vector is precisely the left side
of (3). All these relabelings belong to the permutation group used by the
existing full canonical test. A smaller first block would contradict
canonicality, regardless of subsequent entries. Condition (3) is not a
coordinatewise inequality.

For fixed `i`, enumerate the mixed values `t_k=T_iik` in `[b,M]`, `k!=i`.
Increasing `q` cannot decrease `sort(q,(t_k)_{k!=i})` lexicographically.
Consequently, the admissible `q` in `[b,M]` form an upper interval, possibly
empty. Find its least element. For every cubic value `t_i` in `[0,M]`, record
that element at the weighted sum `z=sum_k u_k t_k`, taking the minimum over
all witnesses. Thus

```
z is attainable subject to (3) at Q_ii=q
    if and only if recorded_minimum[z] <= q.         (4)
```

The diagonal row mask combines (4) with (2). For a partially assigned row,
its missing square terms range over exact bounded sums of squares; the
existing finite convolution computes these possibilities. This is a
necessary condition during partial enumeration and an exact test of the
single contraction (2) once the row is complete. It need not enforce the
other associativity equations at this stage.

During reachable-sum construction, values attached to equal weights `u_k`
may be enumerated in nondecreasing order. Permuting those values changes
neither their weighted sum nor their sorted tuple. This removes redundant
assignments without changing (4).

## Three bounded moment identities

Once the first tail row of `Q` is assigned, put

```
q=Qe_0,    t=T_0 e_0.
```

The actual unknown vector `t` satisfies `0<=t_0<=M`, `b<=t_j<=M` for `j>0`,
and `sort(Q_00,t_1,...,t_(N-1))>=u`. From (1), symmetry, and the commutator in
(1), one obtains the following exact identities:

```
u^t t = ||q||^2 + u_0^2 - C - a q_0,                 (K0)

t^t Q u = q^t Q q - C q_0 + 2u_0 q^t u
          - ||u||^2 q_0 - a ||q||^2,                (K1)

t^t Q^2 u = ||Qq||^2 - C ||q||^2 + 2u_0 q^t Q u
            + (q^t u)^2 - ||u||^2 ||q||^2
            - q_0 u^t Q u - a q^t Q q.             (K2)
```

For example, `K0` is the `e_0` component of the first identity in (1).
For `K1`, substitute that identity into
`T_0 Q=Q T_0-q u^t+u q^t` and take the `e_0,u` matrix coefficient.
For `K2`, use

```
T_0 Q^2 = Q^2 T_0 - Qq u^t + Qu q^t
                      - q u^t Q + u q^t Q
```

and take the same matrix coefficient. These derivations require no inverse
and remain valid for singular matrices and singular modular reductions.

Enumerating every bounded `t` satisfying `K0` and its canonical row condition
therefore retains the true `t` of every canonical completion.

## Early linear filtering

With `q` fixed, move `K1` to one side. It becomes

```
t^t Q u - q^t Q q + Cq_0 - 2u_0 q^t u
                    + ||u||^2 q_0 + a||q||^2 = 0.    (5)
```

The coefficient of an unassigned off-diagonal entry `Q_ij` is exactly

```
c_ij=t_i u_j+t_j u_i-2q_i q_j.
```

The diagonal entries and first tail row have already been assigned.
For each witness, let `R` be the accumulated constant and assigned terms of
(5). If the remaining coefficients are `c_e`, any completion must satisfy

```
R + sum_e min(0,M c_e) <= 0 <= R + sum_e max(0,M c_e),
gcd(c_e) divides R when that gcd is nonzero.          (6)
```

These interval and divisibility tests are necessary integer conditions.
The implementation updates `R` upon descent and restores it upon return.
If no witness survives for a value of `a`, that value cannot extend to a
canonical solution. The exact bounded range is used when solving a final
linear variable; a zero coefficient never justifies division.

## Exact masks for a small final block of edges

Take a final block of unassigned edges lying outside the fixed first row.
Write

```
Q = B + sum_e z_e E_e,
```

where each `E_e` has ones at the two symmetric positions of its edge and
zeros elsewhere, and `0<=z_e<=M`. Equation (5) is linear in these variables.
Moving `K2` to one side gives the quadratic polynomial

```
F(Q) = (Qu)^t(Qt) - ||Qq||^2 - 2u_0 q^t Qu - (u^t q)^2
       + (C+||u||^2)||q||^2 + q_0 u^t Qu + a q^t Qq. (7)
```

All polynomial coefficients are obtained by exact expansion of (7).
For each retained witness, enumerate the bounded final-edge assignments
satisfying both (5) and `F(Q)=0`. Where possible, solve the last linear
variable using divisibility and range checks. If its coefficient and the
residual both vanish, enumerate its entire bounded range. If its coefficient
vanishes and the residual does not, there are no assignments for that witness.

The resulting mask is the union over witnesses, with a bit recording each
supported `a`. A partial lookup takes the union over the still-unassigned
mask coordinates. Thus the mask records an existential necessary condition;
it cannot remove a completion whose genuine `t` satisfies `K0`--`K2`.
The number of final edges grouped together affects performance, not this
argument. Precomputing coefficient vectors such as `B^2 u` instead of
repeatedly multiplying `B t` is the same exact polynomial calculation.

The existing modular reconstruction or exhaustive singular-completion solver
still checks the remaining constraints and the full canonical condition.
Passing a new mask alone is never treated as a completed ring.

## Degenerate and resource-limited cases

If `sum(u)=0`, nonnegativity gives `u=0`. Every expression involving `t` in
`K0`--`K2` then vanishes. The canonical row inequality against the zero vector
is automatic. For these filters only, one may therefore use the surrogate
`t=0`: it records exactly the same moment restrictions as every actual `t`.
This does not set the actual tail coefficients to zero; reconstruction or
exhaustive completion still determines and checks them.

If a witness-generation visit limit or storage limit is reached, the new
witness filter is disabled for the affected first-row branch and enumeration
returns to the original necessary masks and completion path. An interrupted
witness list is never used as though exhaustive. This fallback may reduce
speed but preserves completeness.

All statements are uniform in `N` and the coefficient bound. Practical
supported ranks, integer widths, and storage bounds are implementation
limits; they are not additional mathematical hypotheses for these tests.
