# Provenance and attribution

## Primary mathematical source

Gert Vercleyen and Joost K. Slingerland, *On low rank fusion rings*, Journal of
Mathematical Physics **64** (2023), 091703; arXiv:2205.15637v4.
The retained input is the v4 ancillary `FusionRingMultiplicationTables` file:

- SHA-256: `b587c3f683157369da7cc090f762bbff0e18dcf11acc3f5031d6bc0c643843f8`.
- Original size: 16,531,197 bytes; original records: 28,451.
- Distinct based-isomorphism classes in that input: 25,138.
- Redundant records: 3,313, all at rank five and multiplicities 9–12.

The copy originally came from the retained rank-five project archive, not a fresh
arXiv download during repository assembly. Its exact checksum is the provenance
identifier. Deduplication is not a proof of completeness of an original partial
cell. Each deletion has a concrete checked unit-fixing basis permutation.
The Vercleyen–Slingerland data are used for **comparison**, not enumeration input.

## Retained project materials

The specialized rank-four and rank-five reductions are retained from the
Dong–Palcoux census project and its exact-certificate supplements, September 2026.
The preserved proof excerpts explicitly record zero coefficients and singular
Krylov branches. They are unpublished project manuscripts; no journal acceptance,
DOI or arXiv identifier for these companions is asserted.

Rank-three data through 1000 and the complete rank-four through rank-seven datasets
come from completed computations of 18 September 2026. Their execution ledgers and
independent audits are retained. The repository assembly does not retrospectively
change their run times or attribute those runs to GitHub Actions.

Rank eight required enlarging the general solver's actual workspace, not merely
changing its rank flag: self-dual rank eight has 84 variables and 231 equations,
and other duality types can have more equations. Fixed 80-variable/200-equation
buffers were replaced by size-dependent storage. Regression searches cover every
supported rank, and the rank-eight multiplicity-one result is independently
verified under all 5,040 unit-fixing permutations.

## AI assistance and verification

GPT-6 Astra Pro assisted in algorithm development, code assembly, documentation,
proof exposition and computational checks. This disclosure is not a substitute
for human mathematical review. Exact integer output verification and exhaustive
search arguments are separate forms of evidence. The manuscripts are explanatory
computational companions, not a claim of peer-reviewed publication or formal
proof-assistant verification. No Lean certification is claimed.

## Scope of this release

Only full-rank verified datasets belong to `results/`. Earlier partial searches
may be discussed in historical provenance but cannot enter new OEIS terms.
Rank three is deliberately capped at 1000. The scope is based-ring enumeration,
not tensor-category categorification. Every reference, name and count must retain
this distinction when the repository is advertised or cited.

## Local rank-eight extension attempt

The whole-rank multiplicity-two attempt ended after 1,099.817 seconds of a
1,100-second enumeration allowance without completing every duality type. It
does not enlarge the release. Only status/timing and source hashes are retained
in `verification/repository_checks/rank8_bound2_no_extension.json`; partial
tensors and partial-stratum counts are not included. This was a local attempt,
not a GitHub Actions run. The rank-four through rank-seven large bounds were
not rerun in this repository-assembly session; their original full run records
and the fresh independent audit remain separate.

## GitHub publication and reviewed extension, 19 September 2026

The repository was published privately at commit
`5173786bd7c60d9bc7713db559c38ef9f9731527`. Its first frontier run
35433992685 did not extend ranks 5–8. The later four-rank campaign,
[run 35440299307](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35440299307),
used commit `931addc686e8d93e86e480c6a8cc56d0301dfabf` and two CPU threads per job.
It completed rank 5 through multiplicity 19, with 34,133 distinct classes.
Both rank-five duality strata completed and the exhaustive independent verifier
checked every tensor and all 24 unit-fixing basis permutations. Exact-multiplicity
counts through 18 agree with the earlier release; the new count at 19 is 5,640.

A second independent audit ran on GitHub in run 35449570360 before integration.
Original candidate and fresh verifier reports are under
`verification/imports/rank5_through19/`. Small campaign diagnostics for every rank
are permanently retained under `verification/github_actions/run35440299307/`.
The rank-five bound-18 data and all earlier verification reports remain preserved
as historical evidence. They have not been relabelled as checks of the new bound.

Rank 5 at 20 and ranks 6/7/8 at 7/4/2 exhausted their enumeration allowance.
Successful nonselfdual strata at those bounds do not establish whole-rank counts.
No compilation, resource or verification failure was found in the retained logs.
Ranks 3 and 4 were not recomputed or extended. The review changed the rank-five
release and derived documentation, not the enumerator algorithms or proof methods.
