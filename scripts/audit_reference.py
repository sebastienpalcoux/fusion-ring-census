#!/usr/bin/env python3
"""Rerun the original-source deduplication with all deletion witnesses checked."""
import argparse,gzip,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 with tempfile.TemporaryDirectory(prefix='fusion-reference-') as d:
  src=Path(d)/'FusionRingMultiplicationTables'
  with gzip.open(ROOT/'audit/input/FusionRingMultiplicationTables.gz','rb') as f,src.open('wb') as g:shutil.copyfileobj(f,g)
  subprocess.run([sys.executable,str(ROOT/'audit/audit_fusion_rings.py'),str(src),'--out',str(a.out.resolve()),'--verify-witnesses'],check=True)
if __name__=='__main__':main()
