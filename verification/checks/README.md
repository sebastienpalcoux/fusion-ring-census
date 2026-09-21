# Repository checks

These are lightweight release checks, separate from the full independent
mathematical audits in the rank directories. No census enumeration ran here.

- `unit-tests.txt`: 31 tests, including mocked deadlines, failure classification,
  local launch scope, verification gates and result packaging.
- `integrity.json`: compressed and decompressed hashes, record totals and manifest
  consistency for all six current datasets.
- `consistency.json`: internal links, CSV/OEIS projections, audit-to-release
  agreement, manual workflow configuration, HTML controls and final LaTeX passes.
- `pdf-build.json`: six completed PDF builds, page bounds and resolved references.
  Every page was also reviewed visually for layout and legibility.

Reproduce routine checks with `make test`, `python3 scripts/check_release.py` and
`make docs`. The current mathematical results were freshly audited on GitHub
for ranks 5–8; ranks 3 and 4 retain their earlier full audits.
