# Documentation audit revision · 24 October 2026

This revision changes mathematical qualifications and their generated displays.
It does not change a census tensor, enumeration count or completeness receipt.

- The signed rank-five commutativity lemma requires the dimension character
  to be nonzero at **every** basis element and equal on dual basis elements.
- The rank-eight audit corrected the scope of an earlier near-group argument. The current classification uses a separate replacement proof for R8_3_436; see the [current classification account](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md).
- Rank-seven producer-source availability, the general generator's rank range
  and the nine rank-specific census PDFs are described consistently.

This audit record pins the companion classification at commit
`d22bdcf3f97b7d6991362a417e25172fda4c8a8a`; its original source identities remain attached to the audit evidence. Current classification totals are recorded separately in [classification.json](../classification.json).

Validation completed:

```bash
python scripts/build_manuscripts.py --ranks 5 8 --compile --sync-readme
python scripts/build_site.py
python scripts/check_release.py
python -m unittest discover -s tests -v
```

The release check passed for ranks 3–11 and all 43 tests passed. The revised
rank-five and rank-eight PDFs compile and have no text outside their page bounds.
These checks do not independently rerun the large enumerations or verify every
categorical argument in the companion project.
