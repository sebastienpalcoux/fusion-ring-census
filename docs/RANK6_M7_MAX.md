# Rank 6, multiplicity 7: maximum-duration hosted job

This separately authorized campaign attempts **rank 6 through multiplicity 7
only**. The released baseline is bound 6 with 5,799 classes. It restarts the
unfinished bound; the previous attempts left no verified resumable checkpoint.
It does not search bound 8 or run any other rank.

## Limits and included capacity

GitHub documents a [six-hour limit for each hosted-runner job](https://docs.github.com/en/actions/reference/limits).
The manual `.github/workflows/rank6-m7-max.yml` uses one standard `ubuntu-24.04`
job with `timeout-minutes: 360`. It uses the actual CPU allocation from `nproc`.
No paid larger runner, AI API or model is involved.

- Shared driver deadline: **21,300 seconds (355 minutes)**, covering compilation,
  all duality strata, export, compression, independent verification and acceptance.
- Three seconds remain reserved inside that deadline for cleanup. Enumeration
  receives the remaining driver allowance minus a **120-second reserve** for
  other phases, approximately **21,177 seconds (5 h 52 min 57 s)** at launch.
  Compilation consumes the same outer wall-clock budget. This explicitly scoped
  campaign does not retain the shorter 4,200-second or 90% enumeration ceiling.
- Five minutes outside the driver budget accommodate checkout, status recording
  and artifact upload within the six-hour job. All limits remain finite, and
  the search stops early if it completes or encounters a genuine error.
- At preparation, authenticated billing showed **351 / 2,000 included minutes
  used**, leaving 1,649; the storage display showed 0 GB used / 0.5 GB included
  (rounded UI values). The account-wide Actions budget was **$0**, with enforced
  **Stop usage: Yes** and $0 billable usage. Billing settings were not changed.

The explicit `--rank6-m7-max` option is required by both Python drivers. The
frontier rejects any rank other than 6, any baseline other than 6, any start other
than 7 or any upper search bound other than 7. The low-level program requires
rank 6, bound 7, verification and a propagated finite deadline. All standard
campaigns retain their prior limits. There is one attempt, no automatic retries,
and the workflow shares the existing `census-frontier` concurrency lock.

## Acceptance and evidence

Every duality type and noncommutative case remains included; no categorifiability
filter or mathematical pruning rule changes. Acceptance requires completion of
all strata, independent checking of every tensor and every unit-fixing basis
permutation, zero duplicates, and agreement of all prior exact-multiplicity
counts. A timeout is not a complete census result.

Always-run artifact upload retains `frontier.json`, `SUMMARY.md`, source/environment,
commands, per-duality logs and available verification reports for 14 days.
Only a complete independently verified candidate enters `best/`. Partial tensor
collections are excluded. Genuine errors fail the job; expected budget exhaustion
records `no_extension_within_budget` without changing the released baseline.

The user requested **launch then stop**. No integration job, automatic commit,
manuscript build or OEIS update runs in this campaign. A successful candidate
will be reviewed and integrated when the user returns. The repository stays private.

The equivalent driver invocation on GitHub is:

```bash
python3 scripts/extend_census.py --rank 6 --rank6-m7-max --seconds 21300 \
  --max-bound 7 --threads "$(nproc)" --out frontier/rank6
```

Tests for the longer deadline, the inner allowance, single-bound stopping and
invalid scope use mocked numerical subprocesses; no census is run in Work.
