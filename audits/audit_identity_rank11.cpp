#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <random>
int main(){std::mt19937 rng(20261018);uint64_t total=0;long long observed=0;
 for(int n=2;n<=9;++n)for(int C=1;C<=2;++C)for(int trial=0;trial<10000;++trial){
  int M=trial%15+1,a=rng()%(M+1),u[9]{},Q[9][9]{},T[9][9]{};
  for(int i=0;i<n;++i){u[i]=rng()%(M+1);for(int j=i;j<n;++j){Q[i][j]=Q[j][i]=rng()%(M+1);T[i][j]=T[j][i]=rng()%(M+1);}}
  // T is the full symmetric tail multiplication matrix for generator 0.
  // Derive the moment residual from two direct associativity blocks:
  // B=T u-Q² e0-u u0+C e0+a Q e0, K=[Q,T]-q uᵀ+u qᵀ.
  long long B[9]{},K[9][9]{};
  for(int i=0;i<n;++i){B[i]=C*(i==0)+(long long)a*Q[i][0]-(long long)u[i]*u[0];
   for(int j=0;j<n;++j)B[i]+=(long long)T[i][j]*u[j]-(long long)Q[i][j]*Q[j][0];
   for(int j=0;j<n;++j){K[i][j]=-(long long)Q[i][0]*u[j]+(long long)u[i]*Q[0][j];
    for(int k=0;k<n;++k)K[i][j]+=(long long)Q[i][k]*T[k][j]-(long long)T[i][k]*Q[k][j];}
  }
  long long direct=0;for(int j=0;j<n;++j)direct+=(long long)Q[0][j]*B[j]-K[0][j]*u[j];
  int qnorm=0,qu=0,unorm=0;for(int i=0;i<n;++i){qnorm+=Q[0][i]*Q[0][i];qu+=Q[0][i]*u[i];unorm+=u[i]*u[i];}
  int expanded=C*Q[0][0]-2*u[0]*qu+unorm*Q[0][0]+a*qnorm;
  for(int j=0;j<n;++j)expanded+=(T[0][j]*u[j]-Q[0][j]*Q[0][j])*Q[j][j];
  for(int j=0;j<n;++j)for(int l=j+1;l<n;++l)expanded+=(T[0][j]*u[l]+T[0][l]*u[j]-2*Q[0][j]*Q[0][l])*Q[j][l];
  assert(expanded==direct);
  long long Q2[9][9]{},Qu[9]{},Qt[9]{},Qq[9]{};
  for(int i=0;i<n;++i)for(int j=0;j<n;++j){
   Qu[i]+=(long long)Q[i][j]*u[j];Qt[i]+=(long long)Q[i][j]*T[0][j];Qq[i]+=(long long)Q[i][j]*Q[0][j];
   for(int k=0;k<n;++k)Q2[i][j]+=(long long)Q[i][k]*Q[k][j];
  }
  long long direct2=0,expanded2=-(long long)qu*qu+(C+(long long)unorm)*qnorm;
  for(int i=0;i<n;++i){
   direct2+=Q2[0][i]*B[i]-K[0][i]*Qu[i];
   for(int j=0;j<n;++j)direct2-=(long long)Q[0][i]*K[i][j]*u[j];
   expanded2+=Qu[i]*Qt[i]-Qq[i]*Qq[i]-2LL*u[0]*Q[0][i]*Qu[i]+(long long)Q[0][0]*u[i]*Qu[i]+(long long)a*Q[0][i]*Qq[i];
  }
  assert(expanded2==direct2);observed=std::max(observed,std::abs(direct2));++total;
 }
 std::cout<<"PASS direct_associativity_first_and_second_moment_identities="<<total<<" ranks=4..11 bounds=1..15 C=1,2 seed=20261018 max_observed_residual="<<observed<<'\n';
}
