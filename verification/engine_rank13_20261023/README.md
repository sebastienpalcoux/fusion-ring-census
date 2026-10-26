# Exact rank-12 producer source

The unchanged [rank-13 symmetry package](../../packages/Fusion_Census_rank13_symmetry.zip)
contains the complete generator, systems, exact verifier, finite symmetry audits,
and no-clock-limit laptop launcher used for the supplied rank-12 data.
Every code-file hash in the producer provenance matches this archive exactly.
The archive's complete SHA256SUMS also verifies. These source-identity checks
do not repeat the approximately 40-hour whole-rank search.

Extract the package, enter its directory, and run
`python3 scripts/run_laptop.py --rank 12 --bound 1`.
The older root launcher is retained as the rank-3–11 implementation; use this
explicit source package to reproduce the rank-12 symmetry run.
