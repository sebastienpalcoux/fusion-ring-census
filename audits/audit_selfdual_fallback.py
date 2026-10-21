#!/usr/bin/env python3
"""Force each witness cap and compare complete outputs with the normal caps."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'code' / 'enumerate_selfdual_fast.cpp'
HEADER = ROOT / 'code' / 'completion_solver.hpp'
source = SOURCE.read_text()
replacements = {
    'static constexpr size_t MAX_WITNESSES=4096;': 'inline static const size_t MAX_WITNESSES=std::getenv("AUDIT_WITNESS_CAP")?std::stoul(std::getenv("AUDIT_WITNESS_CAP")):4096;',
    'static constexpr int WITNESS_VISIT_LIMIT=200000;': 'inline static const int WITNESS_VISIT_LIMIT=std::getenv("AUDIT_VISIT_CAP")?std::stoi(std::getenv("AUDIT_VISIT_CAP")):200000;',
}
for old, new in replacements.items():
    if source.count(old) != 1:
        raise RuntimeError('The source changed: review the cap injection before running this audit.')
    source = source.replace(old, new)
source = '#include <cstdlib>\n' + source
report = {'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
          'header_sha256': hashlib.sha256(HEADER.read_bytes()).hexdigest(), 'checks': []}
with tempfile.TemporaryDirectory(prefix='fusion-cap-audit-') as directory:
    work = Path(directory)
    (work / 'audit.cpp').write_text(source)
    (work / 'completion_solver.hpp').write_bytes(HEADER.read_bytes())
    binary = work / 'audit'
    subprocess.run(['g++', '-O2', '-std=c++17', '-fopenmp', str(work / 'audit.cpp'), '-o', str(binary)], check=True)
    for rank, bound in [(6, 2), (7, 1)]:
        expected = None
        for name, options in [('normal', {}), ('stored_cap_1', {'AUDIT_WITNESS_CAP': '1'}), ('visit_cap_1', {'AUDIT_VISIT_CAP': '1'})]:
            environment = dict(os.environ)
            environment.pop('AUDIT_WITNESS_CAP', None)
            environment.pop('AUDIT_VISIT_CAP', None)
            environment.update(options)
            run = subprocess.run([str(binary), str(ROOT / 'systems' / f'system{rank}sd.txt'), str(rank), str(bound), '55', '1'],
                                 env=environment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True, timeout=60)
            lines = sorted(run.stdout.splitlines())
            if expected is None:
                expected = lines
            if lines != expected:
                raise AssertionError((rank, bound, name, 'output mismatch'))
            report['checks'].append({'rank': rank, 'bound': bound, 'mode': name, 'exact_match': True,
                                     'sorted_output_sha256': hashlib.sha256(('\n'.join(lines) + '\n').encode()).hexdigest(),
                                     'final_log': run.stderr.splitlines()[-1]})
print(json.dumps(report, indent=2))
