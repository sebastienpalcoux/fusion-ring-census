# OEIS drafts

[Counting table](../results/table.md) · [Verification](../verification/README.md) · [Source audit](../audit/README.md)

All files are **proposed data or edits, not submitted changes**. Terms count based
fusion rings at exact multiplicity. Only complete whole-rank counts are exported
from `results/census.json`.

| Sequence | Direction | Prepared coverage | File |
|---|---|---|---|
| A354471 | Rank 3; multiplicity varies | 1–1000 | [b-file](b354471.txt) |
| A354472 | Rank 4; multiplicity varies | 1–128 | [b-file](b354472.txt) |
| A354473 | Rank 5; multiplicity varies | 1–20 | [b-file](b354473.txt) |
| A348305 | Multiplicity 1; rank varies | 1–9¹ | [b-file](b348305.txt) |
| A354475 | Multiplicity 2; rank varies | 1–8 | [b-file](b354475.txt) |
| A354476 | Multiplicity 3; rank varies | 1–7 | [b-file](b354476.txt) |
| A354477 | Multiplicity 4; rank varies | 1–7 | [b-file](b354477.txt) |

¹ The rank-nine value 142 is retained from the reference census; it is not an
independently recomputed rank-nine result. This repository's computation scope
ends at rank 8. Rank-1 and rank-2 terms follow symbolically.

Unassigned fixed-rank drafts: [rank 6](fixed_rank_6.txt), [rank 7](fixed_rank_7.txt),
[rank 8](fixed_rank_8.txt). No A-number is invented or reserved here.

## Correction and extensions

The source audit replaces A354473 terms 9–12:
**1463 → 863, 1794 → 1082, 2283 → 1383, 3049 → 1948**.
Suggested comment:

> Terms a(9)–a(12) were corrected by removing repeated isomorphism classes from the ancillary database of Vercleyen and Slingerland (arXiv:2205.15637v4).

The independent census extends the rank-5 draft through 20, with **a(20)=6866**.
The multiplicity-2 draft includes **A354475: a(8)=877**; the multiplicity-4 draft
includes **A354477: a(7)=2780**. The multiplicity-3 draft includes
**A354476: a(7)=1059**. Fixed-rank drafts include **c₆(7)=3814**, **c₇(4)=2780**
and **c₈(2)=877**. These additions preserve the old verified prefixes.

## Before submitting

Check the live entry, indexing and b-file; the retained source snapshot is dated
18 September 2026. Preserve attribution to Vercleyen and Slingerland and credit
the independent census separately. Supply a public, stable reference to the exact
revision and verification evidence. Use a permanent commit link to this public
repository and the corresponding audit records. Search for existing entries before
proposing new fixed-rank sequences. Check other projections of a changed cell using `impact_map.json`.
The source correction and newly appended terms are different changes.

OEIS text retains its [attribution and licensing terms](../NOTICE.md).
