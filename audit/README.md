# Exact fusion-ring database audit

**Input:** `FusionRingMultiplicationTables`, ancillary to G. Vercleyen and
J. K. Slingerland, *On Low Rank Fusion Rings*, arXiv:2205.15637v4.

**Status:** local audit and proposed OEIS correction only. Neither OEIS nor the
original online database has been edited.

## Results

The 28,451 source records represent **25,138 based-isomorphism classes**.
Exactly **3,313** records are redundant: 2,973 repeated labelled tensors and
340 additional labellings of already represented classes. All repetitions
occur at rank 5 and exact multiplicities 9--12:

| Multiplicity | Source records | Distinct rings | Removed | Literal repeats | Other labellings |
|---:|---:|---:|---:|---:|---:|
| 9 | 1463 | 863 | 600 | 541 | 59 |
| 10 | 1794 | 1082 | 712 | 636 | 76 |
| 11 | 2283 | 1383 | 900 | 792 | 108 |
| 12 | 3049 | 1948 | 1101 | 1004 | 97 |

Here "literal repeat" means equality of the full labelled integer tensor
with some earlier source record; whitespace is irrelevant. That earlier
record need not itself be the first representative of the isomorphism class.

All 118 noncommutative rings are retained. No repetitions were found in any
other rank/multiplicity cell in this input.

The corrected A354473 prefix, at n=1,...,12, is:

`16, 37, 82, 134, 209, 336, 477, 733, 863, 1082, 1383, 1948`.

The checked prefixes of A348305, A354471, A354472, A354475, A354476 and A354477
are unchanged. Public sequence values are recorded in `oeis_snapshot.json`.
The comparison is with the retrieved September 18, 2026 pages, not a live
OEIS write. A later website edit requires a fresh comparison before submission.

## Run on your laptop

Requirements: Python 3.9 or later and a C++17 compiler (GCC or Clang); no
third-party Python packages, SageMath or Mathematica are needed. A compiler
must already be installed. The Python driver does not install software.

From this directory, using the included input copy:

```sh
python3 audit_fusion_rings.py input/FusionRingMultiplicationTables --out my_audit --verify-witnesses
```

Or pass the path to your own download of the ancillary file. The runner compiles
the C++ code, performs the full exact audit, generates the table/OEIS drafts for
the checksum-pinned v4 input, and creates `my_audit.zip`. The directory and zip
must not already contain results; choose a new output name to rerun. The
platform-specific compiled executable is written beside that directory.

The core code also works without Python:

```sh
c++ -O3 -std=c++17 dedup_fusion.cpp -o dedup_fusion
./dedup_fusion input/FusionRingMultiplicationTables my_audit_cpp
```

That direct command generates the clean database, counts, maps, certificates
and summary. The Python driver additionally supplies SHA-256 hashes, the
publication table with completeness labels, and the OEIS amendment package.
The C++ command accepts the ancillary file's Mathematica braces or JSON square
brackets, one complete three-dimensional tensor per nonblank line.

For a second audit that bypasses all invariant-based permutation pruning:

```sh
python3 audit_fusion_rings.py input/FusionRingMultiplicationTables --out my_audit_full --exhaustive
```

The core `--skip-associativity` option is for already validated data only. It
was **not** used in any delivered counting run and is not recommended for an
OEIS correction. The Python runner deliberately does not expose this shortcut.

## What the algorithm counts

The entry `T[i][j][k]` is the coefficient of basis element k in the product of
elements i and j. Labels are **zero-based**, and 0 is the two-sided unit.
Multiplicity means `max(T[i][j][k])`, including the unit coefficients: it is
an exact maximum, not an upper bound.

Two records are identified precisely when a permutation q fixing 0 satisfies

`source[i][j][k] == representative[q[i]][q[j]][q[k]]`

for every ordered triple (i,j,k). This is based-ring isomorphism, not arbitrary
abstract ring isomorphism. Noncommutative rings are included. Preservation of
duality follows from preservation of the unit coefficients. No
categorifiability condition is imposed.

All nonnegativity, shape, two-sided unit, duality, Frobenius reciprocity and
associativity axioms are checked with integer arithmetic in the default run.
Associativity is tested directly as

`sum_s T[i][j][s]*T[s][k][l] == sum_s T[j][k][s]*T[i][s][l]`.

The parser enforces rank <= 32 and coefficients <= 1,000,000 so the sums of
products fit in uint64_t. The v4 file is much smaller (rank <= 9, multiplicity
<= 16). These safety limits are not promises of tractability for large ranks;
the worst-case permutation complexity is factorial. Malformed or invalid
records abort the run, rather than silently disappearing from the count.

### Exact canonicalization and its proof

To each nonunit label i attach the following signature, with components in the
specified fixed order:

1. Whether i is self-dual, and `T[i][i][i]`.
2. The sorted list of all `T[i][j][k]` as (j,k) varies.
3. The lexicographically sorted list, as j varies, of six-tuples
   `(T[i][j][j], T[j][i][j], T[j][j][i], T[i][i][j], T[i][j][i], T[j][i][i])`.

Every based-ring isomorphism preserves these signatures. Sort the signature
cells lexicographically, keep the unit first, and try **every permutation
inside each tied cell**. The canonical key is the lexicographically least
full multiplication tensor under these labellings.

