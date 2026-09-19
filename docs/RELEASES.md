# Publication and promotion of computed data

## Initial GitHub publication

The assembled package is local. No remote creation or Actions execution is
implied by the presence of workflow files. Install GitHub CLI, authenticate as
`sebastienpalcoux`, and run:

```bash
gh auth login
python3 scripts/publish_github.py --run-census
```

The helper verifies account identity and release hashes, refuses to overwrite an
existing repository, makes a local initial commit if needed, creates a **private**
repository, pushes it, and requests the frontier workflow exactly once. Use
`--public` only as an explicit decision to publish. Credentials remain in the
GitHub CLI authentication store; they are neither arguments nor repository files.
Creating the repository or dispatching a run can fail because of permissions,
Actions policy, billing restrictions or an existing name. Such failures must be
resolved explicitly; the script does not pretend they succeeded.

Private-repository Actions usage may consume the account's included allowance or
be billed according to its configuration. Five rank jobs can run concurrently;
rank three has a short additional job. The job ceiling is 20 minutes **per rank**,
not 20 minutes for the entire matrix. The user must retain control of account
visibility, spending and any later publication.

## Review a frontier result

Download and extract the workflow artifact. Check the run's conclusion, exact
commit, command and environment, then read `frontier.json` and `best/run.json`.
An artifact without `best/` contains no new certified bound. To import a candidate:

```bash
python3 scripts/promote_result.py extracted-artifact/best
python3 scripts/refresh_documentation.py
python3 scripts/build_manuscripts.py --compile
python3 scripts/build_site.py
python3 scripts/check_release.py --full
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
