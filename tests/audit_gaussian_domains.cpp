// Independent bounded exhaustive check of the modular Gaussian propagator.
// Every satisfying assignment modulo 257 must survive every domain reduction.
#include "completion_solver.hpp"
#include <random>
#include <cstdio>
int main(){
 const char*path="fusion_gauss_audit_system.txt";
 {std::ofstream f(path);f<<"4 1 6 1 0\n1 -1 -1 0\n";}
 CompletionSolver solver(path,5,10000,std::chrono::steady_clock::now());std::remove(path);
 std::mt19937 rng(682030);uint64_t cases=0,assignments=0,solutions=0;
 for(int trial=0;trial<5000;trial++){
  int n=3+rng()%4,M=1+rng()%5,m=1+rng()%n;solver.M=M;solver.eqs.assign(m,{});solver.inc.assign(6,{});solver.dom.assign(6,1);solver.trail.clear();
  int witness[6]={0};
  for(int v=0;v<n;v++){witness[v]=rng()%(M+1);Mask mask=1u<<witness[v];for(int a=0;a<=M;a++)if(rng()%3)mask|=1u<<a;solver.dom[v]=mask;}
  for(int k=0;k<m;k++){
   auto&e=solver.eqs[k];int c=0;
   for(int v=0;v<n;v++){int coef=int(rng()%13)-6;if(coef){e.ts.push_back({v,-1,coef});e.vs.push_back(v);solver.inc[v].push_back(k);c-=coef*witness[v];}}
   if(trial%3==0)c+=int(rng()%5)-2;
   e.ts.push_back({-1,-1,c});
  }
  auto before=solver.dom;std::vector<int>q;std::vector<char>inq(m);bool valid=solver.gauss(q,inq);int values[6]={0};
  auto enumerate=[&](auto&&self,int v)->void{
   if(v<n){for(Mask d=before[v];d;d&=d-1){values[v]=solver.low(d);self(self,v+1);}return;}
   assignments++;for(auto&e:solver.eqs){int sum=0;for(auto&t:e.ts)sum+=t.c*(t.a<0?1:values[t.a])*(t.b<0?1:values[t.b]);if(sum%257)return;}
   solutions++;if(!valid)throw std::runtime_error("Gaussian rejected a satisfying assignment");for(int j=0;j<n;j++)if(!(solver.dom[j]&(1u<<values[j])))throw std::runtime_error("Gaussian removed a supported value");
  };enumerate(enumerate,0);cases++;
 }
 std::cout<<"PASS cases="<<cases<<" assignments="<<assignments<<" modular_solutions="<<solutions<<"\n";
}
