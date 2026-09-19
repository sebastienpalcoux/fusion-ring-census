# Checks for the reviewed GitHub integration

- `integrity.json`: lightweight compressed/uncompressed tensor and parameter
  hashes, record totals and manifest consistency for all six ranks. This is not
  a new full mathematical audit of unchanged ranks.
- `tests.txt`: 24 passing regression tests, including mocked deadline, timeout,
  genuine-error, candidate-retention and prefix-agreement cases.
- `pdf_build.json`: all six companions rebuilt with pdfLaTeX/latexmk in temporary
  build directories; valid PDF structure, updated outcome text and no overfull
  boxes. Covers, result pages, campaign/reproduction pages and changed end pages
  were rendered and visually inspected. Complete command blocks stay together.
- All workflows parsed successfully and remain manual-only. The long campaign
  still selects only ranks 5–8 with the existing 4,200/75-minute limits.
- Existing rank-3/4/6/7/8 manifest records and data remain unchanged; numerical
  source, systems, proof methods, licenses, attribution and reference inputs
  were not modified. All count CSV/OEIS projections agree with the manifest.
- A credential-pattern scan of changed text files found no suspected tokens or
  private keys. The Git diff passed whitespace checks.

The full new rank-five mathematical audit ran on GitHub, not in Work:
https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35449570360
Original and fresh results are under `verification/imports/rank5_through19/`.
PDF builds now replace released outputs only after a completed temporary build;
this prevents incomplete build output from replacing an existing companion.
