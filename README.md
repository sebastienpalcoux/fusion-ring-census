# Fusion Ring Census

### Exact enumeration · all duality types · independently checked tensors

A reproducible collection of **1,385,692 fusion rings**, with fast integer generators,
complete counting tables, explanatory mathematical companions and an OEIS workspace.

[View the landing page](docs/index.html) · [Start with the data](results/census.json) · [Read the manuscripts](manuscripts/README.md) ·
[Reproduce a census](docs/REPRODUCIBILITY.md) · [OEIS](oeis/README.md) · [Audit the source](audit/README.md)

## Certified coverage

| Rank | Complete multiplicity bound | Distinct classes | Manuscript | Full tensors |
|---:|---:|---:|---|---|
| **3** | **1000** | **460,353** | [PDF](manuscripts/rank3.pdf) · [TeX](manuscripts/rank3.tex) | [gzip](results/rank3_through1000_tables.txt.gz) |
| **4** | **128** | **889,530** | [PDF](manuscripts/rank4.pdf) · [TeX](manuscripts/rank4.tex) | [gzip](results/rank4_through128_tables.txt.gz) |
| **5** | **18** | **28,493** | [PDF](manuscripts/rank5.pdf) · [TeX](manuscripts/rank5.tex) | [gzip](results/rank5_through18_tables.txt.gz) |
| **6** | **6** | **5,799** | [PDF](manuscripts/rank6.pdf) · [TeX](manuscripts/rank6.tex) | [gzip](results/rank6_through6_tables.txt.gz) |
| **7** | **3** | **1,421** | [PDF](manuscripts/rank7.pdf) · [TeX](manuscripts/rank7.tex) | [gzip](results/rank7_through3_tables.txt.gz) |
| **8** | **1** | **96** | [PDF](manuscripts/rank8.pdf) · [TeX](manuscripts/rank8.tex) | [gzip](results/rank8_through1_tables.txt.gz) |

The unit has index zero and `N[i][j][k]` is the coefficient of basis element `k`
in the **ordered** product `i*j`. All results include every duality type.
**These are classifications of based rings, not of fusion categories.** No
categorifiability criterion is applied. Rank three is intentionally capped at 1000.

Ranks 3–7 retain the completed census data and provenance from 18 September 2026.
Rank eight is independently generated with the expanded solver in this repository.
New local verification is recorded separately from the original execution logs.

## Three ways to use the project

Read `manuscripts/rankR.pdf` for the definitions, mathematical coverage argument,
rank-specific method, results, singular cases and verification boundary.

Verify the released tensors without repeating the search:

```bash
python3 scripts/check_release.py --full
```

Reproduce a complete bounded census, or request a larger whole-rank search:

```bash
python3 code/run_census.py --rank 6 --bound 6 --seconds 1200 \
  --threads 4 --verify --out runs/rank6-reproduction
python3 scripts/extend_census.py --rank 6 --seconds 1100 \
  --threads 4 --out runs/rank6-frontier
```

Requirements: Python 3.9+, GNU g++ with C++17/OpenMP. The mathematical code uses
only Python's standard library. LaTeX is needed only to rebuild PDFs. No SageMath,
Mathematica or NumPy is required. See [platform notes](docs/REPRODUCIBILITY.md).

## A complete result, or no new claim

A whole-rank result must finish **every** involution type. The independent checker
then verifies every fusion-ring axiom, all integer associativity identities and
all unit-fixing basis permutations. A larger interrupted attempt cannot replace
the last completed and verified bound. No partial-stratum counts are exported to OEIS.

Completeness is justified by the exhaustive parameterization and safe-pruning
proofs; checking emitted tensors alone would not prove that nothing was omitted.
The distinction is made explicitly in [the methods](methods/completeness.md).

## GitHub computation

[The frontier workflow](.github/workflows/frontier.yml) runs a manually requested
matrix for ranks 3–8. Each rank has a **20-minute job ceiling**, and all attempts
within that job share a 1,100-second driver deadline including compilation,
export and verification. Rank three regenerates through 1000 and stops. The other
ranks try increasing complete bounds. Starting points are heuristics, not promises
of a particular improvement on a GitHub runner.

Only verified whole-rank `best/` results become candidate artifacts. To review and
import one, use [the release procedure](docs/RELEASES.md). The workflow never pushes
unreviewed numerical results to `main` and never edits OEIS automatically.

**Publication state of this package:** prepared and tested locally. The session
that assembled it had read-only GitHub access; no remote repository or Actions
run is claimed. The authenticated publisher is:

```bash
python3 scripts/publish_github.py --run-census
```

This creates `sebastienpalcoux/fusion-ring-census` as **private** by default,
pushes the committed material and requests the workflow once. Add `--public`
only when deliberately publishing the manuscripts and data publicly. The script
uses the user's existing `gh auth login` session and refuses another account or
an existing repository. It never asks for a token in an argument or prints credentials.

## Source audit and attribution

The audit of Vercleyen–Slingerland's arXiv v4 ancillary file identifies 3,313
redundant records, all at rank five and multiplicities 9–12. Exact permutation
witnesses and the corrected table are retained under `audit/`. The source was
used for comparison only, never as enumeration input. Its original partial
search cells are not promoted to complete counts merely by deduplication.

The specialized rank-four and rank-five derivations come from the Dong–Palcoux
census project; the original excerpts and execution records are preserved.
See [provenance](docs/PROVENANCE.md), [citation metadata](CITATION.cff), and
[licensing scope](NOTICE.md). AI assistance and verification status are disclosed.

## Repository map

```text
code/          Exact generators, exporters and independent tensor checker
systems/       Regenerable reciprocity orbits and associativity systems
results/       Only complete datasets, count tables and the primary manifest
manuscripts/   Six explanatory companions, in LaTeX and PDF
methods/       Coverage proofs and retained rank-specific derivations
oeis/          b-files, correction text, impact map and submission policy
audit/         Original-database deduplication code and certificates
verification/  Execution provenance, regression tests and independent audits
scripts/       Timed search, release checking, publication and result import
tests/         Regressions, symmetry checks, scope checks and timeout tests
.github/       CI, manual frontier search and issue templates
```

## Cite and contribute

Use **Cite this repository** after publication, or the metadata in `CITATION.cff`.
Report a suspected missed ring with its full multiplication tensor, rank,
multiplicity, generating command and revision. Improvements must preserve every
singular and zero-coefficient branch and pass independent checks. See
[CONTRIBUTING.md](CONTRIBUTING.md).
