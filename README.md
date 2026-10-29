# Fusion Ring Census

**Exact enumeration of based fusion rings at ranks 3–12.**

[**Browse the counts →**](results/table.md) · [Datasets](#datasets) · [Run & verify](docs/REPRODUCIBILITY.md) · [Methods](methods/completeness.md)

**1,434,042 based-isomorphism classes** in the released datasets, including every duality type and noncommutative rings. Categorifiability is recorded separately in the companion [Grothendieck Ring Classification](https://github.com/sebastienpalcoux/grothendieck-ring-classification) and its [interactive atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/).

> **AI-generated research · independent verification pending.** Automated checks establish only their stated scope. [Provenance and verification](docs/PROVENANCE.md).

**Current companion classification.** R8_3_1768 is excluded over the complex numbers by pivotal conjugation parity, using the established sphericalization/Galois reduction and six exact separation certificates. **Six cases remain unresolved: two at rank six, three at rank eight and one at rank nine.** No new model is claimed. Census data and counts are unchanged. [Unified proofs and exact replay](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md) · [Current classification snapshot](verification/classification.json).

Rank twelve at multiplicity one contains 632 rings: 480 general exclusions and 152 modeled rings, with none unresolved. Exactly 151 models are known unitary; R12_1_623 is complex/pseudo-unitary with unitarity unproved. [Source and exact checks](verification/rank12/README.md).

<a id="complete-datasets"></a>

## Datasets

Bounds are cumulative: all rings of multiplicity **at most M**.

| Rank | Complete through | Classes in total | Data | Companion / evidence |
|---:|---:|---:|---|---|
| 3 | 1,000 | 460,353 | [Tensors](results/rank3/tables.txt.gz) · [Counts](results/rank3/counts.csv) | [PDF](manuscripts/rank3.pdf) · [TeX](manuscripts/rank3.tex) |
| 4 | 128 | 889,530 | [Tensors](results/rank4/tables.txt.gz) · [Counts](results/rank4/counts.csv) | [PDF](manuscripts/rank4.pdf) · [TeX](manuscripts/rank4.tex) |
| 5 | 20 | 40,999 | [Tensors](results/rank5/tables.txt.gz) · [Counts](results/rank5/counts.csv) | [PDF](manuscripts/rank5.pdf) · [TeX](manuscripts/rank5.tex) |
| 6 | 9 | 25,421 | [Tensors](results/rank6/tables.txt.gz) · [Counts](results/rank6/counts.csv) | [PDF](manuscripts/rank6.pdf) · [TeX](manuscripts/rank6.tex) |
| 7 | 5 | 10,006 | [Tensors](results/rank7/tables.txt.gz) · [Counts](results/rank7/counts.csv) | [PDF](manuscripts/rank7.pdf) · [TeX](manuscripts/rank7.tex) |
| 8 | 3 | 4,500 | [Tensors](results/rank8/tables.txt.gz) · [Counts](results/rank8/counts.csv) | [PDF](manuscripts/rank8.pdf) · [TeX](manuscripts/rank8.tex) |
| 9 | 2 | 2,225 | [Tensors](results/rank9/tables.txt.gz) · [Counts](results/rank9/counts.csv) | [PDF](manuscripts/rank9.pdf) · [TeX](manuscripts/rank9.tex) |
| 10 | 1 | 194 | [Tensors](results/rank10/tables.txt.gz) · [Counts](results/rank10/counts.csv) | [PDF](manuscripts/rank10.pdf) · [TeX](manuscripts/rank10.tex) |
| 11 | 1 | 182 | [Tensors](results/rank11/tables.txt.gz) · [Counts](results/rank11/counts.csv) | [PDF](manuscripts/rank11.pdf) · [TeX](manuscripts/rank11.tex) |
| 12 | 1 | 632 | [Tensors](results/rank12/tables.txt.gz) · [Counts](results/rank12/counts.csv) | [PDF](manuscripts/rank12.pdf) · [TeX](manuscripts/rank12.tex) |

The newly supplied ranks 9–12 passed fresh exact tensor and uniqueness checks. Enumeration completeness is producer-reported, with all strata completed and the complete source supplied; the full searches were not independently rerun. The same qualification applies to rank 7 through 5 and rank 8 through 3. [Verification by rank](verification/README.md).

<details id="counts-by-rank-and-multiplicity">
<summary><strong>Counts at each exact multiplicity</strong></summary>

Each entry counts classes at **exactly** the stated multiplicity. A dash means not completely enumerated.

[Full count table](results/table.md) · [CSV](results/counts.csv) · [Interactive table](docs/index.html) · [Definitions and scope](docs/PROJECT_GUIDE.md#counts-by-rank-and-multiplicity)

</details>

<a id="reproduce-a-census"></a>

## Reproduce and explore

```bash
python3 scripts/run_laptop.py --rank 11 --bound 1
```

The local launcher has no clock limit. [Installation, supported bounds and verification](docs/REPRODUCIBILITY.md). A census is complete only after every stratum finishes and the output passes verification.

<a id="read-and-reuse"></a>

| Resource | Contents |
|---|---|
| Mathematics | [Ten rank-specific companions](manuscripts/README.md) · [High-rank methods](methods/COMPACT_SYMMETRY.md) |
| Evidence | [Verification records](verification/README.md) · [Source update](verification/engine_20261023/README.md) |
| Categorification | [Current classification and open cases](https://github.com/sebastienpalcoux/grothendieck-ring-classification) |
| Project details | [Definitions and project guide](docs/PROJECT_GUIDE.md) |
| Reuse | [Cite](CITATION.cff) · [Licensing](NOTICE.md) · [OEIS drafts](oeis/README.md) |

Sébastien Palcoux · BIMSA · [Current project announcement · PDF](announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf) · [Hexagon](https://hexagonmath.org/2610.00300) · [How to cite](https://sebastienpalcoux.github.io/grothendieck-ring-classification/#cite)
