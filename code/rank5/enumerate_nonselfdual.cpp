#include <array>
#include <vector>
#include <algorithm>
#include <iostream>
#include <string>
#include <numeric>
#include <cmath>
#include <chrono>
#include <stdexcept>
#include "census_integer.hpp"
using I=long long;int M;bool counts;std::vector<I> cn2,cn4;using V=std::array<I,13>;
void emit2(V v){
if(!((-2*v[10]*v[9] + v[11]*v[8] + v[12]*v[8] + v[3]*v[5] - (v[4]*v[4]) + v[7]*v[9] - (v[8]*v[8])==0) && (-(v[10]*v[10]) + v[10]*v[7] + 2*v[12]*v[8] + v[3]*v[6] - (v[4]*v[4]) - (v[8]*v[8]) - (v[9]*v[9]) + 1==0) && (-(v[10]*v[10]) + (v[11]*v[11]) - (v[12]*v[12]) + (v[5]*v[5]) - (v[6]*v[6]) + (v[9]*v[9]) - 1==0) && (-v[10]*v[4] + v[11]*v[5] - v[12]*v[5] + v[2]*v[5] - v[2]*v[6] + v[4]*v[9]==0) && (-v[10]*v[8] + v[11]*v[9] - v[12]*v[9] + v[4]*v[5] - v[4]*v[6] + v[8]*v[9]==0) && (v[0]*v[3] - (v[1]*v[1]) + v[1]*v[7] + 2*v[2]*v[8] - (v[3]*v[3]) - 2*(v[4]*v[4]) + 1==0) && (v[0]*v[4] - v[1]*v[2] + v[1]*v[8] + v[10]*v[2] + v[2]*v[9] - v[3]*v[4] - v[4]*v[5] - v[4]*v[6]==0) && (v[0]*v[5] + v[1]*v[9] + v[11]*v[2] + v[12]*v[2] - (v[2]*v[2]) - (v[4]*v[4]) - 2*v[5]*v[6]==0) && (v[0]*v[6] + v[1]*v[10] + 2*v[12]*v[2] - (v[2]*v[2]) - (v[4]*v[4]) - (v[5]*v[5]) - (v[6]*v[6]) + 1==0) && (v[1]*v[4] + v[10]*v[4] - v[2]*v[3] + v[3]*v[8] - v[4]*v[7] + v[4]*v[9] - v[5]*v[8] - v[6]*v[8]==0) && (v[1]*v[5] - v[10]*v[5] + v[11]*v[4] + v[12]*v[4] - v[2]*v[4] + v[3]*v[9] - v[4]*v[8] - v[6]*v[9]==0) && (v[1]*v[6] + v[10]*v[3] - v[10]*v[6] + 2*v[12]*v[4] - v[2]*v[4] - v[4]*v[8] - v[5]*v[9]==0)))return;
{V w{};w[0]=v[0];w[1]=v[1];w[2]=v[2];w[3]=v[3];w[4]=v[4];w[5]=v[5];w[6]=v[6];w[7]=v[7];w[8]=v[8];w[9]=v[9];w[10]=v[10];w[11]=v[11];w[12]=v[12];if(w<v)return;}
{V w{};w[0]=v[7];w[1]=v[3];w[2]=v[8];w[3]=v[1];w[4]=v[4];w[5]=v[9];w[6]=v[10];w[7]=v[0];w[8]=v[2];w[9]=v[5];w[10]=v[6];w[11]=v[11];w[12]=v[12];if(w<v)return;}
int mu=1;for(int i=0;i<13;i++)mu=std::max<I>(mu,v[i]);++cn2[mu];if(!counts){std::cout<<"N2";for(int i=0;i<13;i++)std::cout<<' '<<v[i];std::cout<<'\n';}}
void complete2(V v){
Wide A[11][5]{};
A[0][2]=v[5];
A[0][3]=v[9];
A[0][4]=2*v[10]*v[9] - v[11]*v[8] - v[12]*v[8] + (v[4]*v[4]) + (v[8]*v[8]);
A[1][2]=v[6];
A[1][3]=v[10];
A[1][4]=(v[10]*v[10]) - 2*v[12]*v[8] + (v[4]*v[4]) + (v[8]*v[8]) + (v[9]*v[9]) - 1;
A[2][4]=(v[10]*v[10]) - (v[11]*v[11]) + (v[12]*v[12]) - (v[5]*v[5]) + (v[6]*v[6]) - (v[9]*v[9]) + 1;
A[3][4]=v[10]*v[4] - v[11]*v[5] + v[12]*v[5] - v[2]*v[5] + v[2]*v[6] - v[4]*v[9];
A[4][4]=v[10]*v[8] - v[11]*v[9] + v[12]*v[9] - v[4]*v[5] + v[4]*v[6] - v[8]*v[9];
A[5][0]=v[4];
A[5][1]=-v[2] + v[8];
A[5][2]=-v[4];
A[5][4]=-v[10]*v[2] - v[2]*v[9] + v[4]*v[5] + v[4]*v[6];
A[6][0]=v[5];
A[6][1]=v[9];
A[6][4]=-v[11]*v[2] - v[12]*v[2] + (v[2]*v[2]) + (v[4]*v[4]) + 2*v[5]*v[6];
A[7][0]=v[6];
A[7][1]=v[10];
A[7][4]=-2*v[12]*v[2] + (v[2]*v[2]) + (v[4]*v[4]) + (v[5]*v[5]) + (v[6]*v[6]) - 1;
A[8][1]=v[4];
A[8][2]=-v[2] + v[8];
A[8][3]=-v[4];
A[8][4]=-v[10]*v[4] - v[4]*v[9] + v[5]*v[8] + v[6]*v[8];
A[9][1]=v[5];
A[9][2]=v[9];
A[9][4]=v[10]*v[5] - v[11]*v[4] - v[12]*v[4] + v[2]*v[4] + v[4]*v[8] + v[6]*v[9];
A[10][1]=v[6];
A[10][2]=v[10];
A[10][4]=v[10]*v[6] - 2*v[12]*v[4] + v[2]*v[4] + v[4]*v[8] + v[5]*v[9];
const int nr=11,nc=4;int vars[]{0,1,3,7},piv[nc],rank=0;bool isp[nc]{};Wide prev=1;
for(int j=0;j<nc;++j){int hit=rank;while(hit<nr&&A[hit][j]==0)++hit;if(hit==nr)continue;for(int k=j;k<=nc;++k)std::swap(A[hit][k],A[rank][k]);Wide z=A[rank][j];for(int i=rank+1;i<nr;++i){Wide x=A[i][j];for(int k=j+1;k<=nc;++k){Wide y=wsub(wmul(A[i][k],z),wmul(x,A[rank][k]));if(y%prev)throw std::logic_error("Bareiss division");A[i][k]=y/prev;}A[i][j]=0;}prev=z;piv[rank++]=j;isp[j]=true;}
for(int i=rank;i<nr;++i)if(A[i][nc])return;std::vector<int> free;for(int j=0;j<nc;++j)if(!isp[j])free.push_back(j);
auto rec=[&](auto&&self,int k)->void{if(k<(int)free.size()){for(int x=0;x<=M;++x){v[vars[free[k]]]=x;self(self,k+1);}return;}for(int i=rank-1;i>=0;--i){int p=piv[i];Wide rhs=A[i][nc];for(int j=p+1;j<nc;++j)rhs=wsub(rhs,wmul(A[i][j],v[vars[j]]));if(rhs%A[i][p])return;rhs/=A[i][p];if(rhs<0||rhs>M)return;v[vars[p]]=rhs;}emit2(v);};rec(rec,0);}
void emit4(V v){
if(!((2*v[1]*v[6] - (v[2]*v[2]) - (v[4]*v[4]) + 2*v[4]*v[9] - (v[5]*v[5]) - (v[6]*v[6]) + 1==0) && (2*v[1]*v[6] - (v[3]*v[3]) - (v[4]*v[4]) + 2*v[4]*v[9] - (v[6]*v[6]) - (v[7]*v[7]) + 1==0) && ((v[0]*v[0]) - (v[1]*v[1]) + (v[2]*v[2]) + (v[3]*v[3]) - 2*(v[4]*v[4]) - 1==0) && (v[0]*v[2] - v[1]*v[3] + v[2]*v[5] + v[3]*v[6] - v[4]*v[6] - v[4]*v[7]==0) && (v[0]*v[3] - v[1]*v[2] + v[2]*v[6] + v[3]*v[7] - v[4]*v[5] - v[4]*v[6]==0) && (v[0]*v[5] + v[1]*v[7] + v[2]*v[8] - 2*v[3]*v[4] + v[3]*v[9] - 2*v[6]*v[7]==0) && (v[0]*v[6] + v[1]*v[6] - v[2]*v[4] + v[2]*v[9] - v[3]*v[4] + v[3]*v[9] - v[5]*v[7] - (v[6]*v[6])==0) && (v[0]*v[7] + v[1]*v[5] - 2*v[2]*v[4] + v[2]*v[9] + v[3]*v[8] - 2*v[5]*v[6]==0) && (v[1]*v[5] + v[1]*v[7] - v[2]*v[3] - (v[4]*v[4]) + v[4]*v[8] + v[4]*v[9] - v[5]*v[6] - v[6]*v[7]==0) && ((v[2]*v[2]) - (v[3]*v[3]) + (v[5]*v[5]) - (v[7]*v[7])==0) && (v[2]*v[5] - v[3]*v[6] - v[4]*v[6] + v[4]*v[7] + v[5]*v[8] - v[7]*v[9]==0) && (v[2]*v[6] - v[3]*v[7] - v[4]*v[5] + v[4]*v[6] + v[5]*v[9] - v[7]*v[8]==0) && ((v[5]*v[5]) - 2*(v[6]*v[6]) + (v[7]*v[7]) + (v[8]*v[8]) - (v[9]*v[9]) - 1==0)))return;
{V w{};w[0]=v[0];w[1]=v[1];w[2]=v[2];w[3]=v[3];w[4]=v[4];w[5]=v[5];w[6]=v[6];w[7]=v[7];w[8]=v[8];w[9]=v[9];if(w<v)return;}
{V w{};w[0]=v[0];w[1]=v[1];w[2]=v[3];w[3]=v[2];w[4]=v[4];w[5]=v[7];w[6]=v[6];w[7]=v[5];w[8]=v[8];w[9]=v[9];if(w<v)return;}
{V w{};w[0]=v[8];w[1]=v[9];w[2]=v[5];w[3]=v[7];w[4]=v[6];w[5]=v[2];w[6]=v[4];w[7]=v[3];w[8]=v[0];w[9]=v[1];if(w<v)return;}
{V w{};w[0]=v[8];w[1]=v[9];w[2]=v[7];w[3]=v[5];w[4]=v[6];w[5]=v[3];w[6]=v[4];w[7]=v[2];w[8]=v[0];w[9]=v[1];if(w<v)return;}
int mu=1;for(int i=0;i<10;i++)mu=std::max<I>(mu,v[i]);++cn4[mu];if(!counts){std::cout<<"N4";for(int i=0;i<10;i++)std::cout<<' '<<v[i];std::cout<<'\n';}}
void complete4(V v){
Wide A[12][3]{};
A[0][1]=2*v[4];
A[0][2]=-2*v[1]*v[6] + (v[2]*v[2]) + (v[4]*v[4]) + (v[5]*v[5]) + (v[6]*v[6]) - 1;
A[1][1]=2*v[4];
A[1][2]=-2*v[1]*v[6] + (v[3]*v[3]) + (v[4]*v[4]) + (v[6]*v[6]) + (v[7]*v[7]) - 1;
A[2][2]=-(v[0]*v[0]) + (v[1]*v[1]) - (v[2]*v[2]) - (v[3]*v[3]) + 2*(v[4]*v[4]) + 1;
A[3][2]=-v[0]*v[2] + v[1]*v[3] - v[2]*v[5] - v[3]*v[6] + v[4]*v[6] + v[4]*v[7];
A[4][2]=-v[0]*v[3] + v[1]*v[2] - v[2]*v[6] - v[3]*v[7] + v[4]*v[5] + v[4]*v[6];
A[5][0]=v[2];
A[5][1]=v[3];
A[5][2]=-v[0]*v[5] - v[1]*v[7] + 2*v[3]*v[4] + 2*v[6]*v[7];
A[6][1]=v[2] + v[3];
A[6][2]=-v[0]*v[6] - v[1]*v[6] + v[2]*v[4] + v[3]*v[4] + v[5]*v[7] + (v[6]*v[6]);
A[7][0]=v[3];
A[7][1]=v[2];
A[7][2]=-v[0]*v[7] - v[1]*v[5] + 2*v[2]*v[4] + 2*v[5]*v[6];
A[8][0]=v[4];
A[8][1]=v[4];
A[8][2]=-v[1]*v[5] - v[1]*v[7] + v[2]*v[3] + (v[4]*v[4]) + v[5]*v[6] + v[6]*v[7];
A[9][2]=-(v[2]*v[2]) + (v[3]*v[3]) - (v[5]*v[5]) + (v[7]*v[7]);
A[10][0]=v[5];
A[10][1]=-v[7];
A[10][2]=-v[2]*v[5] + v[3]*v[6] + v[4]*v[6] - v[4]*v[7];
A[11][0]=-v[7];
A[11][1]=v[5];
A[11][2]=-v[2]*v[6] + v[3]*v[7] + v[4]*v[5] - v[4]*v[6];
const int nr=12,nc=2;int vars[]{8,9},piv[nc],rank=0;bool isp[nc]{};Wide prev=1;
for(int j=0;j<nc;++j){int hit=rank;while(hit<nr&&A[hit][j]==0)++hit;if(hit==nr)continue;for(int k=j;k<=nc;++k)std::swap(A[hit][k],A[rank][k]);Wide z=A[rank][j];for(int i=rank+1;i<nr;++i){Wide x=A[i][j];for(int k=j+1;k<=nc;++k){Wide y=wsub(wmul(A[i][k],z),wmul(x,A[rank][k]));if(y%prev)throw std::logic_error("Bareiss division");A[i][k]=y/prev;}A[i][j]=0;}prev=z;piv[rank++]=j;isp[j]=true;}
for(int i=rank;i<nr;++i)if(A[i][nc])return;std::vector<int> free;for(int j=0;j<nc;++j)if(!isp[j])free.push_back(j);
auto rec=[&](auto&&self,int k)->void{if(k<(int)free.size()){for(int x=0;x<=M;++x){v[vars[free[k]]]=x;self(self,k+1);}return;}for(int i=rank-1;i>=0;--i){int p=piv[i];Wide rhs=A[i][nc];for(int j=p+1;j<nc;++j)rhs=wsub(rhs,wmul(A[i][j],v[vars[j]]));if(rhs%A[i][p])return;rhs/=A[i][p];if(rhs<0||rhs>M)return;v[vars[p]]=rhs;}emit4(v);};rec(rec,0);}
I sqroot(I q){if(q<0)return -1;I z=std::sqrt((double)q);while((z+1)*(z+1)<=q)++z;while(z*z>q)--z;return z*z==q?z:-1;}
void onepair(){V v{};
 for(v[5]=0;v[5]<=M;v[5]++)for(v[6]=0;v[6]<=M;v[6]++)for(v[9]=0;v[9]<=M;v[9]++)for(v[10]=0;v[10]<=M;v[10]++)for(v[12]=0;v[12]<=M;v[12]++){
 v[11]=sqroot(1+v[12]*v[12]-v[5]*v[5]+v[6]*v[6]-v[9]*v[9]+v[10]*v[10]);if(v[11]<0||v[11]>M)continue;
 I A=v[6]-v[5],B=v[10]-v[9],C=v[11]-v[12];
 if(A&&B){for(v[4]=0;v[4]<=M;v[4]++){I xx=C*v[5]-B*v[4],yy=C*v[9]-A*v[4];if(xx%A||yy%B)continue;v[2]=xx/A;v[8]=yy/B;if(v[2]<0||v[2]>M||v[8]<0||v[8]>M)continue;complete2(v);}}
 else if(B){I xx=C*v[5],yy=C*v[9];if(xx%B||yy%B)continue;v[4]=xx/B;v[8]=yy/B;if(v[4]<0||v[4]>M||v[8]<0||v[8]>M)continue;for(v[2]=0;v[2]<=M;v[2]++)complete2(v);}
 else if(A){I xx=C*v[5],yy=C*v[9];if(xx%A||yy%A)continue;v[2]=xx/A;v[4]=yy/A;if(v[2]<0||v[2]>M||v[4]<0||v[4]>M)continue;for(v[8]=0;v[8]<=M;v[8]++)complete2(v);}
 else if(C*v[5]==0&&C*v[9]==0)for(v[2]=0;v[2]<=M;v[2]++)for(v[4]=0;v[4]<=M;v[4]++)for(v[8]=0;v[8]<=M;v[8]++)complete2(v);
 }
}
void twopairs(){V v{};
 for(v[1]=0;v[1]<=M;v[1]++)for(v[2]=0;v[2]<=M;v[2]++)for(v[3]=0;v[3]<=M;v[3]++)for(v[4]=0;v[4]<=M;v[4]++){
  v[0]=sqroot(1+v[1]*v[1]-v[2]*v[2]-v[3]*v[3]+2*v[4]*v[4]);if(v[0]<0||v[0]>M)continue;
  for(v[5]=0;v[5]<=M;v[5]++){
   v[7]=sqroot(v[2]*v[2]-v[3]*v[3]+v[5]*v[5]);if(v[7]<0||v[7]>M)continue;
   I A=v[3]-v[4],B=-v[0]*v[2]+v[1]*v[3]-v[2]*v[5]+v[4]*v[7];
   I C=v[2]-v[4],D=-v[0]*v[3]+v[1]*v[2]-v[3]*v[7]+v[4]*v[5];
   if(A){if(B%A)continue;v[6]=B/A;if(C*v[6]!=D||v[6]<0||v[6]>M)continue;complete4(v);}
   else if(B==0&&C){if(D%C)continue;v[6]=D/C;if(v[6]<0||v[6]>M)continue;complete4(v);}
   else if(!A&&!B&&!C&&!D)for(v[6]=0;v[6]<=M;v[6]++)complete4(v);
  }
 }
}
int main(int argc,char**argv){if(argc<2||argc>3)return 2;M=std::stoi(argv[1]);if(M<1||M>100)throw std::invalid_argument("bound 1..100");counts=argc==3;if(counts&&std::string(argv[2])!="--counts")return 2;cn2.resize(M+1);cn4.resize(M+1);auto start=std::chrono::steady_clock::now();onepair();twopairs();if(counts)for(int m=1;m<=M;m++)std::cout<<m<<' '<<cn2[m]<<' '<<cn4[m]<<'\n';std::cerr<<"seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';}

