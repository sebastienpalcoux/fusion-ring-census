# Mathematical companions

Each companion gives definitions, a rank-specific coverage argument, exact counts, independent verification and reproduction commands. They are computational research notes, not claims of journal publication.

> **AI-generated research · independent verification pending.** Independent human verification and Lean formalization are pending. Treat the results and data with caution: automated checks establish only their stated scope.

The separate [Grothendieck-ring classification project](https://github.com/sebastienpalcoux/grothendieck-ring-classification) supplies the unrestricted rank-four categorification theorem and its proof. These six companions enumerate based rings at the displayed bounds.

| Rank | Complete through | Classes | Read |
|---:|---:|---:|---|
| 3 | 1000 | 460,353 | [PDF](rank3.pdf) · [LaTeX](rank3.tex) |
| 4 | 128 | 889,530 | [PDF](rank4.pdf) · [LaTeX](rank4.tex) |
| 5 | 20 | 40,999 | [PDF](rank5.pdf) · [LaTeX](rank5.tex) |
| 6 | 9 | 25,421 | [PDF](rank6.pdf) · [LaTeX](rank6.tex) |
| 7 | 4 | 4,201 | [PDF](rank7.pdf) · [LaTeX](rank7.tex) |
| 8 | 2 | 973 | [PDF](rank8.pdf) · [LaTeX](rank8.tex) |

Rebuild with `python3 scripts/build_manuscripts.py --compile`, or select one companion with `--ranks 6 --compile`. Counts and the displayed release date are read from the same manifest as the repository front page.
