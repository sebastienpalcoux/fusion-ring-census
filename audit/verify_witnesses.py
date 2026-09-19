#!/usr/bin/env python3
"""Independently verify all line-map isomorphisms using Python integers.

This verifies that no ring was incorrectly removed and the output/counts agree.
It does NOT on its own establish pairwise nonisomorphism of retained rings;
use the C++ --exhaustive audit as the separate completeness-of-deduplication check.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from time import perf_counter


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def verify(source: Path, output: Path) -> dict:
    start = perf_counter()
    records: dict[int, tuple[str, list]] = {}
    with source.open(encoding="utf-8") as stream:
        for number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            tensor = json.loads(line.replace("{", "[").replace("}", "]"))
            n = len(tensor)
            require(n > 0 and all(len(a) == n and all(len(b) == n for b in a) for a in tensor), f"bad tensor at {number}")
            require(all(type(v) is int and v >= 0 for a in tensor for b in a for v in b), f"bad coefficients at {number}")
            records[number] = (line.rstrip("\r\n"), tensor)
    with (output / "line_map.csv").open(newline="", encoding="utf-8") as stream:
        mapping = list(csv.DictReader(stream))
    require([int(r["source_line"]) for r in mapping] == list(records), "source coverage/order mismatch")
    by_line = {int(row["source_line"]): row for row in mapping}
    clean = (output / "FusionRingMultiplicationTables.deduplicated").read_text(encoding="utf-8").splitlines()
    counts: dict[tuple[int, int], Counter] = {}
    labelled: set[tuple] = set()
    retained = []
    duplicates = []
    for row in mapping:
        number, rep = int(row["source_line"]), int(row["representative_source_line"])
        clean_line, n, m = (int(row[k]) for k in ("clean_line", "rank", "multiplicity"))
        q = tuple(map(int, row["permutation_source_to_representative"].split(";")))
        a = records[number][1]
        require(rep in records and rep <= number, f"bad representative at {number}")
        b = records[rep][1]
        require(n == len(a) == len(b), f"rank mismatch at {number}")
        require(max(v for mat in a for line in mat for v in line) == m, f"multiplicity mismatch at {number}")
        require(sorted(q) == list(range(n)) and q[0] == 0, f"bad permutation at {number}")
        require(all(a[i][j][k] == b[q[i]][q[j]][q[k]] for i in range(n) for j in range(n) for k in range(n)), f"false isomorphism at {number}")
        rep_row = by_line[rep]
        require(rep_row["kind"] == "retained" and rep_row["clean_line"] == row["clean_line"], f"representative map mismatch at {number}")
        require(1 <= clean_line <= len(clean) and clean[clean_line-1] == records[rep][0], f"clean file mismatch at {number}")
        flat = tuple(v for mat in a for line in mat for v in line)
        repeated = flat in labelled
        labelled.add(flat)
        c = counts.setdefault((n, m), Counter())
        c["source_records"] += 1
        if row["kind"] == "retained":
            require(rep == number and not repeated and q == tuple(range(n)), f"retained row mismatch at {number}")
            retained.append(number)
            require(clean_line == len(retained), f"clean ordering mismatch at {number}")
            c["distinct_rings"] += 1
            comm = all(a[i][j][k] == a[j][i][k] for i in range(n) for j in range(n) for k in range(n))
            c["commutative" if comm else "noncommutative"] += 1
        else:
            require(rep < number, f"non-earlier duplicate at {number}")
            expected = "literal_repeat" if repeated else "new_labelling"
            require(row["kind"] == expected, f"duplicate kind mismatch at {number}")
            c["duplicates"] += 1
            c["literal_repeats" if repeated else "new_labellings"] += 1
            duplicates.append(row)
    require(len(clean) == len(retained), "wrong number of retained lines")
    with (output / "duplicates.csv").open(newline="", encoding="utf-8") as stream:
        require(list(csv.DictReader(stream)) == duplicates, "duplicate certificate file mismatch")
    with (output / "counts.csv").open(newline="", encoding="utf-8") as stream:
        actual = list(csv.DictReader(stream))
    require(len(actual) == len(counts), "number of counting cells mismatch")
    for row in actual:
        c = counts[(int(row["rank"]), int(row["multiplicity"]))]
        for key, value in row.items():
            if key not in ("rank", "multiplicity"):
                require(int(value) == c[key], f"count mismatch for {key}")
    summary = json.loads((output / "summary.json").read_text())
    require(summary["input_records"] == len(records), "summary input mismatch")
    require(summary["distinct_rings"] == len(retained), "summary retained mismatch")
    require(summary["duplicates"] == len(duplicates), "summary duplicates mismatch")
    result = {"verified": True, "records": len(records), "retained": len(retained),
              "duplicate_witnesses": len(duplicates), "elapsed_seconds": perf_counter() - start,
              "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "scope": "coverage, isomorphism witnesses, retained lines and all count columns; not retained pairwise nonisomorphism"}
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.input, args.output)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        raise SystemExit(f"VERIFICATION FAILED: {error}") from error
    text = json.dumps(result, indent=2) + "\n"
    print(text, end="")
    if args.report:
        args.report.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    main()
