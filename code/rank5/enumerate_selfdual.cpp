#include <algorithm>
#include <array>
#include <vector>
#include <numeric>
#include <iostream>
#include <string>
#include <chrono>
#include <stdexcept>
#include <cmath>
#include <omp.h>
#include <cstdint>
using I=long long;using Vec=std::array<I,20>;using V3=std::array<I,3>;using Mat=std::array<V3,3>;
int M;
constexpr int Pmod=257;
int inverses[Pmod];
uint64_t allowed_a[Pmod][Pmod];
void prepare_modular_filter(){
 for(int i=1;i<Pmod;++i)for(int j=1;j<Pmod;++j)if(i*j%Pmod==1){inverses[i]=j;break;}
 for(int u=0;u<Pmod;++u)for(int v=0;v<Pmod;++v){
  uint64_t mask=0; int z=u;
  for(int a=0;a<=M;++a){if(z<=M)mask|=uint64_t(1)<<a;z+=v;if(z>=Pmod)z-=Pmod;}
  allowed_a[u][v]=mask;
 }
}
bool counts;std::vector<I> cnt;std::vector<std::array<int,20>> perms;thread_local long long cells=0,cyclics=0,singulars=0,completes=0;long long totalcells=0,totalcyclics=0,totalsingulars=0,totalcompletes=0;auto start=std::chrono::steady_clock::now();
bool all_associative(const Vec&v);void emit(const Vec&v){
 if(!all_associative(v))return;
 for(auto&p:perms){Vec w;for(int i=0;i<20;i++)w[i]=v[p[i]];
  if(w[1]!=v[1]||w[2]>w[3])continue;
  if(w<v)return;
 }
 int mu=std::max<I>(1,*std::max_element(v.begin(),v.end()));
 #pragma omp atomic update
 ++cnt[mu];
 if(!counts){
 #pragma omp critical(output)
 {std::cout<<"S";for(I x:v)std::cout<<' '<<x;std::cout<<'\n';}}
}
#include "linear_completion.hpp"
I mod(I a,I n){I r=a%n;return r<0?r+n:r;}
I inv(I a,I n){I r0=n,r1=mod(a,n),s0=0,s1=1;while(r1){I q=r0/r1,r=r0-q*r1,ss=s0-q*s1;r0=r1;r1=r;s0=s1;s1=ss;}return mod(s0,n);}
V3 mul(const Mat&A,const V3&v){V3 w{};for(int i=0;i<3;i++)for(int j=0;j<3;j++)w[i]+=A[i][j]*v[j];return w;}
Mat mul(const Mat&A,const Mat&B){Mat C{};for(int i=0;i<3;i++)for(int j=0;j<3;j++)for(int k=0;k<3;k++)C[i][j]+=A[i][k]*B[k][j];return C;}
I dot(const V3&u,const V3&v){return u[0]*v[0]+u[1]*v[1]+u[2]*v[2];}
V3 cross(const V3&u,const V3&v){return {u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]};}
void singular(Vec v,const Mat&Q,const V3&u,const V3&q,const V3&q2){
 ++singulars;I s=dot(u,u),t=dot(u,q),tr=Q[0][0]+Q[1][1]+Q[2][2];V3 w=cross(u,q);I aa=0,bb=0;
 if(w!=V3{}){
  I al=0,be=0;bool got=false;for(int i=0;i<3&&!got;i++)for(int j=i+1;j<3&&!got;j++){I dd=u[i]*q[j]-u[j]*q[i];if(dd){I x=q2[i]*q[j]-q[i]*q2[j],y=u[i]*q2[j]-q2[i]*u[j];if(x%dd||y%dd)return;al=x/dd;be=y/dd;got=true;}}
  I lam=tr-be,rr=lam*lam-be*lam-al;aa=-lam*rr;bb=(lam*lam-1)*rr-lam*(s*lam+t-be*s);
 }else if(s){
  int ii=0;while(!u[ii])++ii;if(q[ii]%u[ii])return;I lam=q[ii]/u[ii];
  I T=tr-lam,U=Q[0][0]*Q[1][1]+Q[0][0]*Q[2][2]+Q[1][1]*Q[2][2]-Q[0][1]*Q[0][1]-Q[0][2]*Q[0][2]-Q[1][2]*Q[1][2]-lam*T;
  if(T*T==4*U){if(T%2)return;I mu=T/2;aa=-mu*mu+lam*mu;bb=mu*mu*mu-lam*mu*mu-(1+s)*mu+lam;}
  else {aa=lam-T;bb=T*T-U-lam*T-1-s;I a2=U,b2=-T*U+lam*U+lam;if(aa){if(bb%aa||a2*(-bb/aa)+b2)return;}else {if(bb)return;aa=a2;bb=b2;}}
 }else{
  // u=0: a=0 and Q is a symmetric permutation matrix.
  if(Q[0][0]==1&&Q[1][1]==1&&Q[2][2]==1&&Q[0][1]==0&&Q[0][2]==0&&Q[1][2]==0)return; // separate weighted rank-four branch
  auto Q2=mul(Q,Q);for(int i=0;i<3;i++)for(int j=0;j<3;j++)if(Q2[i][j]!=(i==j))return;
  v[0]=0;++completes;linear_completion(v,0);return;
 }
 if(aa){if(bb%aa)return;I a=-bb/aa;if(a<0||a>M)return;v[0]=a;++completes;linear_completion(v,v[1]);}
 else if(!bb)for(int a=0;a<=M;a++){v[0]=a;++completes;linear_completion(v,v[1]);}
}
void cell(Vec v,const Mat&Q,const Mat&Q2,const Mat&Q3,const Mat&Q4){
 ++cells;V3 u{v[1],v[2],v[3]};V3 q=mul(Q,u),q2=mul(Q,q);V3 c0=cross(q,q2),c1=cross(q2,u),c2=cross(u,q);I den=dot(u,c0);
 if(!den){singular(v,Q,u,q,q2);return;}
 ++cyclics;I ss=dot(u,u),tt=dot(u,q);
 I h=Q2[0][0]-1+u[0]*u[0],j=Q3[0][0]-(1+ss)*Q[0][0]+2*q[0]*u[0],k=Q4[0][0]-(1+ss)*Q2[0][0]-tt*Q[0][0]+2*q2[0]*u[0]+q[0]*q[0];
 I a0=h*c0[0]+j*c1[0]+k*c2[0],b0=-Q[0][0]*c0[0]-Q2[0][0]*c1[0]-Q3[0][0]*c2[0];
 auto finish=[&](I a){v[0]=a;int n=10;
  for(int i=0;i<3;i++)for(int j=i;j<3;j++)for(int k=j;k<3;k++){
   I h=Q2[j][i]-(i==j)+u[j]*u[i]-a*Q[j][i];
   I jj=Q3[j][i]-(1+ss)*Q[j][i]+q[j]*u[i]+u[j]*q[i]-a*Q2[j][i];
   I kk=Q4[j][i]-(1+ss)*Q2[j][i]-tt*Q[j][i]+q2[j]*u[i]+q[j]*q[i]+u[j]*q2[i]-a*Q3[j][i];
   I nu=h*c0[k]+jj*c1[k]+kk*c2[k];if(nu%den)return;I z=nu/den;if(z<0||z>M)return;v[n++]=z;
  }
  for(int j:{11,12,13,15,17,18})if(v[j]<v[1])return;emit(v);
 };
 // Necessary finite-field conditions on R_000 and R_001.
 // A deficient denominator mod 257 falls back to the original exact algorithm.
 int dmod=int(den%Pmod);if(dmod<0)dmod+=Pmod;
 if(dmod){
  int dinv=inverses[dmod];
  auto residue=[&](I x){int r=int(x%Pmod);if(r<0)r+=Pmod;return r*dinv%Pmod;};
  uint64_t possible=allowed_a[residue(a0)][residue(b0)];
  if(!possible)return;
  I a1=h*c0[1]+j*c1[1]+k*c2[1];
  I b1=-Q[0][0]*c0[1]-Q2[0][0]*c1[1]-Q3[0][0]*c2[1];
  possible &= allowed_a[residue(a1)][residue(b1)];
  while(possible){int a=__builtin_ctzll(possible);possible&=possible-1;
   I num=a0+b0*a;if(num%den)continue;I z=num/den;if(z<0||z>M)continue;
   num=a1+b1*a;if(num%den)continue;z=num/den;if(z<0||z>M)continue;
   finish(a);
  }
  return;
 }
 if(!b0){if(a0%den)return;I z=a0/den;if(z<0||z>M)return;for(int a=0;a<=M;a++)finish(a);return;}
 I g=std::gcd(b0,den);if(a0%g)return;I step=std::abs(den/g),aa=0;if(step>1)aa=(__int128)mod(-a0/g,step)*inv(b0/g,step)%step;
 for(I a=aa;a<=M;a+=step)finish(a);
}
#include "weighted.hpp"
int main(int argc,char**argv){if(argc<2||argc>3)return 2;M=std::stoi(argv[1]);counts=argc==3;if(counts&&std::string(argv[2])!="--counts")return 2;if(M<1||M>32)throw std::invalid_argument("bound 1..32");cnt.resize(M+1);prepare_modular_filter();
 std::vector<std::array<int,3>>tri;for(int i=0;i<4;i++)for(int j=i;j<4;j++)for(int k=j;k<4;k++)tri.push_back({i,j,k});std::array<int,4>p{0,1,2,3};do{std::array<int,20>map;for(int k=0;k<20;k++){std::array<int,3>q{p[tri[k][0]],p[tri[k][1]],p[tri[k][2]]};std::sort(q.begin(),q.end());map[k]=std::find(tri.begin(),tri.end(),q)-tri.begin();}perms.push_back(map);}while(std::next_permutation(p.begin(),p.end()));
 weighted();omp_set_num_threads(std::min(8,omp_get_max_threads()));
 I size=1;for(int i=0;i<6;i++)size*=M+1;
 #pragma omp parallel
 {
 #pragma omp for schedule(dynamic,512)
 for(I ind=0;ind<size;ind++){
  Vec v{};I temp=ind;for(int j:{4,7,9,5,6,8}){v[j]=temp%(M+1);temp/=M+1;}
  Mat Q{{{v[4],v[5],v[6]},{v[5],v[7],v[8]},{v[6],v[8],v[9]}}};Mat Q2=mul(Q,Q),Q3=mul(Q2,Q),Q4=mul(Q2,Q2);
  I bmax=std::min({v[4],v[7],v[9]});
  for(v[1]=0;v[1]<=bmax;v[1]++)for(v[2]=v[1];v[2]<=M;v[2]++)for(v[3]=v[2];v[3]<=M;v[3]++)cell(v,Q,Q2,Q3,Q4);
 }
 #pragma omp critical(statistics)
 {totalcells+=cells;totalcyclics+=cyclics;totalsingulars+=singulars;totalcompletes+=completes;}
 }
 if(counts)for(int m=1;m<=M;m++)std::cout<<m<<' '<<cnt[m]<<'\n';
 std::cerr<<"cells "<<totalcells<<" cyclic "<<totalcyclics<<" singular "<<totalsingulars<<" completions "<<totalcompletes<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
}
