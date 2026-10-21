#!/usr/bin/env python3
"""Compile and run the independent finite-domain and moment audits."""
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    cases = [
        (ROOT/'tests/audit_optimized_pruning.cpp', [ROOT/'systems/system4sd.txt']),
        (ROOT/'tests/audit_exact3.cpp', [ROOT/'systems/system4sd.txt']),
        (ROOT/'tests/audit_gaussian.cpp', [ROOT/'systems/system4sd.txt']),
        (ROOT/'tests/audit_gaussian_domains.cpp', []),
        (ROOT/'audits/audit_selfdual_local.cpp', [ROOT/'systems']),
        (ROOT/'audits/audit_identity.cpp', []),
    ]
    with tempfile.TemporaryDirectory(prefix='fusion_audits_') as tmp:
        for source, args in cases:
            binary = Path(tmp)/source.stem
            print(source.name, flush=True)
            subprocess.run([os.environ.get('CXX', 'g++'), '-O2', '-std=c++17',
                            '-fopenmp', '-I', str(ROOT/'code'), str(source),
                            '-o', str(binary)], check=True)
            subprocess.run([str(binary), *map(str, args)], cwd=tmp, check=True)
    print('All independent audits passed.')


if __name__ == '__main__':
    main()
