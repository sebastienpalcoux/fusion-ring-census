# Verification evidence

[Data](../results/README.md) · [Coverage arguments](../methods/completeness.md) · [Provenance](../docs/PROVENANCE.md)

Every released census covers the entire rank, including every duality type.
Completeness uses the exhaustive search argument and normally completed enumeration;
independent tensor checks establish validity and uniqueness. At rank 7 through
multiplicity 5 and rank 8 through multiplicity 3, completion is producer-reported.
The complete optimized sources are now supplied and hash-matched, but the full
searches have not been independently rerun. See [the rank-7 qualification](rank7/README.md).

| Rank | Complete through | Classes | Evidence |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | [Audit](rank3/audit.json) · [Source](rank3/source.json) |
| 4 | 128 | 889,530 | [Audit](rank4/audit.json) · [Source](rank4/source.json) |
| 5 | 20 | 40,999 | [Audit](rank5/audit.json) · [Source](rank5/source.json) · [Completed run](rank5/run.json) |
| 6 | 9 | 25,421 | [Audit](rank6/audit.json) · [Source](rank6/source.json) · [Completed run](rank6/run.json) |
| 7 | 5 | 10,006 | [Audit](rank7/audit.json) · [Source](rank7/source.json) · [Completed run](rank7/run.json) |
| 8 | 3 | 4,500 | [Audit](rank8/audit.json) · [Source](rank8/source.json) · [Completed run](rank8/run.json) |
| 9 | 2 | 2,225 | [Current checks](rank9/README.md) · [Audit](rank9/multiplicity2/audit.json) · [Source](rank9/multiplicity2/source.json) |
| 10 | 1 | 194 | [Audit](rank10/audit.json) · [Source](rank10/source.json) · [Completed run](rank10/run.json) |
| 11 | 1 | 182 | [Audit](rank11/audit.json) · [Source](rank11/source.json) · [Completed run](rank11/run.json) |
| 12 | 1 | 632 | [Checks and source](rank12/README.md) |

## Supplied high-rank datasets

Ranks 9–12 are included in the current manifest, including rank nine through multiplicity two. All supplied tensors and exact based-isomorphism uniqueness passed fresh checks. The complete sources and normally completed strata support producer-reported enumeration completeness; full searches were not independently repeated. [High-rank source](engine_20261023/README.md) · [Rank-twelve source](engine_rank13_20261023/README.md).

## Independent checks

Every released tensor is checked for nonnegative integer coefficients, both unit
laws, duality, reciprocity and all integer associativity identities. Canonicalization
uses exhaustive unit-fixing permutations at lower ranks and exact invariant refinement at ranks 9–12, with full tensor comparison of witnesses. All released
lists have zero duplicate based-isomorphism classes.

The supplied laptop datasets at ranks 5–8 passed independent checks of their
tensors, counts and established count prefixes. At rank 7, the verifier,
exporter and equation-system hashes were checked against available sources;
the complete optimized sources were subsequently supplied and hash-matched, as recorded above. Hosted audits:

- Rank 5: [audit 35553424461](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35553424461).

Local checks (no hosted audit is claimed for these current datasets):

- Rank 6: [local audit](rank6/audit.json), [fresh check](rank6/fresh_verification/summary.json) and [retained log](rank6/logs/fresh_verification.log).
- Rank 7: [local audit](rank7/audit.json), [fresh check](rank7/fresh_verification/summary.json) and [retained log](rank7/logs/fresh_verification.log).
- Rank 8: [local audit](rank8/audit.json), [fresh check](rank8/fresh_verification/summary.json) and [retained log](rank8/logs/fresh_verification.log).

The rank-6 audit checked **25,421 tensors** and
**3,050,520 permutations**.
These checks performed verification only; they did not rerun enumeration.
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

## Rank-twelve release

The 632 supplied multiplicity-one rings are released with all exact checks and producer logs. [Verification](../verification/rank12/README.md) · [Matching complete rank-13 symmetry source and reproduction command](../verification/engine_rank13_20261023/README.md). The older root launcher remains the rank-3–11 driver; the separate source package reproduces rank twelve.


## Companion classification

R8_3_1768 is generally excluded by pivotal conjugation parity after the established sphericalization/Galois reduction. Six cases remain unresolved across ranks six, eight and nine. The rank-eight exact-M3 partition is 3,508 general exclusions, 16 unitary models and three unresolved rings; cumulative rank eight through three is 4,404/93/3. Rank nine exact-M2 remains 2,046/36/1.

These are categorification decisions. Census tensors, count terms and enumeration-completeness qualifications are unchanged. [Current snapshot](classification.json) · [Unified proofs and exact certificates](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md).
