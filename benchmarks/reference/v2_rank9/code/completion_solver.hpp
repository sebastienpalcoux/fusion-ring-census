// C++17, ranks 4--9, multiplicity 1--15 (rank 9: multiplicity 1 only).
// No source database is read.
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
// Propagation is complete before recursive search starts, so these scratch
// buffers can safely be reused at every search node within one worker.
std::vector<int> queue_, indices_, variables_, pivots_, matrix_;
std::vector<char> queued_;
struct Interval {long long il,ih,ll,lh,sq,linear;};
std::vector<Interval> intervals_;
std::vector<std::vector<std::pair<int,int>>> symmetries_;
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
 auto&idx=indices_;auto&vs=variables_;int n=0;
 for(int v=0;v<nv;v++){idx[v]=-1;if(!single(dom[v])){idx[v]=n;vs[n++]=v;}}
 if(n<3)return true;
 // Every currently linear equation gives a necessary modular consequence.
 // Apply it immediately, independent of which prefix variables are fixed.
 auto&A=matrix_;int stride=n+1;A.resize(eqs.size()*stride);int rows=0;
 for(auto&e:eqs){
  int*row=A.data()+rows*stride;std::fill(row,row+stride,0);bool nonlinear=false;
  for(auto&t:e.ts){
   int a=t.a<0?-1:idx[t.a],b=t.b<0?-1:idx[t.b];
   if(a>=0&&b>=0){nonlinear=true;break;}
   if(a>=0)row[a]+=t.c*value(t.b);
   else if(b>=0)row[b]+=t.c*value(t.a);
   else row[n]+=t.c*value(t.a)*value(t.b);
  }
  if(nonlinear)continue;
  bool nonzero=false;for(int j=0;j<=n;j++){row[j]=(row[j]%prime+prime)%prime;nonzero|=row[j]!=0;}
  if(nonzero)++rows;
 }
 int h=0;auto&piv=pivots_;
 for(int j=0;j<n&&h<rows;j++){
  int k=h;while(k<rows&&A[(k)*stride+(j)]==0)k++;if(k==rows)continue;
  if(k!=h)for(int z=j;z<=n;z++)std::swap(A[(k)*stride+(z)],A[(h)*stride+(z)]);
  int inv=inverse_[A[(h)*stride+(j)]];
  for(int z=j;z<=n;z++)A[(h)*stride+(z)]=(A[(h)*stride+(z)]*inv)%prime;
  for(int k2=0;k2<rows;k2++)if(k2!=h&&A[(k2)*stride+(j)]){
   int factor=A[(k2)*stride+(j)];A[(k2)*stride+(j)]=0;
   for(int z=j+1;z<=n;z++)A[(k2)*stride+(z)]=(A[(k2)*stride+(z)]+prime*prime-factor*A[(h)*stride+(z)])%prime;
  }
  piv[h++]=j;
 }
 for(int k=h;k<rows;k++)if(A[(k)*stride+(n)])return false;
 for(int k=0;k<h;k++){
  int freecol=-1,freecnt=0;
  for(int j=piv[k]+1;j<n;j++)if(A[(k)*stride+(j)]){freecol=j;freecnt++;}
  if(freecnt==0){int val=(prime-A[(k)*stride+(n)])%prime;if(val>M)return false;if(!update(vs[piv[k]],1u<<val,q,inq))return false;}
  else if(freecnt==1){
   int x=vs[piv[k]],y=vs[freecol];Mask sx=0,sy=0;
   for(Mask d=dom[y];d;d&=d-1){int yv=low(d);int xv=(prime*prime-A[(k)*stride+(n)]-A[(k)*stride+(freecol)]*yv)%prime;
    if(xv<=M&&(dom[x]&(1u<<xv))){sx|=1u<<xv;sy|=1u<<yv;}}
   if(!update(x,sx,q,inq)||!update(y,sy,q,inq))return false;
  }else if(freecnt<=3){
   int vv[3],aa[3],cc=0;Mask support[3]={0,0,0},sx=0;
   for(int j=piv[k]+1;j<n;j++)if(A[k*stride+j]){vv[cc]=vs[j];aa[cc++]=A[k*stride+j];}
   int pvar=vs[piv[k]],constant=A[k*stride+n];
   for(Mask a=dom[vv[0]];a;a&=a-1){int av=low(a);
    for(Mask b=dom[vv[1]];b;b&=b-1){int bv=low(b);
     if(freecnt==2){int xv=(prime*prime-constant-aa[0]*av-aa[1]*bv)%prime;
      if(xv<=M&&(dom[pvar]&(1u<<xv))){sx|=1u<<xv;support[0]|=a&-a;support[1]|=b&-b;}
     }else for(Mask c=dom[vv[2]];c;c&=c-1){int cv=low(c);int xv=(prime*prime-constant-aa[0]*av-aa[1]*bv-aa[2]*cv)%prime;
      if(xv<=M&&(dom[pvar]&(1u<<xv))){sx|=1u<<xv;support[0]|=a&-a;support[1]|=b&-b;support[2]|=c&-c;}
     }
    }
   }
   if(!update(pvar,sx,q,inq))return false;
   for(int j=0;j<freecnt;j++)if(!update(vv[j],support[j],q,inq))return false;

  }
 }
 return true;
}

 bool support_three(const Equation& e,const int *unknown,std::vector<int>&q,std::vector<char>&inq){
  constexpr int n=3;int v[3];Mask support[3]{};long long c=0,L[3]{},H[3][3]{};
  for(int i=0;i<n;i++)v[i]=unknown[i];
  // Prefer a variable without a square as the last variable, then a larger domain.
  int squares[3]{};for(const auto&t:e.ts)if(t.a==t.b)for(int i=0;i<n;i++)if(t.a==v[i])squares[i]+=t.c;
  int last=n-1;for(int i=0;i<n;i++)if((squares[i]==0&&squares[last]!=0)||((squares[i]==0)==(squares[last]==0)&&__builtin_popcount(dom[v[i]])>__builtin_popcount(dom[v[last]])))last=i;
  std::swap(v[last],v[n-1]);
  for(const auto&t:e.ts){int a=-1,b=-1;for(int i=0;i<n;i++){if(t.a==v[i])a=i;if(t.b==v[i])b=i;}
   if(a<0&&b<0)c+=(long long)t.c*value(t.a)*value(t.b);
   else if(a<0)L[b]+=(long long)t.c*value(t.a);
   else if(b<0)L[a]+=(long long)t.c*value(t.b);
   else H[std::min(a,b)][std::max(a,b)]+=t.c;
  }
  bool all=false;

   Mask d0=dom[v[0]],d1=dom[v[1]],d2=dom[v[2]];
   for(Mask dx=d0;dx&&!all;dx&=dx-1){int x=low(dx);long long c0=c+x*(L[0]+H[0][0]*x),l1=L[1]+H[0][1]*x,l2=L[2]+H[0][2]*x;
    for(Mask dy=d1;dy&&!all;dy&=dy-1){int y=low(dy);long long constant=c0+y*(l1+H[1][1]*y),linear=l2+H[1][2]*y;Mask sm=0;
     if(!H[2][2]){if(!linear){if(!constant)sm=d2;}else if(constant%linear==0){long long z=-constant/linear;if(z>=0&&z<=M&&(d2&(1u<<z)))sm=1u<<z;}}
     else for(Mask dz=d2;dz;dz&=dz-1){int z=low(dz);if(constant+z*(linear+H[2][2]*z)==0)sm|=dz&-dz;}
     if(sm){support[0]|=dx&-dx;support[1]|=dy&-dy;support[2]|=sm;all=support[0]==d0&&support[1]==d1&&support[2]==d2;}
    }
   }
  for(int i=0;i<n;i++)if(!update(v[i],support[i],q,inq))return false;
  return true;
 }

