# Reproduce, verify, extend

## Environment

The released generators need Python 3.9 or later and GNU g++ supporting C++17
and OpenMP. Linux (including Ubuntu under Windows Subsystem for Linux) is the
reference platform. On macOS install GNU GCC and set `CXX` to its actual versioned
executable, rather than Apple's `g++` alias. The process-group deadline wrapper
requires a POSIX environment. No third-party Python module is needed to enumerate,
verify, or export. PDF rebuilding additionally needs `latexmk`, pdfLaTeX, Latin
Modern and the usual TeX Live mathematics packages.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/smoke_test.py --out runs/smoke
python3 scripts/check_release.py --full --out runs/release-check.json
```

The smoke test generates complete small censuses at **all six ranks**, including
every duality type. It is not a rerun of the large enumeration. The release check
is a full check of every shipped tensor, not a sample: it verifies SHA-256 hashes,
unit and duality, reciprocity, all associativity identities and canonicalization
under every unit-fixing basis permutation. Input order need not be canonical.

## Reproduce a particular bound

```bash
python3 code/run_census.py --rank 7 --bound 3 --seconds 1200 \
  --threads 4 --verify --out runs/rank7
```

The `--seconds` flag on this low-level driver is one shared **enumeration** allowance
for the whole rank; compilation, export and independent verification are separately
reported. Existing output directories are not silently reused. A failed or
interrupted search is marked incomplete and supplies no full-rank count file.
Recorded benchmark times from 18 September 2026 are historical measurements,
not guaranteed times on another processor or on GitHub's shared runners.

## Strict whole-job extension budget

```bash
python3 scripts/extend_census.py --rank 7 --seconds 1100 \
  --threads 4 --out runs/rank7-frontier
```

This wrapper enforces one wall-clock deadline over **all** successive bounds,
including compilation, search, export and verification. It can terminate process
groups, not merely the Python parent. Only a complete independently verified
bound enters `best/`. A later timed-out bound leaves diagnostic status, not a
mathematical dataset. See `.github/workflows/frontier.yml`: the job itself has a
20-minute ceiling; the 1,100-second wrapper leaves room for setup and artifact
upload. Artifact upload can still fail if GitHub cancels or loses the runner.
Neither cancellation nor an uploaded log constitutes a completed computation.

Starting bounds 160, 19, 7, 4 and 2 for ranks 4–8 are scheduling heuristics.
They are not published census claims. Rank three is capped at 1000 in the driver,
frontier wrapper, release checks and its specialized C++ generator.

## Input format

Each line is a complete tensor in nested curly braces. The basis unit is index
zero; `N[i][j][k]` is the coefficient of `k` in the **ordered** product `i*j`.
Thus multiplication is not symmetrized in noncommutative cases. Multiplicity is
the maximum of the **full** tensor; all rings have multiplicity at least one.
Use gzip streaming to avoid keeping an entire database in memory.

```bash
python3 code/combine_tables.py combined_tables.txt --ranks 4 5 6 7 8
python3 scripts/audit_reference.py --out runs/reference-audit
```

The audit wrapper decompresses the retained source into a temporary file. The
historical audit README describes its original standalone archive, where the
source and cleaned tensors were uncompressed. In this repository these two files
are gzip-compressed; the wrapper is the simplest faithful rerun.

## Exactness and reproducibility boundary

A successful output audit proves validity and nonduplication of the emitted
rings. It does not by itself prove exhaustive coverage. Coverage is justified by
the orbit parameterization, full associativity equations and safe-pruning proofs
in `methods/` and the mathematical companions. No singular modular system,
vanishing denominator or lower Krylov rank may be discarded. Changing a pruning
rule requires an argument and a comparison with a nonoptimized complete search.

Compiler caches are content-keyed. Run reports retain code hashes, machine and
compiler details where available, commands, completion status and timing. No
network connection is necessary for a local mathematical search.
