# Provenance and attribution

[Overview](../README.md) · [Verification](../verification/README.md) · [Licensing](../NOTICE.md)

## Certified data

Release 0.2.3, dated 2026-10-19, contains **1,427,282**
distinct based-ring classes across six bounded regions. The
[manifest](../results/census.json) fixes every bound, exact-multiplicity count,
tensor checksum and verification location.

| Rank | Bound | Classes | Origin |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | Completed project census |
| 4 | 128 | 889,530 | Completed project census |
| 5 | 20 | 40,999 | Completed laptop census |
| 6 | 9 | 25,421 | Completed laptop census |
| 7 | 5 | 10,006 | Completed laptop census |
| 8 | 2 | 973 | Completed laptop census |

Each [rank's evidence](../verification/README.md) identifies its enumeration source,
completed computation and independent audit. Laptop source receipts record the
archive checksum and exact code revision; run records retain commands, environment
and timings. Archive inventories, decompressed hashes and established count prefixes
are checked before integration. Every required duality stratum must finish normally.

The supplied rank-5–8 tensors were independently checked under every unit-fixing
basis permutation, with no duplicate classes. The evidence index distinguishes
hosted audits from local checks. These checks ran verification only; laptop
enumeration times remain attributed to the laptop.
No incomplete search contributes an exhaustive count.

### Rank-7 multiplicity-5 qualification

The supplied archive reports normal completion of all four duality strata in
77,046 seconds on the producer's laptop. Its new exact-multiplicity-5 band has
5,805 classes; the cumulative list has 10,006. Fresh local checks verify all
tensor axioms, 7,204,320 unit-fixing permutations, zero duplicate classes,
byte-identical parameter re-export, and exact tensor-set agreement with the
previous 4,201-class prefix. These checks did not rerun enumeration.

The producer used an optimized local source package based on commit
`d4c36cc2ee5eb5f0e5291de18d2bb433ffb7ce8b`. The archive contains source hashes
and logs, but omits the modified enumeration sources. Therefore enumeration
completeness remains **producer-reported**, not independently reproduced in
this release. The original receipt, logs and previous audit are retained under
[rank7](../verification/rank7/README.md). The available repository enumerator
can attempt an independent rerun; matching its source to the producer's modified
implementation is not claimed.

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
