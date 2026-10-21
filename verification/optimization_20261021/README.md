# Optimized source integration, 21 October 2026

The complete supplied optimized code has aggregate SHA-256
`9177263413f1e4c775e5a81aa802a683d119de5af1123a8b9991b23daa1b0658`,
matching both the rank-7 M5 and rank-8 M3 producer run records. All numerical C++
sources are integrated byte-for-byte. `code/run_census.py` additionally checks
and repairs executable permissions in its build cache. `scripts/run_laptop.py`
places that cache outside synced project folders and supports `--build-dir`.
The integrated source hash differs and is recorded in [integration.json](integration.json).
LICENSE and NOTICE are unchanged.

Both original archive hashes and all 448 optimized-package / 15 dataset
inventory entries were verified before integration. After workspace loss this
integration was rebuilt from those same archives; the fresh checks below were
rerun. No missing receipt has been recreated from remembered outcomes.

- Six independent finite pruning, witness, rollback and identity audits:
  [fresh transcript](fresh_audits.log), run with `python3 tests/run_audits.py`.
- Normal versus forced-cap-1 complete output comparisons at rank 6 M2 and
  rank 7 M1: [receipt](forced_cap_audit.json), run with
  `python3 audits/audit_selfdual_fallback.py`.
- Eight complete pre-optimization/optimized stratum comparisons at rank 7 M2
  and rank 8 M1: [script](compare_baseline.py) and
  [receipt](baseline_comparison.json). All sorted parameter lists match.
- Thirty Python regression tests: [transcript](unit_tests.log).
- End-to-end small censuses at all six supported ranks, each independently
  verified and checked against the released counts: [summary](fresh_smoke.json)
  and the source-bound `smoke/rank*/run.json` receipts.
- Fresh extraction of the standalone package built from the durable recovery
  checkpoint, with verified rank8 M1 launcher execution: [receipt](package_smoke.json).
- All released compressed and decompressed tensor/parameter hashes:
  [manifest check](manifest_check.json).
- Fresh rank-8 replay: all 4,500 tensors, 22,680,000 unit-fixing permutations,
  zero duplicates, and byte-identical parameter export, under
  [rank8](../rank8/README.md).

The original supplied audits, benchmarks and reference sources are retained in
`audits/` and `benchmarks/` as producer evidence, separately from these fresh
integration checks. Bounded audits do not establish that the entire rank-7 M5
or rank-8 M3 enumeration has been independently reproduced. Full completeness
remains producer-reported.

Classification crosslinks and final manuscript review are updated only after
the companion classification project's final decisions are frozen.
