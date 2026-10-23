#include <random>
#include <sstream>
#include <map>
#include "completion_solver.hpp"

using Vec=std::vector<int>;
Vec brute(const CompletionSolver&s,const Vec&v){
 Vec best=v,w(v.size());
 for(const auto&p:s.perms){for(size_t k=0;k<v.size();k++)w[k]=v[p[k]];if(w<best)best=w;}
 return best;
}
struct Raw{std::vector<std::vector<Term>> equations;};
Raw read_raw(const char*path){
 std::ifstream f(path);int rank,p,nv,ne,np;f>>rank>>p>>nv>>ne>>np;Raw raw;
 for(int i=0;i<ne;i++){int nt;f>>nt;std::vector<Term> terms(nt);for(auto&t:terms)f>>t.a>>t.b>>t.c;raw.equations.push_back(terms);}
 return raw;
}
long long raw_eval(const std::vector<Term>&e,const Vec&v,int weight){
 long long z=0;for(auto t:e)z+=(long long)t.c*(t.a<0?1:v[t.a])*(t.b<0?1:v[t.b])*(t.a<0&&t.b<0?weight:1);return z;
}
int main(int argc,char**argv){
 if(argc!=4)return 2;
 auto now=std::chrono::steady_clock::now();
 CompletionSolver explicit_s(argv[1],1,1e9,now),compact(argv[2],1,1e9,now),weight2(argv[2],1,1e9,now,2);
 if(explicit_s.compact_symmetry_||!compact.compact_symmetry_)return 3;
 auto raw=read_raw(argv[1]);std::mt19937 rng(817236);int corpus=0,samples=0,partials=0;
 auto check=[&](const Vec&v,bool valid){
  const Vec best=brute(explicit_s,v);
  if(compact.canonicalize(v)!=best)throw std::runtime_error("canonical minimum mismatch");
  if(compact.canonical_complete(v)!=(v==best))throw std::runtime_error("canonical predicate mismatch");
  if(!compact.canonical_complete(best))throw std::runtime_error("canonical minimum rejected");
  for(int rel=0;rel<3;rel++){
   const auto&p=explicit_s.perms[rng()%explicit_s.perms.size()];Vec w(v.size());for(size_t k=0;k<v.size();k++)w[k]=v[p[k]];
   if(compact.canonicalize(w)!=best)throw std::runtime_error("relabel minimum mismatch");
  }
  for(size_t j=0;j<v.size();j++){compact.dom[j]=1u<<v[j];weight2.dom[j]=1u<<v[j];}
  for(size_t e=0;e<raw.equations.size();e++){
   if(compact.exact(compact.eqs[e])!=raw_eval(raw.equations[e],v,1))throw std::runtime_error("Boolean reduction mismatch");
   if(weight2.exact(weight2.eqs[e])!=raw_eval(raw.equations[e],v,2))throw std::runtime_error("weighted Boolean reduction mismatch");
  }
  if(valid)for(int trial=0;trial<3;trial++){
   compact.trail.clear();for(size_t j=0;j<v.size();j++)compact.dom[j]=(rng()%3==0?1u<<best[j]:3);
   if(!compact.propagate(-1))throw std::runtime_error("valid partial domain rejected");
   for(size_t j=0;j<v.size();j++)if(!(compact.dom[j]&(1u<<best[j])))throw std::runtime_error("valid coefficient pruned");
   partials++;
  }
  samples++;
 };
 for(int trial=0;trial<100;trial++){
  Vec v(explicit_s.nv);for(int&x:v)x=trial<2?trial:int(rng()%2);check(v,false);
 }
 std::ifstream params(argv[3]);std::string line;
 while(std::getline(params,line)){std::istringstream f(line);int p;f>>p;if(p!=explicit_s.pairs_)continue;Vec v;int x;while(f>>x)v.push_back(x);if(v.size()!=size_t(explicit_s.nv))throw std::runtime_error("parameter size");check(v,true);corpus++;}
 std::cout<<"PASS rank="<<explicit_s.rank_<<" pairs="<<explicit_s.pairs_<<" group="<<explicit_s.perms.size()<<" corpus="<<corpus<<" vectors="<<samples<<" relabels="<<3*samples<<" partials="<<partials<<"\n";
}
