#!/usr/bin/env python3
"""Small independent regression suite; optionally add the full source audit.
Usage: python3 test_audit.py /path/to/dedup_fusion
"""
from __future__ import annotations
import csv
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
from verify_witnesses import verify


def group_table(elements, multiply):
    index = {x: i for i, x in enumerate(elements)}
    n = len(elements)
    return [[[int(k == index[multiply(a, b)]) for k in range(n)] for b in elements] for a in elements]


def relabel(a, p):
    return [[[a[i][j][k] for k in p] for j in p] for i in p]


def run_tests(binary: Path) -> dict:
    rng = random.Random(20260918)
    cases = [group_table(list(range(n)), lambda a, b, n=n: (a+b) % n) for n in (2,4,6,9)]
    cases += [group_table(list(range(4)), lambda a,b: a ^ b),
              group_table(list(itertools.permutations(range(3))), lambda a,b: tuple(a[b[k]] for k in range(3))),
              group_table(list(itertools.product(range(3), repeat=2)), lambda a,b: ((a[0]+b[0]) % 3,(a[1]+b[1]) % 3)),
              [[[1,0],[0,1]],[[0,1],[1,1]]]]  # Fibonacci ring
    records = []
    for a in cases:
        records.append(a)
        for _ in range(3):
            tail = list(range(1,len(a))); rng.shuffle(tail)
            records.append(relabel(a,[0]+tail))
        records.append(a)
    with tempfile.TemporaryDirectory(prefix="fusion_audit_test_") as directory:
        root = Path(directory); source = root / "input.txt"
        strings = [json.dumps(a) if i % 2 else json.dumps(a).replace('[','{').replace(']','}') for i,a in enumerate(records)]
        source.write_text("\n\n" + "\n\n".join(strings) + "\n", encoding="utf-8")
        for mode in ("fast", "exhaustive"):
            command = [str(binary), str(source), str(root/mode)]
            if mode == "exhaustive": command.append("--exhaustive")
            subprocess.run(command, check=True, capture_output=True, text=True)
            summary = json.loads((root/mode/"summary.json").read_text())
            if summary["distinct_rings"] != len(cases): raise ValueError("incorrect group/Fibonacci classification")
            verify(source, root/mode)
        for filename in ("counts.csv","FusionRingMultiplicationTables.deduplicated"):
            if (root/"fast"/filename).read_bytes() != (root/"exhaustive"/filename).read_bytes(): raise ValueError("fast and exhaustive disagree")
        invalid = ["{{{-1}}}", "{{{1000001}}}", "{{{2}}}", "[[[1,0],[0,1]]]", "{{{1}}} extra", ""]
        # Unital, nonnegative and reciprocal, but nonassociative: x^2=y^2=1, xy=0.
        a = [[[0]*3 for _ in range(3)] for _ in range(3)]
        for i in range(3): a[0][i][i]=a[i][0][i]=a[i][i][0]=1
        invalid.append(json.dumps(a))
        for i,text in enumerate(invalid):
            bad = root/f"bad{i}.txt"; bad.write_text(text, encoding="utf-8")
            target = root/f"badout{i}"
            process = subprocess.run([str(binary),str(bad),str(target)],capture_output=True,text=True)
            if process.returncode == 0 or (target/"summary.json").exists(): raise ValueError("invalid input not safely rejected")
        process = subprocess.run([str(binary),str(source),str(root/"fast")],capture_output=True,text=True)
        if process.returncode == 0: raise ValueError("nonempty output directory overwritten")
    return {"passed":True,"known_isomorphism_classes":len(cases),"labelled_test_records":len(records),
            "invalid_inputs_rejected":len(invalid),"noncommutative_group_test":True,
            "both_canonical_modes_tested":True,"independent_python_witness_checks":True,
            "overwrite_protection_tested":True,"random_seed":20260918}

if __name__ == "__main__":
    if len(sys.argv)!=2: raise SystemExit(__doc__)
    result=run_tests(Path(sys.argv[1]).resolve())
    print(json.dumps(result,indent=2))
