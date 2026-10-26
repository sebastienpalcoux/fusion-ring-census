#!/usr/bin/env python3
"""Refresh current count projections while preserving historical research notes."""
import csv
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def table(ranks, first, last, columns=None):
    columns = list(columns or sorted(map(int, ranks)))
    lines = ['| Multiplicity | ' + ' | '.join(f'Rank {r}' for r in columns) + ' |', '|---:|' + '---:|' * len(columns)]
    for m in range(first, last + 1):
        values = [f"{ranks[str(r)]['counts'][str(m)]:,}" if str(m) in ranks[str(r)]['counts'] else '—' for r in columns]
        lines.append('| ' + str(m) + ' | ' + ' | '.join(values) + ' |')
    return '\n'.join(lines)

def main():
    data = json.loads((ROOT / 'results/census.json').read_text()); ranks = data['ranks']
    all_rows = []
    coverage = ['| Rank | Complete through | Classes in total | Data | Companion / evidence |', '|---:|---:|---:|---|---|']
    for r, item in ranks.items():
        assert item['complete'] is True and item['verified'] is True
        assert sorted(map(int, item['counts'])) == list(range(1, item['bound'] + 1))
        assert sum(item['counts'].values()) == item['classes']
        rows = [(int(r), int(m), count) for m, count in item['counts'].items()]; all_rows += rows
        with (ROOT / f'results/rank{r}/counts.csv').open('w', newline='') as f:
            writer = csv.writer(f, lineterminator='\n'); writer.writerow(['rank', 'multiplicity', 'classes']); writer.writerows(rows)
        evidence = f'[PDF](manuscripts/rank{r}.pdf) · [TeX](manuscripts/rank{r}.tex)' if (ROOT / f'manuscripts/rank{r}.pdf').is_file() else f'[Verification](verification/rank{r}/README.md)'
        coverage.append(f'| {r} | {item["bound"]:,} | {item["classes"]:,} | [Tensors]({item["tables"]}) · [Counts](results/rank{r}/counts.csv) | {evidence} |')
    assert sum(item['classes'] for item in ranks.values()) == data['total_classes']
    with (ROOT / 'results/counts.csv').open('w', newline='') as f:
        writer = csv.writer(f, lineterminator='\n'); writer.writerow(['rank', 'multiplicity', 'classes']); writer.writerows(all_rows)
    (ROOT / 'results/table.md').write_text('# Exact-multiplicity census\n\n[Overview](../README.md) · [CSV](counts.csv) · [Manifest](census.json)\n\nCounts are at exact multiplicity. A dash is unavailable, not zero.\n\n' + table(ranks, 1, 1000) + '\n')
    (ROOT / 'README.md').write_text(f'''# Fusion Ring Census

**Exact enumeration of based fusion rings at ranks 3–12.**

[**Browse the counts →**](results/table.md) · [Datasets](#datasets) · [Run & verify](docs/REPRODUCIBILITY.md) · [Methods](methods/completeness.md)

**{data['total_classes']:,} based-isomorphism classes** in the released datasets, including every duality type and noncommutative rings. Categorifiability is recorded separately in the companion [Grothendieck Ring Classification](https://github.com/sebastienpalcoux/grothendieck-ring-classification) and its [interactive atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/).

> **AI-generated research · independent verification pending.** Automated checks establish only their stated scope. [Provenance and verification](docs/PROVENANCE.md).

**26 October 2026 · rank twelve, multiplicity one.** The new dataset contains **632 fusion rings**. The companion classifies them as **480 general exclusions and 152 modeled rings**, with none unresolved. Of the models, **151 are unitary**; R12_1_623 has a complex/pseudo-unitary realization whose unitarity is unproved. [Source and exact checks](verification/rank12/README.md) · [Classification scope](verification/rank12/categorification.json) · [Public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/?rank=12&m=1).

The ten previously open cases at ranks six, eight and nine remain open. Earlier census data and classification decisions are unchanged. [Previous correctness audit](verification/audit_20261025/README.md).


<a id="complete-datasets"></a>

## Datasets

Bounds are cumulative: all rings of multiplicity **at most M**.

{chr(10).join(coverage)}

The newly supplied ranks 9–12 passed fresh exact tensor and uniqueness checks. Enumeration completeness is producer-reported, with all strata completed and the complete source supplied; the full searches were not independently rerun. The same qualification applies to rank 7 through 5 and rank 8 through 3. [Verification by rank](verification/README.md).

<details id="counts-by-rank-and-multiplicity">
<summary><strong>Counts at each exact multiplicity</strong></summary>

Each entry counts classes at **exactly** the stated multiplicity. A dash means not completely enumerated.

[Full count table](results/table.md) · [CSV](results/counts.csv) · [Interactive table](docs/index.html) · [Definitions and historical details](docs/PROJECT_GUIDE.md#counts-by-rank-and-multiplicity)

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
| Project details | [Historical research and definitions](docs/PROJECT_GUIDE.md) |
| Reuse | [Cite](CITATION.cff) · [Licensing](NOTICE.md) · [OEIS drafts](oeis/README.md) |

Sébastien Palcoux · BIMSA · [Current project announcement · PDF](announcements/hexagon-2026-10/Low_rank_Grothendieck_rings_announcement.pdf) · [Hexagon](https://hexagonmath.org/2610.00300) · [How to cite](https://sebastienpalcoux.github.io/grothendieck-ring-classification/#cite)
''')
    assigned = {3: '354471', 4: '354472', 5: '354473'}
    for r, item in ranks.items():
        filename = f'b{assigned[int(r)]}.txt' if int(r) in assigned else f'fixed_rank_{r}.txt'
        (ROOT / 'oeis' / filename).write_text(''.join(f'{m} {n}\n' for m, n in item['counts'].items()))
    for m, number in [(1, '348305'), (2, '354475'), (3, '354476'), (4, '354477')]:
        rows = [(1, 1 if m == 1 else 0), (2, 2 if m == 1 else 1)]
        for r in sorted(map(int, ranks)):
            if str(m) not in ranks[str(r)]['counts']: break
            rows.append((r, ranks[str(r)]['counts'][str(m)]))
        (ROOT / f'oeis/b{number}.txt').write_text(''.join(f'{r} {n}\n' for r, n in rows))
    print('Updated current count projections and clean overview; historical notes preserved.')

if __name__ == '__main__':
    main()
