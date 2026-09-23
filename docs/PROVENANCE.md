# Provenance and attribution

[Overview](../README.md) · [Verification](../verification/README.md) · [Licensing](../NOTICE.md)

## Certified data

Release 0.2.1, dated 2026-09-23, contains **1,412,668**
distinct based-ring classes across six complete regions. The
[manifest](../results/census.json) fixes every bound, exact-multiplicity count,
tensor checksum and verification location.

| Rank | Bound | Classes | Origin |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | Completed project census |
| 4 | 128 | 889,530 | Completed project census |
| 5 | 20 | 40,999 | Completed laptop census |
| 6 | 8 | 16,612 | Completed laptop census |
| 7 | 4 | 4,201 | Completed laptop census |
| 8 | 2 | 973 | Completed laptop census |

Each [rank's evidence](../verification/README.md) identifies its enumeration source,
completed computation and independent audit. Laptop source receipts record the
archive checksum and exact code revision; run records retain commands, environment
and timings. Archive inventories, decompressed hashes and established count prefixes
are checked before integration. Every required duality stratum must finish normally.

The supplied rank-5–8 tensors were independently checked on GitHub under every
unit-fixing basis permutation, with no duplicate classes. The hosted jobs ran
verification only. Laptop enumeration times remain attributed to the laptop.
No incomplete search contributes an exhaustive count.

## Mathematical sources

Gert Vercleyen and Joost K. Slingerland, *On Low Rank Fusion Rings*, Journal of
Mathematical Physics **64** (2023), 091703; arXiv:2205.15637v4. The retained ancillary
`FusionRingMultiplicationTables` file has SHA-256
`b587c3f683157369da7cc090f762bbff0e18dcf11acc3f5031d6bc0c643843f8`.
Its 28,451 records represent 25,138 distinct classes. The 3,313 redundant records
all occur at rank five and exact multiplicities 9–12; each deletion has a checked
unit-fixing basis-permutation witness. The source identity is recorded in
[audit/source.json](../audit/source.json).

The [source audit](../audit/README.md) is a comparison and deduplication study.
The source data do not feed the independent enumerators. Deduplication alone
does not establish completeness of the source's partial-search cells.

Rank-four and rank-five reductions come from the Dong–Palcoux census project
and exact-certificate supplements. The [methods](../methods/completeness.md) include
zero-coefficient and singular branches. The six
[companions](../manuscripts/README.md) are computational research notes; no journal
acceptance, DOI or arXiv identifier is asserted for them.

## Code and computational evidence

Rank-eight support uses dynamically sized linear-algebra workspaces: its self-dual
system has 84 variables and 231 equations. The general solver includes all duality
types and noncommutative cases. No categorifiability filter is applied.

GPT-6 Astra Pro assisted with algorithm development, code, exposition and
computational checks. Exact independent verification and exhaustive coverage
arguments are separate evidence. Neither implies proof-assistant certification
or external peer review. These counts classify based rings, not tensor categories.

## Organization and access

There is one dataset and evidence directory per rank, one manifest and one
reproduction guide. The front-page table, CSV files, companions and OEIS data
projections derive from the same manifest. Source attribution, licensing and
verification evidence are retained alongside the data.

The repository is public. [OEIS files](../oeis/README.md) are prepared data and
edit text; the repository does not certify their acceptance by OEIS.
