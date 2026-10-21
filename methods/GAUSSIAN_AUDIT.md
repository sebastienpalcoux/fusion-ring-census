# Independent audit of the combined completion solver

Audited file: `code/completion_solver.hpp`
SHA-256: `9cc88c01a5d50953bb39b6977dfbb6ace206447cc528aa86e7d78b1ffe93dc86`

The packaged header removes an unused experimental gate (whose default was zero)
and an unused array from the initial audit snapshot. All four general audits were
rerun against this cleaned header and passed. This audit covers the earlier application of Gaussian elimination, support propagation from reduced rows with two or three free variables, interactions with domain mutation, and the added exact three-variable quadratic propagator.

## Mathematical and code review

1. **Earlier elimination is sound.** At entry, the solver records all variables whose domains are not singletons. It includes an equation in the linear system only if every monomial has at most one such variable. All other factors are known singleton values and are substituted exactly. Skipping an equation with two unfixed factors is conservative, including when nonlinear terms would happen to cancel. Every resulting linear congruence modulo 257 is necessary for every integer solution in the current domains. There is no mathematical need for the former first-matrix-prefix gate.

2. **Row reduction is sound.** The matrix is reduced by invertible field row operations modulo the prime 257. Each nonzero pivot is normalized and eliminated from all other rows, giving reduced rows of the form `x_p + sum_j a_j x_j + c = 0 mod 257`. A row with all variable coefficients zero and nonzero constant correctly proves infeasibility. Arrays for rows, columns and pivots are bounded by the equation and variable counts. Nonpivot columns are precisely the possible nonzero columns after each pivot in a final reduced row.

3. **Two- and three-free-variable support is exact for its row.** The new block enumerates every tuple from the current actual domains of the two or three free variables, computes the unique pivot residue, and retains it only when it lies in `[0,M]` and is present in the pivot domain. The bound `M <= 15 < 257` makes residue-to-domain-value conversion injective. The union of all accepted tuples is exactly the unary support projection of that reduced row. Therefore removing all other values cannot remove a solution of the full system. The existing zero- and one-free-variable cases have the same justification.

4. **Residues and shifts are safe on the supported input range.** The smallest numerator in the three-free-variable block is `257^2 - 256 - 3*256*15 = 54273 > 0`. Thus C++ remainder cannot be negative. A bit shift is evaluated only after the residue is checked to be at most `M <= 15`. Products and offsets in modular elimination are at most on the order of `257^2`, comfortably within `int`. Original generated associativity coefficients and the supported bounds also keep pre-reduction accumulation within `int`.

5. **Domain mutation does not invalidate the matrix.** The matrix is constructed and reduced before the first domain update. Its equations remain necessary under every subsequent restriction of domains. A later row may use domains narrowed by earlier rows; enumerating these narrower domains is sound. Within one row, every support mask is collected before any of that row's updates, so successive updates only intersect with sound projections. If another row later removes supporting values, the earlier mask may temporarily be weak, but never unsound. Updates queue affected original equations; another propagation cycle may strengthen the result. Matrix scratch arrays are reused only after propagation has finished, as required by the search recursion.

6. **Trail restoration is exact.** Every successful domain restriction records the preceding domain, and unsuccessful empty intersections do not mutate it. Reversing the trail therefore restores the entry domain box even when a later row discovers a contradiction.

7. **Three-variable quadratic support is exact.** After substituting fixed variables, coefficients are collected into one residual quadratic polynomial, including repeated and mixed monomials. The routine enumerates two actual variable domains and exactly solves or enumerates the final variable. The final linear zero-coefficient case correctly supports all final-domain values only when the constant also vanishes. Early termination occurs only after all current values of all three variables already have witnesses. This propagator is independent of the Gaussian congruence filter.

## Executed independent tests

`tests/audit_optimized_pruning.cpp` is the independent full-propagation audit,
compiled against the packaged header.

- 30,000 random polynomial systems: 422,833 exhaustive assignments; all 52,840 exact solutions retained by full propagation.
- 100,000 random symmetric-matrix moment checks passed.
- 10,000 independently exhaustive reachable-mask checks passed.

`audit_gaussian.cpp` calls `gauss()` directly before any other propagation, preventing earlier exact-polynomial propagation from hiding Gaussian bugs.

- 12,000 systems, using bounds throughout 1 through 15 and domains with holes.
- 1,629,740 exhaustive assignments; all 69,379 modular solutions retained.
- 9,171 satisfiable systems and 2,829 unsatisfiable systems.
- 2,000 single reduced rows with exactly two free variables and 2,000 with exactly three free variables: feasibility and every unary support mask matched exhaustive modular enumeration exactly.
- The remaining systems combine several equations, fixed factors, signed coefficients, and possible dependencies to exercise row operations and successive domain restrictions.
- 8,990 successful domain reductions.
- Exact trail restoration checked for every trial, including rejected domain boxes.

`audit_exact3.cpp` independently checked 20,000 residual polynomial support instances by exhaustive enumeration, including arbitrary signs, constants, repeated monomials, squares, domain holes and fixed variables. All passed.

Complete census output comparisons already performed: rank 7 / one dual pair / bound 3 (385 classes), rank 8 / one dual pair / bound 2 (306 classes), and self-dual rank 7 / bound 2 (212 classes) all match their former-code output sets exactly.

## Conclusion

No soundness or completeness defect was found in the reviewed Gaussian changes or the exact three-variable polynomial propagator. The numerical comparisons are finite tests; the preservation arguments above explain why these particular pruning operations cannot discard valid bounded integer solutions. This audit does not claim a formal proof of every component of the entire census implementation.

The experimental `GATE` preprocessor switch and its zero-length loop have been removed from the delivered source.
