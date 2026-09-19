# Fusion Ring Census

### Exact enumeration · all duality types · independently checked tensors

A reproducible collection of **1,391,332 fusion rings**, with fast integer generators,
complete counting tables, explanatory mathematical companions and an OEIS workspace.

[View the landing page](docs/index.html) · [Start with the data](results/census.json) · [Read the manuscripts](manuscripts/README.md) ·
[Reproduce a census](docs/REPRODUCIBILITY.md) · [OEIS](oeis/README.md) · [Audit the source](audit/README.md)

## Certified coverage

| Rank | Complete multiplicity bound | Distinct classes | Manuscript | Full tensors |
|---:|---:|---:|---|---|
| **3** | **1000** | **460,353** | [PDF](manuscripts/rank3.pdf) · [TeX](manuscripts/rank3.tex) | [gzip](results/rank3_through1000_tables.txt.gz) |
| **4** | **128** | **889,530** | [PDF](manuscripts/rank4.pdf) · [TeX](manuscripts/rank4.tex) | [gzip](results/rank4_through128_tables.txt.gz) |
| **5** | **19** | **34,133** | [PDF](manuscripts/rank5.pdf) · [TeX](manuscripts/rank5.tex) | [gzip](results/rank5_through19_tables.txt.gz) |
| **6** | **6** | **5,799** | [PDF](manuscripts/rank6.pdf) · [TeX](manuscripts/rank6.tex) | [gzip](results/rank6_through6_tables.txt.gz) |
| **7** | **3** | **1,421** | [PDF](manuscripts/rank7.pdf) · [TeX](manuscripts/rank7.tex) | [gzip](results/rank7_through3_tables.txt.gz) |
| **8** | **1** | **96** | [PDF](manuscripts/rank8.pdf) · [TeX](manuscripts/rank8.tex) | [gzip](results/rank8_through1_tables.txt.gz) |

The unit has index zero and `N[i][j][k]` is the coefficient of basis element `k`
in the **ordered** product `i*j`. All results include every duality type.
**These are classifications of based rings, not of fusion categories.** No
categorifiability criterion is applied. Rank three is intentionally capped at 1000.

The original datasets and execution provenance remain preserved. The reviewed
GitHub campaign extended rank 5 through multiplicity 19; ranks 3, 4 and 6–8
retain their earlier complete datasets. Independent verification reports are
recorded separately from enumeration logs. See [the campaign review](docs/CAMPAIGN_REVIEW.md).

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
python3 scripts/extend_census.py --rank 6 --seconds 4200 \
  --threads "$(nproc)" --out runs/rank6-frontier
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

The separately authorized [rank-6 multiplicity-7 campaign](docs/RANK6_M7_MAX.md)
uses one standard Ubuntu job with GitHub's **six-hour maximum job ceiling** and
one 21,300-second shared driver deadline. It searches only bound 7, preserves
verified artifacts, and does not automatically change the release. Its explicit
`--rank6-m7-max` option does not enlarge the budgets of the other workflows.

Published privately at [sebastienpalcoux/fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census).
The [long campaign](.github/workflows/long-frontier.yml) is manually triggered and
runs **ranks 5, 6, 7 and 8 only**, with at most four concurrent standard Ubuntu jobs.
Each rank receives one **4,200-second (70-minute) shared driver budget** and a
**75-minute job ceiling**: at most **300 runner-minutes** for the four jobs.
Compilation, all attempted bounds and duality types, export, compression and
independent verification share that budget. The thread count comes from `nproc`.
The enumeration allowance is 90% of the remaining driver time, reserving the rest
for verification and export; no shorter 1,100/1,200-second cap remains in this campaign.

The first bounds are read from the released manifest plus one (currently 20, 7, 4, 2 for ranks 5–8). An interrupted search is restarted, not resumed. A completed candidate
must pass exhaustive independent tensor/isomorphism verification and agree with
the entire old exact-multiplicity count prefix before entering `best/`.

Outcomes are `verified_extension`, `no_extension_within_budget`, or `error`.
Expected timeouts make no new claim; genuine failures make the job fail. Logs,
timing ledgers, commands, environment and verifier reports are retained for
14 days, together with the last verified candidate, if any. Incomplete tensor
collections are excluded. Candidates are never automatically promoted or copied
into manuscripts or OEIS tables. See [campaign details](docs/LONG_CAMPAIGN.md).

The original [frontier workflow](.github/workflows/frontier.yml) remains a
separate manual tool with its 1,100-second driver and 20-minute job limits; it is
not dispatched by the long campaign. Both workflows share a concurrency lock,
and job reruns are disabled to prevent resetting the campaign allowance.
Verification and manuscript workflows also remain manual. Check account-wide
included usage and enforced spending controls before each authorized dispatch.
Do not change visibility or billing to obtain more capacity.

The first published run found no complete extension for ranks 5–8. The longer
[run 35440299307](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35440299307)
completed rank 5 through multiplicity 19: **34,133 classes**, including **5,640
at exact multiplicity 19**. It did not complete rank 5 at 20, rank 6 at 7,
rank 7 at 4 or rank 8 at 2. After a fresh independent GitHub audit, the rank-5
candidate was integrated; every other released bound is unchanged. Permanent
[review evidence](docs/CAMPAIGN_REVIEW.md) records the accepted result and timeouts. Review [the release procedure](docs/RELEASES.md) before any
future promotion. `scripts/publish_github.py` is an initial-publication helper;
do not use it to recreate this existing repository.

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

Use **Cite this repository**, or the metadata in `CITATION.cff`.
Report a suspected missed ring with its full multiplication tensor, rank,
multiplicity, generating command and revision. Improvements must preserve every
singular and zero-coefficient branch and pass independent checks. See
[CONTRIBUTING.md](CONTRIBUTING.md).
