# OEIS workspace

All files here are **proposed data or edits**, not submitted changes. The primary
source for numerical output is `results/census.json`, which contains only complete
whole-rank datasets. `scripts/refresh_documentation.py` regenerates this folder's
b-files and impact map.

| Entry | Meaning | File |
|---|---|---|
| A354471 | Rank 3, multiplicity varies; stop at 1000 | `b354471.txt` |
| A354472 | Rank 4, multiplicity varies | `b354472.txt` |
| A354473 | Rank 5, multiplicity varies | `b354473.txt` |
| A348305 | Multiplicity 1, rank varies | `b348305.txt` |
| A354475 | Multiplicity 2, rank varies | `b354475.txt` |
| A354476 | Multiplicity 3, rank varies | `b354476.txt` |
| A354477 | Multiplicity 4, rank varies | `b354477.txt` |

`fixed_rank_6.txt`, `fixed_rank_7.txt`, and `fixed_rank_8.txt` are separately prepared
fixed-rank sequences. **No new A-numbers are invented or reserved here.** Search OEIS
for an existing entry before proposing one. Their current prefixes may be too short
for a new entry without further explanatory content.

The multiplicity-one b-file retains the published rank-nine value 142 from the
reference census. It is **not** an independently recomputed rank-nine result in
this repository, whose computation scope ends at rank eight. All newly generated
numerical additions are restricted to the verified manifest.

## Rank-five correction sentence

> Terms a(9)–a(12) were corrected by removing repeated isomorphism classes from the ancillary database of Vercleyen and Slingerland (arXiv:2205.15637v4).

The replacements are 1463 → 863, 1794 → 1082, 2283 → 1383, and 3049 → 1948.
The original authors' enumeration remains credited; the correction and independent
extensions should be credited separately. Keep the existing references and add a
publicly accessible stable reference before submitting. This repository exists
but remains private, so its URL alone is not a public OEIS reference.

## Cross-sequence impact

A correction to c_r(m) affects a fixed-rank entry at a(m), a fixed-multiplicity
entry at a(r), and any derived sequence using that cell. `impact_map.json` records
the entries handled by this package; it is not an exhaustive assertion about all
of OEIS. In particular, check fixed-multiplicity entries at 9, 10, 11 and 12 if any
are located. The four rank-five duplicate corrections do not change the existing
multiplicity-1, -2, -3 or -4 prefixes.

The rank-five multiplicity-19 value 5640 extends the local A354473 draft to a(19).
It comes from the reviewed complete GitHub run, with the entire old prefix checked.
The reviewed laptop result adds c_6(7)=3814 to `fixed_rank_6.txt`, after a fresh
independent GitHub audit; no OEIS accession is assigned here.
The rank-seven multiplicity-three value 1059 extends A354476 at a(7).
Any additional rank-eight multiplicity-two value is exported to A354475 only when
the complete rank-eight bound-two run is certified in the manifest.

## Submission checklist

Check the live entry, its indexing and existing b-file. Compare the entire old
prefix. Distinguish corrected terms from newly appended terms. Provide the exact
release revision, source checksum, algorithm, completeness explanation and audit
witnesses. Submit through the OEIS editorial workflow; do not claim acceptance
until the edit is actually approved.
