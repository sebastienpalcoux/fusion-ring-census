# Repository checks

These checks are separate from mathematical enumeration. No enumeration ran
during the 19 October 2026 integration.

- `integrity.json`: current compressed and decompressed hashes, record totals
  and manifest consistency for all six datasets.
- `rank7-M5-consistency.json`: current rank CSVs and audits, rank-7 OEIS
  projection, embedded HTML manifest, local links and rank-7 PDF review.
- `unit-tests-2026-10-19.txt`: 31 repository tests passed after integration.
- `unit-tests.txt`, `consistency.json` and `pdf-build.json`: retained historical
  checks from the earlier release; their totals and build scope are historical.

The current rank-7 full tensor audit is
[`../rank7/release_check.json`](../rank7/release_check.json).
Its source and completeness qualification is in
[`../rank7/README.md`](../rank7/README.md). The new rank-7 PDF has eight pages;
all were rendered and visually reviewed. Other PDFs retain their prior build.

Reproduce routine checks with `make test`,
`python3 scripts/check_release.py`, and `make docs`.
