# Rank 7 through multiplicity 5

The supplied `rank7_multiplicity5_verified.zip` contains **10,006** tensors:
43, 319, 1,059, 2,780 and **5,805** at exact multiplicities 1 through 5.
The release has all four duality types. In the new band, their counts are
4,654, 1,012, 138 and 1 (respectively 0, 1, 2 and 3 nontrivial dual pairs);
9 of the 5,805 new rings are noncommutative.

## Independent checks performed for this release

- Every archive `SHA256SUMS` entry, compressed and decompressed release hashes.
- All fusion-ring axioms using a freshly compiled repository verifier.
- All 7,204,320 unit-fixing permutations; zero duplicate based-isomorphism classes.
- Fresh export of the supplied parameter records gives byte-identical tensors.
- Exact tensor-set equality of the multiplicity-at-most-4 prefix with the
  previous 4,201-class release, in addition to count agreement.
- Rank-7 equation-system, exporter and independent-verifier source hashes match
  the source hashes supplied by the producer.

See [audit.json](audit.json), [integration_check.json](integration_check.json),
[fresh verification](fresh_verification/summary.json), and
[the retained log](logs/fresh_verification.log).

## Completeness qualification

The [producer run](run.json) reports normal completion of all four duality
strata, with 77,046 seconds total elapsed time (about 21.4 hours) on the
producer's laptop. Those timings are not timings from this independent check.

The [source receipt](source.json) and [laptop provenance](laptop_provenance.json)
identify modified local optimized enumeration sources based on commit
`d4c36cc2ee5eb5f0e5291de18d2bb433ffb7ce8b`. The archive includes source
hashes but **does not bundle the modified enumeration source files**.
Consequently completeness is **producer-reported**, and has not been
independently reproduced in this release. Output verification proves tensor
validity and uniqueness; it cannot detect a class omitted by enumeration.
The manifest's `complete: true` retains the producer's completion report;
`completeness_basis` and `independent_enumeration_rerun: false` record this limit.

The earlier multiplicity-4 evidence remains in [previous_M4](previous_M4/).
The supplied independent check remains in [supplied_check](supplied_check/).
No hosted verification run or independent full enumeration is claimed for the
new multiplicity-5 release.
