# Run, verify and extend the census

[Counting table](../README.md) · [Methods](../methods/completeness.md) · [Evidence](../verification/README.md)

The standalone programs require **Python 3.9+ and GNU g++ with C++17/OpenMP**.
They use exact integer arithmetic and Python's standard library. No AI model,
paid API, SageMath, Mathematica or third-party Python package is used.

## Run on your own computer

On Ubuntu or Ubuntu under Windows Subsystem for Linux:

```bash
sudo apt-get update
sudo apt-get install -y python3 g++ unzip
```

Use a checkout of this repository, or extract the standalone laptop package and
enter its `Fusion_Census_Deep_Optimized` directory. On macOS, install Python and GNU GCC,
then set `CXX` to the installed versioned GNU compiler (for example `g++-15` if
that is the installed executable). Apple's `g++` alias does not supply GNU OpenMP.
Native Windows is not tested; use WSL Ubuntu.

Run one chosen census from the project root:

```bash
python3 scripts/run_laptop.py --rank 7 --bound 5
```

This searches **all rings through the chosen multiplicity**, including every
duality type and all noncommutative cases. It has **no clock limit** and requires
independent verification. `--mult` is an alias for `--bound`.

| Rank | Current complete bound | Next unfinished bound | Supported input bound |
|---:|---:|---:|---:|
| 3 | 1000 | Supported ceiling reached | 1–1000 |
| 4 | 128 | 129 | 1–1000 |
| 5 | 20 | 21 | 1–32 |
| 6 | 9 | 10 | 1–15 |
| 7 | 5 | 6 | 1–15 |
| 8 | 3 | 4 | 1–15 |
| 9 | 1 | 2 | 1–15 |
| 10 | 1 | 2 | 1–15 |
| 11 | 1 | 2 | 1–15 |

Keep the computer awake and connected to power. These limits protect the
implementation; they do not guarantee feasible runtime or memory at every bound.
Thread count follows available CPU affinity, capped at 64; choose fewer with
`--threads 8`, for example. Only parallel phases use all the requested threads.

### Progress and result ZIPs

For rank 7, bound 5, reports are under `runs/rank7_M5/`:

```bash
tail -f runs/rank7_M5/logs/selfdual.log
```

The log appears when that phase starts; `run.json` records the current phase.
Work units have unequal cost, so progress is not a runtime forecast. A search
restarts the unfinished bound: checkpoints are not implemented. Existing output
is never overwritten; choose a fresh `--output-dir` to repeat a bound.

A result ZIP such as `runs/rank7_multiplicity5_verified.zip` is created only when:

1. Every required duality search finishes normally.
2. Every tensor passes the independent full axiom checker.
3. Exact based-isomorphism checking finds no duplicates. Ranks 9–11 use exact invariant refinement, with exhaustive reference mode retained.
4. All earlier exact-multiplicity counts agree with the certified release.

The ZIP contains compressed tensors and parameters, exact counts, source and
baseline provenance, checksums, completion logs and verification reports. Send
this ZIP for review. Failure or interruption creates no verified ZIP, and partial
output is never a census term. Reproducing a smaller or equal bound does not
extend the release. The laptop launcher never publishes results automatically.

## Optimized source and executable cache

The supplied 23 October 2026 v3 package supports ranks 3–11 and is integrated with unchanged
numerical C++ sources. The laptop launcher places compiler products in
`$XDG_CACHE_HOME/fusion-ring-census` (or `~/.cache/fusion-ring-census`) so synced
folders cannot strip their executable permission. Override with `--build-dir`.
The low-level driver also repairs missing executable bits in a valid cache.

Run `python3 tests/run_audits.py` for six finite pruning/identity audits and
`python3 audits/audit_selfdual_fallback.py` for complete forced-cap comparisons.
Their exact scopes are recorded under `verification/optimization_20261021/`.
Full rank-7 M5 and rank-8 M3 enumeration remains producer-reported; the supplied
source hash matches both producer run records, but these full searches were
not independently repeated.

