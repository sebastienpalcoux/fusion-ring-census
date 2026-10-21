#include "completion_solver.hpp"
#include <random>
int main(int argc,char**argv){
 std::mt19937 rng(41819);CompletionSolver c(argv[1],6,60,std::chrono::steady_clock::now());
 c.nv=7;c.dom.resize(7);c.inc.assign(7,{});std::vector<int>q;std::vector<char>inq;
 for(int trial=0;trial<20000;trial++){
  int n=3;c.M=1+rng()%6;std::vector<Mask> before(7);int unknown[4];
  for(int i=0;i<7;i++){if(i<n){unknown[i]=i;do{before[i]=rng()&((1u<<(c.M+1))-1);}while(__builtin_popcount(before[i])<2);}else before[i]=1u<<(rng()%(c.M+1));}
  c.dom=before;c.trail.clear();Equation e;int nt=1+rng()%20;
  for(int k=0;k<nt;k++){int a=int(rng()%8)-1,b=int(rng()%8)-1,co=int(rng()%7)-3;e.ts.push_back({a,b,co});}
  std::vector<Mask> expected(n,0);std::vector<int> vals(7);for(int i=n;i<7;i++)vals[i]=c.low(before[i]);
  auto enumerate=[&](auto&&self,int k)->void{if(k<n){for(Mask d=before[k];d;d&=d-1){vals[k]=c.low(d);self(self,k+1);}return;}long long z=0;for(auto t:e.ts)z+=(long long)t.c*(t.a<0?1:vals[t.a])*(t.b<0?1:vals[t.b]);if(!z)for(int i=0;i<n;i++)expected[i]|=1u<<vals[i];};
  enumerate(enumerate,0);bool ok=c.support_three(e,unknown,q,inq);
  if(ok!=(expected[0]!=0)){std::cerr<<"mismatch feasibility "<<trial<<'\n';return 1;}
  if(ok)for(int i=0;i<n;i++)if(c.dom[i]!=expected[i]){std::cerr<<"mismatch support "<<trial<<' '<<i<<'\n';return 1;}
 }
 std::cout<<"PASS 20000 random exact supports with arbitrary signs, repeated monomials, constants, squares, holes, and fixed variables\n";
}
