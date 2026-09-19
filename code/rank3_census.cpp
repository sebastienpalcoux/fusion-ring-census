// Complete rank-three fusion-ring enumeration, up to based isomorphism.
// Self-dual basis (1,X,Y):
// X^2=1+mX+kY, XY=kX+lY, Y^2=1+lX+nY.
// The sole associativity equation is k*k+l*l=1+l*m+k*n.
// Swapping X,Y sends (k,l,m,n) to (l,k,n,m).
// Canonical representatives: k<l, or k=l and m<=n.
// The only non-self-dual rank-three ring is Z[C3].
// Usage: ./rank3_census M [--emit]
// Default output: exact_multiplicity count. --emit: C3 or S k l m n.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using I=std::int64_t;
I inverse_coprime(I a,I mod){
 I r0=mod,r1=a%mod,s0=0,s1=1;
 while(r1){I q=r0/r1,r=r0-q*r1,s=s0-q*s1;r0=r1;r1=r;s0=s1;s1=s;}
 if(r0!=1)return -1;
 s0%=mod;return s0<0?s0+mod:s0;
}
int main(int argc,char**argv){
 try{
  if(argc<2||argc>3)throw std::invalid_argument("usage: rank3_census M [--emit]");
  I M=std::stoll(argv[1]);if(M<1||M>1000)throw std::invalid_argument("M must be 1..1000");
  bool emit=argc==3;if(emit&&std::string(argv[2])!="--emit")throw std::invalid_argument("unknown option");
  auto start=std::chrono::steady_clock::now();std::vector<I>cnt(M+1,0);
  auto put=[&](I k,I l,I m,I n){
   if(k<0||l<0||m<0||n<0||std::max({k,l,m,n})>M||k*k+l*l!=1+l*m+k*n)
    throw std::logic_error("invalid solution");
   ++cnt[std::max({I(1),k,l,m,n})];
   if(emit)std::cout<<"S "<<k<<' '<<l<<' '<<m<<' '<<n<<'\n';
  };
  ++cnt[1];if(emit)std::cout<<"C3\n";
  // k=0 forces l=1,m=0, with n arbitrary.
  for(I n=0;n<=M;++n)put(0,1,0,n);
  // k=l forces k=l=1,m+n=1; use m<=n.
  put(1,1,0,1);
  for(I l=2;l<=M;++l)for(I k=1;k<l;++k){
   I inv=k==1?0:inverse_coprime(l,k);if(inv<0)continue;
   I C=k*k+l*l-1;
   I m0=k==1?0:((C%k)*inv)%k;
   I n0=(C-l*m0)/k;
   I lo=std::max<I>(0,(n0-M+l-1)/l);
   I hi=std::min((M-m0)/k,n0/l);
   for(I t=lo;t<=hi;++t)put(k,l,m0+k*t,n0-l*t);
  }
  I total=0;for(I j=1;j<=M;++j){total+=cnt[j];if(!emit)std::cout<<j<<' '<<cnt[j]<<'\n';}
  std::cerr<<"M="<<M<<" total="<<total<<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
