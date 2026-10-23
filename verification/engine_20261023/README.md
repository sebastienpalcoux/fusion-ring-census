# Optimized engine and high-rank datasets — 23 October 2026

The supplied v3 source extends the census engine to ranks **3–11**, including every duality type. The current multiplicity-one datasets contain **142**, **194**, and **182** rings at ranks **9**, **10**, and **11**.

[Fresh output verification](fresh_release_check.json) · [Integration receipt](integration.json) · [Exact supplied source package](../../packages/Fusion_Census_Deep_Optimized_rank11_2026-10-23.zip) · [Supplied validation report](VALIDATION_V3.md) · [Original source description](SOURCE.json)

The package inventory was verified before integration. Its numerical C++ sources are copied unchanged. Compact symmetry systems, sparse Boolean elimination, bounded-memory self-dual symmetry, rank-specific compilation and the exact refined verifier are included with their proofs, tests and finite audit programs. The wrapper retains the earlier local executable-cache repair for synced Ubuntu folders; this and documentation/test integration changes are recorded separately from the original package.

Fresh checks certify all **518** supplied rank-9–11 tensors, exact uniqueness, counts, hashes and complete parameter re-export. Every producer run records normal completion of all required strata, without a clock limit. Enumeration completeness remains producer-reported: these integration checks did not repeat the full enumeration.

The original package validation report predates the completed laptop rank-11 run. Its historical timed-out attempt is retained as provenance, while the current completed run is under [rank11](../rank11/README.md). The current result is 182 rings; the historical timeout supplies no count.

Run the engine from a checkout with:

```bash
python3 scripts/run_laptop.py --rank 11 --bound 1
```

Run output verification without enumerating with:

```bash
python3 scripts/check_release.py --full --ranks 9 10 11
```

The source regression suite is `python3 -m unittest discover -s tests -v`. Additional compiled pruning audits are separate from complete searches. Rank-11 categorification has not been assessed or added to the Grothendieck-ring classification.
