#!/usr/bin/env python3
"""Create the requested repository through the user's authenticated GitHub CLI.

Default visibility is private: unpublished manuscripts are not made public
implicitly. Pass --public deliberately to publish them publicly. No credentials
are accepted on the command line, printed, or stored by this script.
"""
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DESCRIPTION='Exact fusion-ring censuses in ranks 3–8: data, proofs, fast C++ generators, independent verification and OEIS tables.'

def run(args: list[str], capture: bool=False):
    return subprocess.run(args,cwd=ROOT,check=True,text=True,stdout=subprocess.PIPE if capture else None)

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--name',default='fusion-ring-census');ap.add_argument('--public',action='store_true')
    ap.add_argument('--run-census',action='store_true',help='Dispatch the manual 20-minute-per-rank frontier workflow once')
    a=ap.parse_args()
    if not shutil.which('gh') or not shutil.which('git'):
        ap.error('Install GitHub CLI and Git, then authenticate using: gh auth login')
    run(['gh','auth','status'])
    login=run(['gh','api','user','--jq','.login'],True).stdout.strip()
    if login!='sebastienpalcoux':ap.error(f'Authenticated as {login!r}, not sebastienpalcoux; refusing to publish to a different account')
    if '/' in a.name or not a.name or any(c not in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._' for c in a.name):
        ap.error('invalid repository name')
    remote=f'{login}/{a.name}'
    probe=subprocess.run(['gh','repo','view',remote,'--json','nameWithOwner'],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if probe.returncode==0:ap.error(f'{remote} already exists; no overwrite or force-push is performed')
    run([sys.executable,'scripts/check_release.py'])
    if not (ROOT/'.git').exists():
        run(['git','init','-b','main']);run(['git','config','user.name','Sebastien Palcoux']);run(['git','config','user.email','sebastienpalcoux@gmail.com'])
        run(['git','add','.']);run(['git','commit','-m','Initial reproducible census release, ranks 3–8'])
    if run(['git','status','--porcelain'],True).stdout.strip():ap.error('local repository has uncommitted changes; commit them before publication')
    run(['gh','auth','setup-git'])
    run(['gh','repo','create',remote,'--public' if a.public else '--private','--source','.',
         '--remote','origin','--push','--description',DESCRIPTION])
    run(['gh','repo','edit',remote,'--default-branch','main'])
    # Read back the created repository; print only its observed canonical URL.
    info=json.loads(run(['gh','repo','view',remote,'--json','url,nameWithOwner,visibility'],True).stdout)
    for topic in ('fusion-rings','tensor-categories','computational-algebra','oeis','reproducible-research'):
        run(['gh','repo','edit',remote,'--add-topic',topic])
    print(json.dumps(info,indent=2))
    if a.run_census:
        run(['gh','workflow','run','frontier.yml','--repo',remote,'--ref','main','-f','ranks=all'])
        print('Frontier workflow dispatch accepted. Check Actions for its actual completion and artifacts; no results are asserted here.')
    return 0
if __name__=='__main__':raise SystemExit(main())
