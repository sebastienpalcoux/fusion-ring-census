// Exact bounded self-dual fusion-ring enumeration by modular Krylov reconstruction.
// Singular reductions are completed by a separate exhaustive constraint solver.
#include <atomic>
#include <filesystem>
#include <functional>
#include <omp.h>
#include "completion_solver.hpp"
using Clock=std::chrono::steady_clock;
static std::atomic<bool> expired(false);
static Clock::time_point began;
static double allowance;
static std::string system_dir;
static int single_job=-1;

template<int P> struct FieldFilter {
 int inv[P]{}; uint32_t mask[P][P]{};
 explicit FieldFilter(int M){
  for(int i=1;i<P;++i)for(int j=1;j<P;++j)if(i*j%P==1){inv[i]=j;break;}
  for(int c=0;c<P;++c)for(int d=0;d<P;++d){int v=c;uint32_t w=0;
   for(int a=0;a<=M;++a){if(v<=M)w|=1u<<a;v+=d;if(v>=P)v-=P;}mask[c][d]=w;}
 }
};

template<int N> struct Worker {
 static constexpr int R=N+2, E=N*(N-1)/2, TOP=2*N+E+1;
 int M,C,b,sum,g,u[N]{},Q[N][N]{},norm[N]{},missing[N]{};
 std::array<std::pair<int,int>,E> edge;
 int edge_index[N][N]{};
 std::vector<std::array<int,E>> stabilizers;
 int norm_length,dot_length;
 std::vector<uint32_t> row_masks,dot_masks;
 const uint32_t* row_ptr[N]{};
 CompletionSolver csp;
 FieldFilter<37> f17; FieldFilter<257> f257;
 uint64_t steps=0,matrices=0,singular=0,cyclic=0;
 Worker(const char *system,int m,int weight=1):M(m),C(weight),csp(system,m,allowance,began,weight),f17(m),f257(m){
  norm_length=N*M*M+1;dot_length=(N+1)*M*M+1;
  row_masks.resize(N*(M+1)*N*norm_length);dot_masks.resize(E*(M+1)*dot_length);
  int z=0;for(int i=0;i<N;++i)for(int j=i+1;j<N;++j){edge[z]={i,j};edge_index[i][j]=edge_index[j][i]=z++;}
 }
 bool check_time(){
  if(expired.load(std::memory_order_relaxed))return false;
  if((++steps&65535u)==0 && std::chrono::duration<double>(Clock::now()-began).count()>=allowance){expired=true;return false;}
  return true;
 }
 std::vector<int> prefix(int a) const {
  std::vector<int> v;v.reserve(csp.nv);
  for(int x:u)v.push_back(x);for(int i=0;i<N;++i)v.push_back(Q[i][i]);
  for(auto [i,j]:edge)v.push_back(Q[i][j]);v.push_back(a);return v;
 }

 void prepare_masks(){
  for(int i=0;i<N;++i)for(int q=0;q<=M;++q)for(int left=0;left<N;++left)for(int norm=0;norm<norm_length;++norm){
   uint32_t keep=0;int c=norm+u[i]*u[i]-C,lower=b*(sum-u[i]),upper=M*sum;
   for(int a=0;a<=M;++a){int lo=c-a*q,hi=lo+left*M*M;
    if(lo>upper||hi<lower)continue;
    if(!left&&((g==0&&lo!=0)||(g>1&&lo%g)))continue;keep|=1u<<a;
   }
   row_masks[((i*(M+1)+q)*N+left)*norm_length+norm]=keep;
  }
  for(int e=0;e<E;++e){auto[i,j]=edge[e];int lower=b*(u[i]+u[j]),upper=M*sum;
   for(int q=0;q<=M;++q)for(int c=0;c<dot_length;++c){uint32_t keep=0;
    for(int a=0;a<=M;++a){int z=c-a*q;if(z<lower||z>upper||(g==0&&z!=0)||(g>1&&z%g))continue;keep|=1u<<a;}
    dot_masks[(e*(M+1)+q)*dot_length+c]=keep;
   }
  }
 }
 uint32_t row_filter(int i,uint32_t mask)const{
  return mask & row_ptr[i][missing[i]*norm_length+norm[i]];
 }
 uint32_t dot_filter(int i,int j,uint32_t mask)const{
  int c=u[i]*u[j];for(int k=0;k<N;++k)c+=Q[i][k]*Q[k][j];
  return mask & dot_masks[(edge_index[i][j]*(M+1)+Q[i][j])*dot_length+c];
 }
 bool canonical_edges(int filled)const{
  for(const auto&p:stabilizers){
   for(int k=0;k<filled;++k){int j=p[k];if(j==k)continue;if(j>=filled)break;
    auto [a,b]=edge[k];auto[c,d]=edge[j];
    if(Q[a][b]>Q[c][d])return false;if(Q[a][b]<Q[c][d])break;
   }
  }return true;
 }

 template<int P> bool firstrow_filter(uint32_t &possible,const FieldFilter<P>&f){
  int V[N+1][N],ha[N][N],hb[N][N],A[N][N+2];
  for(int i=0;i<N;++i)V[0][i]=u[i];
  for(int k=1;k<=N;++k)for(int i=0;i<N;++i){int z=0;for(int j=0;j<N;++j)z+=Q[i][j]*V[k-1][j];V[k][i]=z%P;}
  for(int j=0;j<N;++j){int z=u[j]*u[0]-C*(j==0);for(int k=0;k<N;++k)z+=Q[j][k]*Q[k][0];ha[0][j]=(z+P*P)%P;hb[0][j]=(P-Q[j][0]%P)%P;}
  for(int k=1;k<N;++k){int mom=0;for(int j=0;j<N;++j)mom+=u[j]*V[k-1][j];mom%=P;
   for(int j=0;j<N;++j){int c=P*P-mom*Q[j][0]+u[j]*V[k][0],d=0;
    for(int l=0;l<N;++l){c+=Q[j][l]*ha[k-1][l];d+=Q[j][l]*hb[k-1][l];}ha[k][j]=c%P;hb[k][j]=d%P;}
  }
  for(int i=0;i<N;++i){for(int j=0;j<N;++j)A[i][j]=V[i][j];A[i][N]=ha[i][0];A[i][N+1]=hb[i][0];}

  // Rank-deficient systems still impose necessary congruences on a.
  // Retain every compatible singular case for the exhaustive fallback.
  int h=0,piv[N];bool pivot[N]{};
  for(int j=0;j<N&&h<N;++j){int p=h;while(p<N&&!A[p][j])++p;if(p==N)continue;
   if(p!=h)for(int k=j;k<N+2;++k)std::swap(A[p][k],A[h][k]);
   int iv=f.inv[A[h][j]];for(int k=j+1;k<N+2;++k)A[h][k]=A[h][k]*iv%P;
   for(int i=h+1;i<N;++i){int z=A[i][j];A[i][j]=0;if(z)for(int k=j+1;k<N+2;++k)A[i][k]=(A[i][k]+P*P-z*A[h][k])%P;}
   piv[h++]=j;pivot[j]=true;
  }
  for(int i=h;i<N;++i){int c=A[i][N],d=A[i][N+1];
   if(!d){if(c){possible=0;return true;}}
   else{int a=(P-c)*f.inv[d]%P;possible &= a<=M?(1u<<a):0u;if(!possible)return true;}
  }
  if(h<N){
   int free_index[N],nf=0;for(int i=0;i<N;++i)if(!pivot[i])free_index[nf++]=i;
   if(nf<=2){uint32_t supported=0;
    for(uint32_t am=possible;am;am&=am-1){int a=__builtin_ctz(am);int trials=1;for(int k=0;k<nf;++k)trials*=M+1;
     for(int t=0;t<trials;++t){int x[N]{},z=t;bool ok=true;
      for(int k=0;k<nf;++k){int j=free_index[k];x[j]=z%(M+1);z/=M+1;if(j&&x[j]<b)ok=false;}
      if(!ok)continue;
      for(int k=h-1;k>=0;--k){int j=piv[k],rhs=A[k][N]+a*A[k][N+1]+N*P*P;
       for(int l=j+1;l<N;++l)rhs-=A[k][l]*x[l];x[j]=rhs%P;
       if(x[j]>M||(j&&x[j]<b)){ok=false;break;}
      }
      if(ok){supported|=1u<<a;break;}
     }
    }
    possible=supported;if(!possible)return true;
   }
   return false;
  }
  int c[N],d[N];
  for(int i=N-1;i>=0;--i){int x=A[i][N]+N*P*P,y=A[i][N+1]+N*P*P;
   for(int j=i+1;j<N;++j){x-=A[i][j]*c[j];y-=A[i][j]*d[j];}c[i]=x%P;d[i]=y%P;
   possible&=f.mask[c[i]][d[i]];if(!possible)return true;
  }
  return true;
 }
 template<int P> bool reconstruct(uint32_t possible,const FieldFilter<P>&f){
  // K has columns u,Q u,...,Q^(N-1)u over F_P.
  int V[N+1][N]{},moment[N]{},A[N][2*N]{};
  for(int i=0;i<N;++i)V[0][i]=u[i];
  for(int k=1;k<=N;++k)for(int i=0;i<N;++i){int z=0;for(int j=0;j<N;++j)z+=Q[i][j]*V[k-1][j];V[k][i]=z%P;}
  for(int k=0;k<N;++k){int z=0;for(int i=0;i<N;++i){z+=u[i]*V[k][i];A[i][k]=V[k][i];}moment[k]=z%P;A[k][N+k]=1;}
  for(int j=0;j<N;++j){int p=j;while(p<N&&!A[p][j])++p;if(p==N)return false;
   if(p!=j)for(int k=j;k<2*N;++k)std::swap(A[p][k],A[j][k]);
   int iv=f.inv[A[j][j]];for(int k=j;k<2*N;++k)A[j][k]=A[j][k]*iv%P;
   for(int i=0;i<N;++i)if(i!=j&&A[i][j]){int z=A[i][j];A[i][j]=0;
    for(int k=j+1;k<2*N;++k)A[i][k]=(A[i][k]+P*P-z*A[j][k])%P;}
  }
  int H[N][N][N]{},B[N][N][N]{};bool made[N]{};
  auto build=[&](int i){
   if(made[i])return;made[i]=true;
   for(int j=0;j<N;++j){int z=u[j]*u[i]-C*(i==j);for(int k=0;k<N;++k)z+=Q[j][k]*Q[k][i];H[i][0][j]=(z+P*P)%P;B[i][0][j]=(P-Q[j][i]%P)%P;}
   for(int k=1;k<N;++k)for(int j=0;j<N;++j){int h=0,d=0;
    for(int l=0;l<N;++l){h+=Q[j][l]*H[i][k-1][l];d+=Q[j][l]*B[i][k-1][l];}
    h+=P*P-moment[k-1]*Q[j][i]+u[j]*V[k][i];H[i][k][j]=h%P;B[i][k][j]=d%P;
   }
  };
  auto coeff=[&](int i,int j,int k){int c=0,d=0;for(int l=0;l<N;++l){c+=H[i][l][j]*A[l][N+k];d+=B[i][l][j]*A[l][N+k];}return std::pair<int,int>{c%P,d%P};};
  build(0);auto[c0,d0]=coeff(0,0,0);possible&=f.mask[c0][d0];if(!possible)return true;
  if(N>1){auto[c1,d1]=coeff(0,0,1);possible&=f.mask[c1][d1];if(!possible)return true;}
  for(uint32_t t=possible;t;t&=t-1){int a=__builtin_ctz(t);std::vector<int> v=prefix(a);bool ok=true;
   for(int i=0;i<N&&ok;++i){build(i);for(int j=i;j<N&&ok;++j)for(int k=j;k<N;++k){
    auto[c,d]=coeff(i,j,k);int z=(c+a*d)%P;
    if(z>M||((i==j||j==k)&&i!=k&&z<b)){ok=false;break;}v.push_back(z);
   }}
   if(ok)csp.accept(v);
  }
  return true;
 }
 void finish(uint32_t possible){
  ++matrices;
  if constexpr(N>=3){
   bool fixed_invertible=C==1&&sum==0&&possible==1;
   for(int i=0;i<N&&fixed_invertible;++i)for(int j=0;j<N;++j)if(Q[i][j]!=(i==j))fixed_invertible=false;
   if(fixed_invertible){
    // g^2=1 and g fixes every other nonunit basis element. Folding {1,g}
    // changes only the unit coefficient in tail associativity, from 1 to 2.
    std::string lower_path=system_dir+"/system"+std::to_string(N+1)+"sd.txt";
    Worker<N-1> sub(lower_path.c_str(),M,2);
    sub.csp.output_callback=[&](const std::vector<int>&wv){
     std::vector<int> v=prefix(0);v.push_back(wv[Worker<N-1>::TOP-1]);
     for(int k=0;k<N-1;++k)v.push_back(wv[k]);
     for(int i=0;i<N-1;++i)for(int j=i;j<N-1;++j)
      v.push_back(i==j?wv[N-1+i]:wv[2*(N-1)+sub.edge_index[i][j]]);
     v.insert(v.end(),wv.begin()+Worker<N-1>::TOP,wv.end());
     std::vector<int> best=v,t(v.size());
     for(const auto&p:csp.perms){for(size_t k=0;k<v.size();++k)t[k]=v[p[k]];if(t<best)best=t;}
     if(!csp.accept(best))throw std::logic_error("weighted unfolding failed exact verification");
    };
    std::array<int,N-1> u2{};
    auto rec=[&](auto&&self,int k,int lo)->void{
     if(expired)return;if(k==N-1){sub.run(u2);return;}
     for(int z=lo;z<=M&&!expired;++z){u2[k]=z;self(self,k+1,z);}
    };rec(rec,0,0);
    return;
   }
  }
  uint32_t allowed=possible;
  if(firstrow_filter<257>(allowed,f257)){++cyclic;if(allowed)reconstruct<257>(allowed,f257);return;}
  if(firstrow_filter<37>(allowed,f17)){++cyclic;if(allowed)reconstruct<37>(allowed,f17);return;}
  ++singular;
  for(uint32_t t=allowed;t&&!expired.load(std::memory_order_relaxed);t&=t-1){int a=__builtin_ctz(t);csp.complete_prefix(prefix(a));if(csp.stopped){expired=true;return;}}
 }
 void offdiagonal(int k,uint32_t possible){
  if(!check_time())return;
  if(k==E){finish(possible);return;}
  auto[i,j]=edge[k];
  for(int z=0;z<=M&&!expired.load(std::memory_order_relaxed);++z){
   Q[i][j]=Q[j][i]=z;norm[i]+=z*z;norm[j]+=z*z;--missing[i];--missing[j];
   uint32_t a=row_filter(i,possible);if(a)a=row_filter(j,a);
   if(a&&!missing[i])for(int l=0;l<N&&a;++l)if(l!=i&&!missing[l])a=dot_filter(i,l,a);
   if(a&&!missing[j])for(int l=0;l<N&&a;++l)if(l!=j&&l!=i&&!missing[l])a=dot_filter(j,l,a);
   if(a&&canonical_edges(k+1))offdiagonal(k+1,a);
   norm[i]-=z*z;norm[j]-=z*z;++missing[i];++missing[j];
  }
 }
 void prepare_stabilizers(){
  stabilizers.clear();std::array<int,N> p;std::iota(p.begin(),p.end(),0);
  do{bool keep=true,identity=true;for(int i=0;i<N;++i){keep&=u[i]==u[p[i]]&&Q[i][i]==Q[p[i]][p[i]];identity&=i==p[i];}
   if(keep&&!identity){std::array<int,E> map;for(int k=0;k<E;++k){auto[i,j]=edge[k];map[k]=edge_index[p[i]][p[j]];}stabilizers.push_back(map);}
  }while(std::next_permutation(p.begin(),p.end()));
 }
 void diagonal(int k,uint32_t possible){
  if(!check_time())return;
  if(k==N){prepare_stabilizers();offdiagonal(0,possible);return;}
  int lo=b;if(k&&u[k]==u[k-1])lo=Q[k-1][k-1];
  for(int x=lo;x<=M&&!expired.load(std::memory_order_relaxed);++x){
   Q[k][k]=x;norm[k]=x*x;missing[k]=N-1;row_ptr[k]=row_masks.data()+(k*(M+1)+x)*N*norm_length;
   uint32_t a=row_filter(k,possible);if(a)diagonal(k+1,a);
  }
 }
 void run(const std::array<int,N>&v){
  b=v[0];sum=0;g=0;for(int i=0;i<N;++i){u[i]=v[i];sum+=u[i];g=std::gcd(g,u[i]);}
  prepare_masks();diagonal(0,(1u<<(M+1))-1);
 }
};

