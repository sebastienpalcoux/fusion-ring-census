#!/usr/bin/env python3
"""Run exact finite audits of the self-dual extension through rank 11."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='rank11-selfdual-audits-') as td:
        for source, arguments in (
            ('audit_partial_dot.cpp', [str(ROOT / 'systems')]),
            ('audit_graph_canonicality.cpp', [str(ROOT / 'systems')]),
            ('audit_identity_rank11.cpp', []),
        ):
            executable = Path(td) / Path(source).stem
            print(source, flush=True)
            subprocess.run([
                os.environ.get('CXX', 'g++'), '-O2', '-std=c++17', '-fopenmp',
                '-DCENSUS_SELFDUAL_RANK=4', str(ROOT / 'audits' / source),
                '-o', str(executable),
            ], check=True)
            subprocess.run([str(executable), *arguments], check=True)
    print('All rank-11 self-dual finite audits passed.')


if __name__ == '__main__':
    main()
