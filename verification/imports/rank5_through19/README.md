# Rank 5 through multiplicity 19: reviewed import

- Source campaign: https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35440299307
- Fresh independent audit: https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35449570360
- `run.json` and `artifact_independent_check/` are original candidate evidence.
- `fresh_independent_check/` contains the exhaustive rerun of the independent
  tensor and based-isomorphism audit: 34,133 distinct records, zero duplicates.
- `review.json` records the fresh verifier source, command and environment.
- `source-run.json` is source-run metadata read back from GitHub during review;
  `verification.log` is the fresh importer/verifier output.

The two compressed release files match the original accepted candidate bytes.
Their compressed and uncompressed hashes are in `results/census.json`.
Exact-multiplicity counts through 18 agree with the earlier complete release;
only c_5(19)=5640 is newly appended. No count at multiplicity 20 is certified.
The redundant uncompressed canonical tensor copy is not retained; full compressed
input tensors plus summary, counts, line map and duplicate reports are preserved.