bool propagate(int changed){
 auto&q=queue_;auto&inq=queued_;q.clear();std::fill(inq.begin(),inq.end(),0);
 if(changed<0){q.resize(eqs.size());std::iota(q.begin(),q.end(),0);std::fill(inq.begin(),inq.end(),1);}
 else for(int e:inc[changed]){q.push_back(e);inq[e]=1;}
 size_t pos=0;bool again=true;
 while(again){again=false;
 if(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>maxseconds){stopped=true;return false;}
 for(;pos<q.size();pos++){
  int ei=q[pos];inq[ei]=0;auto&e=eqs[ei];int x=-1,y=-1,n=0;int unknown[3];
  for(int v:e.vs)if(!single(dom[v])){if(n==0)x=v;else if(n==1)y=v;if(n<3)unknown[n]=v;n++;}
  if(n==0){if(exact(e))return false;continue;}
  if(n==3){if(!support_three(e,unknown,q,inq))return false;}
  else if(n<=2){
   // Collect the polynomial once. Re-evaluating all original monomials for
   // every pair of domain values dominated completion of singular systems.
   long long c=0,lx=0,ly=0,xx=0,xy=0,yy=0;
   for(const auto&t:e.ts){
    if(t.a==x){if(t.b==x)xx+=t.c;else if(t.b==y&&y>=0)xy+=t.c;else lx+=(long long)t.c*value(t.b);}
    else if(t.b==x){if(t.a==y&&y>=0)xy+=t.c;else lx+=(long long)t.c*value(t.a);}
    else if(y>=0&&t.a==y){if(t.b==y)yy+=t.c;else ly+=(long long)t.c*value(t.b);}
    else if(y>=0&&t.b==y)ly+=(long long)t.c*value(t.a);
    else c+=(long long)t.c*value(t.a)*value(t.b);
   }
   Mask dx=dom[x],dy=y<0?1:dom[y],sx=0,sy=0;
   for(Mask a=dx;a;a&=a-1){int xv=low(a);Mask ax=a&-a;
    long long constant=c+xv*(lx+xx*xv);
    if(y<0){if(!constant)sx|=ax;continue;}
    long long linear=ly+xy*xv;
    if(!yy){
     if(!linear){if(!constant){sx|=ax;sy|=dy;}}
     else if(constant%linear==0){long long yv=-constant/linear;
      if(yv>=0&&yv<=M&&(dy&(1u<<yv))){sx|=ax;sy|=1u<<yv;}}
    }else for(Mask b=dy;b;b&=b-1){int yv=low(b);
     if(constant+yv*(linear+yy*yv)==0){sx|=ax;sy|=b&-b;}
    }
   }
   if(!update(x,sx,q,inq))return false;if(y>=0&&!update(y,sy,q,inq))return false;
  }else{
   long long lo=0,hi=0;
   for(int v:e.vs)intervals_[v]={0,0,0,0,0,0};
   for(const auto&t:e.ts){
    int al=t.a<0?1:low(dom[t.a]),ah=t.a<0?1:high(dom[t.a]);
    int bl=t.b<0?1:low(dom[t.b]),bh=t.b<0?1:high(dom[t.b]);
    if(al==ah&&bl==bh){long long z=(long long)t.c*al*bl;lo+=z;hi+=z;continue;}
    if(al==ah){intervals_[t.b].linear+=(long long)t.c*al;continue;}
    if(bl==bh){intervals_[t.a].linear+=(long long)t.c*bl;continue;}
    long long tl=(long long)t.c*(t.c>0?al*bl:ah*bh);
    long long th=(long long)t.c*(t.c>0?ah*bh:al*bl);
    lo+=tl;hi+=th;
    auto&a=intervals_[t.a];a.il+=tl;a.ih+=th;
    if(t.a==t.b)a.sq+=t.c;
    else{
     a.ll+=(long long)t.c*(t.c>0?bl:bh);a.lh+=(long long)t.c*(t.c>0?bh:bl);
     auto&b=intervals_[t.b];b.il+=tl;b.ih+=th;
     b.ll+=(long long)t.c*(t.c>0?al:ah);b.lh+=(long long)t.c*(t.c>0?ah:al);
    }
   }
   for(int v:e.vs)if(!single(dom[v])){
    auto&i=intervals_[v];long long c=i.linear;
    int a=low(dom[v]),b=high(dom[v]);
    long long tl=c*(c>0?a:b),th=c*(c>0?b:a);
    lo+=tl;hi+=th;i.il+=tl;i.ih+=th;i.ll+=c;i.lh+=c;
   }
   if(lo>0||hi<0)return false;
   // Every incident term is v^2*c or v times a linear expression.
   // Remove its old enclosure, then substitute each candidate value of v.
   // All bounds come from the pre-update domains, so sequential reductions
   // below can only weaken, never invalidate, this necessary condition.
   for(int v:e.vs)if(!single(dom[v])){
    const auto&i=intervals_[v];Mask keep=0;
    for(Mask d=dom[v];d;d&=d-1){int z=low(d);
     if(lo-i.il+z*(i.ll+i.sq*z)<=0&&hi-i.ih+z*(i.lh+i.sq*z)>=0)keep|=d&-d;
    }
    if(!update(v,keep,q,inq))return false;
   }

  }
 }
 size_t before=q.size();if(!gauss(q,inq))return false;if(q.size()!=before)again=true;
 for(const auto&p:symmetries_){for(auto[k,j]:p){
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
 for(const auto&p:symmetries_){for(auto[k,j]:p){
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
 if(!in||rank_<4||rank_>9||nv<1||nv>128||ne<1||ne>2048||bound<1||bound>15||(rank_==9&&bound!=1))throw std::runtime_error("invalid system");
 M=bound;maxseconds=seconds;start=began;
 eqs.resize(ne);inc.resize(nv);counts.resize(M+1);
 for(int i=0;i<ne;i++){auto&e=eqs[i];int nt;in>>nt;e.ts.resize(nt);for(auto&t:e.ts){in>>t.a>>t.b>>t.c;if(t.a>=0)e.vs.push_back(t.a);if(t.b>=0)e.vs.push_back(t.b);}std::sort(e.vs.begin(),e.vs.end());e.vs.erase(std::unique(e.vs.begin(),e.vs.end()),e.vs.end());for(int v:e.vs)inc[v].push_back(i);}
 perms.resize(np,std::vector<int>(nv));for(auto&p:perms)for(int&x:p)in>>x;
 if(!in)throw std::runtime_error("malformed system");
 for(auto&e:eqs)for(auto&t:e.ts)if(t.a==-1&&t.b==-1)t.c*=unit_weight;
 for(int i=1;i<prime;i++)for(int j=1;j<prime;j++)if(i*j%prime==1){inverse_[i]=j;break;}
 dom.assign(nv,(1u<<(M+1))-1);
 indices_.resize(nv);variables_.resize(nv);pivots_.resize(nv);intervals_.resize(nv);
 queue_.reserve(4*eqs.size());queued_.resize(eqs.size());
 for(const auto&p:perms){std::vector<std::pair<int,int>> moved;
  for(int k=0;k<nv;++k)if(p[k]!=k)moved.emplace_back(k,p[k]);
  if(!moved.empty())symmetries_.push_back(std::move(moved));}
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
