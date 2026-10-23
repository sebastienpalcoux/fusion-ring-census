"""Build exact associativity equations with unit and Frobenius reciprocity."""
import itertools,collections,json,argparse,math,os
from pathlib import Path

def system(r,pairs,compact=None):
 if not 4<=r<=11 or not 0<=pairs<=(r-1)//2:raise ValueError("rank 4..11; valid number of dual pairs required")
 if compact is None:compact=r>=9
 d=list(range(r))
 for i in range(1,2*pairs+1,2): d[i],d[i+1]=i+1,i
 triples=list(itertools.product(range(1,r),repeat=3))
 owner={};orbits=[]
 # N_ij^k = N_i*k^j = N_kj*^i; these imply anti-involution.
 for t in triples:
  if t in owner:continue
  orb={t};todo=[t]
  while todo:
   i,j,k=todo.pop()
   for u in [(d[i],k,j),(k,d[j],i)]:
    if u not in orb:orb.add(u);todo.append(u)
  for u in orb:owner[u]=len(orbits)
  orbits.append(sorted(orb))
 # Put a mixed coefficient first; every full orbit still has one lex minimum.
 # For self-dual rings move N_11^1 after the rest of the first multiplication slice.
 if pairs==0:
  first=r*(r-1)//2
  orbits=orbits[1:first]+orbits[:1]+orbits[first:]
  owner={t:i for i,o in enumerate(orbits) for t in o}
 def coefficient(i,j,k):
  if i==0:return -1 if j==k else -2
  if j==0:return -1 if i==k else -2
  if k==0:return -1 if d[i]==j else -2
  return owner[i,j,k]
 eqs=set()
 for i,j,k,l in itertools.product(range(1,r),repeat=4):
  eq=collections.Counter()
  for s in range(r):
   for c,a,b in [(1,coefficient(i,j,s),coefficient(s,k,l)),(-1,coefficient(j,k,s),coefficient(i,s,l))]:
    if a==-2 or b==-2:continue
    eq[tuple(sorted((a,b)))]+=c
  t=tuple((a,b,c) for (a,b),c in sorted(eq.items()) if c)
  if t:
   if t[0][2]<0:t=tuple((a,b,-c) for a,b,c in t)
   eqs.add(t)
 perms=[]
 if not compact:
  for p in itertools.permutations(range(1,r)):
   q=(0,)+p
   if any(q[d[i]]!=d[q[i]] for i in range(r)):continue
   perms.append([owner[q[o[0][0]],q[o[0][1]],q[o[0][2]]] for o in orbits])
 result={'rank':r,'pairs':pairs,'dual':d,'orbits':orbits,'equations':sorted(eqs),'perms':perms}
 if compact:
  result['symmetry_format']='duality-centralizer-v1'
  result['symmetry_order']=2**pairs*math.factorial(pairs)*math.factorial(r-1-2*pairs)
 return result

def atomic_text(path,text):
 path=Path(path);temporary=path.with_name(path.name+'.next')
 with temporary.open('w') as f:
  f.write(text);f.flush();os.fsync(f.fileno())
 temporary.replace(path)

def write_system(s,path):
 np=-1 if s.get('symmetry_format')=='duality-centralizer-v1' else len(s['perms'])
 lines=[' '.join(map(str,(s['rank'],s['pairs'],len(s['orbits']),len(s['equations']),np)))]
 for e in s['equations']:lines.append(' '.join(map(str,[len(e)]+[v for term in e for v in term])))
 if s.get('symmetry_format')=='duality-centralizer-v1':
  lines.append(' '.join(map(str,s['dual'])))
  lines.extend(' '.join(map(str,orbit[0])) for orbit in s['orbits'])
 else:
  lines.extend(' '.join(map(str,p)) for p in s['perms'])
 atomic_text(path,'\n'.join(lines)+'\n')
 atomic_text(str(path)+'.json',json.dumps(s,separators=(',',':'))+'\n')

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('rank',type=int);ap.add_argument('pairs',type=int);ap.add_argument('output');a=ap.parse_args();s=system(a.rank,a.pairs)
 write_system(s,a.output)
 print('variables',len(s['orbits']),'equations',len(s['equations']),'permutations',len(s['perms']))
