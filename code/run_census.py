#!/usr/bin/env python3
"""Recompute one complete rank-3--11 bounded census, independently of any database.

The shared --seconds allowance covers ALL enumeration strata of this rank.
Compilation, sorting/export, and optional independent verification are timed
separately. A timeout never produces a complete census or partial OEIS terms.
Requires Python 3.9+ and a C++17 compiler with OpenMP (g++ recommended).
"""
from __future__ import annotations
import csv
import argparse
import collections
import gzip
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT/'code'
SYSTEMS = ROOT/'systems'


def check_local_prefix(rank, bound, counts):
    baseline = json.loads((ROOT/'results/census.json').read_text())['ranks'].get(str(rank))
    if baseline is None:
        if rank in (9,10,11):
            return 0  # No released count for this rank to compare.
        raise ValueError('released baseline is missing')
    if not (baseline.get('complete') is True and baseline.get('verified') is True):
        raise ValueError('released baseline is not certified')
    through = min(bound, baseline['bound'])
    if any(counts.get(str(m)) != baseline['counts'].get(str(m)) for m in range(1, through+1)):
        raise ValueError('existing exact-multiplicity prefix mismatch')
    return through


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--rank', type=int, choices=range(3,12), required=True)
    ap.add_argument('--bound', type=int, required=True)
    ap.add_argument('--seconds', type=float, default=None)
    ap.add_argument('--local-unlimited', action='store_true',
                    help='Local laptop only: no clock limit; requires independent verification')
    ap.add_argument('--deadline', type=float, help='Parent monotonic wall-clock deadline; never reset between phases')
    ap.add_argument('--threads', type=int, default=min(64, len(os.sched_getaffinity(0))) if hasattr(os, 'sched_getaffinity') else min(64, os.cpu_count() or 1))
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--compiler', default=os.environ.get('CXX','g++'))
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--build-dir', type=Path, help='Content-keyed compilation cache; never used as census data')
    a = ap.parse_args()
    cap={3:1000,4:1000,5:32,6:15,7:15,8:15,9:15,10:15,11:15}[a.rank]
    if not 1 <= a.bound <= cap or not 1 <= a.threads <= 64:
        ap.error(f'bound must be in [1,{cap}]; threads in [1,64]')
    budget = a.seconds if a.seconds is not None else (60 if a.rank == 3 else 1200)
    limit = 4200
    if a.local_unlimited:
        if os.environ.get('GITHUB_ACTIONS') or not a.verify or a.seconds is not None or a.deadline is not None:
            ap.error('--local-unlimited requires --verify, local execution, and no other budget flags')
        budget = math.inf
    if not a.local_unlimited and (not math.isfinite(budget) or not 0 < budget <= limit):
        ap.error(f'--seconds must be finite, positive and at most {limit}')
    if a.deadline is not None and (not math.isfinite(a.deadline) or not 0 < a.deadline-time.monotonic() <= limit):
        ap.error(f'--deadline must be finite and within the next {limit} seconds')
    if a.out.exists() and any(a.out.iterdir()):
        ap.error('--out must be absent or empty')
    a.out=a.out.resolve()
    a.out.mkdir(parents=True,exist_ok=True)
    build=a.build_dir.resolve() if a.build_dir else a.out/'build'
    build.mkdir(parents=True,exist_ok=True)
    logs=a.out/'logs';logs.mkdir()
    raw=a.out/'diagnostics';raw.mkdir()
    report={'rank':a.rank,'bound':a.bound,'threads':a.threads,
            'enumeration_budget_seconds':None if a.local_unlimited else budget,
            'time_limit':'none (local laptop)' if a.local_unlimited else 'bounded',
            'environment':{'python':platform.python_version(),'system':platform.system()+' '+platform.release()+' '+platform.machine(),
                           'cpu_count':os.cpu_count(),'threads':a.threads},
            'complete':False,'verified':False,'runs':[],
            'github_sha':os.environ.get('GITHUB_SHA'),'github_run_id':os.environ.get('GITHUB_RUN_ID'),
            'deadline_monotonic':a.deadline,'phase':'initialization','commands':[]}
    env=dict(os.environ,OMP_NUM_THREADS=str(a.threads))
    started=time.monotonic()
    source_hash=hashlib.sha256()
    for path in sorted(CODE.rglob('*')):
        if path.is_file() and path.suffix in ('.cpp','.hpp','.py'):
            source_hash.update(str(path.relative_to(CODE)).encode());source_hash.update(path.read_bytes())
    report['code_sha256']=source_hash.hexdigest()

    def persist():
        report['elapsed_seconds']=time.monotonic()-started
        temp=a.out/'run.json.next'
        temp.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
        temp.replace(a.out/'run.json')

    def phase(name):
        report['phase']=name
        persist()

    def run_checked(cmd, **kwargs):
        item={'phase':report['phase'],'command':cmd,'started_elapsed_seconds':time.monotonic()-started}
        report['commands'].append(item);persist()
        if a.deadline is not None:
            remaining=a.deadline-time.monotonic()
            if remaining<=0:raise TimeoutError('shared wall-clock deadline exhausted')
            kwargs['timeout']=remaining
        st=time.monotonic()
        try:
            result=subprocess.run(cmd,check=True,**kwargs)
            item['returncode']=result.returncode
            return result
        except subprocess.TimeoutExpired as exc:
            item['timeout']=True
            raise TimeoutError('shared wall-clock deadline exhausted during '+report['phase']) from exc
        except subprocess.CalledProcessError as exc:
            item['returncode']=exc.returncode
            raise
        finally:
            item['elapsed_seconds']=time.monotonic()-st;persist()

    def compile_one(source: str, name: str, openmp: bool=True, defines=()) -> Path:
        dest=build/name
        stamp=build/(name+'.build.json')
        # Python/export/documentation edits do not invalidate a C++ executable.
        # Follow every local quoted include, including rank-five helper headers.
        dependencies=set()
        def include(path):
            path=path.resolve()
            if path in dependencies:return
            dependencies.add(path)
            for local in re.findall(r'^\s*#\s*include\s*"([^"]+)"',path.read_text(),re.MULTILINE):
                include(path.parent/local)
        include(CODE/source)
        digest=hashlib.sha256()
        for path in sorted(dependencies):
            digest.update(str(path.relative_to(CODE)).encode());digest.update(path.read_bytes())
        compiler_path=Path(shutil.which(a.compiler) or a.compiler).resolve()
        compiler_stat=compiler_path.stat()
        signature={'dependencies_sha256':digest.hexdigest(),'compiler':str(compiler_path),
                   'compiler_mtime_ns':compiler_stat.st_mtime_ns,'compiler_size':compiler_stat.st_size,
                   'source':source,'openmp':openmp,'defines':list(defines),'flags':['-O3','-std=c++17']}
        if dest.exists() and stamp.exists() and json.loads(stamp.read_text())==signature:
            if not os.access(dest, os.X_OK):
                dest.chmod(dest.stat().st_mode | 0o111)
            if not os.access(dest, os.X_OK):
                raise PermissionError('Compilation cache is not executable; choose --build-dir on a local executable filesystem')
            return dest
        phase('compilation:'+name)
        cmd=[a.compiler,'-O3','-std=c++17']+(['-fopenmp'] if openmp else [])+['-D'+d for d in defines]+[str(CODE/source),'-o',str(dest)]
        with (logs/(name+'_compile.log')).open('w') as log:
            run_checked(cmd,stdout=log,stderr=subprocess.STDOUT)
        dest.chmod(dest.stat().st_mode | 0o111)
        if not os.access(dest, os.X_OK):
            raise PermissionError('Compilation cache is not executable; choose --build-dir on a local executable filesystem')
        stamp.write_text(json.dumps(signature,indent=2)+'\n')
        return dest

    try:
        jobs=[]
        if a.rank==3:
            exe=compile_one('rank3_census.cpp','rank3',False)
            jobs=[('all',[str(exe),str(a.bound),'--emit'],None)]
        elif a.rank==4:
            exe=compile_one('rank4_census.cpp','rank4')
            jobs=[('all',[str(exe),str(a.bound)],None)]
        elif a.rank==5:
            ns=compile_one('rank5/enumerate_nonselfdual.cpp','rank5_ns')
            sd=compile_one('rank5/enumerate_selfdual.cpp','rank5_sd')
            jobs=[('nonselfdual',[str(ns),str(a.bound)],None),
                  ('selfdual',[str(sd),str(a.bound)],None)]
        else:
            # The adaptive frontier handles every nonselfdual involution type.
            general=None
            fast=compile_one('enumerate_selfdual_fast.cpp',f'selfdual_fast_r{a.rank}',defines=(f'CENSUS_SELFDUAL_RANK={a.rank}',))
            parallel=compile_one('enumerate_parallel.cpp','parallel_general')
            for p in range(1,(a.rank-1)//2+1):
                path=SYSTEMS/f'rank{a.rank}_pairs{p}.txt'
                jobs.append((f'pairs{p}',[str(parallel),str(path),str(a.bound),'TIME',str(a.threads),str(max(64,64*a.threads))],3))
            jobs.append(('selfdual',[str(fast),str(SYSTEMS/f'system{a.rank}sd.txt'),str(a.rank),str(a.bound),'TIME',str(a.threads)],4))
        report['compilation_seconds']=time.monotonic()-started
        report['expected_strata']=[job[0] for job in jobs]
        search_start=time.monotonic()
        files=[]
        for name,base,index in jobs:
            remaining=budget-(time.monotonic()-search_start)
            if remaining <= 0:
                raise TimeoutError('shared enumeration budget exhausted')
            cmd=list(base)
            if a.deadline is not None:
                remaining=min(remaining,a.deadline-time.monotonic())
                if remaining<=0:raise TimeoutError('shared wall-clock deadline exhausted')
            if index is not None:
                cmd[index]=str(max(0.001,remaining-0.05))
            output=raw/(name+'.parameters.txt');logpath=logs/(name+'.log')
            st=time.monotonic()
            phase('enumeration:'+name)
            entry={'name':name,'command':cmd,'allowance_seconds':None if a.local_unlimited else remaining}
            report['runs'].append(entry);persist()
            try:
                with output.open('w') as out,logpath.open('w') as log:
                    run=subprocess.run(cmd,stdout=out,stderr=log,env=env,timeout=None if a.local_unlimited else remaining)
                    out.flush();os.fsync(out.fileno())
                    log.flush();os.fsync(log.fileno())
                elapsed=time.monotonic()-st
                entry.update(elapsed_seconds=elapsed,returncode=run.returncode);persist()
                if run.returncode==3:
                    raise TimeoutError(f'{name} did not finish')
                if run.returncode:
                    raise RuntimeError(f'{name} failed: see {logpath}')
                if a.rank >= 6:
                    final=re.search(r'^FINAL\b.*\bcomplete 1\b.*\bclasses (\d+)\b.*\bcounts((?: \d+)+)\s*$',logpath.read_text(),re.MULTILINE)
                    if final is None:
                        raise ValueError(f'{name}: missing complete enumerator summary')
                    totals=list(map(int,final.group(2).split()))
                    if len(totals)!=a.bound or sum(totals)!=int(final.group(1)):
                        raise ValueError(f'{name}: inconsistent enumerator summary')
                    entry['reported_classes']=int(final.group(1))
                    entry['reported_counts']={str(m):totals[m-1] for m in range(1,a.bound+1)}
            except subprocess.TimeoutExpired as exc:
                entry.update(elapsed_seconds=time.monotonic()-st,timeout=True);persist()
                raise TimeoutError(f'{name} exceeded the shared enumeration budget') from exc
            files.append(output)
        report['enumeration_seconds']=time.monotonic()-search_start
        phase('sort_and_export')
        st=time.monotonic()
        rows=[];counts=collections.Counter()
        for path,entry in zip(files,report['runs']):
            stratum_counts=collections.Counter()
            for line in path.read_text().splitlines():
                tag,*words=line.split();v=tuple(map(int,words))
                if not v and a.rank==3 and tag=='C3':
                    rows.append((tag,v));counts[1]+=1;continue
                if not v or min(v)<0 or max(v)>a.bound:
                    raise ValueError('invalid enumerator output')
                rows.append((tag,v));counts[max(1,max(v))]+=1
                stratum_counts[max(1,max(v))]+=1
            if a.rank >= 6 and (sum(stratum_counts.values())!=entry['reported_classes'] or
                    any(stratum_counts[m]!=entry['reported_counts'][str(m)] for m in range(1,a.bound+1))):
                raise ValueError(f"{entry['name']}: output does not match enumerator totals")
        rows.sort()
        if len(rows)!=len(set(rows)):
            raise ValueError('literal parameter duplicate')
        params=a.out/'parameters.txt'
        with params.open('w') as out:
            for tag,v in rows:
                out.write(tag+' '+' '.join(map(str,v))+'\n')
        table=a.out/'FusionRingMultiplicationTables.txt'
        with (logs/'export.log').open('w') as log:
            run_checked([sys.executable,str(CODE/'export_tables.py'),'--rank',str(a.rank),
                         '--input',str(params),'--systems',str(SYSTEMS),'--output',str(table)],stdout=log,stderr=subprocess.STDOUT)
        report['counts']={str(m):counts[m] for m in range(1,a.bound+1)}
        report['classes']=sum(counts.values())
        with (a.out/'counts.csv').open('w') as f:
            f.write('rank,multiplicity,classes\n')
            for m in range(1,a.bound+1):f.write(f'{a.rank},{m},{counts[m]}\n')
        report['sort_export_seconds']=time.monotonic()-st
        if a.verify:
            st=time.monotonic();verifier=compile_one('verify_tables.cpp','verify_tables',False)
            report['verifier_compilation_seconds']=time.monotonic()-st
            st=time.monotonic()
            phase('independent_verification')
            with (logs/'verification.log').open('w') as log:
                run_checked([str(verifier),str(table),str(a.out/'independent_check')],stdout=log,stderr=subprocess.STDOUT)
            check=json.loads((a.out/'independent_check/summary.json').read_text())
            if (check['duplicates']!=0 or check['distinct_rings']!=len(rows)
                    or check.get('input_records')!=len(rows)
                    or check.get('associativity_checked') is not True
                    or check.get('canonical_mode')!='individualization-refinement (exact)'):
                raise ValueError('independent verification found duplicate or missing records')
            verified_counts={str(m):0 for m in range(1,a.bound+1)}
            with (a.out/'independent_check/counts.csv').open() as f:
                for row in csv.DictReader(f):
                    if int(row['rank'])!=a.rank or row['multiplicity'] not in verified_counts:
                        raise ValueError('independent verification found a wrong rank or multiplicity')
                    verified_counts[row['multiplicity']]=int(row['distinct_rings'])
            if verified_counts!=report['counts']:
                raise ValueError('independent exact-multiplicity counts do not match')
            report['independent_verification_seconds']=time.monotonic()-st
            report['independent_verification']=check
            if a.local_unlimited:
                report['existing_prefix_checked_through']=check_local_prefix(a.rank,a.bound,report['counts'])
                report['released_baseline_available']=report['existing_prefix_checked_through'] > 0
            report['verified']=True
        st=time.monotonic()
        phase('compression')
        for path in [params,table]:
            report[path.name+'_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
            with path.open('rb') as src,gzip.GzipFile(filename=str(path)+'.gz',mode='wb',mtime=0) as dst:
                shutil.copyfileobj(src,dst)
            path.unlink()
        report['compression_seconds']=time.monotonic()-st
        shutil.rmtree(raw)
        if a.deadline is not None and time.monotonic()>=a.deadline:
            raise TimeoutError('shared deadline reached before final completion')
        report['complete']=True
        report['outcome']='verified_complete' if a.verify else 'complete_unverified'
        phase('complete')
        print(json.dumps(report,indent=2))
        return 0
    except Exception as exc:
        report['complete']=False;report['verified']=False;report['error']=str(exc)
        report['failure_kind']='budget_exhausted' if isinstance(exc,TimeoutError) else 'error'
        report['error_type']=type(exc).__name__
        for filename in ('counts.csv','parameters.txt.gz','FusionRingMultiplicationTables.txt.gz'):
            (a.out/filename).unlink(missing_ok=True)
        report.pop('counts',None);report.pop('classes',None)
        persist()
        print(f'NOT A COMPLETE CENSUS: {exc}\nNo partial counts are certified.',file=sys.stderr)
        if not isinstance(exc,TimeoutError):traceback.print_exc()
        return 3 if isinstance(exc,TimeoutError) else 1

if __name__=='__main__':
    raise SystemExit(main())