The high-rank source and data update is documented in [the integration receipt](../verification/engine_20261023/README.md). The original package’s historical rank-11 timeout predates the completed laptop run now released.

## Verify the released data

```bash
# Lightweight checksums, record totals and manifest consistency
python3 scripts/check_release.py

# Every tensor and exact uniqueness checking; no enumeration
python3 scripts/check_release.py --full --out runs/verification.json

# Small deterministic tests and separate compiled regression searches
python3 -m unittest discover -s tests -v
python3 scripts/smoke_test.py --out runs/smoke
```

The verifier proves validity and uniqueness of the emitted tensors. Completeness
also relies on the [coverage arguments](../methods/completeness.md) and normally
completed searches. An equality of counts alone is not an isomorphism proof.

Full enumeration belongs on GitHub Actions or the user’s own computer. Output verification is separate from enumeration. PDF builds are document operations, not census searches.

## Bounded GitHub campaigns

All workflows are manual and have read-only repository permissions. A push never
starts numerical work. The [frontier workflow](../.github/workflows/frontier.yml)
selects ranks **5, 6, 7, 8**, with `max-parallel: 4` and `fail-fast: false`.
Each rank has a **4,200-second shared driver budget** and a **75-minute job
ceiling**: at most 300 runner-minutes per campaign.

The deadline covers compilation, every attempted bound and duality type, export,
compression and independent verification. Enumeration receives 90% of remaining
driver time, with three seconds reserved for process cleanup. It begins at the
released bound plus one, reuses content-keyed compilation, and retains each fully
verified candidate before trying the next bound with the remaining allowance.
A later timeout preserves the last accepted candidate. There are no automatic
retries, checkpoint claims or idle waits. A concurrency lock prevents overlapping
campaigns. Threads follow `nproc`.

Expected timeout records `no_extension_within_budget`; a completed candidate
records `verified_extension`; compilation, resource or verification failures
record `error` and fail the job. Artifacts retain diagnostics and complete verified
candidates for 14 days. Partial tensor collections are excluded.

Before an authorized dispatch, check account-wide included minutes/storage and
enforced spending controls. Use standard Ubuntu runners and do not enable paid
overages. The local unlimited mode refuses GitHub Actions. Standard low-level timed runs accept at most 4,200 seconds; the frontier
wrapper limits ranks 3–4 to 1,200 seconds and ranks 5–8 to 4,200 seconds.

## Review and publication

[Release procedure](RELEASES.md) explains candidate auditing and integration.
Publication is a reviewed Git commit; neither an audit nor a search pushes data.
The current evidence is indexed by rank, rather than by successive campaigns.

To regenerate presentation files from the manifest:

```bash
make docs
```

This updates the README, count tables, OEIS drafts, HTML viewer and all nine rank-specific PDFs.
PDF compilation requires `latexmk`, pdfLaTeX, Latin Modern and standard TeX Live
mathematics packages; shell escape is disabled. All numerical data remain unchanged.

To build a small standalone laptop package from a clean committed checkout:

```bash
python3 scripts/build_laptop_package.py --out /tmp/Fusion_Census_Laptop.zip
```

It contains code, equation systems, proofs, manifest, attribution and tests, without
duplicating released tensor datasets. Checksums are checked before computation.
Its baseline is the snapshot identified in `SOURCE.json`.

## Rank-seven source qualification

At the 19 October checkpoint, the modified producer source had not yet been
bundled. It has since been supplied: the current optimized source is hash-matched
to the producer records for the rank-seven M5 and rank-eight M3 runs. See the
[rank-seven receipt](../verification/rank7/README.md) and
[optimized-source provenance](../verification/optimization_20261021/).
The 10,006 rank-seven tensors passed output verification and extend the earlier
4,201-class set by 5,805 classes at exact multiplicity five. All four producer
strata report normal completion. The full large enumeration has not been
independently repeated; source identity and output validity are separate from
an independent completeness reproduction.
