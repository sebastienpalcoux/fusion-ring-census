# Census data

`census.json` is the authoritative manifest. `counts.csv` and [the full table](table.md)
are generated from it. Each `rankR/` directory contains the current complete
`tables.txt.gz`, `counts.csv`, and, where available, `parameters.txt.gz`.

A tensor is a nested array of nonnegative integers: `N[i][j][k]` is the
coefficient of basis element k in the ordered product i·j; basis element 0 is
the unit. Each line represents one based-isomorphism class. Multiplicity is
the maximum entry of the full tensor, so even group rings have multiplicity 1.
Parameter files contain generator coordinates, not additional classes.

Only complete, independently verified whole-rank data appear here. Earlier
releases remain in Git history. See [verification](../verification/README.md)
and [reproduction](../docs/REPRODUCIBILITY.md).
