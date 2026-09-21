# Verification evidence

[Data](../results/README.md) · [Coverage arguments](../methods/completeness.md) · [Provenance](../docs/PROVENANCE.md)

Every released census covers the entire rank, including every duality type.
Completeness uses the exhaustive search arguments and completed enumeration;
independent tensor checks establish validity and uniqueness.

| Rank | Complete through | Classes | Evidence |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | [Independent audit](rank3/audit.json) · [Source](rank3/source.json) |
| 4 | 128 | 889,530 | [Independent audit](rank4/audit.json) · [Run log](rank4/logs/enumeration.log) · [Source](rank4/source.json) |
| 5 | 20 | 40,999 | [Fresh audit](rank5/audit.json) · [Completed run](rank5/run.json) · [Source](rank5/source.json) |
| 6 | 7 | 9,613 | [Fresh audit](rank6/audit.json) · [Completed run](rank6/run.json) · [Source](rank6/source.json) |
| 7 | 4 | 4,201 | [Fresh audit](rank7/audit.json) · [Completed run](rank7/run.json) · [Source](rank7/source.json) |
| 8 | 2 | 973 | [Fresh audit](rank8/audit.json) · [Completed run](rank8/run.json) · [Source](rank8/source.json) |

## What was checked

The rank-5–8 uploads were independently rechecked in
[GitHub audit 35553424461](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/35553424461),
at commit `b5e15383c75f46e1d00679a3815dc56e638f4a56`.
Every tensor passed the unit, duality, reciprocity and integer associativity tests.
Canonicalization examined every unit-fixing basis permutation: respectively
983,976; 1,153,560; 3,024,720; and 4,903,920 permutations. All four lists have
zero duplicate isomorphism classes and agree with every previously released count.
The source code hash and both decompressed data hashes were checked.
[The audit environment](audit_environment.json) is retained.

Ranks 5, 7 and 8 extend the preceding release. Rank 6 reproduces its existing
bound-7 result: its decompressed tensors and parameter file are identical. Each
rank directory retains the laptop commands, environment, phase timings, source
receipt and nonempty subprocess logs. Original absolute laptop paths in run logs
are historical evidence, not commands to use on another machine.

Ranks 3 and 4 retain their prior full independent audits and unchanged tensor
hashes; they were not re-enumerated. The rank-4 audit jointly checked 889,530
released tensors and 2,787 reference records. Its raw comparison therefore reports
2,787 repetitions, all from the reference suffix; the released enumeration itself
has **zero duplicates**. The raw comparison and containment witnesses are retained
under [rank4/reference_comparison](rank4/reference_comparison/).

## Evidence without duplicate releases

The manifest points to one current dataset per rank. Original supplied payloads,
identity line maps and superseded campaigns remain recoverable at
[the audit revision](https://github.com/sebastienpalcoux/fusion-ring-census/tree/b5e15383c75f46e1d00679a3815dc56e638f4a56/verification)
and in Git history. Current evidence is kept here without second copies of the
tensor datasets. Historical [optimization regressions](regressions/) are explicitly
labelled and do not stand in for current-release checks.

[Repository checks](checks/) cover file integrity, documentation and lightweight
unit tests. They are separate from the mathematical audit above. Run the complete
checker on GitHub Actions or your own computer as described in
[reproduction](../docs/REPRODUCIBILITY.md).
