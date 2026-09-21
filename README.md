# Fusion Ring Census

**Exact enumeration of based fusion rings, at ranks 3–8.**

[Data](#complete-datasets) · [Manuscripts](manuscripts/README.md) · [Run & verify](docs/REPRODUCIBILITY.md) · [OEIS](oeis/README.md) · [Evidence](verification/README.md)

1,405,669 distinct classes in the certified datasets. Every duality
type is included, including noncommutative rings. No categorifiability filter.

## Counts by rank and multiplicity

Each entry is **the number of based-isomorphism classes at exactly multiplicity
m**. A dash means *not yet completely enumerated*, never zero.

| Multiplicity | Rank 3 | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4 | 10 | 16 | 39 | 43 | 96 |
| 2 | 3 | 17 | 37 | 154 | 319 | 877 |
| 3 | 4 | 24 | 82 | 384 | 1,059 | — |
| 4 | 6 | 45 | 134 | 872 | 2,780 | — |
| 5 | 5 | 55 | 209 | 1,582 | — | — |
| 6 | 9 | 81 | 336 | 2,768 | — | — |
| 7 | 6 | 92 | 477 | 3,814 | — | — |
| 8 | 10 | 137 | 733 | — | — | — |
| 9 | 12 | 151 | 863 | — | — | — |
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

| Rank | Complete through | Classes in total | Data | Companion |
|---:|---:|---:|---|---|
| 3 | 1,000 | 460,353 | [Tensors](results/rank3/tables.txt.gz) · [Counts](results/rank3/counts.csv) | [PDF](manuscripts/rank3.pdf) · [TeX](manuscripts/rank3.tex) |
| 4 | 128 | 889,530 | [Tensors](results/rank4/tables.txt.gz) · [Counts](results/rank4/counts.csv) | [PDF](manuscripts/rank4.pdf) · [TeX](manuscripts/rank4.tex) |
| 5 | 20 | 40,999 | [Tensors](results/rank5/tables.txt.gz) · [Counts](results/rank5/counts.csv) | [PDF](manuscripts/rank5.pdf) · [TeX](manuscripts/rank5.tex) |
| 6 | 7 | 9,613 | [Tensors](results/rank6/tables.txt.gz) · [Counts](results/rank6/counts.csv) | [PDF](manuscripts/rank6.pdf) · [TeX](manuscripts/rank6.tex) |
| 7 | 4 | 4,201 | [Tensors](results/rank7/tables.txt.gz) · [Counts](results/rank7/counts.csv) | [PDF](manuscripts/rank7.pdf) · [TeX](manuscripts/rank7.tex) |
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
