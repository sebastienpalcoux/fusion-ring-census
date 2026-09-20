# Completed campaign review — 19 September 2026

The longer GitHub campaign produced **one complete extension**: rank 5 through
multiplicity 19, with **34,133 distinct based-isomorphism classes**. The new exact
multiplicity term is **c₅(19) = 5,640**. After a fresh independent audit on GitHub,
this candidate was integrated into the release. All other complete bounds remain
unchanged. The six-rank total at that review was **1,391,332 classes**.
The subsequent [laptop review](RANK6_LAPTOP_REVIEW.md) extended rank 6; this page
retains the historical campaign snapshot.

| Rank | Previous bound / classes | Reviewed bound / classes | Incomplete attempt |
|---:|---:|---:|---|
| 3 | 1000 / 460,353 | 1000 / 460,353 | Not run in this campaign |
| 4 | 128 / 889,530 | 128 / 889,530 | Not run in this campaign |
| 5 | 18 / 28,493 | **19 / 34,133** | Bound 20: selfdual timeout |
| 6 | 6 / 5,799 | 6 / 5,799 | Bound 7: selfdual budget exhaustion |
| 7 | 3 / 1,421 | 3 / 1,421 | Bound 4: selfdual budget exhaustion |
| 8 | 1 / 96 | 1 / 96 | Bound 2: selfdual budget exhaustion |

## Source run and actual search progress

[Campaign 35440299307](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35440299307)
ran source commit `931addc686e8d93e86e480c6a8cc56d0301dfabf` once. GitHub reported
success. The four rank jobs each had 4,200 shared driver seconds and a 75-minute
job ceiling, using two CPU threads on standard Ubuntu runners. The green
conclusion includes expected budget exhaustion and is not a completeness claim.

| Rank | Attempted bounds | Driver elapsed seconds | Reviewed outcome |
|---:|---|---:|---|
| 5 | 19, then 20 | 3993.774 | `verified_extension` |
| 6 | 7 | 3790.509 | `no_extension_within_budget` |
| 7 | 4 | 3791.783 | `no_extension_within_budget` |
| 8 | 2 | 3789.300 | `no_extension_within_budget` |

Rank 5 completed both nonselfdual and selfdual enumeration at 19. Enumeration
took 2151.251 seconds, and the entire accepted attempt took 2164.157 seconds,
including compilation, export, independent verification and compression. The
driver immediately retained that candidate, then attempted 20 with only the
remaining shared budget. The latter stopped during selfdual enumeration after
about 1829.6 seconds; its incomplete files did not replace the accepted data.

At ranks 6–8, every nonselfdual stratum completed before the selfdual search
exhausted the remaining enumeration allowance. Rank 6 used about 24.8 seconds
for its two nonselfdual strata and 3752.5 seconds for selfdual enumeration.
Rank 7 used about 3455.1 seconds for its three nonselfdual strata, leaving about
322.1 seconds for selfdual enumeration. Rank 8 used about 3556.4 seconds for its
three nonselfdual strata, leaving about 220.9 seconds for selfdual enumeration.
These are elapsed search times, not estimates of the fraction of the whole
search space covered.

The driver reserves 10% of remaining time for other phases, so a legitimate
enumeration stop can occur before the 4,200-second outer deadline. It did not
idle to consume that reserve. The rank-5 timeout came from the Python deadline;
the incomplete selfdual enumerators at ranks 6–8 returned their expected code 3.
The retained logs show successful compilation and no unexpected exception,
out-of-memory report, invalid tensor or verification mismatch. Verification was
not reached for the incomplete bounds. No valid resumable checkpoint exists.
Future authorized searches would restart at bounds **20, 7, 4 and 2**.

## Acceptance and fresh independent verification

The original rank-5 verifier checked all 34,133 full tensors, including every
integer associativity identity and all 24 unit-fixing basis permutations per
tensor: 819,192 permutations in total. It found zero duplicates or additional
isomorphic labellings. Both enumeration strata terminated normally. Coverage
continues to rely on the existing exhaustive parameterization and proofs; tensor
verification alone is not a proof that enumeration omitted nothing.

[Fresh audit 35449570360](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35449570360)
ran commit `235f3f716973c95689adc217d44a0f650e2bcebc` on a standard GitHub Ubuntu
runner. Its single verification-only job had a 10-minute ceiling and completed
successfully in 18 seconds. No enumeration was launched. Before dispatch, the
account-wide Actions budget showed $0 with enforced “Stop usage: Yes”; billing
and visibility were not changed.

The guarded importer checked the original candidate reports, every required
duality stratum, compressed payload contents against the recorded uncompressed
SHA-256 hashes, and the full earlier exact-multiplicity prefix. It compiled the
independent verifier afresh, checked every tensor and based isomorphism again,
and obtained the same exact counts and zero duplicates. The downloaded verified
integration files were compared with the original candidate bytes before import.

The original and fresh reports are retained under
[`verification/imports/rank5_through19/`](../verification/imports/rank5_through19/).
Earlier full-release audits remain historical records of their original bounds.
The unchanged rank-3/4/6/7/8 datasets were checked for file integrity in this
review; their full mathematical audits were not unnecessarily rerun.

## Repository revision and evidence

- The primary manifest points to the new complete rank-5 tensor and parameter
  files; the older bound-18 files remain preserved.
- Count CSVs, the combined table, README, landing page, six LaTeX/PDF companions,
  provenance and local OEIS drafts now agree with the manifest. Only the rank-5
  exact-multiplicity sequence gains the new term 19 → 5640.
- Original per-rank ledgers, environment, commands, compiler/duality logs and
  available verifier reports are permanently retained under
  [`verification/github_actions/run35440299307/`](../verification/github_actions/run35440299307/),
  with a SHA-256 inventory. Partial numbers inside diagnostic logs are not
  released census counts. No incomplete tensor collection is committed.
- Algorithms, singular and zero-coefficient branches, licensing and attribution
  are preserved. All duality types and noncommutative cases remain in scope,
  without a categorifiability filter. The importer now also enforces the same
  explicit duality-completion checks as the campaign driver.
- The repository remains private. Workflows remain manual. No new census
  campaign, automatic retry, public release tag or online OEIS submission was
  made as part of this review.

Lightweight regression and dataset-integrity checks are recorded in
[`verification/repository_checks/review_2026-09-19/`](../verification/repository_checks/review_2026-09-19/).
The mathematical companions remain computational project notes, not a claim of
formal proof-assistant certification or peer-reviewed acceptance.
