# R8_3_3472: general-complex exclusion

**R8_3_3472 has no complex fusion categorification.** Its proof is retained in the classification repository. The [current classification account](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md) supplies the current totals and unresolved list.

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

