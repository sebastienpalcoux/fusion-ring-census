# Research overview and Hexagon record

**Low-rank Grothendieck rings: an AI-assisted classification project, constructions, and open problems**

The current four-page repository overview, dated 29 October 2026, presents the classification through rank twelve, the constructions catalogue, and the six remaining unresolved cases.

The census contains **1,434,042 rings: 1,433,506 general exclusions, 530 realizations, and 6 unresolved cases**. The new exclusion is **R8_3_1768**; no additional model is claimed. At rank eight the counts are 3,508 exclusions, 16 models and 3 unresolved rings at exact multiplicity three, and 4,404 exclusions, 93 models and 3 unresolved rings cumulatively through multiplicity three.

**AI-generated research · independent human verification pending.** The overview distinguishes categorical proofs, exact certificate checks, and enumeration completeness. The general-complex exclusion of R8_3_1768 uses the established sphericalization/Galois existence reduction and complete necessary center domains. The [unified frontier proofs](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/frontier/README.md) identify these dependencies and the progress on all six open cases.

- [Current overview · PDF](Low_rank_Grothendieck_rings_announcement.pdf)
- [LaTeX source](main.tex) · [Source ZIP](Hexagon_Source.zip)
- [Citation · BibTeX](citation.bib)
- [Overview metadata](submission_metadata.txt) · [Snapshot and checksums](snapshot_manifest.json)

## Hexagon record and citation

The persistent preprint record is [hexagon:2610.00300](https://hexagonmath.org/2610.00300). The repository overview incorporates subsequent project results; this repository update does not change the existing Hexagon deposit.

Sébastien Palcoux, *Low-rank Grothendieck rings: an AI-assisted classification project, constructions, and open problems*, Hexagon, hexagon:2610.00300 (2026).

For a particular theorem, construction, dataset or software run, also cite its primary source and exact repository commit. The live catalogues can change.

## Construction terminology

“New” means that the specific construction has not, to our knowledge, been explicitly recorded in the literature. Its ingredients may be known; the project checks their hypotheses and the resulting fusion rules. This is not a claim of novelty up to tensor equivalence or of exoticness, and independent verification remains pending.

## Rebuild and source bindings

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with a standard TeX Live installation. The source has an inline bibliography and needs no external images or custom class.

The immutable source baselines are classification commit `d920cc2531d8b03583c797886a3c2ab6170a281a` and census commit `27d0c66fbcec1b399c0e39b4b9dcff71bbf7150f`; the unified frontier revision supplies the new exclusion. The dated counts and exact input bindings are recorded in the current publication and frontier manifests. The four overview pages are separate from the research-manuscript inventory.

[Classification repository](https://github.com/sebastienpalcoux/grothendieck-ring-classification) · [Fusion-ring census](https://github.com/sebastienpalcoux/fusion-ring-census) · [Public Atlas](https://sebastienpalcoux.github.io/grothendieck-ring-classification/)
