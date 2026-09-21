# Audit of the reference database

[Current census](../README.md) · [Current OEIS drafts](../oeis/README.md) · [Attribution](../NOTICE.md)

This directory documents the Vercleyen–Slingerland v4 ancillary database, independently
of the new census. Its 28,451 input records contain **25,138 distinct based-ring
classes** and **3,313 redundant records**. Every deletion is accompanied by a
checked unit-fixing basis permutation. The source identity and checksum are in
[source.json](source.json); the compressed original is in [input/](input/).

| Exact multiplicity at rank 5 | Original records | Distinct classes |
|---:|---:|---:|
| 9 | 1,463 | 863 |
| 10 | 1,794 | 1,082 |
| 11 | 2,283 | 1,383 |
| 12 | 3,049 | 1,948 |

## Evidence

- [Summary](results/summary.json), [counts](results/counts.csv) and [coverage status](results/counts_with_status.csv).
- [Deletion witnesses](results/duplicates.csv), [line map](results/line_map.csv) and [worked examples](results/duplicate_examples.json).
- [Deduplicated reference](results/FusionRingMultiplicationTables.deduplicated.gz), [input provenance](results/provenance.json) and [witness verification](results/python_verification.json).
- [Independent cross-checks](checks/) and [historical OEIS snapshot](oeis_snapshot.json).

These are counts of the reference file, not new census frontiers. The coverage-status
table preserves the distinction between complete and partial source cells.
Deduplication cannot turn a partial search into a complete census. The current
complete counts, including later extensions, are in [results/](../results/).

## Reproduce

From the repository root, on your own computer or a suitably authorized GitHub runner:

```bash
python3 scripts/audit_reference.py --out runs/reference-audit
```

The wrapper decompresses the retained source and runs `audit_fusion_rings.py`
with every deletion witness checked. `dedup_fusion.cpp` supplies canonicalization;
`verify_witnesses.py` independently checks the explicit basis maps. The code and
original source attribution retain their respective [licensing](../NOTICE.md).
The current proposed OEIS edits live only in [oeis/](../oeis/README.md).
