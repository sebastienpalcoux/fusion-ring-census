# Rank 8 through multiplicity 3

The supplied archive contains **4,500** based fusion rings: **96**, **877** and
**3,527** at exact multiplicities 1, 2 and 3. In the new band the counts by
0, 1, 2 and 3 nontrivial dual pairs are 2,152, 972, 362 and 41; 85 are noncommutative.

Fresh independent verification checks every tensor axiom and all **22,680,000**
unit-fixing permutations, with no duplicates. Parameter re-export is byte-identical.
The full previous 973-record tensor and parameter sequences are recovered by
filtering to multiplicity at most two. New records are interleaved in the sorted
file; this is not a literal contiguous prefix. See [audit.json](audit.json),
[integration_check.json](integration_check.json), [fresh verification](fresh_verification/summary.json),
[previous release](previous_M2/) and [line map](previous_M2_line_map.json).

The [producer run](run.json) reports completion of all four strata in 62,292
seconds, including 61,908 seconds for the self-dual stratum. These are producer
timings. The complete optimized source archive is supplied, and its aggregate
code hash matches this run and the rank-7 multiplicity-5 run. Its numerical C++
sources are integrated unchanged. [Finite audits](../optimization_20261021/README.md)
check the optimized pruning and bounded baseline agreement.

**Completeness is producer-reported.** This release independently verifies
validity and uniqueness, but does not rerun the full exhaustive search. The
manifest's `complete: true` retains that producer report; its explicit
`completeness_basis` and `independent_enumeration_rerun: false` record the limit.
The supplied verifier output is preserved separately in [producer_verification](producer_verification/).
