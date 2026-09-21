# Contributing

Start with the mathematical companions and `docs/REPRODUCIBILITY.md`. Keep changes
small and distinguish mathematical changes from performance and formatting work.

A new pruning rule needs a proof that it discards no valid ring, including all
zero, singular and noncommutative branches. Compare an optimization with a complete
small-bound baseline and retain the full set of canonical tensors, not only the
number of outputs. A numerical invariant collision is never an isomorphism proof.

Run lightweight unit tests for changes. For enumerator changes, run all-rank
smoke tests and the full release audit on GitHub Actions or your own computer. Preserve command lines, code hashes, compiler details, timing and status.
A full-rank count requires every duality type to finish. Do not submit a partial
stratum as an OEIS term or silently replace an exact entry with a lower bound.

Report suspected missing rings using the issue template, with a complete ordered
multiplication tensor and an explicit explanation of the mismatch. Do not post
private credentials, account identifiers or unpublished third-party correspondence.

Manuscript edits should preserve attribution and distinguish proof, computation,
historical report and conjecture. A new public release requires maintainer review.
