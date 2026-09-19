# Complete fusion-ring censuses, ranks four through seven

18 September 2026. Independent bounded enumeration from the fusion-ring axioms.
All duality types, all based-isomorphism classes, no categorification filter.

| Rank | Original v4 complete multiplicity bound | New complete bound | Classes through new bound | Total enumeration wall time | Authorized enumeration ceiling |
|---:|---:|---:|---:|---:|---:|
| 4 | 16 | **128** | **889,530** | 285.711 s | 300 s |
| 5 | 12 | **18** | **28,493** | 477.712 s | 600 s |
| 6 | 4 | **6** | **5,799** | 548.843 s | 900 s |
| 7 | 2 | **3** | **1,421** | 483.095 s | 1,200 s |

**925,243 full multiplication tensors.** Every tensor was independently checked
against all fusion-ring axioms, including full integer associativity, and
canonicalized over every unit-fixing permutation. There are **zero generated
duplicate classes** and **zero missing source records within these bounds**.
There are **905,280 classes absent from the original ancillary file** in this
complete four-rank region. The source itself is not an enumeration input.

The original bounds are those of the arXiv v4 ancillary census, not a claim
about every later website or database. The retained source copy and SHA-256
are documented in `reference/source.json`. Nothing was submitted online.

## Exact multiplicity counts

`results/counts.csv` contains every count at each exact multiplicity.
`results/corrected_extended_table.md` is the readable complete table. The JSON
manifest is `results/census.json`. The higher-rank sequences are:

    rank 6, m=1,...,6: 39, 154, 384, 872, 1582, 2768
    rank 7, m=1,...,3: 43, 319, 1059

The rank-five sequence through 18 is:

    16, 37, 82, 134, 209, 336, 477, 733, 863, 1082, 1383, 1948,
    2211, 2554, 2936, 4157, 4255, 5080.

There is no claim of a complete rank-six bound seven or rank-seven bound four
census in this release. No partial-search higher-bound parameter file is
included as census data. These are achieved bounds, not proven optimal limits
of what another algorithm or machine can do within the same time allowances.

## Full databases and parameters

The eight `results/rank*_through*_{tables,parameters}.txt.gz` files contain
respectively complete full tensors and the smaller exact parameter records.
Every full tensor is one line in the same nested-curly-brace format as the
original `FusionRingMultiplicationTables` ancillary file. Read an entry as
`N[i][j][k]`, the coefficient of basis element k in the ordered product i*j.
The unit has index 0. No output-index dualization is required by the reader.

The release is sorted by (parameter tag, integer parameter vector), independently
of thread scheduling. The parameter encodings are specific to each rank and
are expanded by `code/export_tables.py`; the fully explicit tensors require
no such encoding knowledge. Rank four also has a fast C++ sorting/exporter.
The uncompressed and compressed checksums are in `results/census.json`.

To concatenate all four complete regions into one original-format file:

```bash
python3 code/combine_tables.py FusionRingMultiplicationTables_Ranks4to7
```

This contains only ranks 4--7 within the stated complete bounds. It does not
silently add the original file's partial higher-multiplicity cells.

## Reproduce a full census on a laptop

Requirements: Python 3.9 or later, GNU g++ with C++17 and OpenMP support.
No SageMath, Mathematica, NumPy, SymPy, or other Python dependency is needed.
The actual compiler/machine used here is recorded in `verification/environment.json`.

From the extracted main directory:

```bash
python3 code/run_census.py --rank 4 --bound 128 --seconds 300 --threads 4 --verify --out rerun_rank4
python3 code/run_census.py --rank 5 --bound 18  --seconds 600 --threads 4 --verify --out rerun_rank5
python3 code/run_census.py --rank 6 --bound 6   --seconds 900 --threads 4 --verify --out rerun_rank6
python3 code/run_census.py --rank 7 --bound 3   --seconds 1200 --threads 4 --verify --out rerun_rank7
```

The shared seconds allowance is per whole rank, NOT per duality stratum.
A slower machine may time out. A timed-out run is marked incomplete and never
issues a complete count or an OEIS term from its partial output. Output
directories must be empty or absent; the input/source database is never altered.

The runner compiles its programs, enumerates every required duality type,
exports the full tensors, and optionally performs the all-permutation independent
check. Compilation, export, verification, and compression are separately timed
and are NOT charged to the enumeration allowance. The enumerations reported
above include all exploratory/regression enumeration runs in this turn, not
merely the final successful larger run. Algorithm development and the full
interaction duration are not enumeration timings. See `verification/budget_ledger.json`.

The measured main larger runs themselves took 223.15 s at rank four, 459.21 s
across the rank-five strata, approximately 376.11 s across the rank-six strata,
and approximately 275.83 s across the rank-seven strata. The larger totals
in the opening table also charge earlier smaller-bound runs, optimization
regressions, and abandoned diagnostics. Do not treat these hardware-specific
measurements as laptop guarantees.

The runner's complete rank-seven multiplicity-one workflow, including fresh
compilation and independent verification, was itself tested end to end;
see `verification/runner_end_to_end.json`.

## Independent audit, including old-source containment

```bash
python3 code/verify_release.py --database /path/to/FusionRingMultiplicationTables --out checked_release
```

Omit `--database` to verify just the released tensors. The supplied audit used
all unit-fixing basis permutations, not the enumerators' canonicalization
conventions. It checks the ordered tensor even for noncommutative rings.

`verification/independent/rankR.json` records each audit. Source witnesses in
`rankR_source_witnesses.csv` match every covered original source line to a
released tensor. Both line numbers are **1-based**; the semicolon-separated
basis permutation is **0-based** and satisfies

    N_source[i][j][k] = N_release[q[i]][q[j]][q[k]].

In each underlying raw-check file the new tensors precede the source records.
Thus duplicates in a raw summary are deliberately appended source records,
not duplicate new outputs. The top-level reports separately certify zero
new-output duplicates and no missing source records. This also detects the
3,313 repeated records previously found in the rank-five source.

An independent output check establishes soundness and uniqueness, not alone
exhaustiveness. The human-readable exhaustiveness proof is in
`methods/completeness.md`, with the full specialized low-rank derivations
in the accompanying TeX excerpts. All singular branches are retained. The
new modular and weighted-folding optimizations have parameter-set regression
checks in `verification/optimization_regressions.json`.

## OEIS preparation

`oeis/b354472.txt`: rank-four counts through 128.
`oeis/b354473.txt`: corrected rank-five counts, extended through 18.
`oeis/b354476.txt`: fixed-multiplicity-three sequence with a(7)=1059 appended.

`oeis/proposed_updates.md` distinguishes correction from extension and gives
proposed wording. No OEIS change has been submitted. A public stable archive
reference should be supplied before any submission; chat sandbox links are
not suitable permanent OEIS references.

## Provenance and code status

The algorithms build on the earlier rank-four and rank-five census work,
with new exact modular reconstruction, bounded-domain completion, and
weighted-folding improvements. The source/data were generated with AI
assistance and computationally cross-checked as described. These are not
Lean-formalized proofs or a claim of third-party peer review.

The benchmark-only medium-prime variant under `reference/` was tested at
rank five through ten; it is not the engine used for the released rank-five
through-eighteen computation. Main reproductions use `code/run_census.py`.

The SHA-256 manifest covers all release files other than itself. The
`work/` directory, temporary executables, and incomplete enumeration outputs
are excluded from the distributed archive.