template<int N> int run_all(const char*system,int M,int threads){
 std::vector<std::array<int,N>> jobs;std::array<int,N> v{};
 auto rec=[&](auto&&self,int k,int lo)->void{if(k==N){jobs.push_back(v);return;}for(int a=lo;a<=M;++a){v[k]=a;self(self,k+1,a);}};rec(rec,0,0);
 std::vector<uint64_t> counts(M+1);uint64_t matrices=0,singular=0,nodes=0,completed=0,sols=0;
 omp_set_num_threads(threads);
 #pragma omp parallel
 {
  Worker<N> w(system,M);
  #pragma omp for schedule(dynamic,1)
  for(size_t t=0;t<jobs.size();++t){if(single_job>=0&&int(t)!=single_job)continue;if(expired.load(std::memory_order_relaxed))continue;
   auto start=Clock::now();auto old=w.csp.sols;auto mat=w.matrices;w.run(jobs[t]);
   #pragma omp critical(progress)
   {if(!expired)++completed;std::cerr<<"job "<<t<<" / "<<jobs.size()<<" done "<<(!expired)<<" u";for(int x:jobs[t])std::cerr<<' '<<x;
    std::cerr<<" matrices "<<w.matrices-mat<<" rings "<<w.csp.sols-old<<" seconds "<<std::chrono::duration<double>(Clock::now()-start).count()<<'\n';}
  }
  #pragma omp critical(collect)
  {for(int k=1;k<=M;++k)counts[k]+=w.csp.counts[k];matrices+=w.matrices;singular+=w.singular;nodes+=w.csp.nodes;sols+=w.csp.sols;}
 }
 bool complete=!expired&&completed==jobs.size();
 std::cerr<<"FINAL rank "<<N+2<<" bound "<<M<<" complete "<<complete<<" jobs "<<completed<<" / "<<jobs.size()<<" matrices "<<matrices<<" singular "<<singular<<" completion_nodes "<<nodes<<" classes "<<sols<<" seconds "<<std::chrono::duration<double>(Clock::now()-began).count()<<" counts";for(int k=1;k<=M;++k)std::cerr<<' '<<counts[k];std::cerr<<'\n';
 return complete?0:3;
}
int main(int argc,char**argv){
 if(argc!=6&&argc!=7){std::cerr<<"usage: selfdual_fast SYSTEM RANK M SECONDS THREADS [SINGLE_JOB]\n";return 2;}
 int r=std::stoi(argv[2]),M=std::stoi(argv[3]),threads=std::stoi(argv[5]);allowance=std::stod(argv[4]);
 if(r<4||r>7||M<1||M>30||threads<1||allowance<=0)return 2;
 system_dir=std::filesystem::path(argv[1]).parent_path().string();
 if(argc==7)single_job=std::stoi(argv[6]);
 began=Clock::now();int rc=2;
 if(r==4)rc=run_all<2>(argv[1],M,threads);
 if(r==5)rc=run_all<3>(argv[1],M,threads);
 if(r==6)rc=run_all<4>(argv[1],M,threads);
 if(r==7)rc=run_all<5>(argv[1],M,threads);
 if(!std::cout)return 2;return rc;
}
