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
reported. The optional `--deadline` propagates the parent wall-clock deadline
to every subprocess; the parent additionally terminates the whole process group.
Existing output directories are not silently reused. A failed or
interrupted search is marked incomplete and supplies no full-rank count file.
Recorded benchmark times from 18 September 2026 are historical measurements,
not guaranteed times on another processor or on GitHub's shared runners.

## Strict shared extension budget

The long manual campaign selects exactly ranks 5–8. Example for one rank:

```bash
python3 scripts/extend_census.py --rank 7 --seconds 4200 \
  --threads "$(nproc)" --out runs/rank7-frontier
```

The wrapper accepts a finite maximum of 4,200 seconds for ranks 5–8 (ranks 3–4
retain their 1,200-second validation ceiling). The long workflow passes 4,200,
sets 75 minutes per job and uses four jobs: at most 300 runner-minutes, including
setup and always-run artifact upload. The legacy workflow still passes 1,100 and
has a 20-minute ceiling. Neither launches from a push. Both share a concurrency
lock; rerunning jobs is disabled. Rank three remains capped at multiplicity 1000.

One monotonic deadline covers compilation, every successive multiplicity and
duality type, export, compression, independent verification and acceptance.
Three seconds are reserved for child-process termination and evidence cleanup.
Each attempt receives 90% of its remaining execution time for enumeration, with
the balance available for compilation/export/verification; the outer deadline
also bounds those phases. At a fresh 4,200-second budget this makes about 3,777
seconds of enumeration available, subject to compilation time and the hard shared
deadline. It does not guarantee completion or an hour of search if a bound ends
sooner. Content-keyed builds are reused within the job. There are no idle waits,
checkpoint-resume claims, automatic retries, AI calls or paid API calls.

The next bound is the released bound plus one for ranks 5–8. All tensors and
unit-fixing basis permutations are independently checked, then exact-multiplicity
counts are checked against the full released prefix and every earlier accepted
candidate in the same job. Only then is the candidate retained in `best/`.
A later timeout or error preserves that candidate. The release stays unchanged.

Before deleting an incomplete attempt, the driver preserves its run report,
per-duality logs, commands and available verifier reports under `diagnostics/`.
Partial tensor collections are never uploaded. `frontier.json` and `SUMMARY.md`
distinguish `verified_extension`, `no_extension_within_budget` and `error`.
Unexpected exits, compiler failures and verification/prefix mismatches are
errors and produce a nonzero driver exit. An expected budget exhaustion is a
normal outcome with no new claim. Artifacts expire after 14 days. Upload can
still fail if GitHub cancels or loses the runner; a green check or an uploaded
artifact name alone is never a certificate of a new census.

See [the launch contract](LONG_CAMPAIGN.md) and [the completed campaign review](CAMPAIGN_REVIEW.md).
The six companions now document both workflow limits and the reviewed outcome.
In the Work environment, use only lightweight tests and checks: enumeration and
full tensor verification belong on GitHub Actions. Manuscript builds do not run
numerical searches. The targeted `review-rank5-m19.yml` audit ran only the accepted
rank-five tensors, with a 10-minute job ceiling and no enumeration.

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
