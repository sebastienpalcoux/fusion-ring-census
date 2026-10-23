# Reproducible original / v1 / v2 comparison

Measurements are from completed exhaustive computations, not estimates from
partial search trees. Every timed output is checked as an exact sorted parameter
set against both other versions and the corresponding released subset. No
isomorphic duplicates or repeated parameter lines were found.

- Original: upstream commit `d4c36cc2ee5eb5f0e5291de18d2bb433ffb7ce8b`.
- v1: the previous optimized package delivered in this conversation.
- v2: the frozen source in this package (`SOURCE.json` contains hashes).
- Hardware: AMD EPYC 9V74 host, 9 CPUs available to this process; Linux x86-64.
- Compiler: GNU g++ 13.3.0, identical `-O3 -std=c++17 -fopenmp` flags.
- Each case was run three times, rotating the order of the three versions.
  Timed processes ran sequentially, without concurrent development/audit jobs.
- Times are medians of the C++ enumeration timer, in seconds. Compilation,
  export, compression, and independent verification are excluded.
- The original's existing engine selection and fixed-prefix parallel scheduler
  are retained; v1/v2 use their propagated frontiers. All use the same equation
  system files. Threads are explicitly fixed to 1 or 4.

## Complete whole-rank enumeration

Each entry sums the per-duality-type median times for **all** duality types,
including the self-dual component and the noncommutative types. It is not a
median end-to-end Python-launcher time. The class counts are cumulative through
the stated bound.

| Rank | Bound | Threads | Classes | Original | v1 | v2 | Original/v2 | v1/v2 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7 | 2 | 1 | 362 | 11.9729 | 9.2838 | 1.5098 | 7.93x | 6.15x |
| 8 | 1 | 1 | 96 | 2.1912 | 0.7203 | 0.4263 | 5.14x | 1.69x |
| 7 | 2 | 4 | 362 | 4.3564 | 2.4526 | 0.4106 | 10.61x | 5.97x |
| 8 | 1 | 4 | 96 | 1.0911 | 0.4384 | 0.3752 | 2.91x | 1.17x |

## Higher-bound completed component tests

These are complete components, not whole-rank totals. All use one thread and
three repetitions.

| Component | Classes | Original | v1 | v2 | Original/v2 | v1/v2 |
|---|---:|---:|---:|---:|---:|---:|
| Rank 6, bound 3, self-dual | 408 | 2.7807 | 2.3864 | 0.4741 | 5.87x | 5.03x |
| Rank 7, bound 3, one dual pair | 385 | 92.0684 | 12.2810 | 3.5089 | 26.24x | 3.50x |

## Every measured stratum

Here `sd` denotes self-dual; `p` counts dual pairs. All stratum outputs match
exactly. Small subsecond cases are sensitive to scheduling and measurement
noise; some do not improve relative to v1.

| Case | Threads | Original | v1 | v2 | Original/v2 | v1/v2 |
|---|---:|---:|---:|---:|---:|---:|
| sd7m2 | 1 | 9.89056 | 8.53440 | 0.99207 | 9.97x | 8.60x |
| ns7p1m2 | 1 | 1.67991 | 0.41292 | 0.25586 | 6.57x | 1.61x |
| ns7p2m2 | 1 | 0.35812 | 0.26850 | 0.21985 | 1.63x | 1.22x |
| ns7p3m2 | 1 | 0.04427 | 0.06803 | 0.04201 | 1.05x | 1.62x |
| sd8m1 | 1 | 0.79246 | 0.43807 | 0.15635 | 5.07x | 2.80x |
| ns8p1m1 | 1 | 0.81583 | 0.11277 | 0.11027 | 7.40x | 1.02x |
| ns8p2m1 | 1 | 0.50075 | 0.12144 | 0.11150 | 4.49x | 1.09x |
| ns8p3m1 | 1 | 0.08219 | 0.04804 | 0.04821 | 1.70x | 1.00x |
| sd7m2 | 4 | 3.47085 | 2.17913 | 0.21282 | 16.31x | 10.24x |
| ns7p1m2 | 4 | 0.50372 | 0.12922 | 0.09064 | 5.56x | 1.43x |
| ns7p2m2 | 4 | 0.34366 | 0.08015 | 0.06982 | 4.92x | 1.15x |
| ns7p3m2 | 4 | 0.03821 | 0.06412 | 0.03736 | 1.02x | 1.72x |
| sd8m1 | 4 | 0.25457 | 0.16051 | 0.11013 | 2.31x | 1.46x |
| ns8p1m1 | 4 | 0.26556 | 0.10484 | 0.10798 | 2.46x | 0.97x |
| ns8p2m1 | 4 | 0.49443 | 0.12320 | 0.11254 | 4.39x | 1.09x |
| ns8p3m1 | 4 | 0.07651 | 0.04981 | 0.04459 | 1.72x | 1.12x |

