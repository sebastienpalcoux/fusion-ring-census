#!/usr/bin/env python3
"""Generate every public count projection and index from the certified manifest."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def table(ranks, first, last, columns=range(3,9)):
 columns=list(columns)
 lines=['| Multiplicity | '+' | '.join(f'Rank {r}' for r in columns)+' |','|---:|'+'---:|'*len(columns)]
 for m in range(first,last+1):
  values=[f"{ranks[str(r)]['counts'][str(m)]:,}" if str(m) in ranks[str(r)]['counts'] else '—' for r in columns]
  lines.append('| '+str(m)+' | '+' | '.join(values)+' |')
 return '\n'.join(lines)

def main():
 d=json.loads((ROOT/'results/census.json').read_text());ranks=d['ranks'];oeis=ROOT/'oeis'
 for r,v in ranks.items():
  assert v.get('complete') is True and v.get('verified') is True
  assert sorted(map(int,v['counts']))==list(range(1,v['bound']+1)) and sum(v['counts'].values())==v['classes']
  folder=ROOT/f'results/rank{r}';folder.mkdir(exist_ok=True)
  with (folder/'counts.csv').open('w',newline='') as f:
   w=csv.writer(f,lineterminator='\n');w.writerow(['rank','multiplicity','classes']);w.writerows((r,m,n) for m,n in v['counts'].items())
 with (ROOT/'results/counts.csv').open('w',newline='') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['rank','multiplicity','classes']);w.writerows((r,m,n) for r,v in ranks.items() for m,n in v['counts'].items())
 coverage=['| Rank | Complete through | Classes in total | Data | Companion |','|---:|---:|---:|---|---|']
 for r,v in ranks.items():coverage.append(f'| {r} | {v["bound"]:,} | {v["classes"]:,} | [Tensors]({v["tables"]}) · [Counts](results/rank{r}/counts.csv) | [PDF](manuscripts/rank{r}.pdf) · [TeX](manuscripts/rank{r}.tex) |')
 readme=f'''# Fusion Ring Census

**Exact enumeration of based fusion rings, at ranks 3–8.**

[Data](#complete-datasets) · [Manuscripts](manuscripts/README.md) · [Run & verify](docs/REPRODUCIBILITY.md) · [OEIS](oeis/README.md) · [Evidence](verification/README.md)

{d['total_classes']:,} distinct classes in the certified datasets. Every duality
type is included, including noncommutative rings. No categorifiability filter.

## Counts by rank and multiplicity

Each entry is **the number of based-isomorphism classes at exactly multiplicity
m**. A dash means *not yet completely enumerated*, never zero.

{table(ranks,1,20)}

<details>
<summary><strong>Multiplicities 21–128 · ranks 3 and 4</strong></summary>

{table(ranks,21,128,[3,4])}

</details>

[Full table through multiplicity 1000](results/table.md) · [Download CSV](results/counts.csv) · [Offline interactive table](docs/index.html)

Download `docs/index.html` and open it in a browser to filter the interactive table.

## Complete datasets

Bounds and totals below are cumulative: all rings of multiplicity **at most M**.

{chr(10).join(coverage)}

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
'''
 (ROOT/'README.md').write_text(readme)
 (ROOT/'results/table.md').write_text('# Exact-multiplicity census\n\n[Overview](../README.md) · [CSV](counts.csv) · [Manifest](census.json)\n\nCounts are at exact multiplicity. A dash is unavailable, not zero.\n\n'+table(ranks,1,1000)+'\n')
 (ROOT/'results/README.md').write_text('''# Census data

`census.json` is the authoritative manifest. `counts.csv` and [the full table](table.md)
are generated from it. Each `rankR/` directory contains the current complete
`tables.txt.gz`, `counts.csv`, and, where available, `parameters.txt.gz`.

A tensor is a nested array of nonnegative integers: `N[i][j][k]` is the
coefficient of basis element k in the ordered product i·j; basis element 0 is
the unit. Each line represents one based-isomorphism class. Multiplicity is
the maximum entry of the full tensor, so even group rings have multiplicity 1.
Parameter files contain generator coordinates, not additional classes.

Only complete, independently verified whole-rank data appear here.
See [verification](../verification/README.md)
and [reproduction](../docs/REPRODUCIBILITY.md).
''')
 index=['# Mathematical companions','','Each companion gives definitions, a rank-specific coverage argument, exact counts, independent verification and reproduction commands. They are computational research notes, not claims of journal publication.','','| Rank | Complete through | Classes | Read |','|---:|---:|---:|---|']
 for r,v in ranks.items():index.append(f'| {r} | {v["bound"]} | {v["classes"]:,} | [PDF](rank{r}.pdf) · [LaTeX](rank{r}.tex) |')
 index+=['','Rebuild with `python3 scripts/build_manuscripts.py --compile`. Counts are read from the same manifest as the repository front page.','']
 (ROOT/'manuscripts/README.md').write_text('\n'.join(index))
 assigned={3:'A354471',4:'A354472',5:'A354473'};impact=[]
 for r,v in ranks.items():
  entry=assigned.get(int(r));name='b'+entry[1:]+'.txt' if entry else f'fixed_rank_{r}.txt'
  (oeis/name).write_text(''.join(f'{m} {n}\n' for m,n in v['counts'].items()))
  impact.append({'rank':int(r),'bound':v['bound'],'entry':entry,'file':name,'submission_status':'not submitted'})
 for m,entry in [(1,'A348305'),(2,'A354475'),(3,'A354476'),(4,'A354477')]:
  rows=[(1,1 if m==1 else 0),(2,2 if m==1 else 1)]
  for r in range(3,9):
   if str(m) not in ranks[str(r)]['counts']:break
   rows.append((r,ranks[str(r)]['counts'][str(m)]))
  if m==1:rows.append((9,142))
  name='b'+entry[1:]+'.txt';(oeis/name).write_text(''.join(f'{r} {n}\n' for r,n in rows))
  impact.append({'multiplicity':m,'entry':entry,'through_rank':rows[-1][0],'file':name,'rank9_reference_only':m==1,'submission_status':'not submitted'})
 (oeis/'impact_map.json').write_text(json.dumps(impact,indent=2)+'\n')
 (oeis/'README.md').write_text(f'''# OEIS drafts

[Counting table](../results/table.md) · [Verification](../verification/README.md) · [Source audit](../audit/README.md)

All files are **proposed data or edits, not submitted changes**. Terms count based
fusion rings at exact multiplicity. Only complete whole-rank counts are exported
from `results/census.json`.

| Sequence | Direction | Prepared coverage | File |
|---|---|---|---|
| A354471 | Rank 3; multiplicity varies | 1–{ranks['3']['bound']} | [b-file](b354471.txt) |
| A354472 | Rank 4; multiplicity varies | 1–{ranks['4']['bound']} | [b-file](b354472.txt) |
| A354473 | Rank 5; multiplicity varies | 1–{ranks['5']['bound']} | [b-file](b354473.txt) |
| A348305 | Multiplicity 1; rank varies | 1–9¹ | [b-file](b348305.txt) |
| A354475 | Multiplicity 2; rank varies | 1–8 | [b-file](b354475.txt) |
| A354476 | Multiplicity 3; rank varies | 1–7 | [b-file](b354476.txt) |
| A354477 | Multiplicity 4; rank varies | 1–7 | [b-file](b354477.txt) |

¹ The rank-nine value 142 is retained from the reference census; it is not an
independently recomputed rank-nine result. This repository's computation scope
ends at rank 8. Rank-1 and rank-2 terms follow symbolically.

Fixed-rank data files: [rank 6](fixed_rank_6.txt), [rank 7](fixed_rank_7.txt),
[rank 8](fixed_rank_8.txt). No A-number is assigned to these files in this repository.

## Correction and extensions

The source audit replaces A354473 terms 9–12:
**1463 → 863, 1794 → 1082, 2283 → 1383, 3049 → 1948**.
Suggested comment:

> Terms a(9)–a(12) were corrected by removing repeated isomorphism classes from the ancillary database of Vercleyen and Slingerland (arXiv:2205.15637v4).

The independent census extends the rank-5 draft through 20, with **a(20)=6866**.
The multiplicity-2 draft includes **A354475: a(8)=877**; the multiplicity-4 draft
includes **A354477: a(7)=2780**. The multiplicity-3 draft includes
**A354476: a(7)=1059**. Fixed-rank files include
**c₆({ranks['6']['bound']})={ranks['6']['counts'][str(ranks['6']['bound'])]}**,
**c₇({ranks['7']['bound']})={ranks['7']['counts'][str(ranks['7']['bound'])]}** and
**c₈({ranks['8']['bound']})={ranks['8']['counts'][str(ranks['8']['bound'])]}**.
These terms come from complete, independently verified datasets.

## Before submitting

Check the live entry, indexing and b-file; the retained source snapshot is dated
18 September 2026. Preserve attribution to Vercleyen and Slingerland and credit
the independent census separately. Supply a public, stable reference to the exact
revision and verification evidence. Use a permanent commit link to this public
repository and the corresponding audit records. Search for existing entries before
proposing new fixed-rank sequences. Check other projections of a changed cell using `impact_map.json`.
The source correction and newly appended terms are different changes.

OEIS text retains its [attribution and licensing terms](../NOTICE.md).
''')
 write_release_evidence(d)
 print('Generated census tables, documentation, evidence index and OEIS drafts.')

def write_release_evidence(data):
 ranks=data['ranks']
 rows=['| Rank | Complete through | Classes | Evidence |','|---:|---:|---:|---|']
 for r,v in ranks.items():
  links=f'[Audit](rank{r}/audit.json) · [Source](rank{r}/source.json)'
  if (ROOT/f'verification/rank{r}/run.json').exists():links+=f' · [Completed run](rank{r}/run.json)'
  rows.append(f'| {r} | {v["bound"]} | {v["classes"]:,} | {links} |')
 checks={r:json.loads((ROOT/f'verification/rank{r}/audit.json').read_text()) for r in ['5','6','7','8']}
 for r,a in checks.items():
  assert all(a[k]==ranks[r][k] for k in ('rank','bound','classes','counts','complete','verified')), f'rank {r}: audit and manifest disagree'
 executions={}
 for r,a in checks.items():executions.setdefault(a['verification_run_id'],[]).append(r)
 runs='\n'.join(f'- {"Rank" if len(rs)==1 else "Ranks"} {", ".join(rs)}: [audit {run}](https://github.com/sebastienpalcoux/fusion-ring-census/actions/runs/{run}).' for run,rs in executions.items())
 (ROOT/'verification/README.md').write_text(f'''# Verification evidence

[Data](../results/README.md) · [Coverage arguments](../methods/completeness.md) · [Provenance](../docs/PROVENANCE.md)

Every released census covers the entire rank, including every duality type.
Completeness uses the exhaustive search argument and normally completed enumeration;
independent tensor checks establish validity and uniqueness.

{chr(10).join(rows)}

## Independent checks

Every released tensor is checked for nonnegative integer coefficients, both unit
laws, duality, reciprocity and all integer associativity identities. Canonicalization
uses every unit-fixing basis permutation, with exact tensor comparison. All released
lists have zero duplicate based-isomorphism classes.

The completed laptop datasets at ranks 5–8 also passed independent GitHub audits
of their supplied tensors, source hashes, counts and established count prefixes:

{runs}

The rank-6 audit checked **{ranks['6']['classes']:,} tensors** and
**{checks['6']['independent_verification']['permutations_examined']:,} permutations**.
These hosted jobs performed verification only; they did not rerun enumeration.
[Runner environments](environments.json) are indexed by audit run.

The rank-4 audit jointly checked {ranks['4']['classes']:,} released tensors and 2,787
reference records. The raw comparison consequently has 2,787 repetitions in the
reference suffix; the released enumeration itself has zero duplicates. Its raw
comparison and containment witnesses are in
[rank4/reference_comparison](rank4/reference_comparison/).

## Reproducibility records

Each rank directory contains the audit and source receipt for its current dataset.
Laptop run records retain the exact commands, environment, per-phase timings and
nonempty subprocess logs. Absolute laptop paths in these records document the
computation; use the portable [reproduction commands](../docs/REPRODUCIBILITY.md)
on another computer. Archive hashes identify the supplied payloads, and the
[manifest](../results/census.json) identifies the released compressed data.

Only one current tensor file and parameter file per rank are retained. Verification
reports do not contain duplicate tensor collections. Supporting
[optimization regressions](regressions/) test the indicated small bounds and strata;
they do not substitute for the full independent audits.

[Repository checks](checks/) cover file integrity, count projections, documentation
and lightweight unit tests. They are separate from the mathematical checks above.
''')
 origins={3:'Completed project census',4:'Completed project census',5:'Completed laptop census',6:'Completed laptop census',7:'Completed laptop census',8:'Completed laptop census'}
 coverage=['| Rank | Bound | Classes | Origin |','|---:|---:|---:|---|']
 for r,v in ranks.items():coverage.append(f'| {r} | {v["bound"]} | {v["classes"]:,} | {origins[int(r)]} |')
 (ROOT/'docs/PROVENANCE.md').write_text(f'''# Provenance and attribution

[Overview](../README.md) · [Verification](../verification/README.md) · [Licensing](../NOTICE.md)

## Certified data

Release {data['version']}, dated {data['release_date']}, contains **{data['total_classes']:,}**
distinct based-ring classes across six complete regions. The
[manifest](../results/census.json) fixes every bound, exact-multiplicity count,
tensor checksum and verification location.

{chr(10).join(coverage)}

Each [rank's evidence](../verification/README.md) identifies its enumeration source,
completed computation and independent audit. Laptop source receipts record the
archive checksum and exact code revision; run records retain commands, environment
and timings. Archive inventories, decompressed hashes and established count prefixes
are checked before integration. Every required duality stratum must finish normally.

The supplied rank-5–8 tensors were independently checked on GitHub under every
unit-fixing basis permutation, with no duplicate classes. The hosted jobs ran
verification only. Laptop enumeration times remain attributed to the laptop.
No incomplete search contributes an exhaustive count.

## Mathematical sources

Gert Vercleyen and Joost K. Slingerland, *On Low Rank Fusion Rings*, Journal of
Mathematical Physics **64** (2023), 091703; arXiv:2205.15637v4. The retained ancillary
`FusionRingMultiplicationTables` file has SHA-256
`b587c3f683157369da7cc090f762bbff0e18dcf11acc3f5031d6bc0c643843f8`.
Its 28,451 records represent 25,138 distinct classes. The 3,313 redundant records
all occur at rank five and exact multiplicities 9–12; each deletion has a checked
unit-fixing basis-permutation witness. The source identity is recorded in
[audit/source.json](../audit/source.json).

The [source audit](../audit/README.md) is a comparison and deduplication study.
The source data do not feed the independent enumerators. Deduplication alone
does not establish completeness of the source's partial-search cells.

Rank-four and rank-five reductions come from the Dong–Palcoux census project
and exact-certificate supplements. The [methods](../methods/completeness.md) include
zero-coefficient and singular branches. The six
[companions](../manuscripts/README.md) are computational research notes; no journal
acceptance, DOI or arXiv identifier is asserted for them.

## Code and computational evidence

Rank-eight support uses dynamically sized linear-algebra workspaces: its self-dual
system has 84 variables and 231 equations. The general solver includes all duality
types and noncommutative cases. No categorifiability filter is applied.

GPT-6 Astra Pro assisted with algorithm development, code, exposition and
computational checks. Exact independent verification and exhaustive coverage
arguments are separate evidence. Neither implies proof-assistant certification
or external peer review. These counts classify based rings, not tensor categories.

## Organization and access

There is one dataset and evidence directory per rank, one manifest and one
reproduction guide. The front-page table, CSV files, companions and OEIS data
projections derive from the same manifest. Source attribution, licensing and
verification evidence are retained alongside the data.

The repository is public. [OEIS files](../oeis/README.md) are prepared data and
edit text; the repository does not certify their acceptance by OEIS.
''')

if __name__=='__main__':main()
