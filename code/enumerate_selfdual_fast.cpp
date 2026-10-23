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
#ifndef CENSUS_SELFDUAL_RANK
#define CENSUS_SELFDUAL_RANK 0
#endif

template<int P> struct FieldFilter {
 int inv[P]{}; uint32_t mask[P][P]{};
 explicit FieldFilter(int M){
  for(int i=1;i<P;++i)for(int j=1;j<P;++j)if(i*j%unsigned(P)==1){inv[i]=j;break;}
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
 std::vector<int> stabilizer_starts;
 bool compact_stabilizers=false;
 int norm_length,dot_length;
 std::vector<uint32_t> row_masks,dot_masks,dot_interval_masks;
 const uint32_t* row_ptr[N]{};
 CompletionSolver csp;
 FieldFilter<17> f17; FieldFilter<257> f257;
 // Bounded witnesses t_j=T_{00j} for the first two Krylov moment equations.
 // Construction limits affect performance only: exceeding either cap switches
 // this entire Q-row branch back to the exhaustive, unfiltered Q search.
 static constexpr size_t MAX_WITNESSES=4096;
 static constexpr int WITNESS_VISIT_LIMIT=200000;
 struct Witness {
  int a,residual,coef[E],lo[E+1],hi[E+1],gcd[E+1],t[N];
 };
 std::vector<Witness> witnesses;
 bool witness_active=true;uint32_t pair_masks[16][16]{};
 std::vector<int> supported[E+1];
 bool prepared=false;
 void build_witnesses(uint32_t possible){
  witnesses.clear();supported[N-1].clear();witness_active=true;int visits=0;
  int qnorm=0,qu=0,unorm=0;
  for(int i=0;i<N;++i){qnorm+=Q[0][i]*Q[0][i];qu+=Q[0][i]*u[i];unorm+=u[i]*u[i];}
  int t[N];
  for(uint32_t am=possible;am;am&=am-1){int a=__builtin_ctz(am);
   int rhs=qnorm+u[0]*u[0]-C-a*Q[0][0];
   auto rec=[&](auto&&self,int i,int rem)->void{
    if(!witness_active||rem<0)return;if(++visits>WITNESS_VISIT_LIMIT){witness_active=false;return;}
    if(i<N){
     int remain=0,minremain=0;for(int j=i+1;j<N;++j){remain+=u[j]*M;minremain+=u[j]*b;}
     // If u=0, every coefficient involving t vanishes; t=0 represents
     // all witnesses exactly and avoids enumerating (M+1)^N duplicates.
     for(int z=i?b:0;z<=(sum?M:0);++z)if(rem-u[i]*z>=minremain&&rem-u[i]*z<=remain){t[i]=z;self(self,i+1,rem-u[i]*z);}return;
    }
    if(rem)return;
    std::array<int,N> mixed; mixed[0]=Q[0][0];for(int j=1;j<N;++j)mixed[j]=t[j];std::sort(mixed.begin(),mixed.end());
    bool smaller=false;for(int j=0;j<N;++j)if(mixed[j]!=u[j]){smaller=mixed[j]<u[j];break;}if(smaller)return;
    Witness w{};w.a=a;for(int j=0;j<N;++j)w.t[j]=t[j];
    w.residual=C*Q[0][0]-2*u[0]*qu+unorm*Q[0][0]+a*qnorm;
    for(int j=0;j<N;++j)w.residual+=(t[j]*u[j]-Q[0][j]*Q[0][j])*Q[j][j];
    for(int k=0;k<E;++k){auto[j,l]=edge[k];w.coef[k]=t[j]*u[l]+t[l]*u[j]-2*Q[0][j]*Q[0][l];
     if(k<N-1)w.residual+=w.coef[k]*Q[j][l];}
    for(int k=E-1;k>=N-1;--k){int c=w.coef[k];w.lo[k]=w.lo[k+1]+std::min(0,c*M);w.hi[k]=w.hi[k+1]+std::max(0,c*M);w.gcd[k]=std::gcd(w.gcd[k+1],std::abs(c));}
    int k=N-1;if(w.residual+w.lo[k]>0||w.residual+w.hi[k]<0||(w.gcd[k]&&w.residual%w.gcd[k]))return;
    if(witnesses.size()>=MAX_WITNESSES){witness_active=false;return;}
    supported[N-1].push_back(int(witnesses.size()));witnesses.push_back(w);
   };rec(rec,0,rhs);if(!witness_active)break;
  }
  if(!witness_active){witnesses.clear();supported[N-1].clear();}
 }
 uint32_t filter_witnesses(int k,int z,uint32_t possible){
  auto&out=supported[k+1];out.clear();uint32_t mask=0;
  for(int wi:supported[k]){auto&w=witnesses[wi];if(!(possible&(1u<<w.a)))continue;
   int residual=w.residual+w.coef[k]*z;
   if(residual+w.lo[k+1]>0||residual+w.hi[k+1]<0||(w.gcd[k+1]&&residual%w.gcd[k+1]))continue;
   out.push_back(wi);mask|=1u<<w.a;
  }
  return mask;
 }
 void advance_witnesses(int k,int z,int sign){for(int wi:supported[k+1])witnesses[wi].residual+=sign*witnesses[wi].coef[k]*z;}

 // Intersect the remaining linear moment equation with the next exact
 // moment equation before enumerating the final two Q-edges. With q=Q e_0,
 // the latter is
 // (Qu).(Qt)-||Qq||^2-2u_0 q.(Qu)-(u.q)^2
 //   +(C+||u||^2)||q||^2+Q_00 u.(Qu)+a q.(Qq)=0.
 // It is quadratic in the two unknown edges. All arithmetic is integral.
 void build_pair_masks(uint32_t possible){
  for(int x=0;x<=M;++x)for(int y=0;y<=M;++y)pair_masks[x][y]=0;
  auto[l,h]=edge[E-2];auto[m,h2]=edge[E-1];
  // The lexicographic final edges are (N-3,N-1),(N-2,N-1).
  if(h!=h2)throw std::logic_error("unexpected tail edge order");
  int64_t qu[N]{},qq[N]{},q[N]{},u2=0,q2=0,uq=0;
  for(int i=0;i<N;++i){q[i]=Q[0][i];u2+=u[i]*u[i];q2+=q[i]*q[i];uq+=u[i]*q[i];}
  auto base=[&](int i,int j)->int{
   if((i==l&&j==h)||(i==h&&j==l)||(i==m&&j==h)||(i==h&&j==m))return 0;
   return Q[i][j];
  };
  for(int i=0;i<N;++i)for(int j=0;j<N;++j){qu[i]+=base(i,j)*u[j];qq[i]+=base(i,j)*q[j];}
  int64_t qqu=0,uqu=0,qqq=0,qqnorm=0;
  for(int i=0;i<N;++i){qqu+=q[i]*qu[i];uqu+=u[i]*qu[i];qqq+=q[i]*qq[i];qqnorm+=qq[i]*qq[i];}
  int64_t h2u[N]{},lx[N]{},ly[N]{};
  for(int i=0;i<N;++i)for(int j=0;j<N;++j)h2u[i]+=base(i,j)*qu[j];
  lx[h]+=qu[l];lx[l]+=qu[h];ly[h]+=qu[m];ly[m]+=qu[h];
  for(int k=0;k<N;++k){lx[k]+=u[h]*base(l,k)+u[l]*base(h,k);ly[k]+=u[h]*base(m,k)+u[m]*base(h,k);}
  int64_t common=-qqnorm-2*u[0]*qqu-uq*uq+(C+u2)*q2+uqu*q[0];
  auto linear_common=[&](int i,int j)->int64_t{return -2*(qq[i]*q[j]+qq[j]*q[i])-2*u[0]*(q[i]*u[j]+q[j]*u[i])+2*q[0]*u[i]*u[j];};
  int64_t commonx=linear_common(l,h),commony=linear_common(m,h);
  for(int wi:supported[E-2]){const auto&w=witnesses[wi];if(!(possible&(1u<<w.a)))continue;
   int64_t c=common+w.a*qqq,cx=commonx+2*w.a*q[l]*q[h],cy=commony+2*w.a*q[m]*q[h];
   for(int i=0;i<N;++i){c+=h2u[i]*w.t[i];cx+=lx[i]*w.t[i];cy+=ly[i]*w.t[i];}
   int64_t cxx=u[l]*w.t[l]+u[h]*w.t[h]-q[l]*q[l]-q[h]*q[h];
   int64_t cyy=u[m]*w.t[m]+u[h]*w.t[h]-q[m]*q[m]-q[h]*q[h];
   int64_t cxy=u[l]*w.t[m]+u[m]*w.t[l]-2*q[l]*q[m];
   auto check=[&](int x,int y){if(c+cx*x+cy*y+cxx*x*x+cyy*y*y+cxy*x*y==0)pair_masks[x][y]|=1u<<w.a;};
   for(int x=0;x<=M;++x){int r=-w.residual-w.coef[E-2]*x,cy1=w.coef[E-1];
    if(cy1){if(r%cy1==0){int y=r/cy1;if(y>=0&&y<=M)check(x,y);}}
    else if(!r)for(int y=0;y<=M;++y)check(x,y);
   }
  }
 }

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

 // Exact bounded sums strengthen the interval/gcd necessary conditions.
 // For diagonal tail T_iik, mixed entries k != i are >= b; on an
 // off-diagonal tail T_ijk, the entries k == i or j are >= b.
 std::vector<unsigned char> reachable_tail(int i,int j)const{
  int cap=M*sum;
  std::vector<unsigned char> a(cap+1),next(cap+1);a[0]=1;
  int used=0;
  for(int k=0;k<N;++k){
   std::fill(next.begin(),next.end(),0);
   int lo=i==j?(k!=i?b:0):(k==i||k==j?b:0);
   for(int z=0;z<=used;++z)if(a[z])for(int x=lo;x<=M;++x)next[z+u[k]*x]=1;
   used+=M*u[k];a.swap(next);
  }
  return a;
 }
 void prepare_masks(){
  int lower_z=-M*M-C,cap=M*sum,width=cap-lower_z+1;
  for(int i=0;i<N;++i){
   // Canonical order begins with the sorted mixed-coefficient row u.
   // Replacing generator 1 by i gives mixed entries Q_ii,T_iik (k!=i).
   // Their sorted tuple must be lexicographically at least u.
   std::vector<unsigned char> min_q(cap+1,M+1);
   std::array<int,N> mixed{};
   auto admissible=[&](int q)->bool{
    mixed[N-1]=q;auto sorted=mixed;std::sort(sorted.begin(),sorted.end());
    for(int j=0;j<N;++j){if(sorted[j]<u[j])return false;if(sorted[j]>u[j])return true;}return true;
   };
   auto enumerate=[&](auto&&self,int k,int z,int used,int previous)->void{
    if(k==N){
     if(!admissible(M))return;int lo=b,hi=M;
     while(lo<hi){int mid=(lo+hi)/2;if(admissible(mid))hi=mid;else lo=mid+1;}
     for(int x=0;x<=M;++x)min_q[z+u[i]*x]=std::min<int>(min_q[z+u[i]*x],lo);
     return;
    }
    if(k==i){self(self,k+1,z,used,previous);return;}
    // Equal weights can be permuted without changing the weighted sum
    // or the sorted mixed tuple, so visit one ordering of each such block.
    int lo=previous>=0&&u[k]==u[previous]?mixed[used-1]:b;
    for(int x=lo;x<=M;++x){mixed[used]=x;self(self,k+1,z+u[k]*x,used+1,k);}
   };enumerate(enumerate,0,0,0,-1);
   // feasible[left,z] means z + x_1^2 + ... + x_left^2 is reachable.
   for(int q=b;q<=M;++q){
    std::vector<unsigned char> feasible(N*width);
    for(int z=0;z<=cap;++z)feasible[z-lower_z]=min_q[z]<=q;
    for(int left=1;left<N;++left)for(int z=lower_z;z<=cap;++z){
     for(int x=0;x<=M&&z+x*x<=cap;++x)
      if(feasible[(left-1)*width+z+x*x-lower_z]){feasible[left*width+z-lower_z]=1;break;}
    }
    for(int left=0;left<N;++left)for(int norm=0;norm<norm_length;++norm){
     uint32_t keep=0;int c=norm+u[i]*u[i]-C;
     for(int a=0;a<=M;++a){int z=c-a*q;
      if(z>=lower_z&&z<=cap&&feasible[left*width+z-lower_z])keep|=1u<<a;
     }
     row_masks[((i*(M+1)+q)*N+left)*norm_length+norm]=keep;
    }
   }
  }
  for(int e=0;e<E;++e){auto[i,j]=edge[e];auto reach=reachable_tail(i,j);
   for(int q=0;q<=M;++q)for(int c=0;c<dot_length;++c){uint32_t keep=0;
    for(int a=0;a<=M;++a){int z=c-a*q;if(z>=0&&z<=cap&&reach[z])keep|=1u<<a;}
    dot_masks[(e*(M+1)+q)*dot_length+c]=keep;
   }
  }
  // With multiplicity one, a completed row contracts a partially known row
  // to an exact interval: every unknown summand has coefficient zero or one.
  // Cache unions of masks on these short intervals for early pair pruning.
  if(M==1){
   dot_interval_masks.resize(E*2*dot_length*dot_length);
   for(int e=0;e<E;++e)for(int q=0;q<2;++q)for(int lo=0;lo<dot_length;++lo){
    uint32_t mask=0;
    for(int hi=lo;hi<dot_length;++hi){
     mask|=dot_masks[(e*2+q)*dot_length+hi];
     dot_interval_masks[((e*2+q)*dot_length+lo)*dot_length+hi]=mask;
    }
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
 uint32_t partial_dot_filter(int i,int j,int filled,uint32_t mask)const{
  // Row i is complete; only Q_kj with unvisited off-diagonal indices vary.
  int lo=u[i]*u[j],unknown=0;
  for(int k=0;k<N;++k){
   if(k!=j&&edge_index[k][j]>=filled)unknown+=Q[i][k];
   else lo+=Q[i][k]*Q[k][j];
  }
  int e=edge_index[i][j],hi=lo+unknown;
  return mask & dot_interval_masks[((e*2+Q[i][j])*dot_length+lo)*dot_length+hi];
 }
 // Exact colored-graph canonicality without storing the factorial stabilizer.
 // Earlier rows partition the unused vertices into ordered cells. Within
 // each cell, sorting adjacency to the next chosen vertex minimizes that
 // next row; only equal rows require further branching.
 bool canonical_matrix()const{
  using Cells=std::vector<std::vector<int>>;
  Cells initial;
  for(int i=0;i<N;++i){
   if(!i||u[i]!=u[i-1]||Q[i][i]!=Q[i-1][i-1])initial.emplace_back();
   initial.back().push_back(i);
  }
  auto visit=[&](auto&&self,int row,const Cells&cells)->bool{
   if(cells.empty())return true;
   const auto&first=cells.front();
   for(size_t choice=0;choice<first.size();++choice){
    int x=first[choice];bool redundant=false;
    for(size_t prev=0;prev<choice&&!redundant;++prev){
     int y=first[prev];bool twins=true;
     for(int v=0;v<N;++v)if(v!=x&&v!=y&&Q[x][v]!=Q[y][v]){twins=false;break;}
     redundant=twins;
    }
    if(redundant)continue;
    Cells refined;int column=row+1,comparison=0;
    for(const auto&cell:cells){
     std::array<std::vector<int>,16> bins;
     for(int v:cell)if(v!=x)bins[Q[x][v]].push_back(v);
     for(int value=0;value<=M;++value)if(!bins[value].empty()){
      for(int v:bins[value]){(void)v;if(!comparison&&value!=Q[row][column])comparison=value<Q[row][column]?-1:1;++column;}
      refined.push_back(std::move(bins[value]));
     }
    }
    if(comparison<0)return false;
    if(!comparison&&!self(self,row+1,refined))return false;
   }
   return true;
  };
  return visit(visit,0,initial);
 }
 bool canonical_edges(int filled)const{
  for(size_t h=0;h<stabilizers.size();++h){
   if(stabilizer_starts[h]>=filled)continue;
   const auto&p=stabilizers[h];
   for(int k=stabilizer_starts[h];k<filled;++k){int j=p[k];if(j==k)continue;if(j>=filled)break;
    auto [a,b]=edge[k];auto[c,d]=edge[j];
    if(Q[a][b]>Q[c][d])return false;if(Q[a][b]<Q[c][d])break;
   }
  }
  if(compact_stabilizers&&filled==E)return canonical_matrix();
  return true;
 }

 template<int P> bool firstrow_filter(uint32_t &possible,const FieldFilter<P>&f){
  int V[N][N],moment[N]{},A[N][N+2];
  for(int i=0;i<N;++i)V[0][i]=u[i];
  for(int k=1;k<N;++k)for(int i=0;i<N;++i){int z=0;for(int j=0;j<N;++j)z+=Q[i][j]*V[k-1][j];V[k][i]=z%unsigned(P);}
  for(int k=0;k<N;++k){int z=0;for(int i=0;i<N;++i)z+=u[i]*V[k][i];moment[k]=z%unsigned(P);}
  // Symmetry computes moments w_k=(Q^k)_{00} from half as many
  // matrix-vector products: w_{a+b}=(Q^a e_0)^t(Q^b e_0).
  constexpr int L=(N+2)/2;
  int W[L+1][N]{},w[N+2]{};W[0][0]=1;
  for(int i=0;i<N;++i)W[1][i]=Q[i][0];
  for(int k=2;k<=L;++k)for(int i=0;i<N;++i){int z=0;for(int j=0;j<N;++j)z+=Q[i][j]*W[k-1][j];W[k][i]=z%unsigned(P);}
  for(int k=0;k<=N+1;++k){int z=0;for(int i=0;i<N;++i)z+=W[k/2][i]*W[(k+1)/2][i];w[k]=z%unsigned(P);}
  for(int k=0;k<N;++k){
   for(int j=0;j<N;++j)A[k][j]=V[k][j];
   int h=(N+2)*P*P+w[k+2]-C*w[k];
   for(int t=0;t<=k;++t)h+=V[t][0]*V[k-t][0];
   for(int t=0;t<k;++t)h-=moment[t]*w[k-t];
   A[k][N]=h%unsigned(P);A[k][N+1]=(P-w[k+1])%unsigned(P);
  }

  // Rank-deficient systems still impose necessary congruences on a.
  // Retain every compatible singular case for the exhaustive fallback.
  int h=0,piv[N];bool pivot[N]{};
  for(int j=0;j<N&&h<N;++j){int p=h;while(p<N&&!A[p][j])++p;if(p==N)continue;
   if(p!=h)for(int k=j;k<N+2;++k)std::swap(A[p][k],A[h][k]);
   int iv=f.inv[A[h][j]];for(int k=j+1;k<N+2;++k)A[h][k]=A[h][k]*iv%unsigned(P);
   for(int i=h+1;i<N;++i){int z=A[i][j];A[i][j]=0;if(z)for(int k=j+1;k<N+2;++k)A[i][k]=(A[i][k]+P*P-z*A[h][k])%unsigned(P);}
   piv[h++]=j;pivot[j]=true;
  }
  for(int i=h;i<N;++i){int c=A[i][N],d=A[i][N+1];
   if(!d){if(c){possible=0;return true;}}
   else{int a=(P-c)*f.inv[d]%unsigned(P);possible &= a<=M?(1u<<a):0u;if(!possible)return true;}
  }
  if(h<N){
   int free_index[N],nf=0;for(int i=0;i<N;++i)if(!pivot[i])free_index[nf++]=i;
   if(nf<=2){uint32_t supported=0;
    for(uint32_t am=possible;am;am&=am-1){int a=__builtin_ctz(am);int trials=1;for(int k=0;k<nf;++k)trials*=M+1;
     for(int t=0;t<trials;++t){int x[N]{},z=t;bool ok=true;
      for(int k=0;k<nf;++k){int j=free_index[k];x[j]=z%(M+1);z/=M+1;if(j&&x[j]<b)ok=false;}
      if(!ok)continue;
      for(int k=h-1;k>=0;--k){int j=piv[k],rhs=A[k][N]+a*A[k][N+1]+N*P*P;
       for(int l=j+1;l<N;++l)rhs-=A[k][l]*x[l];x[j]=rhs%unsigned(P);
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
   for(int j=i+1;j<N;++j){x-=A[i][j]*c[j];y-=A[i][j]*d[j];}c[i]=x%unsigned(P);d[i]=y%unsigned(P);
   possible&=f.mask[c[i]][d[i]];if(!possible)return true;
  }
  return true;
 }
 template<int P> bool reconstruct(uint32_t possible,const FieldFilter<P>&f){
  // K has columns u,Q u,...,Q^(N-1)u over F_P.
  int V[N+1][N]{},moment[N]{},A[N][2*N]{};
  for(int i=0;i<N;++i)V[0][i]=u[i];
  for(int k=1;k<N;++k)for(int i=0;i<N;++i){int z=0;for(int j=0;j<N;++j)z+=Q[i][j]*V[k-1][j];V[k][i]=z%unsigned(P);}
  for(int k=0;k<N;++k){int z=0;for(int i=0;i<N;++i){z+=u[i]*V[k][i];A[i][k]=V[k][i];}moment[k]=z%unsigned(P);A[k][N+k]=1;}
  for(int j=0;j<N;++j){int p=j;while(p<N&&!A[p][j])++p;if(p==N)return false;
   if(p!=j)for(int k=j;k<2*N;++k)std::swap(A[p][k],A[j][k]);
   int iv=f.inv[A[j][j]];for(int k=j;k<2*N;++k)A[j][k]=A[j][k]*iv%unsigned(P);
   for(int i=0;i<N;++i)if(i!=j&&A[i][j]){int z=A[i][j];A[i][j]=0;
    for(int k=j+1;k<2*N;++k)A[i][k]=(A[i][k]+P*P-z*A[j][k])%unsigned(P);}
  }
  int H[N][N][N]{},B[N][N][N]{};bool made[N]{};
  auto build=[&](int i){
   if(made[i])return;made[i]=true;
   for(int j=0;j<N;++j){int z=u[j]*u[i]-C*(i==j);for(int k=0;k<N;++k)z+=Q[j][k]*Q[k][i];H[i][0][j]=(z+P*P)%unsigned(P);B[i][0][j]=(P-Q[j][i]%unsigned(P))%unsigned(P);}
   for(int k=1;k<N;++k)for(int j=0;j<N;++j){int h=0,d=0;
    for(int l=0;l<N;++l){h+=Q[j][l]*H[i][k-1][l];d+=Q[j][l]*B[i][k-1][l];}
    h+=P*P-moment[k-1]*Q[j][i]+u[j]*V[k][i];H[i][k][j]=h%unsigned(P);B[i][k][j]=d%unsigned(P);
   }
  };
  auto coeff=[&](int i,int j,int k){int c=0,d=0;for(int l=0;l<N;++l){c+=H[i][l][j]*A[l][N+k];d+=B[i][l][j]*A[l][N+k];}return std::pair<int,int>{c%unsigned(P),d%unsigned(P)};};
  build(0);auto[c0,d0]=coeff(0,0,0);possible&=f.mask[c0][d0];if(!possible)return true;
  if(N>1){auto[c1,d1]=coeff(0,0,1);possible&=f.mask[c1][d1];if(!possible)return true;}
  for(uint32_t t=possible;t;t&=t-1){int a=__builtin_ctz(t);std::vector<int> v=prefix(a);bool ok=true;
   for(int i=0;i<N&&ok;++i){build(i);for(int j=i;j<N&&ok;++j)for(int k=j;k<N;++k){
    auto[c,d]=coeff(i,j,k);int z=(c+a*d)%unsigned(P);
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
     std::vector<int> best=csp.canonicalize(v);
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
  if(firstrow_filter<17>(allowed,f17)){++cyclic;if(allowed)reconstruct<17>(allowed,f17);return;}
  ++singular;
  for(uint32_t t=allowed;t&&!expired.load(std::memory_order_relaxed);t&=t-1){int a=__builtin_ctz(t);csp.complete_prefix(prefix(a));if(csp.stopped){expired=true;return;}}
 }
 void offdiagonal(int k,uint32_t possible){
  if(!check_time())return;
  if(k==E){finish(possible);return;}
  auto[i,j]=edge[k];
  bool pair=witness_active&&E-2>=N-1&&k>=E-2;
  if(pair&&k==E-2)build_pair_masks(possible);
  uint32_t last_masks[16]{};
  if(!pair&&witness_active&&k==E-1&&k>=N-1){
   for(int wi:supported[k]){const auto&w=witnesses[wi];if(!(possible&(1u<<w.a)))continue;
    int c=w.coef[k],r=-w.residual;
    if(c){if(r%c==0){int z=r/c;if(z>=0&&z<=M)last_masks[z]|=1u<<w.a;}}
    else if(!r)for(int z=0;z<=M;++z)last_masks[z]|=1u<<w.a;
   }
  }
  for(int z=0;z<=M&&!expired.load(std::memory_order_relaxed);++z){
   Q[i][j]=Q[j][i]=z;norm[i]+=z*z;norm[j]+=z*z;--missing[i];--missing[j];
   uint32_t a=possible;
   if(pair){if(k==E-2){uint32_t mask=0;for(int y=0;y<=M;++y)mask|=pair_masks[z][y];a&=mask;}
    else{auto[l,h]=edge[E-2];a&=pair_masks[Q[l][h]][z];}}
   else if(witness_active&&k==E-1&&k>=N-1)a&=last_masks[z];
   a=row_filter(i,a);if(a)a=row_filter(j,a);
   if(M==1&&N>=8){
    // A changed edge affects contractions of its endpoints with every
    // completed row. When a row becomes complete, inspect all its partners.
    if(a&&!missing[i])for(int l=0;l<N&&a;++l)if(l!=i)a=partial_dot_filter(i,l,k+1,a);
    if(a&&!missing[j])for(int l=0;l<N&&a;++l)if(l!=j&&l!=i)a=partial_dot_filter(j,l,k+1,a);
    if(a)for(int l=0;l<N&&a;++l)if(l!=i&&l!=j&&!missing[l]){
     if(missing[i])a=partial_dot_filter(l,i,k+1,a);
     if(a&&missing[j])a=partial_dot_filter(l,j,k+1,a);
    }
   }else{
    if(a&&!missing[i])for(int l=0;l<N&&a;++l)if(l!=i&&!missing[l])a=dot_filter(i,l,a);
    if(a&&!missing[j])for(int l=0;l<N&&a;++l)if(l!=j&&l!=i&&!missing[l])a=dot_filter(j,l,a);
   }
   if(a&&canonical_edges(k+1)){
    if(k==N-2){build_witnesses(a);if(witness_active){a=0;for(int wi:supported[N-1])a|=1u<<witnesses[wi].a;}if(a)offdiagonal(k+1,a);}
    else if(pair||!witness_active||(k==E-1&&k>=N-1))offdiagonal(k+1,a);
    else if(k>=N-1){a=filter_witnesses(k,z,a);if(a){advance_witnesses(k,z,1);offdiagonal(k+1,a);advance_witnesses(k,z,-1);}}
    else offdiagonal(k+1,a);
   }
   norm[i]-=z*z;norm[j]-=z*z;++missing[i];++missing[j];
  }
 }
 void prepare_stabilizers(){
  stabilizers.clear();stabilizer_starts.clear();
  std::array<int,N> p;std::iota(p.begin(),p.end(),0);
  size_t group_order=1;
  for(int lo=0;lo<N;){int hi=lo+1;while(hi<N&&u[hi]==u[lo]&&Q[hi][hi]==Q[lo][lo])++hi;
   for(int k=2;k<=hi-lo&&group_order<=4096;++k)group_order*=k;lo=hi;
  }
  compact_stabilizers=group_order>4096;
  if(compact_stabilizers){
   // Swaps and products of two swaps give cheap necessary partial tests.
   // The exact full-matrix test above handles the rest of the group.
   std::vector<std::pair<int,int>> swaps;
   for(int i=0;i<N;++i)for(int j=i+1;j<N;++j)if(u[i]==u[j]&&Q[i][i]==Q[j][j])swaps.emplace_back(i,j);
   auto add=[&](){
    std::array<int,E> map;int first=E;
    for(int k=0;k<E;++k){auto[i,j]=edge[k];map[k]=edge_index[p[i]][p[j]];if(first==E&&map[k]!=k)first=k;}
    if(first<E){stabilizers.push_back(map);stabilizer_starts.push_back(first);}
   };
   for(size_t a=0;a<swaps.size();++a){auto[i,j]=swaps[a];std::swap(p[i],p[j]);add();
    for(size_t b=a+1;b<swaps.size();++b){auto[k,l]=swaps[b];std::swap(p[k],p[l]);add();std::swap(p[k],p[l]);}
    std::swap(p[i],p[j]);
   }
   return;
  }
  // (u_i,Q_ii) is already sorted. Generate its stabilizer directly,
  // without visiting all N! permutations for every diagonal.
  auto blocks=[&](auto&&self,int lo)->void{
   if(lo==N){
    std::array<int,E> map;int first=E;
    for(int k=0;k<E;++k){auto[i,j]=edge[k];map[k]=edge_index[p[i]][p[j]];if(first==E&&map[k]!=k)first=k;}
    if(first<E){stabilizers.push_back(map);stabilizer_starts.push_back(first);}return;
   }
   int hi=lo+1;while(hi<N&&u[hi]==u[lo]&&Q[hi][hi]==Q[lo][lo])++hi;
   do{self(self,hi);}while(std::next_permutation(p.begin()+lo,p.begin()+hi));
  };blocks(blocks,0);
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
 void run(const std::array<int,N>&v,const std::vector<int>&diagonal_prefix={}){
  bool same=prepared;for(int i=0;i<N;++i)same&=u[i]==v[i];
  if(!same){
   b=v[0];sum=0;g=0;for(int i=0;i<N;++i){u[i]=v[i];sum+=u[i];g=std::gcd(g,u[i]);}
   prepare_masks();prepared=true;
  }
  uint32_t possible=(1u<<(M+1))-1;
  for(size_t k=0;k<diagonal_prefix.size();++k){
   int x=diagonal_prefix[k];Q[k][k]=x;norm[k]=x*x;missing[k]=N-1;
   row_ptr[k]=row_masks.data()+(k*(M+1)+x)*N*norm_length;
   possible=row_filter(k,possible);if(!possible)return;
  }
  diagonal(int(diagonal_prefix.size()),possible);
 }

};

template<int N> int run_all(const char*system,int M,int threads){
 struct Job{std::array<int,N> u;std::vector<int> diagonal;int original;};
 std::vector<std::array<int,N>> prefixes;std::array<int,N> v{};
 auto rec=[&](auto&&self,int k,int lo)->void{if(k==N){prefixes.push_back(v);return;}for(int a=lo;a<=M;++a){v[k]=a;self(self,k+1,a);}};rec(rec,0,0);
 // Split the first two diagonal coordinates when the top-level frontier
 // is small; use one otherwise. Each labeled first matrix belongs to
 // exactly one job, including the weighted folding special case.
 int depth=threads==1?0:(prefixes.size()<size_t(threads)*32?std::min(2,N):1);
 std::vector<Job> jobs;std::vector<int> diagonal;
 for(size_t t=0;t<prefixes.size();++t){
  const auto&u=prefixes[t];
  auto split=[&](auto&&self,int k)->void{
   if(k==depth){jobs.push_back({u,diagonal,int(t)});return;}
   int lo=u[0];if(k&&u[k]==u[k-1])lo=diagonal[k-1];
   for(int x=lo;x<=M;++x){diagonal.push_back(x);self(self,k+1);diagonal.pop_back();}
  };split(split,0);
 }
 std::vector<uint64_t> counts(M+1);uint64_t matrices=0,singular=0,nodes=0,completed=0,sols=0;
 omp_set_num_threads(threads);
 #pragma omp parallel
 {
  Worker<N> w(system,M);
  #pragma omp for schedule(dynamic,1)
  for(size_t t=0;t<jobs.size();++t){if(single_job>=0&&jobs[t].original!=single_job)continue;if(expired.load(std::memory_order_relaxed))continue;
   auto start=Clock::now();auto old=w.csp.sols;auto mat=w.matrices;w.run(jobs[t].u,jobs[t].diagonal);
   #pragma omp critical(progress)
   {if(!expired)++completed;std::cerr<<"job "<<t<<" / "<<jobs.size()<<" done "<<(!expired)<<" u";for(int x:jobs[t].u)std::cerr<<' '<<x;
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
 if(r<4||r>11||M<1||M>15||threads<1||allowance<=0)return 2;
 system_dir=std::filesystem::path(argv[1]).parent_path().string();
 if(argc==7)single_job=std::stoi(argv[6]);
 began=Clock::now();int rc=2;
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==4
 if(r==4)rc=run_all<2>(argv[1],M,threads);
#endif
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==5
 if(r==5)rc=run_all<3>(argv[1],M,threads);
#endif
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==6
 if(r==6)rc=run_all<4>(argv[1],M,threads);
#endif
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==7
 if(r==7)rc=run_all<5>(argv[1],M,threads);
#endif
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==8
 if(r==8)rc=run_all<6>(argv[1],M,threads);
#endif
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==9
 if(r==9)rc=run_all<7>(argv[1],M,threads);
#endif
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==10
 if(r==10)rc=run_all<8>(argv[1],M,threads);
#endif
#if CENSUS_SELFDUAL_RANK==0 || CENSUS_SELFDUAL_RANK==11
 if(r==11)rc=run_all<9>(argv[1],M,threads);
#endif
 std::cout.flush();if(!std::cout)return 2;return rc;
}
