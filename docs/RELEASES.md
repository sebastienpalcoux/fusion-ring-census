# Publication and promotion of computed data

## Existing private repository and bounded campaigns

The project is published privately at
[sebastienpalcoux/fusion-ring-census](https://github.com/sebastienpalcoux/fusion-ring-census).
Preserve its Git history; do not rerun the initial repository-creation helper,
force-push, change visibility, or alter billing settings.

The manual `long-frontier.yml` campaign runs ranks 5–8 only, with four jobs at
most, 4,200 driver seconds per rank and 75 job minutes per rank (300 runner-minutes
total). The legacy `frontier.yml` remains manual with its original 1,100-second
and 20-minute limits. Both share the same concurrency lock. Reruns are rejected;
a further campaign requires a separately authorized dispatch and budget check.

The separate [rank-6 bound-7 maximum-duration campaign](RANK6_M7_MAX.md) has one
six-hour job and a 21,300-second shared driver deadline, explicitly restricted to
that rank and bound. It shares the concurrency lock and only uploads verified
candidates/diagnostics. Its launch-then-stop authorization does not promote data.

Before dispatch, inspect active runs and the account-wide included Actions
minutes/storage and enforced spending controls. Use standard Ubuntu runners
and existing included capacity only. If paid usage cannot be excluded, prepare
and push safe changes but stop before dispatch. Do not infer quota from elapsed
run time or an Actions timing API returning zero. Do not enable overages or buy
capacity. Check the exact pushed revision and dispatch once. No results are
implied by launch acceptance, a green check, or an artifact name.

See [the long campaign contract](LONG_CAMPAIGN.md). Candidates and diagnostics
expire after 14 days. There is no automated promotion or manuscript/OEIS update.

## Review a frontier result

Download and extract the workflow artifact. Check the run's conclusion, exact
commit, command and environment, then read `frontier.json` and `best/run.json`.
An artifact without `best/` contains no new certified bound. Full numerical
verification must run on GitHub Actions when operating from Work. For this review,
`review-rank5-m19.yml` pins the source run and commit, invokes the guarded importer
on the runner, and uploads verified integration files without committing them.
It is manual, read-only to the repository, and capped at 10 job minutes.
Its dataset/manifest files are downloaded only after successful verification.
The equivalent importer command below belongs on that runner; documentation
and PDF regeneration can run in Work:

```bash
python3 scripts/promote_result.py extracted-artifact/best
python3 scripts/refresh_documentation.py
python3 scripts/build_manuscripts.py --compile
python3 scripts/build_site.py
python3 scripts/check_release.py  # lightweight integrity check; --full belongs on Actions
python3 -m unittest discover -s tests -v
git diff --stat
```

The importer requires `complete: true` and `verified: true`, an actual larger
bound, agreement with all existing-prefix counts, correct uncompressed hashes,
and a new full independent tensor audit. It does not commit or push. The release
manifest, manuscripts, count files and OEIS projections must be updated together.
Inspect the diff, preserve logs and obtain mathematical review before tagging a
release. The project deliberately does not auto-commit new mathematical claims.

## Release inventory

`results/census.json` is authoritative for complete bounds, class counts and
tensor digests. Historical inputs and reports remain separately under `reference/`,
`audit/` and `verification/`. Never call a source-only partial count exhaustive.
Avoid adding binaries, build caches, raw timed-out tensor fragments or credentials.
Prefer compressed text datasets and release artifacts for large reruns.

A useful release contains tagged source, systems, PDFs and TeX, counts, tensor
digests, independent verification reports, provenance and a clear changelog.
OEIS submission is a separate reviewed action, not part of tagging or CI.

## Platform references

- Repository creation: https://cli.github.com/manual/gh_repo_create
- Workflow dispatch: https://cli.github.com/manual/gh_workflow_run
- Workflow syntax and job limits: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax

The rank-six bound-seven result was subsequently completed on the user's laptop
and [freshly audited and integrated](RANK6_LAPTOP_REVIEW.md). The historical
maximum-duration campaign cannot rerun against the new baseline.
