"""Small deterministic tests; the separate smoke script tests compiled programs."""
import importlib.util,itertools,json,math,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
build=module('builder','code/build_system.py');export=module('exporter','code/export_tables.py')
class CoreTests(unittest.TestCase):
 def test_coverage(self):
  data=json.loads((ROOT/'results/census.json').read_text());self.assertEqual(sorted(map(int,data['ranks'])),[3,4,5,6,7,8]);self.assertLessEqual(data['ranks']['3']['bound'],1000)
  for rank,item in data['ranks'].items():
   self.assertIs(item['complete'],True);self.assertIs(item['verified'],True)
   self.assertEqual(sorted(map(int,item['counts'])),list(range(1,item['bound']+1)));self.assertEqual(sum(item['counts'].values()),item['classes'])
 def test_duality_orbits(self):
  for r in range(4,9):
   for p in range((r-1)//2+1):
    s=build.system(r,p);self.assertEqual(len(s['perms']),2**p*math.factorial(p)*math.factorial(r-1-2*p))
    triples=[tuple(t) for orb in s['orbits'] for t in orb];self.assertEqual(len(triples),(r-1)**3);self.assertEqual(len(set(triples)),len(triples))
    if p==0:self.assertEqual(len(s['orbits']),math.comb(r+1,3))
 def test_rank8_workspace(self):
  s=build.system(8,0);self.assertEqual((len(s['orbits']),len(s['equations'])),(84,231));self.assertGreater(len(build.system(8,3)['equations']),200)
 def test_system_scope(self):
  for r,p in [(9,0),(3,0),(8,4),(6,-1)]:
   with self.assertRaises(ValueError):build.system(r,p)
 def test_cyclic_group_export(self):
  n=export.tensor(3,'C3',ROOT/'systems')
  for i,j,k in itertools.product(range(3),repeat=3):self.assertEqual(n[i][j][k],int((i+j)%3==k))
 def test_exporter_rejects_negative_and_bad_length(self):
  for line in ['S -1 0 1 0','S 1 2 3','C3 0']:
   with self.assertRaises(ValueError):export.tensor(3,line,ROOT/'systems')
 def test_rank3_scope_guard(self):
  with tempfile.TemporaryDirectory() as td:
   r=subprocess.run([sys.executable,str(ROOT/'code/run_census.py'),'--rank','3','--bound','1001','--out',td+'/bad'],capture_output=True,text=True)
   self.assertNotEqual(r.returncode,0);self.assertFalse((Path(td)/'bad/counts.csv').exists())
 def test_frontier_empty_budget(self):
  with tempfile.TemporaryDirectory() as td:
   r=subprocess.run([sys.executable,str(ROOT/'scripts/extend_census.py'),'--rank','8','--seconds','0.05','--out',td+'/frontier'],capture_output=True,text=True,timeout=10)
   self.assertEqual(r.returncode,0,r.stderr);out=Path(td)/'frontier';report=json.loads((out/'frontier.json').read_text())
   self.assertFalse((out/'best').exists());self.assertIsNone(report['best_verified_bound'])
 def test_oeis_projection(self):
  data=json.loads((ROOT/'results/census.json').read_text())
  for number,rank in [('354471',3),('354472',4),('354473',5)]:
   vals={int(a):int(b) for line in (ROOT/f'oeis/b{number}.txt').read_text().splitlines() if line and not line.startswith('#') for a,b in [line.split()]}
   self.assertEqual(vals,{int(k):v for k,v in data['ranks'][str(rank)]['counts'].items()})
if __name__=='__main__':unittest.main()
