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
enter its `Fusion_Census_Laptop` directory. On macOS, install Python and GNU GCC,
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
| 6 | 7 | 8 | 1–15 |
| 7 | 4 | 5 | 1–15 |
| 8 | 2 | 3 | 1–15 |

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
3. Canonicalization under every unit-fixing basis permutation finds no duplicates.
4. All earlier exact-multiplicity counts agree with the certified release.

The ZIP contains compressed tensors and parameters, exact counts, source and
baseline provenance, checksums, completion logs and verification reports. Send
this ZIP for review. Failure or interruption creates no verified ZIP, and partial
output is never a census term. Reproducing a smaller or equal bound does not
extend the release. The laptop launcher never publishes results automatically.

## Verify the released data

```bash
# Lightweight checksums, record totals and manifest consistency
python3 scripts/check_release.py

# Every tensor and every unit-fixing permutation; no enumeration
python3 scripts/check_release.py --full --out runs/verification.json

# Small deterministic tests and separate compiled regression searches
python3 -m unittest discover -s tests -v
python3 scripts/smoke_test.py --out runs/smoke
```

The verifier proves validity and uniqueness of the emitted tensors. Completeness
also relies on the [coverage arguments](../methods/completeness.md) and normally
completed searches. An equality of counts alone is not an isomorphism proof.

In the Work environment, use lightweight checks and mocked numerical subprocesses.
Enumeration and full tensor verification belong on GitHub Actions or the user's
own computer. PDF builds are document operations, not census searches.

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
enforced spending controls. Use standard Ubuntu runners, keep the repository
private, and do not enable paid overages. The local unlimited mode refuses GitHub
Actions. Standard low-level timed runs accept at most 4,200 seconds; the frontier
wrapper limits ranks 3–4 to 1,200 seconds and ranks 5–8 to 4,200 seconds.

## Review and publication

[Release procedure](RELEASES.md) explains candidate auditing and integration.
Publication is a reviewed Git commit; neither an audit nor a search pushes data.
The current evidence is indexed by rank, rather than by successive campaigns.

To regenerate presentation files from the manifest:

```bash
make docs
```

This updates the README, count tables, OEIS drafts, HTML viewer and all six PDFs.
PDF compilation requires `latexmk`, pdfLaTeX, Latin Modern and standard TeX Live
mathematics packages; shell escape is disabled. All numerical data remain unchanged.

To build a small standalone laptop package from a clean committed checkout:

```bash
python3 scripts/build_laptop_package.py --out /tmp/Fusion_Census_Laptop.zip
```

It contains code, equation systems, proofs, manifest, attribution and tests, without
duplicating released tensor datasets. Checksums are checked before computation.
Its baseline is the snapshot identified in `SOURCE.json`.
