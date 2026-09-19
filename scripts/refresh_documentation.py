#!/usr/bin/env python3
"""Regenerate count tables, OEIS drafts and the repository landing page."""
from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    data=json.loads((ROOT/'results/census.json').read_text());ranks=data['ranks']
    for rank,item in ranks.items():
        if item.get('complete') is not True or item.get('verified') is not True:raise ValueError('cannot export an incomplete or unverified census')
        if sorted(map(int,item['counts']))!=list(range(1,item['bound']+1)):raise ValueError('noncontiguous census')
        with (ROOT/f'results/rank{rank}_counts.csv').open('w',newline='') as f:
            w=csv.writer(f);w.writerow(['rank','multiplicity','classes']);w.writerows((rank,m,c) for m,c in item['counts'].items())
    with (ROOT/'results/counts.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['rank','multiplicity','classes'])
        for rank,item in ranks.items():w.writerows((rank,m,c) for m,c in item['counts'].items())
    oeis=ROOT/'oeis';oeis.mkdir(exist_ok=True)
    assigned={3:'A354471',4:'A354472',5:'A354473'}
    impact=[]
    for r,item in ranks.items():
        if int(r) in assigned:
            number=assigned[int(r)];path=oeis/('b'+number[1:]+'.txt')
        else:number=None;path=oeis/f'fixed_rank_{r}.txt'
        path.write_text(''.join(f'{m} {c}\n' for m,c in item['counts'].items()))
        impact.append({'rank':int(r),'bound':item['bound'],'assigned_entry_in_this_package':number,'b_file':str(path.relative_to(ROOT))})
    # Fixed-multiplicity sequences start at rank one; ranks 1/2 follow symbolically.
    for mult,number in [(1,'A348305'),(2,'A354475'),(3,'A354476'),(4,'A354477')]:
        rows=[(1,1 if mult==1 else 0),(2,2 if mult==1 else 1)]
        for r in range(3,9):
            if str(mult) not in ranks[str(r)]['counts']:break
            rows.append((r,ranks[str(r)]['counts'][str(mult)]))
        # Retain the previously published rank-nine multiplicity-one term as reference-only.
        if mult==1:rows.append((9,142))
        (oeis/('b'+number[1:]+'.txt')).write_text(''.join(f'{n} {c}\n' for n,c in rows))
        impact.append({'fixed_multiplicity':mult,'entry':number,'through_rank':rows[-1][0],
                       'rank9_source_only':mult==1,'submission_status':'not submitted'})
    (oeis/'impact_map.json').write_text(json.dumps(impact,indent=2)+'\n')
    lines=['# Complete counting table','', 'All entries below count based-isomorphism classes at exact multiplicity. A dash is unavailable, never zero.','',
           '| Multiplicity | Rank 4 | Rank 5 | Rank 6 | Rank 7 | Rank 8 |','|---:|---:|---:|---:|---:|---:|']
    for m in range(1,max(ranks[str(r)]['bound'] for r in range(4,9))+1):
        lines.append('| '+str(m)+' | '+' | '.join(str(ranks[str(r)]['counts'].get(str(m),'—')) for r in range(4,9))+' |')
    (ROOT/'results/corrected_extended_table.md').write_text('\n'.join(lines)+'\n')
    table=['| Rank | Complete multiplicity bound | Distinct classes | Manuscript | Full tensors |','|---:|---:|---:|---|---|']
    for r,item in ranks.items():
        table.append(f'| **{r}** | **{item["bound"]}** | **{item["classes"]:,}** | [PDF](manuscripts/rank{r}.pdf) · [TeX](manuscripts/rank{r}.tex) | [gzip]({item["tables"]}) |')
    readme=f'''# Fusion Ring Census

### Exact enumeration · all duality types · independently checked tensors

A reproducible collection of **{data['total_classes']:,} fusion rings**, with fast integer generators,
complete counting tables, explanatory mathematical companions and an OEIS workspace.

[View the landing page](docs/index.html) · [Start with the data](results/census.json) · [Read the manuscripts](manuscripts/README.md) ·
[Reproduce a census](docs/REPRODUCIBILITY.md) · [OEIS](oeis/README.md) · [Audit the source](audit/README.md)

## Certified coverage

{chr(10).join(table)}

The unit has index zero and `N[i][j][k]` is the coefficient of basis element `k`
in the **ordered** product `i*j`. All results include every duality type.
**These are classifications of based rings, not of fusion categories.** No
categorifiability criterion is applied. Rank three is intentionally capped at 1000.

Ranks 3–7 retain the completed census data and provenance from 18 September 2026.
Rank eight is independently generated with the expanded solver in this repository.
New local verification is recorded separately from the original execution logs.

## Three ways to use the project

Read `manuscripts/rankR.pdf` for the definitions, mathematical coverage argument,
rank-specific method, results, singular cases and verification boundary.

Verify the released tensors without repeating the search:

```bash
python3 scripts/check_release.py --full
```

Reproduce a complete bounded census, or request a larger whole-rank search:

```bash
python3 code/run_census.py --rank 6 --bound 6 --seconds 1200 \\
  --threads 4 --verify --out runs/rank6-reproduction
python3 scripts/extend_census.py --rank 6 --seconds 1100 \\
  --threads 4 --out runs/rank6-frontier
```

Requirements: Python 3.9+, GNU g++ with C++17/OpenMP. The mathematical code uses
only Python's standard library. LaTeX is needed only to rebuild PDFs. No SageMath,
Mathematica or NumPy is required. See [platform notes](docs/REPRODUCIBILITY.md).

## A complete result, or no new claim

A whole-rank result must finish **every** involution type. The independent checker
then verifies every fusion-ring axiom, all integer associativity identities and
all unit-fixing basis permutations. A larger interrupted attempt cannot replace
the last completed and verified bound. No partial-stratum counts are exported to OEIS.

Completeness is justified by the exhaustive parameterization and safe-pruning
proofs; checking emitted tensors alone would not prove that nothing was omitted.
The distinction is made explicitly in [the methods](methods/completeness.md).

## GitHub computation

[The frontier workflow](.github/workflows/frontier.yml) runs a manually requested
matrix for ranks 3–8. Each rank has a **20-minute job ceiling**, and all attempts
within that job share a 1,100-second driver deadline including compilation,
export and verification. Rank three regenerates through 1000 and stops. The other
ranks try increasing complete bounds. Starting points are heuristics, not promises
of a particular improvement on a GitHub runner.

Only verified whole-rank `best/` results become candidate artifacts. To review and
import one, use [the release procedure](docs/RELEASES.md). The workflow never pushes
unreviewed numerical results to `main` and never edits OEIS automatically.

**Publication state of this package:** prepared and tested locally. The session
that assembled it had read-only GitHub access; no remote repository or Actions
run is claimed. The authenticated publisher is:

```bash
python3 scripts/publish_github.py --run-census
```

This creates `sebastienpalcoux/fusion-ring-census` as **private** by default,
pushes the committed material and requests the workflow once. Add `--public`
only when deliberately publishing the manuscripts and data publicly. The script
uses the user's existing `gh auth login` session and refuses another account or
an existing repository. It never asks for a token in an argument or prints credentials.

## Source audit and attribution

The audit of Vercleyen–Slingerland's arXiv v4 ancillary file identifies 3,313
redundant records, all at rank five and multiplicities 9–12. Exact permutation
witnesses and the corrected table are retained under `audit/`. The source was
used for comparison only, never as enumeration input. Its original partial
search cells are not promoted to complete counts merely by deduplication.

The specialized rank-four and rank-five derivations come from the Dong–Palcoux
census project; the original excerpts and execution records are preserved.
See [provenance](docs/PROVENANCE.md), [citation metadata](CITATION.cff), and
[licensing scope](NOTICE.md). AI assistance and verification status are disclosed.

## Repository map

```text
code/          Exact generators, exporters and independent tensor checker
systems/       Regenerable reciprocity orbits and associativity systems
results/       Only complete datasets, count tables and the primary manifest
manuscripts/   Six explanatory companions, in LaTeX and PDF
methods/       Coverage proofs and retained rank-specific derivations
oeis/          b-files, correction text, impact map and submission policy
audit/         Original-database deduplication code and certificates
verification/  Execution provenance, regression tests and independent audits
scripts/       Timed search, release checking, publication and result import
tests/         Regressions, symmetry checks, scope checks and timeout tests
.github/       CI, manual frontier search and issue templates
```

## Cite and contribute

Use **Cite this repository** after publication, or the metadata in `CITATION.cff`.
Report a suspected missed ring with its full multiplication tensor, rank,
multiplicity, generating command and revision. Improvements must preserve every
singular and zero-coefficient branch and pass independent checks. See
[CONTRIBUTING.md](CONTRIBUTING.md).
'''
    (ROOT/'README.md').write_text(readme)
    (ROOT/'manuscripts/README.md').write_text('# Explanatory manuscripts\n\nEach companion contains definitions, a rank-specific enumeration argument, full-duality coverage, results, verification limits and reproduction commands. They are computational project notes, not claims of journal publication.\n\n'+ '\n'.join(f'- Rank {r}: [PDF](rank{r}.pdf), [LaTeX](rank{r}.tex).' for r in range(3,9))+'\n\nRegenerate sources and PDFs with `python3 scripts/build_manuscripts.py --compile` from the repository root.\n')
    oeisread='''# OEIS workspace

All files here are **proposed data or edits**, not submitted changes. The primary
source for numerical output is `results/census.json`, which contains only complete
whole-rank datasets. `scripts/refresh_documentation.py` regenerates this folder's
b-files and impact map.

| Entry | Meaning | File |
|---|---|---|
| A354471 | Rank 3, multiplicity varies; stop at 1000 | `b354471.txt` |
| A354472 | Rank 4, multiplicity varies | `b354472.txt` |
| A354473 | Rank 5, multiplicity varies | `b354473.txt` |
| A348305 | Multiplicity 1, rank varies | `b348305.txt` |
| A354475 | Multiplicity 2, rank varies | `b354475.txt` |
| A354476 | Multiplicity 3, rank varies | `b354476.txt` |
| A354477 | Multiplicity 4, rank varies | `b354477.txt` |

`fixed_rank_6.txt`, `fixed_rank_7.txt`, and `fixed_rank_8.txt` are separately prepared
fixed-rank sequences. **No new A-numbers are invented or reserved here.** Search OEIS
for an existing entry before proposing one. Their current prefixes may be too short
for a new entry without further explanatory content.

The multiplicity-one b-file retains the published rank-nine value 142 from the
reference census. It is **not** an independently recomputed rank-nine result in
this repository, whose computation scope ends at rank eight. All newly generated
numerical additions are restricted to the verified manifest.

## Rank-five correction sentence

> Terms a(9)–a(12) were corrected by removing repeated isomorphism classes from the ancillary database of Vercleyen and Slingerland (arXiv:2205.15637v4).

The replacements are 1463 → 863, 1794 → 1082, 2283 → 1383, and 3049 → 1948.
The original authors' enumeration remains credited; the correction and independent
extensions should be credited separately. Keep the existing references and add a
stable repository/release link only after one actually exists.

## Cross-sequence impact

A correction to c_r(m) affects a fixed-rank entry at a(m), a fixed-multiplicity
entry at a(r), and any derived sequence using that cell. `impact_map.json` records
the entries handled by this package; it is not an exhaustive assertion about all
of OEIS. In particular, check fixed-multiplicity entries at 9, 10, 11 and 12 if any
are located. The four rank-five duplicate corrections do not change the existing
multiplicity-1, -2, -3 or -4 prefixes.

The rank-seven multiplicity-three value 1059 extends A354476 at a(7).
Any additional rank-eight multiplicity-two value is exported to A354475 only when
the complete rank-eight bound-two run is certified in the manifest.

## Submission checklist

Check the live entry, its indexing and existing b-file. Compare the entire old
prefix. Distinguish corrected terms from newly appended terms. Provide the exact
release revision, source checksum, algorithm, completeness explanation and audit
witnesses. Submit through the OEIS editorial workflow; do not claim acceptance
until the edit is actually approved.
'''
    (oeis/'README.md').write_text(oeisread)
    print('Refreshed README, counts, OEIS drafts and manuscript index.')
if __name__=='__main__':main()
