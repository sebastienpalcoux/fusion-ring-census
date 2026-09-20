# Ranks 5–8: bounded long campaign

This document preserves the launch contract and original starting bounds for the
completed campaign. Its reviewed outcome is now recorded in
[CAMPAIGN_REVIEW.md](CAMPAIGN_REVIEW.md): rank 5 extended to multiplicity 19;
ranks 6–8 did not extend. The enumerator algorithms and mathematical scope did
not change. Original datasets and history remain preserved.

## Reviewed previous run

[Run 35433992685](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35433992685)
used commit `5173786bd7c60d9bc7713db559c38ef9f9731527`. GitHub marked it successful,
but all four extension attempts were incomplete and unverified. The small
artifacts are preserved under `verification/github_actions/run35433992685/`.

| Rank | Initial released bound | Initial classes | Campaign restart bound | Previous timeout stage |
|---:|---:|---:|---:|---|
| 5 | 18 | 28,493 | 19 | selfdual |
| 6 | 6 | 5,799 | 7 | selfdual |
| 7 | 3 | 1,421 | 4 | pairs1 |
| 8 | 1 | 96 | 2 | pairs1 |

The reports record about 990 enumeration seconds per rank. Rank 5 was terminated
by Python's subprocess timeout; the other three enumerators returned their
explicit incomplete-search code 3. Compilation had succeeded. Export and tensor
verification were not reached. There is no evidence of a compiler, resource or
verification failure in these retained reports. The old driver deleted the
per-duality logs, so those unavailable details cannot be independently reviewed.
No valid checkpoint was retained; this campaign restarts each unfinished bound.

## Execution contract

- Workflow: `.github/workflows/long-frontier.yml`, manual dispatch only.
- Exactly four standard `ubuntu-24.04` jobs, ranks `[5,6,7,8]`, maximum parallelism
  four, and `fail-fast: false`. No rank-3 or rank-4 job.
- Each rank: 4,200 shared driver seconds; 75-minute job ceiling. Maximum campaign
  allocation: 300 runner-minutes. No separate remote testing/build job is needed.
- The first bound is read from `results/census.json` plus one. After accepting it,
  advance by one using only the remaining budget, with content-keyed build reuse.
- The existing finite multiplicity caps remain 32 for rank 5 and 15 for ranks
  6–8. Reaching a cap is an explicit early-stop reason, not an incomplete search.
- Enumeration receives 90% of remaining execution time. Compilation, export,
  compression and verification remain subject to the same outer deadline.
  Three seconds within the budget are reserved for termination and cleanup.
- Threads come from `nproc`, not a presumed four CPUs. The previous standard
  runners reported two CPUs.
- Both frontier workflows share a concurrency lock across branches. Automatic
  job reruns are disabled. Check for queued/running campaigns before dispatch.
- Keep the repository private. Use included capacity with enforced no-paid-usage
  controls; do not modify billing, permissions or visibility to obtain capacity.

Every duality type and noncommutative case remains in scope. Exact arithmetic,
zero/singular branches and exhaustive coverage arguments are unchanged. Every
accepted candidate passes the existing independent exhaustive tensor and
based-isomorphism checks, plus agreement of the entire earlier count prefix.

## Outcomes and evidence

`frontier.json` and the job summary state one of `verified_extension`,
`no_extension_within_budget`, or `error`. The first does not imply the last
attempt completed: the ledger records every attempted bound. A later timeout
preserves `best/`; a later genuine failure also preserves it but marks the job
as an error. Missing/malformed child reports and unexpected exits are errors.

The always-run upload retains environment/source revision, each command and
phase/timing report, per-duality and compiler logs, independent verification
reports, and the last accepted `best/`, if any, for 14 days. Partial search
parameters/tensors and redundant uncompressed canonical tensor copies are not
uploaded. Detailed log counts are diagnostic and cannot supply census or OEIS
claims. Runner loss can prevent evidence upload despite `if: always()`.

The launch task left candidates as reviewable artifacts. The subsequent user-requested
review integrated only rank 5 through multiplicity 19, after fresh independent
verification. Future campaigns still require explicit authorization and a spending
check; their starting bounds are read from the current manifest.

The later [laptop review](RANK6_LAPTOP_REVIEW.md) extended rank 6 through 7.
The table above is historical; future starts use the current manifest.
