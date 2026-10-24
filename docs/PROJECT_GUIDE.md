# Fusion Ring Census · project guide

Current datasets extend through rank 11 at multiplicity one. See the [current manifest](../results/census.json), [count table](../results/table.md) and [source update](../verification/engine_20261023/README.md). The detailed historical notes below are retained.

[Repository front page](../README.md) · [Interactive atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)

**Exact enumeration of based fusion rings, at ranks 3–8.**

[Data](#complete-datasets) · [Manuscripts](../manuscripts/README.md) · [Run & verify](../docs/REPRODUCIBILITY.md) · [OEIS](../oeis/README.md) · [Evidence](../verification/README.md)

1,430,809 distinct classes in the released datasets. Every duality
type is included, including noncommutative rings. No categorifiability filter.

**Companion repository:** [Grothendieck Ring Classification](https://github.com/sebastienpalcoux/grothendieck-ring-classification)
classifies which fusion rings admit categorifications over ℂ and records
categorical realizations, proof manuscripts and per-band decisions;
its [visual atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
offers the same distinction interactively. Both are public. The census counts
below include fusion rings that have been excluded from categorification or
remain unresolved.

**Project announcement:** [Hexagon · 2610.00300v1](https://hexagonmath.org/2610.00300?version=1).

The classification project proves that exactly **15 rank-four Grothendieck rings**
are categorifiable over the complex numbers, with **no multiplicity restriction**;
every such category admits a spherical structure. Its unrestricted proof uses
a theoretical dimension bound followed by exact finite certification. For the
pivotal case, see Jingcheng Dong, Sébastien Palcoux and Arnaud Plessis,
[*Classifying Grothendieck rings of pivotal fusion categories of rank four*](https://arxiv.org/abs/2609.33272).

At rank eight, the exact-multiplicity-three band has **3,506 general
exclusions, 16 unitary models and 5 unresolved categorification candidates**
among its 3,527 supplied rings. Together with the earlier 896 exclusions and
77 unitary models through multiplicity two, this gives **4,402 general
exclusions, 93 unitary models and 5 unresolved rings** among 4,500 supplied
rank-eight rings. The candidates are not asserted fusion categories or
established exotic examples. The general questions `R6_4_155` and
`R6_8_1660` also remain open; see the [current classification account](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/docs/RESEARCH_STATUS.md)
for the precise proof scope and individual attempt records.
These counts are bound to the [classification main snapshot `d22bdcf3`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/d22bdcf3f97b7d6991362a417e25172fda4c8a8a) and its [checksummed decision-ledger payload](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/data/payloads/supplements__rank8__output__audited_20261024__ledger_json).
The known unitary construction `R8_3_982` is the triality-zero component of the exceptional E21 chiral fusion category from the conformal embedding SU(3) at level 21 into E7 at level 1. The [exact model proof](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/evidence/rank8_creative_20261022/r982/E21_MODEL.md) reconstructs the known 24-object fusion category from its fundamental graph and matches all 512 neutral fusion coefficients exactly. It also realizes both previously necessary nonregular based-module types. This is a known construction with a new exact census identification.

The general exclusion of `R8_3_65` uses pointed-induction phases and integral Fourier fibers; [six exact certificates](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/evidence/rank8_research_20261022/r65/PROOF.md) cover every pointed associator class.

The new general exclusion of `R8_3_1795` uses finite integer packing of the two pointed twist fibers; [sixteen exact indicator branches](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/evidence/rank8_research_20261022/pointed_followup/PROOF.md) exclude both pointed associator classes.

For the four cases R928, R941, R1154 and R1768, every categorification admits a spherical structure and has a pseudo-unitary Galois conjugate, and no braided Morita representative exists. These reductions are not asserted for the additional general-open R436 case. Further [structural results](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/manuscripts/rank8/paper/m3_research_20261022.tex) restrict module actions and distinguish possible centers. The [followup restrictions](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/manuscripts/rank8/paper/m3_pointed_followup.tex) force the nontrivial pointed associator for `R8_3_1768` and constrain additional twist-one central simples. These necessary restrictions alone supply no categorification.

The [new unified restrictions](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/manuscripts/rank8/paper/m3_creative_20261022.tex) control twists by saturated dimension characters, restrict the irrational dimension-ratio sector of `R8_3_1768`, reconstruct a forced four-object semionic packet for `R8_3_1154`, and record earlier conditional Morita-dual restrictions for `R8_3_3472`. For `R8_3_928`, exact integer phase multiplicities and binary-branch Farkas certificates reduce ten rationally feasible phase patterns to four with integer phase witnesses; the rotation auxiliaries and spectral-mixture parameters remain relaxed. They also give a cyclic-stabilizer divisibility obstruction to two direct near-group quotient constructions.

The general complex exclusion of `R8_3_3472`, established on 22 October 2026, supersedes the earlier focused research restrictions. Sphericalization and Galois transport reduce any hypothetical complex categorification to the pseudo-unitary case. Exact center induction and modular identities exclude all but one orbit of low center frames. For that orbit, complete Galois twist orbits and cyclic-rotation indicator identities force a system of 628 equations in 572 integer variables. A certificate of 1,648 exact integer-bound deductions followed by a rational separating inequality proves this system impossible. The [complete proof and exact certificates](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/evidence/r3472_exclusion_20261022) include two portable exact checkers and an independently checked VIPR infeasibility certificate. Earlier feasible center relaxations imposed fewer conditions and therefore do not contradict this exclusion. The census tensors, enumeration results and completeness qualifications are unchanged.

The five rank-eight cases `R8_3_436`, `R8_3_928`, `R8_3_941`, `R8_3_1154`, `R8_3_1768` remain unresolved; the feasible necessary data are not category models.

The general exclusion of `R8_3_436` is withheld after a source-scope audit; its unitary exclusion remains supported. See [audit correction](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/evidence/audit_20261024/README.md). Together with `R6_4_155` and `R6_8_1660`, seven cases are open at ranks at most eight. Higher-rank questions are counted in the companion atlas; this is not a project-wide total. The known model `R8_3_721` is the Morita dual of the inherited Q-system `1 + rho` in the `C2` de-equivariantization of the known unitary `C8` generalized-Haagerup category. The [construction proof](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/d22bdcf3f97b7d6991362a417e25172fda4c8a8a/evidence/rank8_next_20261021/r721/r721_qsystem_model.tex) includes an exact fusion-coefficient bound and identification across all 4,500 supplied rank-eight tensors. Historical verification at [snapshot `95f38175`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/95f38175256ba852b6634f88a055b674e920f941): the 108-check canonical normal replay passed; all 8 center checks passed in normal and optimized Python. At that checkpoint, optimized core and extracted-package full replays were pending.

At rank seven through multiplicity five, the companion classification resolves
all **10,006 supplied tensors: 9,976 general exclusions, 30 known unitary models
and no unresolved rings**. The new exact-multiplicity-five band has **5,804
general exclusions, 1 known model and no unresolved rings**. Its known model `R7_5_5678` is
`Rep(C7 ⋊ C6) = Rep(AGL(1,7))`.
The classification includes fifteen further exclusions certified on 20 October
2026. Coupled cyclic rotations, all-order phase packets and integral fusion-norm
inequalities exclude both
[`R7_5_3895`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/rank7_m5_20261020/models/sqrt5/R3895_CYCLIC_CHAIN.md) and
[`R7_5_5039`](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/rank7_m5_20261020/models/sqrt5/R5039_CYCLIC_CHAIN.md)
over the complex numbers, with complete exact replay certificates. The census tensors and
enumeration-completeness qualification are unchanged.

**Extended Haagerup at rank six.** The census includes the Grothendieck ring of
EH1, of rank 6 and fusion multiplicity 7. For the fusion categories and their
fusion rules, see P. Grossman, S. Morrison, D. Penneys, E. Peters and N. Snyder,
[*The Extended Haagerup fusion categories*](https://doi.org/10.24033/asens.2541),
*Annales Scientifiques de l'École Normale Supérieure* (4) **56** (2023), no. 2,
589–664 ([arXiv:1810.06076](https://arxiv.org/abs/1810.06076)). The original
construction is S. Bigelow, S. Morrison, E. Peters and N. Snyder,
[*Constructing the extended Haagerup planar algebra*](https://doi.org/10.1007/s11511-012-0081-7),
*Acta Mathematica* **209** (2012), no. 1, 29–82.

> **AI-generated research · independent verification pending.** Independent human verification and Lean formalization are pending. Treat the results and data with caution: automated checks establish only their stated scope.

## Counts by rank and multiplicity

Each entry is **the number of based-isomorphism classes at exactly multiplicity
m**. A dash means *not yet completely enumerated*, never zero.

| Multiplicity | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 10 | 16 | 39 | 43 | 96 |
| 2 | 3 | 17 | 37 | 154 | 319 | 877 |
| 3 | 4 | 24 | 82 | 384 | 1,059 | 3,527 |
| 4 | 6 | 45 | 134 | 872 | 2,780 | — |
| 5 | 5 | 55 | 209 | 1,582 | 5,805 | — |
| 6 | 9 | 81 | 336 | 2,768 | — | — |
| 7 | 6 | 92 | 477 | 3,814 | — | — |
| 8 | 10 | 137 | 733 | 6,999 | — | — |
| 9 | 12 | 151 | 863 | 8,809 | — | — |
| 10 | 9 | 186 | 1,082 | — | — | — |
| 11 | 10 | 238 | 1,383 | — | — | — |
| 12 | 20 | 291 | 1,948 | — | — | — |
| 13 | 9 | 246 | 2,211 | — | — | — |
| 14 | 13 | 340 | 2,554 | — | — | — |
| 15 | 16 | 349 | 2,936 | — | — | — |
| 16 | 25 | 525 | 4,157 | — | — | — |
| 17 | 11 | 424 | 4,255 | — | — | — |
| 18 | 18 | 477 | 5,080 | — | — | — |
| 19 | 20 | 513 | 5,640 | — | — | — |
| 20 | 22 | 713 | 6,866 | — | — | — |

<details>
<summary><strong>Multiplicities 21–128 · ranks 3 and 4</strong></summary>

| Multiplicity | Rank 3 | Rank 4 |
|---:|---:|---:|
| 21 | 24 | 704 |
| 22 | 12 | 668 |
| 23 | 22 | 654 |
| 24 | 44 | 1,121 |
| 25 | 19 | 868 |
| 26 | 28 | 938 |
| 27 | 20 | 989 |
| 28 | 22 | 1,286 |
| 29 | 25 | 1,356 |
| 30 | 42 | 1,347 |
| 31 | 24 | 1,220 |
| 32 | 40 | 1,671 |
| 33 | 36 | 1,460 |
| 34 | 30 | 1,579 |
| 35 | 24 | 1,613 |
| 36 | 55 | 2,301 |
| 37 | 33 | 1,646 |
| 38 | 16 | 1,824 |
| 39 | 36 | 2,111 |
| 40 | 58 | 2,653 |
| 41 | 29 | 2,131 |
| 42 | 48 | 2,588 |
| 43 | 34 | 2,169 |
| 44 | 52 | 2,857 |
| 45 | 48 | 2,699 |
| 46 | 34 | 2,639 |
| 47 | 38 | 2,452 |
| 48 | 82 | 3,985 |
| 49 | 46 | 2,947 |
| 50 | 25 | 3,314 |
| 51 | 58 | 3,378 |
| 52 | 28 | 3,776 |
| 53 | 39 | 3,250 |
| 54 | 74 | 3,704 |
| 55 | 40 | 3,785 |
| 56 | 80 | 5,213 |
| 57 | 40 | 4,182 |
| 58 | 47 | 3,863 |
| 59 | 54 | 3,987 |
| 60 | 95 | 6,004 |
| 61 | 61 | 4,383 |
| 62 | 39 | 4,472 |
| 63 | 48 | 5,150 |
| 64 | 75 | 6,557 |
| 65 | 62 | 5,107 |
| 66 | 78 | 5,773 |
| 67 | 50 | 4,791 |
| 68 | 60 | 6,260 |
| 69 | 50 | 6,001 |
| 70 | 64 | 6,205 |
| 71 | 58 | 5,799 |
| 72 | 142 | 8,710 |
| 73 | 51 | 5,858 |
| 74 | 39 | 6,223 |
| 75 | 88 | 7,280 |
| 76 | 68 | 9,507 |
| 77 | 50 | 6,953 |
| 78 | 76 | 7,917 |
| 79 | 60 | 6,933 |
| 80 | 96 | 10,208 |
| 81 | 68 | 8,031 |
| 82 | 56 | 7,939 |
| 83 | 68 | 7,408 |
| 84 | 156 | 10,993 |
| 85 | 58 | 8,464 |
| 86 | 84 | 8,568 |
| 87 | 80 | 9,088 |
| 88 | 86 | 11,767 |
| 89 | 91 | 9,145 |
| 90 | 90 | 10,765 |
| 91 | 72 | 9,896 |
| 92 | 69 | 11,188 |
| 93 | 74 | 10,385 |
| 94 | 80 | 10,153 |
| 95 | 78 | 10,048 |
| 96 | 212 | 15,447 |
| 97 | 65 | 10,003 |
| 98 | 64 | 11,249 |
| 99 | 104 | 12,082 |
| 100 | 111 | 14,037 |
| 101 | 75 | 11,361 |
| 102 | 68 | 13,068 |
| 103 | 76 | 10,861 |
| 104 | 118 | 16,150 |
| 105 | 118 | 14,958 |
| 106 | 75 | 12,338 |
| 107 | 76 | 12,102 |
| 108 | 72 | 16,509 |
| 109 | 87 | 12,849 |
| 110 | 119 | 14,390 |
| 111 | 128 | 15,119 |
| 112 | 134 | 18,964 |
| 113 | 87 | 13,293 |
| 114 | 169 | 16,769 |
| 115 | 70 | 14,900 |
| 116 | 72 | 17,484 |
| 117 | 126 | 16,252 |
| 118 | 70 | 14,963 |
| 119 | 86 | 16,058 |
| 120 | 272 | 25,126 |
| 121 | 110 | 16,103 |
| 122 | 95 | 15,670 |
| 123 | 106 | 17,292 |
| 124 | 124 | 19,682 |
| 125 | 103 | 17,760 |
| 126 | 140 | 20,720 |
| 127 | 94 | 17,015 |
| 128 | 156 | 23,185 |

</details>

[Full table through multiplicity 1000](../results/table.md) · [Download CSV](../results/counts.csv) · [Offline interactive table](../docs/index.html)

Download `docs/index.html` and open it in a browser to filter the interactive table.

## Complete datasets

Bounds and totals below are cumulative: all rings of multiplicity **at most M**.

**Rank 7 through 5:** the producer reports a completed exhaustive run. Fresh
checks certify all 10,006 tensors and their uniqueness, including 5,805 new
exact-multiplicity-5 classes. The complete optimized source was subsequently
supplied and its hash matches the producer run; full enumeration has not been
independently reproduced. Rank 8 through 3 contains 4,500 checked tensors,
including 3,527 new exact-multiplicity-3 classes, with the same qualification.
See [the source qualification](../verification/rank7/README.md).

| Rank | Complete through | Classes in total | Data | Companion |
|---:|---:|---:|---|---|
| 3 | 1,000 | 460,353 | [Tensors](../results/rank3/tables.txt.gz) · [Counts](../results/rank3/counts.csv) | [PDF](../manuscripts/rank3.pdf) · [TeX](../manuscripts/rank3.tex) |
| 4 | 128 | 889,530 | [Tensors](../results/rank4/tables.txt.gz) · [Counts](../results/rank4/counts.csv) | [PDF](../manuscripts/rank4.pdf) · [TeX](../manuscripts/rank4.tex) |
| 5 | 20 | 40,999 | [Tensors](../results/rank5/tables.txt.gz) · [Counts](../results/rank5/counts.csv) | [PDF](../manuscripts/rank5.pdf) · [TeX](../manuscripts/rank5.tex) |
| 6 | 9 | 25,421 | [Tensors](../results/rank6/tables.txt.gz) · [Counts](../results/rank6/counts.csv) | [PDF](../manuscripts/rank6.pdf) · [TeX](../manuscripts/rank6.tex) |
| 7 | 5 | 10,006 | [Tensors](../results/rank7/tables.txt.gz) · [Counts](../results/rank7/counts.csv) | [PDF](../manuscripts/rank7.pdf) · [TeX](../manuscripts/rank7.tex) |
| 8 | 3 | 4,500 | [Tensors](../results/rank8/tables.txt.gz) · [Counts](../results/rank8/counts.csv) | [PDF](../manuscripts/rank8.pdf) · [TeX](../manuscripts/rank8.tex) |

Each tensor uses basis unit 0 and ordered coefficients `N[i][j][k]`. Data are
gzip-compressed, with one full tensor per line. The [manifest](../results/census.json)
records exact counts, checksums and evidence links. Rank 3 stops at 1000.

## Reproduce a census

Python 3.9+ and GNU g++ with C++17/OpenMP are sufficient. On your own computer:

```bash
python3 scripts/run_laptop.py --rank 7 --bound 5
```

The local launcher has no clock limit. It includes every duality type and creates
a result ZIP only after independent tensor verification, isomorphism checking and
agreement with the released count prefix. [Installation and all rank limits →](../docs/REPRODUCIBILITY.md)

A search is complete only when every stratum finishes. The verifier establishes
validity and uniqueness; [coverage arguments](../methods/completeness.md) establish
why the search is exhaustive. Interrupted output never supplies census terms.

## Read and reuse

The six [mathematical companions](../manuscripts/README.md) explain the definitions,
rank-specific methods and complete counts. These are censuses of **based rings**;
they do not classify their categorifications.

The [source audit](../audit/README.md) corrects 3,313 redundant records in the
Vercleyen–Slingerland ancillary database. Its attribution and deletion witnesses
are retained. The [OEIS folder](../oeis/README.md) contains proposed data and edits;
no online submission is implied.

Sébastien Palcoux · BIMSA · [Cite](../CITATION.cff) · [Attribution & licensing](../NOTICE.md) · [Contribute](../CONTRIBUTING.md)

Repository access is public. [Provenance and verification](../docs/PROVENANCE.md)
explain the current release, AI assistance and the limits of computational evidence.

