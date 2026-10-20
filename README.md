# Fusion Ring Census

**Exact enumeration of based fusion rings, at ranks 3–8.**

[Data](#complete-datasets) · [Manuscripts](manuscripts/README.md) · [Run & verify](docs/REPRODUCIBILITY.md) · [OEIS](oeis/README.md) · [Evidence](verification/README.md)

1,427,282 distinct classes in the released datasets. Every duality
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

At rank eight, the classification through multiplicity two comprises **896
exclusions and 77 unitary models**. The inner-square rigidity argument excludes
`R8_2_24` over the complex numbers. The general questions `R6_4_155` and
`R6_8_1660` remain open; see the [current classification account](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/docs/RESEARCH_STATUS.md)
for the precise proof scope and necessary constraints.

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
| 3 | 4 | 24 | 82 | 384 | 1,059 | — |
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

[Full table through multiplicity 1000](results/table.md) · [Download CSV](results/counts.csv) · [Offline interactive table](docs/index.html)

Download `docs/index.html` and open it in a browser to filter the interactive table.

## Complete datasets

Bounds and totals below are cumulative: all rings of multiplicity **at most M**.

**Rank 7 through 5:** the producer reports a completed exhaustive run. Fresh
checks certify all 10,006 tensors and their uniqueness, including 5,805 new
exact-multiplicity-5 classes. The modified enumeration source was not included
in the supplied archive, so completeness has not been independently reproduced.
See [the source qualification](verification/rank7/README.md).

| Rank | Complete through | Classes in total | Data | Companion |
|---:|---:|---:|---|---|
| 3 | 1,000 | 460,353 | [Tensors](results/rank3/tables.txt.gz) · [Counts](results/rank3/counts.csv) | [PDF](manuscripts/rank3.pdf) · [TeX](manuscripts/rank3.tex) |
| 4 | 128 | 889,530 | [Tensors](results/rank4/tables.txt.gz) · [Counts](results/rank4/counts.csv) | [PDF](manuscripts/rank4.pdf) · [TeX](manuscripts/rank4.tex) |
| 5 | 20 | 40,999 | [Tensors](results/rank5/tables.txt.gz) · [Counts](results/rank5/counts.csv) | [PDF](manuscripts/rank5.pdf) · [TeX](manuscripts/rank5.tex) |
| 6 | 9 | 25,421 | [Tensors](results/rank6/tables.txt.gz) · [Counts](results/rank6/counts.csv) | [PDF](manuscripts/rank6.pdf) · [TeX](manuscripts/rank6.tex) |
| 7 | 5 | 10,006 | [Tensors](results/rank7/tables.txt.gz) · [Counts](results/rank7/counts.csv) | [PDF](manuscripts/rank7.pdf) · [TeX](manuscripts/rank7.tex) |
| 8 | 2 | 973 | [Tensors](results/rank8/tables.txt.gz) · [Counts](results/rank8/counts.csv) | [PDF](manuscripts/rank8.pdf) · [TeX](manuscripts/rank8.tex) |

Each tensor uses basis unit 0 and ordered coefficients `N[i][j][k]`. Data are
gzip-compressed, with one full tensor per line. The [manifest](results/census.json)
records exact counts, checksums and evidence links. Rank 3 stops at 1000.

## Reproduce a census

Python 3.9+ and GNU g++ with C++17/OpenMP are sufficient. On your own computer:

```bash
python3 scripts/run_laptop.py --rank 7 --bound 5
```

The local launcher has no clock limit. It includes every duality type and creates
a result ZIP only after independent tensor verification, isomorphism checking and
agreement with the released count prefix. [Installation and all rank limits →](docs/REPRODUCIBILITY.md)

A search is complete only when every stratum finishes. The verifier establishes
validity and uniqueness; [coverage arguments](methods/completeness.md) establish
why the search is exhaustive. Interrupted output never supplies census terms.

## Read and reuse

The six [mathematical companions](manuscripts/README.md) explain the definitions,
rank-specific methods and complete counts. These are censuses of **based rings**;
they do not classify their categorifications.

The [source audit](audit/README.md) corrects 3,313 redundant records in the
Vercleyen–Slingerland ancillary database. Its attribution and deletion witnesses
are retained. The [OEIS folder](oeis/README.md) contains proposed data and edits;
no online submission is implied.

Sébastien Palcoux · BIMSA · [Cite](CITATION.cff) · [Attribution & licensing](NOTICE.md) · [Contribute](CONTRIBUTING.md)

Repository access is public. [Provenance and verification](docs/PROVENANCE.md)
explain the current release, AI assistance and the limits of computational evidence.
