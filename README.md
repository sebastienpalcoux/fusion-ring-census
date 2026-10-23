# Fusion Ring Census

**Exact enumeration of based fusion rings at ranks 3–8.**

[**Browse the counts →**](results/table.md) · [Datasets](#datasets) · [Run & verify](docs/REPRODUCIBILITY.md) · [Manuscripts](manuscripts/README.md)

**1,430,809 based-isomorphism classes** in the released datasets, including all
duality types and noncommutative rings. Categorifiability is recorded in the
companion [Grothendieck Ring Classification](https://github.com/sebastienpalcoux/grothendieck-ring-classification)
and its [interactive atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/).

> **AI-generated research · independent verification pending.** Automated
> checks establish only their stated scope. [Provenance and verification](docs/PROVENANCE.md).

## Datasets

Bounds are cumulative: all rings of multiplicity **at most M**.

| Rank | Complete through | Classes in total | Data | Companion |
|---:|---:|---:|---|---|
| 3 | 1,000 | 460,353 | [Tensors](results/rank3/tables.txt.gz) · [Counts](results/rank3/counts.csv) | [PDF](manuscripts/rank3.pdf) · [TeX](manuscripts/rank3.tex) |
| 4 | 128 | 889,530 | [Tensors](results/rank4/tables.txt.gz) · [Counts](results/rank4/counts.csv) | [PDF](manuscripts/rank4.pdf) · [TeX](manuscripts/rank4.tex) |
| 5 | 20 | 40,999 | [Tensors](results/rank5/tables.txt.gz) · [Counts](results/rank5/counts.csv) | [PDF](manuscripts/rank5.pdf) · [TeX](manuscripts/rank5.tex) |
| 6 | 9 | 25,421 | [Tensors](results/rank6/tables.txt.gz) · [Counts](results/rank6/counts.csv) | [PDF](manuscripts/rank6.pdf) · [TeX](manuscripts/rank6.tex) |
| 7 | 5 | 10,006 | [Tensors](results/rank7/tables.txt.gz) · [Counts](results/rank7/counts.csv) | [PDF](manuscripts/rank7.pdf) · [TeX](manuscripts/rank7.tex) |
| 8 | 3 | 4,500 | [Tensors](results/rank8/tables.txt.gz) · [Counts](results/rank8/counts.csv) | [PDF](manuscripts/rank8.pdf) · [TeX](manuscripts/rank8.tex) |

Rank 7 through 5 and rank 8 through 3 have independent tensor and uniqueness
checks. Enumeration completeness relies on the producer's completion record;
the full searches have not been independently rerun. [Precise qualification](verification/rank7/README.md).

<details>
<summary><strong>Counts at each exact multiplicity</strong></summary>

Each entry in the [full table](results/table.md) counts based-isomorphism
classes at **exactly** the stated multiplicity. A dash means not completely
enumerated.

[Full count table](results/table.md) · [CSV](results/counts.csv) · [Interactive table](docs/index.html) · [Detailed tables and definitions](docs/PROJECT_GUIDE.md#counts-by-rank-and-multiplicity)

</details>

## Reproduce and explore

Run a census on your computer:

```bash
python3 scripts/run_laptop.py --rank 7 --bound 5
```

[Installation, rank limits and verification](docs/REPRODUCIBILITY.md).
A run is complete only after every stratum finishes.

| Resource | Contents |
|---|---|
| Mathematics | [Six rank-specific companions](manuscripts/README.md) |
| Evidence | [Verification records](verification/README.md) · [Completeness arguments](methods/completeness.md) |
| Categorification | [Current classification and open cases](https://github.com/sebastienpalcoux/grothendieck-ring-classification) |
| Project details | [Research updates, historical checks, extended counts and references](docs/PROJECT_GUIDE.md) |
| Source audit | [Attribution and correction witnesses](audit/README.md) |
| Reuse | [Cite](CITATION.cff) · [Licensing](NOTICE.md) · [Contribute](CONTRIBUTING.md) · [OEIS drafts](oeis/README.md) |

Sébastien Palcoux · BIMSA · [Project announcement](https://hexagonmath.org/2610.00300?version=1)
