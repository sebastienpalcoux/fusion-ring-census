"""Exact verifier comparisons on known rings and adversarial relabellings."""
import csv
import io
import json
from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def group_tensor(n, product):
    return [[[int(product(i, j) == k) for k in range(n)] for j in range(n)] for i in range(n)]


def cyclic(n):
    return group_tensor(n, lambda i, j: (i+j) % n)


def dihedral(m):
    return group_tensor(2*m, lambda i, j: (i % m + (-1 if i//m else 1)*(j % m)) % m + m*((i//m+j//m) % 2))


def direct_product(t, u):
    a, b = len(t), len(u)
    return [[[t[i//b][j//b][k//b]*u[i % b][j % b][k % b] for k in range(a*b)] for j in range(a*b)] for i in range(a*b)]


ISING = [[[1,0,0],[0,1,0],[0,0,1]], [[0,1,0],[1,0,0],[0,0,1]], [[0,0,1],[0,0,1],[1,1,0]]]


def relabel(t, p):
    return [[[t[i][j][k] for k in p] for j in p] for i in p]


def variants(fixtures):
    rng = random.Random(20261023)
    records = []
    for tensor in fixtures:
        records.extend([tensor, tensor])  # Literal duplicates test a separate path.
        for _ in range(4):
            p = list(range(1, len(tensor)))
            rng.shuffle(p)
            records.append(relabel(tensor, [0]+p))
    return records


class VerifierRefinementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler = shutil.which('g++')
        if compiler is None:
            raise unittest.SkipTest('g++ is required for the independent verifier tests')
        cls.temp = tempfile.TemporaryDirectory()
        cls.executable = Path(cls.temp.name) / 'verify'
        subprocess.run([compiler, '-O2', '-std=c++17', str(ROOT/'code/verify_tables.cpp'), '-o', str(cls.executable)], check=True, capture_output=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def run_verifier(self, records, exhaustive=False):
        with tempfile.TemporaryDirectory() as td:
            source, out = Path(td)/'tables.txt', Path(td)/'out'
            source.write_text(''.join(json.dumps(t, separators=(',', ':'))+'\n' for t in records))
            cmd = [str(self.executable), str(source), str(out)] + (['--exhaustive'] if exhaustive else [])
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            summary = json.loads((out/'summary.json').read_text())
            counts = list(csv.DictReader(io.StringIO((out/'counts.csv').read_text())))
            mapping = list(csv.DictReader(io.StringIO((out/'line_map.csv').read_text())))
            # Independently check every reported source-to-representative witness.
            for row in mapping:
                a = records[int(row['source_line'])-1]
                b = records[int(row['representative_source_line'])-1]
                q = list(map(int, row['permutation_source_to_representative'].split(';')))
                self.assertEqual(q[0], 0)
                self.assertEqual(sorted(q), list(range(len(a))))
                self.assertEqual(a, relabel(b, q))
            return summary, counts, mapping

    def test_exact_partition_matches_exhaustive_through_rank8(self):
        fixtures = [cyclic(3), ISING, cyclic(4), direct_product(cyclic(2), cyclic(2)),
                    cyclic(5), cyclic(6), dihedral(3), cyclic(7), cyclic(8),
                    direct_product(cyclic(4), cyclic(2)), group_tensor(8, lambda i,j: i^j), dihedral(4)]
        records = variants(fixtures)
        fast, counts_fast, map_fast = self.run_verifier(records)
        slow, counts_slow, map_slow = self.run_verifier(records, exhaustive=True)
        self.assertEqual(fast['distinct_rings'], len(fixtures))
        self.assertEqual(counts_fast, counts_slow)
        keys = ('source_line', 'representative_source_line', 'clean_line', 'rank', 'multiplicity', 'kind')
        self.assertEqual([[r[k] for k in keys] for r in map_fast], [[r[k] for k in keys] for r in map_slow])
        self.assertEqual(fast['canonical_mode'], 'individualization-refinement (exact)')
        self.assertTrue(fast['associativity_checked'])
        self.assertLess(fast['permutations_examined'], slow['permutations_examined'])

    def test_rank9_to_11_relabellings_and_nonisomorphic_groups(self):
        fixtures = [cyclic(9), direct_product(cyclic(3), cyclic(3)), direct_product(ISING, ISING),
                    cyclic(10), dihedral(5), cyclic(11)]
        summary, counts, mapping = self.run_verifier(variants(fixtures))
        self.assertEqual(summary['distinct_rings'], len(fixtures))
        self.assertEqual(summary['input_records'], 6*len(fixtures))
        self.assertEqual(summary['duplicates'], 5*len(fixtures))
        self.assertEqual({int(r['rank']): int(r['distinct_rings']) for r in counts}, {9: 3, 10: 2, 11: 1})
        self.assertLess(summary['permutations_examined'], 10000)


if __name__ == '__main__':
    unittest.main()
