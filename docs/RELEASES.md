# Reviewing and releasing census data

A release is one complete dataset per rank, described by `results/census.json`.
Generated count tables, manuscripts, the README, HTML viewer and OEIS drafts all
use that manifest. `verification/rankR/` holds the evidence for the current dataset.
Earlier data and execution instructions remain in Git history.

## Candidate audit

Never execute code from an uploaded data archive. Inspect its paths, checksums,
source identity and completion records. Every duality type must finish normally;
every old exact-multiplicity term must agree. An equal-bound submission is a
reproduction and must match every existing uncompressed tensor and parameter checksum.

Stage a reviewed candidate tree and a JSON list of entries with `rank`, `bound`,
`path` and full `source_commit`. Dispatch the manual **Audit candidate data**
workflow at that exact revision, passing the manifest path. It compiles the
repository's independent checker, verifies source and data hashes, checks every
tensor and every unit-fixing permutation, and compares exact counts. The audit
has a 10-minute ceiling and uploads reports for 14 days. Check included allowance
and enforced spending controls before dispatch. Do not rerun enumeration.

Only `verified_extension` may enlarge a bound. `verified_reproduction` adds
confirmation without changing counts. A workflow's green status, an artifact
name or a partial stratum is never sufficient evidence of a larger census.

## Integration checklist

1. Read the successful audit reports and compare their candidate/source hashes.
2. Update the selected rank's current data and manifest; preserve raw run records,
   per-duality logs and the fresh audit under `verification/rankR/`.
3. Run `make docs`, lightweight tests and `scripts/check_release.py`; inspect PDFs,
   links, table projections, scope and the final diff.
4. Remove superseded current-tree payloads, stale one-off instructions and duplicate
   derived output. Keep mathematical arguments, licensing, source attribution and
   evidence needed to reproduce the release. History retains previous versions.
5. Commit and push normally. Confirm the published manifest and authorized
   repository visibility.

## External publication

Change repository visibility only with explicit maintainer authorization.
OEIS drafts are not submissions. Before an OEIS edit, compare
the live entry and provide a stable public reference with exact revision,
checksums, definitions, coverage argument and verification evidence.
