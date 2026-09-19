// C++17, ranks 4--8, multiplicity 1--15. No source database is read.
// Generated with AI assistance; independent verification and proof supplied.
// Exact bounded enumeration of based rings. Input equations generated from axioms.
#include <algorithm>
#include <functional>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <vector>
using Mask=uint32_t;
struct Term {int a,b,c;};
struct Equation{std::vector<Term> ts; std::vector<int> vs;};
class CompletionSolver {
public:
int rank_,pairs_,nv,M;std::vector<Equation> eqs;std::vector<std::vector<int>> perms,inc;
std::vector<Mask> dom;std::vector<std::pair<int,Mask>> trail;
unsigned long long nodes=0,sols=0;std::vector<unsigned long long> counts;
std::chrono::steady_clock::time_point start=std::chrono::steady_clock::now();double maxseconds=60;bool stopped=false;
int low(Mask m){return __builtin_ctz(m);}int high(Mask m){return 31-__builtin_clz(m);}bool single(Mask m){return !(m&(m-1));}
int value(int a){return a<0?1:low(dom[a]);}
bool update(int v,Mask m,std::vector<int>&q,std::vector<char>&inq){
 m&=dom[v];if(!m)return false;if(m==dom[v])return true;
 trail.emplace_back(v,dom[v]);dom[v]=m;
 for(int e:inc[v])if(!inq[e]){inq[e]=1;q.push_back(e);}return true;
}
long long exact(const Equation&e){long long s=0;for(auto&t:e.ts)s+=(long long)t.c*value(t.a)*value(t.b);return s;}
// Modular linear consequences are necessary conditions, not rational approximations.
// The prime exceeds the entire domain; a one-variable congruence fixes that variable.
static constexpr int prime=257;int inverse_[prime];
bool gauss(std::vector<int>&q,std::vector<char>&inq){
 std::vector<int> idx(nv),vs(nv); int n=0;
 for(int v=0;v<nv;v++){idx[v]=-1;if(!single(dom[v])){idx[v]=n;vs[n++]=v;}}
 if(n<3)return true;
 for(int v=0;v<rank_*(rank_-1)/2-(pairs_==0);v++)if(!single(dom[v]))return true;
 std::vector<std::vector<int>> A; A.reserve(eqs.size()); int rows=0;
 for(auto&e:eqs){
  std::vector<int> row(n+1,0); bool nonlinear=false;
  for(auto&t:e.ts){
   int a=t.a<0?-1:idx[t.a],b=t.b<0?-1:idx[t.b];
   if(a>=0&&b>=0){nonlinear=true;break;}
   if(a>=0)row[a]+=t.c*value(t.b);
   else if(b>=0)row[b]+=t.c*value(t.a);
   else row[n]+=t.c*value(t.a)*value(t.b);
  }
  if(nonlinear)continue;
  bool nonzero=false;for(int j=0;j<=n;j++){row[j]=(row[j]%prime+prime)%prime;nonzero|=row[j]!=0;}
  if(nonzero){A.push_back(std::move(row));++rows;}
 }
 int h=0; std::vector<int> piv(n);
 for(int j=0;j<n&&h<rows;j++){
  int k=h;while(k<rows&&A[k][j]==0)k++;if(k==rows)continue;
  if(k!=h)for(int z=j;z<=n;z++)std::swap(A[k][z],A[h][z]);
  int inv=inverse_[A[h][j]];
  for(int z=j;z<=n;z++)A[h][z]=(A[h][z]*inv)%prime;
  for(int k2=0;k2<rows;k2++)if(k2!=h&&A[k2][j]){
   int factor=A[k2][j];A[k2][j]=0;
   for(int z=j+1;z<=n;z++)A[k2][z]=(A[k2][z]+prime*prime-factor*A[h][z])%prime;
  }
  piv[h++]=j;
 }
 for(int k=h;k<rows;k++)if(A[k][n])return false;
 for(int k=0;k<h;k++){
  int freecol=-1,freecnt=0;
  for(int j=piv[k]+1;j<n;j++)if(A[k][j]){freecol=j;freecnt++;}
  if(freecnt==0){int val=(prime-A[k][n])%prime;if(val>M)return false;if(!update(vs[piv[k]],1u<<val,q,inq))return false;}
  else if(freecnt==1){
   int x=vs[piv[k]],y=vs[freecol];Mask sx=0,sy=0;
   for(Mask d=dom[y];d;d&=d-1){int yv=low(d);int xv=(prime*prime-A[k][n]-A[k][freecol]*yv)%prime;
    if(xv<=M&&(dom[x]&(1u<<xv))){sx|=1u<<xv;sy|=1u<<yv;}}
   if(!update(x,sx,q,inq)||!update(y,sy,q,inq))return false;
  }
 }
 return true;
}
bool propagate(int changed){
 std::vector<int> q;std::vector<char> inq(eqs.size(),0);
 if(changed<0){q.resize(eqs.size());std::iota(q.begin(),q.end(),0);std::fill(inq.begin(),inq.end(),1);}
 else for(int e:inc[changed]){q.push_back(e);inq[e]=1;}
 size_t pos=0;bool again=true;
 while(again){again=false;
 if(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>maxseconds){stopped=true;return false;}
 for(;pos<q.size();pos++){
  int ei=q[pos];inq[ei]=0;auto&e=eqs[ei];int x=-1,y=-1,n=0;
  for(int v:e.vs)if(!single(dom[v])){if(n==0)x=v;else if(n==1)y=v;n++;}
  if(n==0){if(exact(e))return false;continue;}
  if(n<=2){
   Mask dx=dom[x],dy=y<0?1:dom[y],sx=0,sy=0;
   for(Mask a=dx;a;a&=a-1){Mask ax=a&-a;dom[x]=ax;
    for(Mask b=dy;b;b&=b-1){Mask by=b&-b;if(y>=0)dom[y]=by;
     if(exact(e)==0){sx|=ax;sy|=by;}
    }
   }
   dom[x]=dx;if(y>=0)dom[y]=dy;
   if(!update(x,sx,q,inq))return false;if(y>=0&&!update(y,sy,q,inq))return false;
  }else{
   long long lo=0,hi=0;
   for(auto&t:e.ts){int al=t.a<0?1:low(dom[t.a]),ah=t.a<0?1:high(dom[t.a]);int bl=t.b<0?1:low(dom[t.b]),bh=t.b<0?1:high(dom[t.b]);
    if(t.c>0){lo+=(long long)t.c*al*bl;hi+=(long long)t.c*ah*bh;}else{lo+=(long long)t.c*ah*bh;hi+=(long long)t.c*al*bl;}}
   if(lo>0||hi<0)return false;
  }
 }
 size_t before=q.size();if(!gauss(q,inq))return false;if(q.size()!=before)again=true;
 for(auto&p:perms){for(int k=0;k<nv;k++){
  int j=p[k];if(j==k)continue;
  if(low(dom[k])>high(dom[j]))return false;
  if(high(dom[k])<low(dom[j]))break;
  if(single(dom[k])&&dom[k]==dom[j])continue;
  Mask a=dom[k]&((1u<<(high(dom[j])+1))-1);
  Mask b=dom[j]&~((1u<<low(dom[k]))-1);
  if(a!=dom[k]||b!=dom[j])again=true;
  if(!update(k,a,q,inq)||!update(j,b,q,inq))return false;
  break;
 }}
 }
 return true;
}
bool canonical_partial(){
 for(auto&p:perms){for(int k=0;k<nv;k++){
  int j=p[k];if(j==k)continue;
  if(low(dom[k])>high(dom[j]))return false;
  if(high(dom[k])<low(dom[j]))break;
  if(single(dom[k])&&dom[k]==dom[j])continue;
  break;
 }}return true;
}
void search(int changed=-1){
 if(stopped)return;++nodes;
 if((nodes&4095)==0&&std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>maxseconds){stopped=true;return;}
 size_t mark=trail.size();
 if(propagate(changed)){
  int x=-1;
  for(int v=0;v<nv;v++)if(!single(dom[v])){x=v;break;}
  if(x<0){
   for(const auto &e:eqs)if(exact(e)!=0)throw std::logic_error("Internal error: nonassociative output");
   ++sols;int mu=1;for(Mask d:dom)mu=std::max(mu,low(d));++counts[mu];
   emit_line();
  }else{
   Mask old=dom[x];for(Mask a=old;a&&!stopped;a&=a-1){dom[x]=a&-a;search(x);}dom[x]=old;
  }
 }
 while(trail.size()>mark){auto[v,d]=trail.back();dom[v]=d;trail.pop_back();}
}

std::function<void(const std::vector<int>&)> output_callback;
void emit_line(){
 if(output_callback){std::vector<int> v;for(Mask d:dom)v.push_back(low(d));output_callback(v);return;}
 #pragma omp critical(output)
 {std::cout<<pairs_;for(Mask d:dom)std::cout<<' '<<low(d);std::cout<<'\n';}
}
CompletionSolver(const char *path,int bound,double seconds,std::chrono::steady_clock::time_point began,int unit_weight=1){
 std::ifstream in(path);int ne,np;in>>rank_>>pairs_>>nv>>ne>>np;
 if(!in||rank_<4||rank_>8||nv<1||nv>128||ne<1||ne>2048||bound<1||bound>15)throw std::runtime_error("invalid system");
 M=bound;maxseconds=seconds;start=began;
 eqs.resize(ne);inc.resize(nv);counts.resize(M+1);
 for(int i=0;i<ne;i++){auto&e=eqs[i];int nt;in>>nt;e.ts.resize(nt);for(auto&t:e.ts){in>>t.a>>t.b>>t.c;if(t.a>=0)e.vs.push_back(t.a);if(t.b>=0)e.vs.push_back(t.b);}std::sort(e.vs.begin(),e.vs.end());e.vs.erase(std::unique(e.vs.begin(),e.vs.end()),e.vs.end());for(int v:e.vs)inc[v].push_back(i);}
 perms.resize(np,std::vector<int>(nv));for(auto&p:perms)for(int&x:p)in>>x;
 if(!in)throw std::runtime_error("malformed system");
 for(auto&e:eqs)for(auto&t:e.ts)if(t.a==-1&&t.b==-1)t.c*=unit_weight;
 for(int i=1;i<prime;i++)for(int j=1;j<prime;j++)if(i*j%prime==1){inverse_[i]=j;break;}
 dom.assign(nv,(1u<<(M+1))-1);
}
void complete_prefix(const std::vector<int>&v){
 dom.assign(nv,(1u<<(M+1))-1);trail.clear();
 for(size_t i=0;i<v.size();++i)dom[i]=1u<<v[i];
 search();
}
bool accept(const std::vector<int>&v){
 for(int i=0;i<nv;++i)dom[i]=1u<<v[i];
 if(!canonical_partial())return false;
 for(const auto&e:eqs)if(exact(e)!=0)return false;
 ++sols;int mu=1;for(int z:v)mu=std::max(mu,z);++counts[mu];emit_line();return true;
}
};