If two inputs are isomorphic, the isomorphism bijects their allowed labellings,
so their sets of relabelled tensors and hence canonical minima are identical.
Conversely, equality of canonical tensors supplies an explicit isomorphism
between the inputs. Thus the canonical key classifies exactly, without any
assumption that the signatures themselves are complete invariants.

The C++ unordered maps use hashes for speed, but always compare full integer
vectors for equality. A hash collision cannot merge different keys.
Every duplicate witness is separately checked against the two original tensors.

The representative of each class is the **first physical source line** in that
class. The retained tensor is not relabelled. Consequently the cleaned file is
an ordered subsequence of the input, and external source labels can be recovered
through `line_map.csv` rather than silently reassigned.

### Independent checks and timings

Recorded single-process runs in this environment, including parsing, all
fusion-ring axiom checks and output writing, but excluding compilation:

| Method | Permutations examined | Elapsed internal seconds |
|---|---:|---:|
| Signature-cell canonicalization | 112936 | 0.604868 |
| Every unit-fixing permutation | 13247806 | 1.616744 |

The counts, cleaned database and complete line map agreed **byte for byte**
between these runs. Peak resident memory was about 64 MB. These are measured
runs here, not timing guarantees for another computer.

`verify_witnesses.py` is an independent, standard-library-only Python checker.
It reparses the source with JSON, checks source coverage, every exact
isomorphism witness, retained line contents, duplicate types, and every column
of the counts. Its separately recorded run took 3.104697 seconds. It proves no
incorrect deletion, but by itself does not prove that two *retained* rings are
nonisomorphic; the all-permutations audit supplies that separate check.

```sh
python3 verify_witnesses.py input/FusionRingMultiplicationTables results
```

`test_audit.py` also checks cyclic/Klein/nonabelian/product group rings and the
Fibonacci ring, randomized relabellings, both canonical modes, malformed and
nonassociative inputs, and overwrite protection:

```sh
python3 test_audit.py ./my_audit_dedup_binary
```

The package contains the recorded test outputs in `checks/`.

## Output files

- `results/FusionRingMultiplicationTables.deduplicated`: all 25,138 retained
  source tables, in original order and with their original basis labels.
- `results/counts.csv` and `results/counts_with_status.csv`: full count audit;
  the latter explicitly records the publication's completeness status.
- `results/corrected_table.md` and `.tex`: corrected Table 2.
- `results/line_map.csv`: one row per input record, mapping it to its retained
  representative; `clean_line` is a 1-based line number in the new database.
- `results/duplicates.csv`: the 3,313 deletion certificates. Physical source
  and clean-file line numbers are 1-based; permutation labels are 0-based.
- `results/duplicate_examples.json`: original tensors for the first literal
  repetition and the first differently labelled repetition.
- `results/oeis/A354473_edit.txt`, `editor_note.txt`, and `b354473.txt`: the
  proposed OEIS edit, explanation for editors, and corrected b-file.
- `results/oeis/comparison.json`: comparison of all seven OEIS prefixes.
- `results/summary.json`, `provenance.json`, `python_verification.json`, and
  `SHA256SUMS`: machine-readable verification and provenance.

## Scope and completeness caveat

Deduplication determines exactly which isomorphism classes are **present in a
file**. It cannot establish that the search producing the file omitted no
classes. The corrected unmarked cells retain the original paper's completeness
claims; this audit does not independently re-prove them.

The original `+` entries remain incomplete-search lower bounds. In particular,
rank-five counts 1300,1323,1550,1925 at multiplicities 13--16 are **not** proposed
as new terms of A354473. Independent-enumeration extensions from other projects
are outside this correction package.

Blank cells in the source Table 2 stay blank/dashes, not zeros. Rank-one counts
above multiplicity one are zero because the only basis element is the unit.

## Provenance

The direct arXiv download was unavailable to the working container. The input
was recovered from the earlier user-accessible package
`Rank5_Dong_Palcoux_Through15.zip`, member
`Rank5_Frontier/data/FusionRingMultiplicationTables`. It has 16,531,197 bytes,
matching the content length reported for the user's arXiv-v4 ancillary URL.
This audit is reproducible on the exact bytes identified below; it does not
claim that a fresh network download was independently hashed in this session.

Source URL:
https://arxiv.org/src/2205.15637v4/anc/FusionRingMultiplicationTables

SHA-256 of the input:

`b587c3f683157369da7cc090f762bbff0e18dcf11acc3f5031d6bc0c643843f8`

The runner hashes your input. If it differs, the numerical audit still runs,
but the v4-specific completeness labels and OEIS edit drafts are **not**
automatically generated. This prevents silently applying a known-version
correction to a different or partial dataset.

Public references consulted: the arXiv HTML version of the paper, Section 2.5
and Table 2; OEIS A348305, A354471--A354473 and A354475--A354477; OEIS Help Page
and QandA For New OEIS for the submission/review process. OEIS edits require an
authenticated session and editorial review. No edit has been submitted here.

The audit software was newly generated with AI assistance and is supplied as
source. Re-running the independent checks is encouraged before publishing an
amendment. The original data retain their authorship and provenance; the MIT
license applies only to the new audit software.
