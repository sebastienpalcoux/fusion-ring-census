#!/usr/bin/env python3
"""Reorder the self-dual orbit system for first-matrix reconstruction."""
from build_system import system
import json,sys

def reordered(r):
 s=system(r,0); old=s['orbits']; owner={tuple(t):i for i,o in enumerate(old) for t in o}
 n=r-2
 first=[owner[1,1,i] for i in range(2,r)]
 first += [owner[1,i,i] for i in range(2,r)]
 first += [owner[1,i,j] for i in range(2,r) for j in range(i+1,r)]
 first += [owner[1,1,1]]
 order=first+[i for i in range(len(old)) if i not in first]
 to_new={v:i for i,v in enumerate(order)}
 s['orbits']=[old[i] for i in order]
 s['equations']=[[(to_new[a] if a>=0 else a,to_new[b] if b>=0 else b,c) for a,b,c in e] for e in s['equations']]
 s['perms']=[[to_new[p[i]] for i in order] for p in s['perms']]
 s['parameter_order']='u; diagonal of Q; strict upper triangle of Q; a; symmetric tail triples'
 return s

def write(s,path):
 with open(path,'w') as f:
  print(s['rank'],s['pairs'],len(s['orbits']),len(s['equations']),len(s['perms']),file=f)
  for e in s['equations']: print(len(e),*(z for t in e for z in t),file=f)
  for p in s['perms']: print(*p,file=f)
 with open(str(path)+'.json','w') as f:json.dump(s,f)
if __name__=='__main__':write(reordered(int(sys.argv[1])),sys.argv[2])
