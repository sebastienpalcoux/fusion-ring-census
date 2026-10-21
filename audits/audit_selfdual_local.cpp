// Independent exhaustive checks of the new local pruning conditions.
#define main census_main_not_used
#include "../code/enumerate_selfdual_fast.cpp"
#undef main
#include <random>
#include <set>
#include <cassert>
static uint64_t masks_checked=0,witness_leaves=0,last_edges=0,rollbacks=0,pair_checks=0;
static std::mt19937 rng(19770506);
template<int N> void set_random(Worker<N>&w){
 for(int i=0;i<N;++i)w.u[i]=rng()%(w.M+1);
 std::sort(w.u,w.u+N);w.b=w.u[0];w.sum=std::accumulate(w.u,w.u+N,0);w.g=0;
 for(int i=0;i<N;++i){w.g=std::gcd(w.g,w.u[i]);w.Q[i][i]=w.b+rng()%(w.M-w.b+1);}
 for(auto[i,j]:w.edge)w.Q[i][j]=w.Q[j][i]=rng()%(w.M+1);
}
template<int N> void audit_rows(const char*system,int M,int C,int trials){
 Worker<N>w(system,M,C);
 for(int it=0;it<trials;++it){set_random(w);w.prepare_masks();
  for(int i=0;i<N;++i)for(int q=w.b;q<=M;++q){
   std::set<int> target;std::array<int,N> t{};
   auto enumerate=[&](auto&&self,int k)->void{
    if(k<N){for(int x=k==i?0:w.b;x<=M;++x){t[k]=x;self(self,k+1);}return;}
    std::array<int,N> mixed{};mixed[0]=q;int z=1,total=0;
    for(int k=0;k<N;++k){total+=w.u[k]*t[k];if(k!=i)mixed[z++]=t[k];}
    std::sort(mixed.begin(),mixed.end());
    if(!std::lexicographical_compare(mixed.begin(),mixed.end(),w.u,w.u+N))target.insert(total);
   };enumerate(enumerate,0);
   std::set<int>squares{0};
   for(int left=0;left<N;++left){
    for(int norm=0;norm<w.norm_length;++norm){uint32_t expected=0;
     for(int a=0;a<=M;++a){int base=norm+w.u[i]*w.u[i]-C-a*q;
      for(int sq:squares)if(target.count(base+sq)){expected|=1u<<a;break;}}
     auto got=w.row_masks[((i*(M+1)+q)*N+left)*w.norm_length+norm];
     if(got!=expected){std::cerr<<"ROW FAIL "<<N<<' '<<M<<' '<<C<<' '<<i<<' '<<q<<' '<<left<<' '<<norm<<' '<<got<<' '<<expected<<'\n';std::abort();}++masks_checked;
    }
    std::set<int>next;for(int sq:squares)for(int x=0;x<=M;++x)next.insert(sq+x*x);squares.swap(next);
   }
  }
 }
}
template<int N> void audit_witnesses(const char*system,int M,int C,int trials){
 Worker<N>w(system,M,C);
 struct Candidate{int a;std::array<int,N>t;};
 for(int it=0;it<trials;++it){set_random(w);uint32_t all=(1u<<(M+1))-1;
  std::vector<Candidate>candidates;std::array<int,N>t{};
  int qnorm=0;for(int i=0;i<N;++i)qnorm+=w.Q[0][i]*w.Q[0][i];
  for(int a=0;a<=M;++a){auto enumerate=[&](auto&&self,int k)->void{
   if(k<N){for(int x=k? w.b:0;x<=M;++x){t[k]=x;self(self,k+1);}return;}
   int weighted=0;for(int i=0;i<N;++i)weighted+=w.u[i]*t[i];
   if(weighted!=qnorm+w.u[0]*w.u[0]-C-a*w.Q[0][0])return;
   std::array<int,N>mixed=t;mixed[0]=w.Q[0][0];std::sort(mixed.begin(),mixed.end());
   if(std::lexicographical_compare(mixed.begin(),mixed.end(),w.u,w.u+N))return;
   candidates.push_back({a,t});
  };enumerate(enumerate,0);}
  w.build_witnesses(all);uint32_t initial=0;for(int wi:w.supported[N-1])initial|=1u<<w.witnesses[wi].a;
  auto recurse=[&](auto&&self,int k,uint32_t possible)->void{
   if(k==w.E){
    long long Qu[N]{},Q2[N][N]{},Q3_00=0,unorm=0;
    for(int i=0;i<N;++i){unorm+=w.u[i]*w.u[i];for(int j=0;j<N;++j)Qu[i]+=(long long)w.Q[i][j]*w.u[j];}
    for(int i=0;i<N;++i)for(int j=0;j<N;++j)for(int l=0;l<N;++l)Q2[i][j]+=(long long)w.Q[i][l]*w.Q[l][j];
    for(int j=0;j<N;++j)Q3_00+=Q2[0][j]*w.Q[j][0];
    uint32_t expected=0;for(const auto&cand:candidates){long long lhs=0;
     for(int j=0;j<N;++j)lhs+=Qu[j]*cand.t[j];
     long long rhs=Q3_00-C*w.Q[0][0]+2*w.u[0]*Qu[0]-unorm*w.Q[0][0]-cand.a*Q2[0][0];
     if(lhs==rhs)expected|=1u<<cand.a;
    }
    if(possible!=expected){std::cerr<<"WITNESS FAIL "<<N<<' '<<M<<' '<<C<<' '<<possible<<' '<<expected<<'\n';std::abort();}++witness_leaves;return;
   }
   if constexpr (Worker<N>::E-2>=N-1){if(k==w.E-2){
    w.build_pair_masks(possible);auto[i0,j0]=w.edge[w.E-2];auto[i1,j1]=w.edge[w.E-1];
    for(int x=0;x<=M;++x)for(int y=0;y<=M;++y){
     w.Q[i0][j0]=w.Q[j0][i0]=x;w.Q[i1][j1]=w.Q[j1][i1]=y;
     long long Qu[N]{},Q2[N][N]{},Q2u[N]{},Q3_00=0,Q4_00=0,unorm=0,uQu=0;
     for(int i=0;i<N;++i){unorm+=w.u[i]*w.u[i];for(int j=0;j<N;++j)Qu[i]+=(long long)w.Q[i][j]*w.u[j];}
     for(int i=0;i<N;++i)for(int j=0;j<N;++j)for(int l=0;l<N;++l)Q2[i][j]+=(long long)w.Q[i][l]*w.Q[l][j];
     for(int j=0;j<N;++j){Q3_00+=Q2[0][j]*w.Q[j][0];Q4_00+=Q2[0][j]*Q2[0][j];uQu+=w.u[j]*Qu[j];for(int i=0;i<N;++i)Q2u[i]+=w.Q[i][j]*Qu[j];}
     uint32_t expected=0;for(const auto&cand:candidates){long long lhs1=0,lhs2=0;
      for(int j=0;j<N;++j){lhs1+=Qu[j]*cand.t[j];lhs2+=Q2u[j]*cand.t[j];}
      long long rhs1=Q3_00-C*w.Q[0][0]+2*w.u[0]*Qu[0]-unorm*w.Q[0][0]-cand.a*Q2[0][0];
      long long rhs2=Q4_00-C*Q2[0][0]+2*w.u[0]*Q2u[0]+Qu[0]*Qu[0]-unorm*Q2[0][0]-uQu*w.Q[0][0]-cand.a*Q3_00;
      if(lhs1==rhs1&&lhs2==rhs2)expected|=1u<<cand.a;
     }
     if(w.pair_masks[x][y]!=expected){std::cerr<<"PAIR FAIL "<<N<<' '<<M<<' '<<C<<' '<<x<<' '<<y<<' '<<w.pair_masks[x][y]<<' '<<expected<<'\n';std::abort();}++pair_checks;
    }
   }}
   uint32_t direct[16]{};
   if(k==w.E-1){for(int wi:w.supported[k]){const auto&ww=w.witnesses[wi];if(!(possible&(1u<<ww.a)))continue;int c=ww.coef[k],r=-ww.residual;
    if(c){if(r%c==0){int z=r/c;if(z>=0&&z<=M)direct[z]|=1u<<ww.a;}}
    else if(!r)for(int z=0;z<=M;++z)direct[z]|=1u<<ww.a;
   }}
   auto[i,j]=w.edge[k];
   for(int z=0;z<=M;++z){w.Q[i][j]=w.Q[j][i]=z;
    std::vector<int>before;for(auto&ww:w.witnesses)before.push_back(ww.residual);
    uint32_t keep=w.filter_witnesses(k,z,possible);
    if(k==w.E-1){if(keep!=direct[z])std::abort();++last_edges;}
    w.advance_witnesses(k,z,1);self(self,k+1,keep);w.advance_witnesses(k,z,-1);
    for(size_t wi=0;wi<before.size();++wi)if(before[wi]!=w.witnesses[wi].residual)std::abort();++rollbacks;
   }
  };recurse(recurse,N-1,initial);
 }
}
int main(int argc,char**argv){
 if(argc!=2)return 2;system_dir=argv[1];allowance=1e9;began=Clock::now();
 auto file=[&](int r){return system_dir+"/system"+std::to_string(r)+"sd.txt";};
 for(int C:{1,2})for(int M:{1,2,3}){
  audit_rows<2>(file(4).c_str(),M,C,10);audit_rows<3>(file(5).c_str(),M,C,10);
  audit_rows<4>(file(6).c_str(),M,C,10);audit_rows<5>(file(7).c_str(),M,C,10);audit_rows<6>(file(8).c_str(),M,C,10);
  audit_witnesses<2>(file(4).c_str(),M,C,40);audit_witnesses<3>(file(5).c_str(),M,C,40);
  audit_witnesses<4>(file(6).c_str(),M,C,40);
  if(M<=2)audit_witnesses<5>(file(7).c_str(),M,C,20);
  if(M==1)audit_witnesses<6>(file(8).c_str(),M,C,10);
 }
 std::cout<<"PASS row_masks="<<masks_checked<<" witness_completions="<<witness_leaves<<" final_edge_masks="<<last_edges<<" residual_rollbacks="<<rollbacks<<" pair_masks="<<pair_checks<<" C=1,2 ranks=4..8 M=1..3 seed=19770506\n";
}
