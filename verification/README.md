# Verification evidence

[Data](../results/README.md) · [Coverage arguments](../methods/completeness.md) · [Provenance](../docs/PROVENANCE.md)

Every released census covers the entire rank, including every duality type.
Completeness uses the exhaustive search argument and normally completed enumeration;
independent tensor checks establish validity and uniqueness.

| Rank | Complete through | Classes | Evidence |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | [Audit](rank3/audit.json) · [Source](rank3/source.json) |
| 4 | 128 | 889,530 | [Audit](rank4/audit.json) · [Source](rank4/source.json) |
| 5 | 20 | 40,999 | [Audit](rank5/audit.json) · [Source](rank5/source.json) · [Completed run](rank5/run.json) |
| 6 | 8 | 16,612 | [Audit](rank6/audit.json) · [Source](rank6/source.json) · [Completed run](rank6/run.json) |
| 7 | 4 | 4,201 | [Audit](rank7/audit.json) · [Source](rank7/source.json) · [Completed run](rank7/run.json) |
| 8 | 2 | 973 | [Audit](rank8/audit.json) · [Source](rank8/source.json) · [Completed run](rank8/run.json) |

## Independent checks

Every released tensor is checked for nonnegative integer coefficients, both unit
laws, duality, reciprocity and all integer associativity identities. Canonicalization
uses every unit-fixing basis permutation, with exact tensor comparison. All released
lists have zero duplicate based-isomorphism classes.

The completed laptop datasets at ranks 5–8 also passed independent GitHub audits
of their supplied tensors, source hashes, counts and established count prefixes:

- Ranks 5, 7, 8: [audit 35553424461](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35553424461).
- Rank 6: [audit 35807052254](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35807052254).

The rank-6 audit checked **16,612 tensors** and
**1,993,440 permutations**.
These hosted jobs performed verification only; they did not rerun enumeration.
[Runner environments](environments.json) are indexed by audit run.

The rank-4 audit jointly checked 889,530 released tensors and 2,787
reference records. The raw comparison consequently has 2,787 repetitions in the
reference suffix; the released enumeration itself has zero duplicates. Its raw
comparison and containment witnesses are in
[rank4/reference_comparison](rank4/reference_comparison/).

## Reproducibility records

Each rank directory contains the audit and source receipt for its current dataset.
Laptop run records retain the exact commands, environment, per-phase timings and
nonempty subprocess logs. Absolute laptop paths in these records document the
computation; use the portable [reproduction commands](../docs/REPRODUCIBILITY.md)
on another computer. Archive hashes identify the supplied payloads, and the
[manifest](../results/census.json) identifies the released compressed data.

Only one current tensor file and parameter file per rank are retained. Verification
reports do not contain duplicate tensor collections. Supporting
[optimization regressions](regressions/) test the indicated small bounds and strata;
they do not substitute for the full independent audits.

[Repository checks](checks/) cover file integrity, count projections, documentation
and lightweight unit tests. They are separate from the mathematical checks above.
