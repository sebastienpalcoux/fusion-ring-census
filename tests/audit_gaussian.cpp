// Independent finite-domain audit of gauss(), before other propagation runs.
#include "completion_solver.hpp"
#include <random>
#include <set>
static std::mt19937 rng(8460218);
static int pick(int n){return int(rng()%unsigned(n));}
static long long eval(const Equation&e,const std::vector<int>&x){long long z=0;for(auto t:e.ts)z+=(long long)t.c*(t.a<0?1:x[t.a])*(t.b<0?1:x[t.b]);return z;}
static int mod(long long z){return int((z%257+257)%257);}
static void must(bool yes,const char*msg){if(!yes)throw std::runtime_error(msg);}
int main(int argc,char**argv){try{
 CompletionSolver c(argv[1],15,1e9,std::chrono::steady_clock::now());c.perms.clear();c.symmetries_.clear();
 unsigned long long assignments=0,solutions=0;int sat=0,unsat=0,one2=0,one3=0,changed=0;
 for(int trial=0;trial<12000;trial++){
  bool simple=trial<4000;int n=simple?(trial%2?3:4):3+pick(5),M=1+pick(15),ne=simple?1:1+pick(5);
  c.M=M;c.trail.clear();c.dom.assign(c.nv,1);std::vector<int> planted(c.nv);
  for(int v=0;v<c.nv;v++){planted[v]=pick(M+1);c.dom[v]=1u<<planted[v];}
  for(int v=0;v<n;v++){int count=std::min(M+1,2+pick(2));while(__builtin_popcount(c.dom[v])<count)c.dom[v]|=1u<<pick(M+1);}
  auto before=c.dom;c.eqs.assign(ne,{});c.inc.assign(c.nv,{});c.queued_.assign(ne,0);
  for(int ei=0;ei<ne;ei++){
   auto&e=c.eqs[ei];
   if(simple){for(int v=0;v<n;v++){int co=1+pick(256);if(pick(2))co=-co;e.ts.push_back({v,-1,co});e.vs.push_back(v);}}
   else{for(int t=0;t<3+pick(12);t++){int a=pick(c.nv+1)-1,b=-1,co=pick(2001)-1000;if(trial%3==0)b=n+pick(c.nv-n);e.ts.push_back({a,b,co});if(a>=0)e.vs.push_back(a);if(b>=0)e.vs.push_back(b);}}
   int constant=-int(eval(e,planted));if(trial%4==0)constant+=1+pick(256);e.ts.push_back({-1,-1,constant});
   std::sort(e.vs.begin(),e.vs.end());e.vs.erase(std::unique(e.vs.begin(),e.vs.end()),e.vs.end());for(int v:e.vs)c.inc[v].push_back(ei);
  }
  std::vector<Mask> support(c.nv);std::vector<int>x=planted;
  auto brute=[&](auto&&self,int v)->void{if(v==n){assignments++;for(const auto&e:c.eqs)if(mod(eval(e,x)))return;solutions++;for(int j=0;j<c.nv;j++)support[j]|=1u<<x[j];return;}for(Mask d=before[v];d;d&=d-1){x[v]=__builtin_ctz(d);self(self,v+1);}};brute(brute,0);
  std::vector<int>q;std::vector<char>inq(ne);bool ok=c.gauss(q,inq);if(support[0]){sat++;must(ok,"Gaussian rejected a modular solution");for(int v=0;v<c.nv;v++)must(!(support[v]&~c.dom[v]),"Gaussian removed a modular solution");}else unsat++;
  if(simple){must(ok==(support[0]!=0),"Single-row Gaussian feasibility mismatch");if(ok)must(c.dom==support,"Single-row Gaussian did not compute exact supports");if(n==3)one2++;else one3++;}
  if(ok&&c.dom!=before)changed++;
  // Domain restoration is what recursive search requires. Verify exact reversal.
  while(!c.trail.empty()){auto[v,d]=c.trail.back();c.trail.pop_back();c.dom[v]=d;}must(c.dom==before,"Gaussian trail did not restore domains");
 }
 std::cout<<"PASS Gaussian:12000 systems; "<<assignments<<" assignments; "<<solutions<<" modular solutions retained; "<<sat<<" satisfiable; "<<unsat<<" unsatisfiable; "<<one2<<" exact2-free rows; "<<one3<<" exact3-free rows; "<<changed<<" successful domain reductions; exact trail restoration\n";
 }catch(const std::exception&e){std::cerr<<"FAIL "<<e.what()<<'\n';return 1;}}
