# Provenance and attribution

[Overview](../README.md) · [Verification](../verification/README.md) · [Licensing](../NOTICE.md)

## Current release

Release 0.2.0, dated 21 September 2026, contains **1,405,669** distinct based-ring
classes across six complete regions. The [manifest](../results/census.json) fixes
every bound, exact-multiplicity count, tensor checksum and verification location.

| Rank | Bound | Classes | Origin |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | Retained complete census and independent audit, 18 September |
| 4 | 128 | 889,530 | Retained complete census and independent audit, 18 September |
| 5 | 20 | 40,999 | Completed laptop census supplied 21 September |
| 6 | 7 | 9,613 | Laptop reproduction of the existing complete census |
| 7 | 4 | 4,201 | Completed laptop census supplied 21 September |
| 8 | 2 | 973 | Completed laptop census supplied 21 September |

The four supplied archives used code from revision
`942dbd9c4f4149479e51acb1224f3c71ca47a64b`. Their complete run records, archive
checksums, source identity, commands and logs are in `verification/rank5/` through
`verification/rank8/`. Both compressed inventories and decompressed data hashes
were checked before integration. A fresh independent
[GitHub audit](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35553424461)
verified every tensor and every unit-fixing basis permutation, with no duplicates
and no change to any prior exact-multiplicity prefix. Rank 6 has identical
decompressed tensors and parameters to its previous release; it is not a new bound.

Laptop timing records describe those laptop computations. They are not attributed
to GitHub. The fresh GitHub run was a verifier, not an enumeration. Rank-3 and
rank-4 historical checks were retained, not relabelled as newly executed checks.
No incomplete search contributes an exhaustive count.

## Mathematical sources

Gert Vercleyen and Joost K. Slingerland, *On Low Rank Fusion Rings*, Journal of
Mathematical Physics **64** (2023), 091703; arXiv:2205.15637v4. The retained ancillary
`FusionRingMultiplicationTables` file has SHA-256
`b587c3f683157369da7cc090f762bbff0e18dcf11acc3f5031d6bc0c643843f8`.
Its 28,451 records represent 25,138 distinct classes. The 3,313 redundant records
all occur at rank five and exact multiplicities 9–12; each deletion has a checked
unit-fixing basis-permutation witness. The input was retained from an earlier
project archive, not freshly downloaded during this revision.

The [source audit](../audit/README.md) is a comparison and deduplication study.
The source data do not feed the independent enumerators. Deduplication alone
does not establish completeness of the source's partial-search cells.

Rank-four and rank-five reductions are retained from the Dong–Palcoux census
project and exact-certificate supplements, September 2026. The
[methods](../methods/completeness.md) retain zero-coefficient and singular branches.
The six [companions](../manuscripts/README.md) are unpublished computational research
notes; no journal acceptance, DOI or arXiv identifier is asserted for them.

## Code and computational evidence

Rank-eight support uses dynamically sized linear-algebra workspaces: its self-dual
system has 84 variables and 231 equations. The general solver includes all duality
types and noncommutative cases. No categorifiability filter is applied. The present
revision reorganizes release materials and removes obsolete launch modes; it does
not change the C++ enumerators or their mathematical pruning rules.

GPT-6 Astra Pro assisted with algorithm development, code, exposition and
computational checks. Exact independent verification and exhaustive coverage
arguments are separate evidence. Neither implies proof-assistant certification
or external peer review. These counts classify based rings, not tensor categories.

## Repository organization and history

There is one current dataset and evidence directory per rank, one manifest, one
reproduction guide and one generic bounded frontier workflow. Counts in the
front page, CSV files, companions and OEIS drafts derive from that manifest.
Superseded tensor copies, dated review narratives, temporary audit payloads and
single-bound workflows have been removed from the current tree. Their records
remain in [Git history](https://github.com/sebastienpalcoux/fusion-ring-census/commits/main),
including the complete [pre-integration audit revision](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b5e15383c75f46e1d00679a3815dc56e638f4a56).
Repository visibility is public by the maintainer’s authorization. No online
OEIS submission is implied.
