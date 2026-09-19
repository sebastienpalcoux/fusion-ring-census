#!/usr/bin/env python3
"""Compile/run the exact C++ audit and write a portable correction package.

Usage: python3 audit_fusion_rings.py FusionRingMultiplicationTables --out my_audit
Requires Python >= 3.9 and a C++17 compiler; no third-party Python packages.
Never edits the input, OEIS, or any remote database. All writes are local.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys
import time
import zipfile

ROOT = Path(__file__).resolve().parent
V4_SHA256 = "b587c3f683157369da7cc090f762bbff0e18dcf11acc3f5031d6bc0c643843f8"
SOURCE_URL = "https://arxiv.org/src/2205.15637v4/anc/FusionRingMultiplicationTables"
# These are the explicitly marked partial-search cells of Table 2, NOT inferred.
PARTIAL = {(5, m) for m in range(13, 17)} | {(6, m) for m in range(5, 9)} | {(7, 3), (7, 4), (8, 2)}


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def enrich(source: Path, out: Path, metadata: dict) -> None:
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    known = digest == V4_SHA256
    with (out / "counts.csv").open(newline="", encoding="utf-8") as stream:
        rows = [{k: int(v) for k, v in r.items()} for r in csv.DictReader(stream)]
    cells = {(r["rank"], r["multiplicity"]): r for r in rows}
    metadata.update(input_sha256=digest, expected_v4_sha256=V4_SHA256, known_v4_input=known,
                    source_url=SOURCE_URL, platform=platform.platform(), python=sys.version,
                    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    cpp_sha256=hashlib.sha256((ROOT / "dedup_fusion.cpp").read_bytes()).hexdigest())
    write_text(out / "provenance.json", json.dumps(metadata, indent=2) + "\n")
    summary = json.loads((out / "summary.json").read_text())
    note = ("These are isomorphism classes PRESENT IN THE INPUT, not an independent exhaustive generation. "
            "No changes have been submitted to OEIS.\n")
    if not known:
        write_text(out / "READ_ME_FIRST.txt", note + "Input checksum differs from the audited arXiv-v4 copy. "
                   "No published completeness labels or OEIS correction files were generated.\n")
    else:
        def count(rank: int, mult: int) -> int:
            if rank == 1 and mult > 1:
                return 0  # the unit is the unique rank-one basis element
            return cells[(rank, mult)]["distinct_rings"]
        table = ["# Corrected Table 2: distinct fusion rings", "",
                 "Source: Vercleyen--Slingerland, arXiv:2205.15637v4, Table 2 and ancillary database.", "",
                 "A trailing + preserves the paper's incomplete-search/lower-bound notation. "
                 "A dash means no count is supplied, not zero. Unmarked cells retain the "
                 "paper's completeness claims; this audit does not independently establish them.", "",
                 "| Multiplicity / rank | " + " | ".join(map(str, range(1, 10))) + " |",
                 "|---:" + "|---:" * 9 + "|"]
        tex = [r"\begin{tabular}{r|rrrrrrrrr}", r"$m\backslash r$ & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 \\", r"\hline"]
        for m in range(1, 17):
            entries = []
            for n in range(1, 10):
                if (n, m) in cells or n == 1:
                    entries.append(str(count(n, m)) + ("+" if (n, m) in PARTIAL else ""))
                else:
                    entries.append("-")
            table.append("| " + " | ".join([str(m)] + entries) + " |")
            tex.append(" & ".join([str(m)] + entries) + r" \\")
        tex.append(r"\end{tabular}")
        table += ["", "Only rank 5, multiplicities 9--12 change: 1463 -> 863; 1794 -> 1082; "
                  "2283 -> 1383; 3049 -> 1948.", "", note]
        write_text(out / "corrected_table.md", "\n".join(table))
        write_text(out / "corrected_table.tex", "\n".join(tex) + "\n")
        status_fields = list(rows[0]) + ["published_search_status"]
        with (out / "counts_with_status.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=status_fields)
            writer.writeheader()
            for r in rows:
                status = "partial_search_lower_bound" if (r["rank"], r["multiplicity"]) in PARTIAL else "reported_complete_not_independently_regenerated"
                writer.writerow(dict(r, published_search_status=status))
        oeis = out / "oeis"
        oeis.mkdir(exist_ok=True)
        snapshot = json.loads((ROOT / "oeis_snapshot.json").read_text())
        comparison = {}
        for ident, seq in snapshot["sequences"].items():
            corrected = [count(seq["fixed_rank"], k) if seq["axis"] == "multiplicity" else count(k, seq["fixed_multiplicity"])
                         for k in range(seq["offset"], seq["offset"] + len(seq["terms"]))]
            changes = [{"n": k, "old": old, "new": new} for k, (old, new) in enumerate(zip(seq["terms"], corrected), seq["offset"]) if old != new]
            comparison[ident] = {"numerical_changes": changes, "audited_terms": corrected}
        write_text(oeis / "comparison.json", json.dumps(comparison, indent=2) + "\n")
        seq = comparison["A354473"]["audited_terms"]
        write_text(oeis / "b354473.txt", "".join(f"{i} {x}\n" for i, x in enumerate(seq, 1)))
        sentence = "Terms a(9)-a(12) were corrected by removing repeated isomorphism classes from the ancillary database of Vercleyen and Slingerland (arXiv:2205.15637v4)."
        write_text(oeis / "A354473_edit.txt", "DRAFT ONLY - NOT SUBMITTED\n\nDATA (replace):\n" + ", ".join(map(str, seq)) +
                   "\n\nOFFSET (unchanged):\n1,1\n\nCOMMENT (replace the existing attribution sentence):\n"
                   "The original enumeration is due to J. Slingerland and G. Vercleyen (see Table 2 of the paper in the links).\n\n"
                   "COMMENT (add):\n" + sentence + "\n\nCHANGE LOG (optional, with submitter attribution):\n"
                   "a(9)-a(12) corrected by _Sébastien Palcoux_, Sep 18 2026.\n\n"
                   "B-FILE: replace with the attached b354473.txt (n=1..12).\n"
                   "Keep the other definitions, example, references, keywords and author unchanged.\n"
                   "Attach the audit code and certificates as supporting material, or add their public URL once available.\n"
                   "Do not extend this sequence with the incomplete database counts at multiplicities 13--16.\n")
        write_text(oeis / "editor_note.txt", f"Proposed correction of A354473; not yet submitted.\n\n"
                   f"Input: {SOURCE_URL}\nSHA-256: {digest}\n"
                   f"{summary['input_records']} records represent {summary['distinct_rings']} distinct based rings.\n"
                   f"Removed {summary['duplicates']} repetitions: {summary['literal_repeats']} exact labelled-tensor repeats "
                   f"and {summary['new_labellings']} further labellings.\n"
                   "All repetitions occur at rank 5, multiplicities 9,10,11,12.\n"
                   "Old counts: 1463,1794,2283,3049. New counts: 863,1082,1383,1948.\n"
                   "Deleted records: 600,712,900,1101 respectively.\n\n"
                   "Each tensor was checked for the fusion-ring axioms, including associativity, in exact integer arithmetic "
                   "in the default run. Isomorphisms are permutations of the distinguished basis fixing its unit. "
                   "The full ordered multiplication tensor is compared, so noncommutative rings are included.\n"
                   "Every removed line has a directly checked permutation witness in duplicates.csv. "
                   "For example, physical lines 11485 and 11486 are identical. "
                   "Line 11602 is isomorphic to line 11601 by the 0-based map [0,2,3,1,4].\n\n"
                   "The optimized canonical algorithm sorts isomorphism-invariant element signatures, then exhausts "
                   "permutations within tied cells. Its equality tests are exact, not probabilistic. "
                   "The --exhaustive switch instead tries all unit-fixing permutations.\n\n"
                   "This fixes duplicate counting within the enumeration; it does not independently re-prove "
                   "the completeness of the original search. No terms beyond n=12 are proposed here.\n"
                   "The six other sequence prefixes in comparison.json are unchanged.\n")
        write_text(out / "READ_ME_FIRST.txt", note + "See corrected_table.md, oeis/A354473_edit.txt, "
                   "oeis/b354473.txt, and duplicates.csv. The original input is never modified.\n")
    files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != "SHA256SUMS")
    write_text(out / "SHA256SUMS", "".join(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(out).as_posix()}\n" for p in files))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, default=Path("fusion_audit_output"))
    parser.add_argument("--cxx", help="C++17 compiler command (defaults to $CXX or c++/g++/clang++)")
    parser.add_argument("--exhaustive", action="store_true", help="try every unit-fixing permutation, bypassing signature pruning")
    parser.add_argument("--verify-witnesses", action="store_true", help="also run the independent Python verifier")
    args = parser.parse_args()
    try:
        source = args.input.resolve(strict=True)
        if not source.is_file():
            raise ValueError("input is not a regular file")
        out = args.out.resolve()
        if out.exists() and (not out.is_dir() or any(out.iterdir())):
            raise ValueError("output directory must be absent or empty; choose a new --out path")
        command = args.cxx or os.environ.get("CXX")
        if command:
            compiler = shlex.split(command)
        else:
            found = next((shutil.which(x) for x in ("c++", "g++", "clang++") if shutil.which(x)), None)
            if not found:
                raise ValueError("no C++17 compiler found; use --cxx or install your platform's C++ compiler")
            compiler = [found]
        executable = out.parent / (out.name + "_dedup_binary" + (".exe" if os.name == "nt" else ""))
        if executable.exists():
            raise ValueError(f"refusing to overwrite existing executable {executable}; choose a new --out path")
        out.parent.mkdir(parents=True, exist_ok=True)
        start = time.perf_counter()
        build = compiler + ["-O3", "-std=c++17", str(ROOT / "dedup_fusion.cpp"), "-o", str(executable)]
        subprocess.run(build, check=True)
        compile_time = time.perf_counter() - start
        command = [str(executable), str(source), str(out)]
        if args.exhaustive:
            command.append("--exhaustive")
        subprocess.run(command, check=True)
        version = subprocess.run(compiler + ["--version"], text=True, capture_output=True, check=True).stdout.splitlines()[0]
        if args.verify_witnesses:
            from verify_witnesses import verify
            result = verify(source, out)
            write_text(out / "python_verification.json", json.dumps(result, indent=2) + "\n")
            print(f"Independent Python witness verification passed in {result['elapsed_seconds']:.3f} seconds.")
        enrich(source, out, {"compiler": version, "build_command": build, "compile_seconds": compile_time,
                             "input_origin": "User-supplied local file; hash-pinned comparison to the archived arXiv-v4 ancillary copy."})
        archive = out.with_name(out.name + ".zip")
        if archive.exists():
            raise ValueError(f"refusing to overwrite {archive}; audit files are available in {out}")
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for p in sorted(out.rglob("*")):
                if p.is_file():
                    z.write(p, arcname=f"{out.name}/{p.relative_to(out).as_posix()}")
        print(f"Results: {out}\nReport archive: {archive}")
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"ERROR: {error}") from error

if __name__ == "__main__":
    main()
