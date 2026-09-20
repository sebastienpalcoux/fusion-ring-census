#!/usr/bin/env python3
"""Build a self-contained laptop archive from a clean Git checkout; no census runs."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile
ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if a.out.exists():ap.error('output exists')
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=ROOT,text=True)
    if status.strip():ap.error('commit reviewed changes first; package must identify exact clean sources')
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    with tempfile.TemporaryDirectory(prefix='fusion-laptop-package-') as td:
        package=Path(td)/'Fusion_Census_Laptop';package.mkdir()
        paths=[]
        for folder in ('code','systems','methods'):
            paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix not in ('.pyc','.pyo'))
        paths.extend(ROOT/p for p in ('scripts/run_laptop.py','results/census.json','tests/test_laptop.py','LICENSE','NOTICE.md','CITATION.cff'))
        for p in paths:
            target=package/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
        shutil.copy2(ROOT/'docs/LAPTOP.md',package/'README.md')
        (package/'SOURCE.json').write_text(json.dumps({'repository':'https://github.com/sebastienpalcoux/fusion-ring-census','commit':commit,'scope':'unmodified code, systems and methods from this revision; no tensor datasets bundled'},indent=2)+'\n')
        (package/'SHA256SUMS').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(package))+'\n' for p in sorted(package.rglob('*')) if p.is_file()))
        a.out.parent.mkdir(parents=True,exist_ok=True)
        with zipfile.ZipFile(a.out,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in sorted(package.rglob('*')):
                if p.is_file():z.write(p,str(Path('Fusion_Census_Laptop')/p.relative_to(package)))
    print(a.out.resolve())
if __name__=='__main__':main()
