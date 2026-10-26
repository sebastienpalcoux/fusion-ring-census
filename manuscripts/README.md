# Mathematical companions

Each companion gives definitions, a rank-specific coverage argument, exact counts, independent verification and reproduction commands. They are computational research notes, not claims of journal publication.

| Rank | Complete through | Classes | Read |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | [PDF](rank3.pdf) · [LaTeX](rank3.tex) |
| 4 | 128 | 889,530 | [PDF](rank4.pdf) · [LaTeX](rank4.tex) |
| 5 | 20 | 40,999 | [PDF](rank5.pdf) · [LaTeX](rank5.tex) |
| 6 | 9 | 25,421 | [PDF](rank6.pdf) · [LaTeX](rank6.tex) |
| 7 | 5 | 10,006 | [PDF](rank7.pdf) · [LaTeX](rank7.tex) |
| 8 | 3 | 4,500 | [PDF](rank8.pdf) · [LaTeX](rank8.tex) |
| 9 | 2 | 2,225 | [PDF](rank9.pdf) · [LaTeX](rank9.tex) |
| 10 | 1 | 194 | [PDF](rank10.pdf) · [LaTeX](rank10.tex) |
| 11 | 1 | 182 | [PDF](rank11.pdf) · [LaTeX](rank11.tex) |
| 12 | 1 | 632 | [PDF](rank12.pdf) · [LaTeX](rank12.tex) |

Rank-7 completeness through multiplicity 5 is producer-reported; the new tensors and their uniqueness were independently verified. The complete optimized source is now supplied and hash-matched; full searches at rank 7 through 5 and rank 8 through 3 were not independently rerun. See [the qualification](../verification/rank7/README.md).

Rank nine at exact multiplicity two has 2,043 general exclusions, 36 unitary models and four unresolved cases; its multiplicity-one conclusions are unchanged.

Ranks 9–11 have complete supplied sources and producer completion records, with independent exact tensor and uniqueness checks. Full enumeration was not independently repeated. The rank-10 companion links the current 136 exclusions and 58 unitary models, completing multiplicity one; R10_1_189 comes from a classical conformal embedding, with exact proofs in the classification repository. The rank-11 companion links the separate classification of all 182 inputs: 155 exclusions and 27 unitary models.

Rebuild with `python3 scripts/build_manuscripts.py --compile`, or select one companion with `--ranks 6 --compile`. Counts and the displayed release date are read from the same manifest as the repository front page.

The [25 October correctness audit](../verification/audit_20261025/README.md) validates every supplied tensor and its based-isomorphism class. The companion incorporates proof and replay repairs without changing the classification.

Rank twelve adds 632 rings, with 480 general exclusions and 152 categorical models in the companion. Exactly 151 models are known unitary; R12_1_623 is complex/pseudo-unitary with unitarity unproved. [Source, exact checks and qualification](../verification/rank12/README.md).