## Work avoided, not just faster arithmetic

In the rank-7/bound-2 self-dual enumeration, full matrix completions fall from
7,547,312 (both original and v1) to 62,782 (v2), about 120 times fewer. The output
remains exactly 212 self-dual classes. Rank-8/bound-1 self-dual completions fall
from 98,631 to 3,529, with the same 38 classes. This work-count reduction is not
itself a wall-clock speedup: witness construction and support masks also cost
time. The measured times above include that cost.

The more aggressive three-edge mask experiment and several alternative search
strategies were slower and are excluded. No rank-specific pruning rule was
introduced to obtain these measurements.

## Reproduce

From the extracted package root:

```bash
python3 scripts/benchmark.py --threads 1 --repeats 3 --work benchmark_t1
python3 scripts/benchmark.py --threads 4 --repeats 3 --work benchmark_t4
python3 scripts/benchmark.py --threads 1 --repeats 3 --seconds 120 --cases sd6m3 ns7p1m3 --work benchmark_extra
```

The higher-bound original component took roughly 90 seconds per repetition on
this host; use a larger `--seconds` on a slower laptop. The default short suite
uses a 60-second limit per stratum. A timeout is marked incomplete and never
reported as a completed census. First-run compilation is excluded from all
reported enumeration timings.

Raw commands, individual timings, logs, outputs, and source hashes are under
`benchmarks/evidence/threads1/`, `threads4/`, and `higher_bound/`.
The script includes unmodified original and v1 kernels under
`benchmarks/reference/`, so no checkout or network access is needed.
To additionally compare with an existing upstream checkout's released parameter
sets, supply `--released-root /path/to/fusion-ring-census` as done for this report.

## Independent validation

The actual launcher completed and independently verified these whole ranks:

| Rank | Bound | Distinct classes | Exact released parameter-set match |
|---:|---:|---:|---|
| 6 | 3 | 577 | Yes |
| 7 | 2 | 362 | Yes |
| 8 | 1 | 96 | Yes |

The unchanged tensor verifier checks unit, duality, Frobenius reciprocity, every
integer associativity identity, and canonicalization under every unit-fixing
permutation. Its raw results are in `benchmarks/evidence/whole_rank/`.
Launcher/packaging regression tests also passed (6 tests).

The independent general-solver audits checked 30,000 full-propagation systems,
20,000 exact three-variable supports, and two Gaussian suites (12,000 and 5,000
systems). The exhaustive domain checks retained every satisfying assignment.
Self-dual audits checked 429,341 row masks, 61,080 bounded-witness completions,
60,120 joint pair masks, and 101,320 rollback operations, plus 100,000 direct
associativity identity tests. Sanitizers and forced resource-cap fallbacks also
passed. Full details and runnable audit sources accompany the code.

These tests and preservation arguments give substantial evidence, but are not
a formal verification of the entire software. No complete rank-7/bound-5 or
rank-8/bound-3 run was performed, and these speedups do not predict their
completion times. Timings are from this host, not from the user's laptop.

The standalone archive was also extracted into a fresh directory without build
products. Its checksum-validated launcher compiled from source and completed
rank 7 through bound 1 with two threads: 43 independently verified classes.
`benchmarks/evidence/clean_extraction/` records that packaging check.
