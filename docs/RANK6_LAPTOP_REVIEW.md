# Rank-six laptop result reviewed on 20 September 2026

**Accepted:** the complete rank-six census through multiplicity **7** contains
**9,613** based-isomorphism classes, including **3,814** of exact multiplicity 7.
The previous 5,799 classes through 6 remain in the count prefix unchanged.
The full six-rank released total is **1,395,146**. Other ranks are unchanged.

## Input and exhaustive completion

The supplied `rank6_multiplicity7_verified.zip` has SHA-256:

`5793f214391f1c3f1d14b82336cb474b3b646c8dbf14099d744fd3c048054de7`.

It was generated from repository commit
`42b7a8f22994b087154fcea880f51b244894ba84` with the supplied laptop-only driver
patch. The exact code-tree hash matches the delivered laptop package:
`ba37fdc2077a1cc14e6b91febe0bed09ac707631f01efa24fa19ef5054e5afc4`.
The patch and old baseline snapshot are retained with the imported reports;
C++ generators, exact arithmetic, all singular/zero-coefficient branches and
coverage arguments were unchanged. No categorifiability filter was imposed.

| Duality stratum | Complete classes through 7 | Exact multiplicity 7 | Enumeration seconds |
|---|---:|---:|---:|
| One dual pair | 1,140 | 342 | 10.263 |
| Two dual pairs | 123 | 23 | 3.534 |
| Self-dual | 8,350 | 3,449 | 3,507.317 |
| Whole rank | **9,613** | **3,814** | **3,521.115** |

All subprocesses returned zero. The self-dual enumerator completed **330/330**
work units. Total driver time, including compilation, export, independent
verification and compression, was **3,532.356 seconds (58 min 52.36 s)**.
The laptop used **12 threads**. Its independent checker reported zero duplicates.

## Fresh independent verification before integration

[GitHub audit run 35499152450](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35499152450)
ran the unchanged repository verifier against the uploaded data, using candidate
commit `7397377085bbdd911a0fc70246a77687b6c579ec` and a 10-minute job ceiling.
It completed successfully without running enumeration. The review checked:

- Both decompressed data checksums and all required duality completion records.
- All **9,613** full tensors: nonnegative integer coefficients, unit, duality,
  reciprocity and every associativity identity.
- Every unit-fixing basis permutation: **1,153,560** permutations in total,
  yielding **zero** literal or based-isomorphism duplicates.
- The exact-multiplicity counts **39, 154, 384, 872, 1582, 2768, 3814** and
  agreement with the full previously released prefix through 6.

Verification proves validity and uniqueness; exhaustive coverage additionally
uses the existing mathematical arguments and normally completed searches of
all duality strata. A green workflow status alone is not a completeness proof.

The compressed data are now in `results/rank6_through7_*.txt.gz`. Original laptop
logs and report, laptop and fresh independent audits, import receipt and source
patch are under `verification/imports/rank6_through7/`. Original bound-six datasets
remain preserved. The staging candidate is retained in the Git history at the
candidate commit rather than duplicated in the current tree. The audit workflow
pins that original candidate and old baseline for future reproducibility.

The original laptop `run.json` uses Python JSON's `Infinity` value for its
unlimited per-stratum clock allowances; it is retained byte-for-byte as evidence.
It does not denote an incomplete search. New launcher reports use standard JSON
`null` for these allowances. The receipt's pending status records the intake
stage; `review.json` and this review record its subsequent acceptance.

## Comparison with the hosted attempt

[Hosted run 35451839114](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35451839114)
used two threads and exhausted its budget after 21,192.87 driver seconds.
The two nonselfdual strata completed, but the self-dual stratum completed only
244/330 work units. Its return code 3 was expected budget exhaustion, with no
complete extension and no detected compilation or verification failure. Small
original diagnostics are preserved under `verification/github_actions/run35451839114/`.
The workflow's success conclusion recorded a handled timeout, not a new census.

The laptop had six times as many requested threads. This plausibly explains much
of the elapsed-time difference, along with CPU and scheduling differences.
Work units have unequal cost; the logs do not support a precise hardware
speedup estimate or a runtime forecast for bound 8.

Before the fresh audit, billing showed 705 / 2,000 included Actions minutes used,
storage rounded to 0 / 0.5 GB, $0 billable usage, and an account-wide $0 Actions
budget with enforced stop-usage enabled. No billing or visibility setting changed.

## Derived files and next searches

All six mathematical companions, the main manifest and count projections,
landing page, README and local OEIS drafts reflect the accepted result. The
fixed-rank-six draft gains c_6(7)=3814; no OEIS accession is invented and no
online submission was made. The repository remains private.

The reusable [laptop launcher](LAPTOP.md) accepts ranks 3–8 and selectable bounds.
The nearest unfinished bounds are 129, 20, 8, 4 and 2 at ranks 4–8. Rank 3 is
already complete through its supported ceiling of 1000. No new search was
launched during this integration.
