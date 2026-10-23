# Validation and measured performance — v3, 2026-10-23

## Completed whole-rank runs

| Rank | Multiplicity bound | Distinct fusion rings | Independent tensor verification |
|---|---:|---:|---|
| 9 | 1 | 142 | Passed; no duplicates |
| 10 | 1 | 194 | Passed; no duplicates |

The final rank-9 laptop command also produced its verified output ZIP. Rank 9
matches the retained explicit-permutation implementation byte-for-byte after
sorting parameters and exporting tensors. The final rank-10 run used the same
final source hash as the rank-9 launcher run. Their data and execution reports
are in `benchmarks/evidence/rank11_extension/whole_rank/`.

A rank-11 test with a **600-second shared enumeration budget** did not complete:
it finished the first two duality strata and timed out in the third. No complete
rank-11 count or verified archive is claimed. The normal laptop launcher has no
time limit. The attempt is recorded separately under `rank11_timed_attempt/`.
This timed attempt preceded the final bounded-memory self-dual refinement; it
never reached the self-dual stratum. The final rank-11 code is covered by the
additional exact symmetry, contraction, moment and known-ring fixture checks.

## Controlled output comparisons

Rank 9, bound 1, one thread, three repetitions per implementation, alternating
run order; the table uses median subprocess wall times in seconds. Compilation
and equation generation are excluded. Every pair has exactly equal sorted
parameter sets. Concurrent work affected timings, so these are measurements on
this machine, not a prediction for a laptop or for other ranks/bounds.

| Duality stratum | v2 reference | v3 | Speedup |
|---|---:|---:|---:|
| pairs1 | 3.089 | 1.797 | 1.72× |
| pairs2 | 4.216 | 3.091 | 1.36× |
| pairs3 | 1.174 | 0.904 | 1.30× |
| pairs4 | 0.228 | 0.155 | 1.47× |
| selfdual | 7.316 | 2.124 | 3.44× |
| Sum of stratum medians | 16.023 | 8.070 | 1.99× |

The v2 reference has only rank-9 guards/template dispatch enabled; its algorithms
are unchanged. The reproducible command is:

```bash
python3 scripts/benchmark_v3.py --rank 9 --bound 1 --threads 1 --repeats 3 --out comparison_v3
```

Logs and JSON are in `benchmarks/evidence/rank11_extension/rank9_paired/`.
The benchmark prepares all lower-rank systems required by weighted folding.

## Independent verification and memory

On the rank-9 corpus augmented with relabelled copies, both verifier modes found
142 classes and 163 duplicate records. In the recorded comparison, invariant
refinement took about 0.168 seconds versus 1.892 seconds for exhaustive
permutations: approximately 11.2× faster. The source tensors and evidence are in
`audits/evidence/`; the proof is `audits/VERIFIER_REFINEMENT.md`.

The rank-9 self-dual equation text shrank from 14,975,944 to 58,279 bytes
(257.0× smaller). At rank 11 the full variable-permutation table would
contain 3,628,800 rows of 220 entries. The delivered format stores the duality
and orbit representatives instead. First-matrix symmetry storage is separately
bounded by 666 maps in its largest rank-11 color block, compared with 362,880
maps in the full-stabilizer method. These are exact storage comparisons;
worst-case search time remains exponential.

## Correctness checks

- All 19 Python regression tests passed, covering CLI limits, missing-reference
  handling, all duality types, packaging, incomplete/truncated output rejection,
  exact rank-9/10/11 fixtures and verifier relabellings.
- Existing equation-support and Gaussian audits passed after the sparse update.
- Compact versus explicit canonicality agreed on 1,138 vectors, including every
  rank-8/9 corpus ring, and 3,414 duality-preserving relabellings. All 714 tested
  partial domains retained their known canonical solution.
- Early contraction masks passed 80,928 cases with 1,109,232 exhaustive binary
  completions.
- Graph canonicality passed 5,724 matrices against 15,715,269 explicit
  permutations and 64,044 canonical-prefix checks.
- The extended moment-identity audit passed 160,000 cases through rank 11 and
  multiplicity bound 15. Analytic arithmetic bounds are documented separately.
- Three rank-10 self-dual variants produced the same 53 sorted parameter rows.

Proofs, portable audit programs, logs and exact parity records are included.
Reproduce the standard checks and the new self-dual audits with:

```bash
python3 -m unittest discover -s tests -v
python3 tests/run_audits.py
python3 audits/run_rank11_selfdual_audits.py
```

The new high-rank tests establish implementation consistency and verify emitted
rings; they do not replace independent human review of the completeness proofs.
Higher multiplicity limits are supported by the arithmetic/domain audit, without
a claim that full high-rank searches at those bounds were completed here.
