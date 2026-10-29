# Fusion Ring Census: project guide

[Overview](../README.md) · [Counts](../results/table.md) · [Datasets](../results/census.json) · [Verification](../verification/README.md)

The release contains **1,434,042 based-isomorphism classes at ranks 3–12**, within the multiplicity bounds in the [manifest](../results/census.json). Every duality type is included, including noncommutative rings. No categorifiability filter is applied. Rank two is treated symbolically by the companion classification rather than included in this finite data total.

## What is counted

A fusion ring is a finite-rank based ring with nonnegative integral structure constants, a distinguished unit and duality satisfying the usual reciprocity identities. A based isomorphism permutes its basis while preserving the unit and multiplication. The multiplicity is the largest coefficient in the full ordered multiplication tensor. These are algebraic objects; a fusion category realizing one is additional structure.

## Counts by rank and multiplicity

Each count is at **exactly** the stated multiplicity. A bound M includes all multiplicities at most M. A dash in a table means unavailable, not zero. The complete exact and cumulative definitions, all data and current counts are in the [count table](../results/table.md), [CSV](../results/counts.csv) and [interactive viewer](index.html).

## Complete datasets

The [manifest](../results/census.json) records one current tensor file and parameter file per rank, source hashes, completed bounds and verification qualifications. Data and rank-specific companions are indexed on the [front page](../README.md#datasets).

Independent output checks establish tensor validity, uniqueness, counts, parameter re-export and checksums. For rank 7 through multiplicity 5, rank 8 through 3, and supplied ranks 9–12, full enumeration completeness is **producer-reported**: all strata completed and the complete source was supplied and hash-matched, but the full searches were not independently repeated. This qualification is separate from the exact verification of their output.

## Companion categorification

The [classification repository](https://github.com/sebastienpalcoux/grothendieck-ring-classification) and [public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/) record exclusions, categorical models and unresolved cases. Exclusion from categorification never removes a ring from this census. A feasible necessary system or a candidate based module is not a categorical model.

At rank eight, the exact-multiplicity-three band has **3,508 general
exclusions, 16 unitary models and 3 unresolved categorification candidates**
among its 3,527 supplied rings. Together with the earlier 896 exclusions and
77 unitary models through multiplicity two, this gives **4,404 general
exclusions, 93 unitary models and 3 unresolved rings** among 4,500 supplied
rank-eight rings. The candidates are not asserted fusion categories or
established exotic examples. The general questions `R6_4_155` and
`R6_8_1660` also remain open; see the [current classification account](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/docs/RESEARCH_STATUS.md)
for the precise proof scope and remaining categorical gaps.
These counts are bound to the [classification main snapshot `19ddd5ac`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/19ddd5ac68a0a356300af35f38743dba89966dd6) and its [decision ledger](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/19ddd5ac68a0a356300af35f38743dba89966dd6/evidence/frontier/rank8_m3_ledger.json).
The general-complex exclusion of `R8_3_1768` follows from a pivotal conjugation-pairing parity obstruction after the established sphericalization/Galois existence reduction. The complete two-sign domain is rejected by six exact rational separation certificates.

The three unresolved rank-eight rings are `R8_3_928`, `R8_3_941`, `R8_3_1154`. Their stronger fusion-matrix, Galois and center restrictions are necessary conditions, not categorical models.

No new model is claimed. The [unified proofs and exact replay](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md) state the categorical hypotheses, exact certificate scope and remaining gaps. Census tensors, counting terms and enumeration-completeness qualifications are unchanged.

At rank seven through multiplicity five, all 10,006 supplied tensors have a classification: 9,976 general exclusions and 30 known unitary models. Rank nine at exact multiplicity two has 2,046 general exclusions, 36 unitary models and one unresolved case. Higher-rank status is displayed uniformly in the public Atlas.

The current total is **six unresolved cases**: R6_4_155, R6_8_1660, R8_3_928, R8_3_941, R8_3_1154 and R9_2_137. The conditional R1660–R941 algebra construction is not an existence proof. The current [classification snapshot](../verification/classification.json) distinguishes these decisions from census provenance.

## Reproduce a census

Use the [reproduction guide](REPRODUCIBILITY.md), with the launcher and source package appropriate for the requested rank. A run is complete only after every duality stratum finishes normally and the output passes all checks. The [coverage arguments](../methods/completeness.md) explain the search model; [verification records](../verification/README.md) identify actual completed runs.

## Read and reuse

- [Mathematical companions](../manuscripts/README.md): definitions, coverage, counts and commands.
- [Provenance](PROVENANCE.md): source identities and the boundary between checking output and repeating enumeration.
- [Attribution and licensing](../NOTICE.md), [citation](../CITATION.cff) and [OEIS files](../oeis/README.md).
- [Current project announcement](../announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf), [Hexagon](https://hexagonmath.org/2610.00300) and [how to cite](https://sebastienpalcoux.github.io/grothendieck-ring-classification/#cite).

**AI-generated research; independent human verification and formalization remain pending.** Computational checks certify only their documented scope.
