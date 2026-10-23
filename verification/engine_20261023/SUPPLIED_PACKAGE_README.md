# Fusion-ring census: optimized laptop package v3 (ranks 3–11)

This standalone source package enumerates bounded fusion rings, including every
duality type and noncommutative rings. It does not assume categorifiability.
The launcher now supports ranks 9, 10, and 11.

## Run on Ubuntu

Extract the ZIP into a fresh directory and enter `Fusion_Census_Deep_Optimized`.
Dependencies are Python 3.9+ and GNU g++ with C++17/OpenMP:

```bash
sudo apt-get install python3 g++ unzip
python3 scripts/run_laptop.py --rank 9 --bound 1
```

For rank 11:

```bash
python3 scripts/run_laptop.py --rank 11 --bound 1
```

Optional CPU count and result location:

```bash
python3 scripts/run_laptop.py --rank 11 --bound 1 --threads 8 --output-dir my_runs
```

Supported bounds: 1–1000 for ranks 3–4, 1–32 for rank 5, and 1–15 for ranks 6–11.
Support does not imply a short runtime for every input, especially higher ranks
and bounds. No completed rank-11 census is assumed.

The launcher has no clock limit. Keep the laptop awake and connected to power.
Interruption does not support resuming; use a fresh `--output-dir` to restart.
The first run compiles automatically; later runs reuse binaries when their
actual C++ dependencies are unchanged. The self-dual executable is compiled
only for the requested rank.

## Results and verification

For rank 11 and bound 1, progress is recorded under `runs/rank11_M1/`.
The final archive is `runs/rank11_multiplicity1_verified.zip`.
It is produced only after every duality stratum finishes, emitted records agree
with the enumerators' totals, every tensor passes exact fusion-ring checks,
an independent exact isomorphism checker finds no duplicates, and any existing
certified reference counts agree.

Ranks 3–8 retain mandatory reference-prefix comparison. There is no released
reference baseline for ranks 9–11 in `results/census.json`; their provenance
records `baseline: null` and `existing_prefix_checked_through: 0`. New computation
results are not silently promoted to an external reference.

The independent checker now uses exact invariant refinement. Its original
`--exhaustive` mode remains available for comparison. Both modes verify every
reported isomorphism witness against the original tensors, as well as unit,
duality, Frobenius reciprocity and associativity.

## Main efficiency changes

- Compact symmetry systems avoid storing factorially many basis permutations;
  full exact canonicality is checked by a streamed search.
- At multiplicity 1, the identity `x² = x` simplifies the integer equations;
  sparse modular elimination skips zero pivot entries.
- Larger self-dual searches use additional exact contraction checks and
  bounded-memory graph symmetry handling.
- Worker initialization reuses parsed equation systems.
- The independent verifier uses individualization and invariant refinement.
- Compilation caches follow actual C++ dependencies; Python and documentation
  edits do not recompile unrelated kernels.

See `VALIDATION_V3.md` for measured results and limits,
`methods/COMPACT_SYMMETRY.md` and `audits/VERIFIER_REFINEMENT.md` for proofs,
and the self-dual audit notes. Earlier proofs remain in `OPTIMIZATIONS.md`,
`methods/SELFDUAL_PROOF.md`, and `methods/GAUSSIAN_AUDIT.md`.

## Reproduce checks and benchmarks

```bash
python3 -m unittest discover -s tests -v
python3 tests/run_audits.py
python3 scripts/benchmark_v3.py --rank 9 --bound 1 --threads 2 --repeats 3 --out benchmark_v3
```

The benchmark excludes compilation and reference-system generation, alternates
run order, and requires exact equality of sorted parameter sets. A timeout,
duplicate or disagreement fails the benchmark. The retained v2 reference has
only its rank guards extended to rank 9; its enumeration algorithms are unchanged.
Reference kernels must use explicit reference systems, never compact v3 files.
The benchmark prepares the appropriate files automatically.

`SOURCE.json` records provenance; `SHA256SUMS` covers the shipped files.
This package does not modify or publish anything on GitHub.
