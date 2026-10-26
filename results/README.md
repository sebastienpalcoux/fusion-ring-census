# Census data

`census.json` is the authoritative manifest. `counts.csv` and [the full table](table.md)
are generated from it. Each `rankR/` directory contains the current complete
`tables.txt.gz`, `counts.csv`, and, where available, `parameters.txt.gz`.

A tensor is a nested array of nonnegative integers: `N[i][j][k]` is the
coefficient of basis element k in the ordered product i·j; basis element 0 is
the unit. Each line represents one based-isomorphism class. Multiplicity is
the maximum entry of the full tensor, so even group rings have multiplicity 1.
Parameter files contain generator coordinates, not additional classes.

Each released list has independently verified valid, distinct tensors.
Rank-7 completeness through multiplicity 5 is producer-reported: the supplied
complete optimized source is now supplied and hash-matched, but enumeration
was not rerun. The same qualification applies to rank 8 through multiplicity 3.
See [the rank-7 qualification](../verification/rank7/README.md).
See [verification](../verification/README.md)
and [reproduction](../docs/REPRODUCIBILITY.md).

The current multiplicity-one release also includes ranks 9–11: 142, 194 and 182 classes, with [fresh exact verification and complete source](../verification/engine_20261023/README.md). Full enumeration remains producer-reported.

Rank twelve through multiplicity one adds 632 classes. See [source and exact checks](../verification/rank12/README.md). No categorifiability filtering is applied.
