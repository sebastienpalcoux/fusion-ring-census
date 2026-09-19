// Independent rank-four census; see finite_sections/census.tex.
// Exact linear Diophantine elimination and S3 representatives. No input list.
#include <algorithm>
#include <array>
#include <cmath>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
#include <omp.h>
using I=long long;
using P=std::array<I,10>;
bool valid(const P&p){auto[a,b,c,d,e,f,g,h,i,j]=p;return
 a*d-b*b+b*g+c*h-d*d-e*e+1==0&&a*e-b*c+b*h+c*i-d*e-e*f==0&&
 b*e-c*d+d*h-e*g+e*i-f*h==0&&a*f+b*i-c*c+c*j-e*e-f*f+1==0&&
 b*f-c*e+d*i-e*h+e*j-f*i==0&&d*f-e*e+g*i-h*h+h*j-i*i+1==0;}
I mod(I a,I n){I r=a%n;return r<0?r+n:r;}
I inverse(I a,I n){
 I r0=n,r1=mod(a,n),x0=0,x1=1;
 while(r1){I q=r0/r1,r=r0-q*r1,x=x0-q*x1;r0=r1;r1=r;x0=x1;x1=x;}
 if(r0!=1)throw std::logic_error("noninvertible residue");
 return mod(x0,n);
}
int main(int argc,char**argv){
 if(argc<2||argc>3)return 2;
 I M=std::stoll(argv[1]);bool counts=argc==3&&std::string(argv[2])=="--counts";
 if(argc==3&&!counts)return 2;
 // Degree-four expressions use int64; modular products use signed int128.
 // At M<=1000, even 100(M+1)^5 is strictly less than 2^63.
 if(M<1||M>1000)throw std::invalid_argument("bound must lie in [1,1000]");
 auto has=[&](I x){return 0<=x&&x<=M;};
 const std::array<std::array<int,3>,10> triples{{{0,0,0},{0,0,1},{0,0,2},
   {0,1,1},{0,1,2},{0,2,2},{1,1,1},{1,1,2},{1,2,2},{2,2,2}}};
 std::vector<std::array<int,10>> maps;std::array<int,3> perm{0,1,2};
 do{std::array<int,10> map{};for(int k=0;k<10;++k){
   std::array<int,3> tri{perm[triples[k][0]],perm[triples[k][1]],perm[triples[k][2]]};
   std::sort(tri.begin(),tri.end());map[k]=std::find(triples.begin(),triples.end(),tri)-triples.begin();
  }maps.push_back(map);
 }while(std::next_permutation(perm.begin(),perm.end()));
 std::vector<I> sd(M+1),ns(M+1);
 auto emit=[&](const P&p){
  if(!valid(p))return;
  // b is minimal among the six mixed entries. Compare only images
  // preserving this condition, not all images of the tuple.
  for(const auto&map:maps){if(p[map[1]]!=p[1])continue;
   for(int k=0;k<10;++k){if(p[map[k]]<p[k])return;if(p[map[k]]>p[k])break;}}
  I mu=std::max<I>(1,*std::max_element(p.begin(),p.end()));
  #pragma omp atomic update
  ++sd[mu];
  if(!counts){
   #pragma omp critical(output)
   {std::cout<<"S";for(I v:p)std::cout<<' '<<v;std::cout<<'\n';}}
 };
 // Every orbit has b=min(b,c,d,f,h,i). Positive minimal mixed entry.
 #pragma omp parallel for schedule(dynamic,1)
 for(I b=1;b<=M;++b)for(I c=b;c<=M;++c)for(I d=b;d<=M;++d)
 for(I e=0;e<=M;++e)for(I f=b;f<=M;++f){
  I H0=e*(d+f)+b*c,G0=b*b+d*d+e*e-1,J0=c*c+e*e+f*f-1;
  I A=e*(b*b-c*c)+b*c*(f-d),C=e*(b*f-c*e);
  I B0=b*b*b*e-b*b*c*d+b*(d-f)*H0-e*b*G0+e*c*H0;
  auto finish=[&](I a,I i){
   if(i<b||i>M)return;
   I hh=H0-a*e-c*i;if(hh%b)return;I h=hh/b;if(h<b||h>M)return;
   I gg=G0-a*d-c*h;if(gg%b)return;I g=gg/b;if(!has(g))return;
   I jj=J0-a*f-b*i;if(jj%c)return;I j=jj/c;if(!has(j))return;
   emit({a,b,c,d,e,f,g,h,i,j});
  };
  // C*a+A*i=-B0. Retain every bounded solution, including zeros.
  if(A){
   I div=std::gcd(A,C);if(B0%div)continue;I step=std::abs(A/div),a0=0;
   if(step>1)a0=static_cast<I>((static_cast<__int128>(mod(-B0/div,step))*inverse(C/div,step))%step);
   for(I a=a0;a<=M;a+=step){I rhs=-B0-C*a;if(rhs%A==0)finish(a,rhs/A);}
  }else if(C){if(B0%C==0&&has(-B0/C))for(I i=b;i<=M;++i)finish(-B0/C,i);}
  else if(B0==0)for(I a=0;a<=M;++a)for(I i=b;i<=M;++i)finish(a,i);
 }
 // b=0<c, e>0: i integrality gives a=d+f modulo c/gcd(c,e).
 #pragma omp parallel for schedule(dynamic,1)
 for(I c=1;c<=M;++c)for(I d=0;d<=M;++d)for(I e=1;e<=M;++e){
  I step=c/std::gcd(c,e);
  for(I f=0;f<=M;++f){
   I lo=std::max<I>(0,d+f-c*M/e),hi=std::min(M,d+f);
   auto restrict_a=[&](I q,I numerator){
    if(q){lo=std::max(lo,(numerator-c*M+q-1)/q);hi=std::min(hi,numerator/q);}
    else if(numerator<0||numerator>c*M){lo=1;hi=0;}
   };
   restrict_a(d,d*d+e*e-1);restrict_a(f,c*c+e*e+f*f-1);
   if(lo>hi)continue;
   I a0=lo+mod(d+f-lo,step);
   for(I a=a0;a<=hi;a+=step){
    I hh=d*d+e*e-a*d-1,ii=e*(d+f-a),jj=c*c+e*e+f*f-a*f-1;
    if(hh%c||ii%c||jj%c)continue;
    I h=hh/c,i=ii/c,j=jj/c;if(!has(h)||!has(i)||!has(j))continue;
    I gg=h*(d-f)+e*i-c*d;
    if(gg%e==0&&has(gg/e))emit({a,0,c,d,e,f,gg/e,h,i,j});
   }
  }
 }
 // b=0<c, e=0. Necessarily d>0 and h>0; h(d-f)=cd fixes f.
 #pragma omp parallel for schedule(dynamic,1)
 for(I c=1;c<=M;++c)for(I d=1;d<=M;++d){
  if(std::gcd(c,d)!=1)continue;
  I a0=c==1?0:mod(d-inverse(d,c),c);
  for(I a=a0;a<=M;a+=c){
   I hh=d*d-a*d-1;if(hh<=0||hh%c)continue;I h=hh/c;
   if(!has(h)||c*d%h)continue;I f=d-c*d/h;if(!has(f))continue;
   I jj=c*c+f*f-a*f-1;if(jj%c)continue;I j=jj/c;if(!has(j))continue;
   for(I g=0;g<=M;++g)emit({a,0,c,d,0,f,g,h,0,j});
  }
 }
 // b=c=0<e: a=d+f and df=e^2-1.
 #pragma omp parallel for schedule(dynamic,1)
 for(I e=1;e<=M;++e)for(I d=0;d<=M;++d){
  I rhs=e*e-1;
  auto finish=[&](I f){I a=d+f;if(!has(f)||!has(a))return;
   for(I h=0;h<=M;++h)for(I i=0;i<=M;++i){
    I gg=h*(d-f)+e*i,jj=e*h+i*(f-d);
    if(gg%e==0&&jj%e==0&&has(gg/e)&&has(jj/e))emit({a,0,0,d,e,f,gg/e,h,i,jj/e});
   }
  };
  if(d){if(rhs%d==0)finish(rhs/d);}else if(rhs==0)for(I f=0;f<=M;++f)finish(f);
 }
 // b=c=e=0 forces a=0,d=f=1. Solve gi+hj=h^2+i^2-2.
 #pragma omp parallel for schedule(dynamic,1)
 for(I h=0;h<=M;++h)for(I i=0;i<=M;++i){
  I rhs=h*h+i*i-2;
  if(h){for(I g=0;g<=M;++g){I jj=rhs-g*i;if(jj%h==0&&has(jj/h))emit({0,0,0,1,0,1,g,h,i,jj/h});}}
  else if(i&&rhs%i==0&&has(rhs/i))for(I j=0;j<=M;++j)emit({0,0,0,1,0,1,rhs/i,0,i,j});
 }
 // One dual pair. Swapping it fixes the tuple, so each tuple is one class.
 #pragma omp parallel for schedule(dynamic,1)
 for(I c=0;c<=M;++c)for(I d=0;d<=M;++d)for(I e=0;e<=M;++e){
  I q=1+c*c-d*d+e*e;if(q<0)continue;
  I f=static_cast<I>(std::sqrt(static_cast<double>(q)));
  while((f+1)*(f+1)<=q)++f;while(f*f>q)--f;
  if(f*f!=q||!has(f))continue;
  auto finish=[&](I b){
   I rhs=b*b-2*b*e+c*c+d*d-1;
   auto test=[&](I a){if(a*c-b*b+2*b*e-c*c-d*d+1==0&&
    a*d-b*b+b*e+b*f-2*c*d==0&&b*(c-d)+d*(e-f)==0){
     
     #pragma omp atomic update
     ++ns[std::max({I(1),a,b,c,d,e,f})];
     if(!counts){
      #pragma omp critical(output)
      {std::cout<<"N "<<a<<' '<<b<<' '<<c<<' '<<d<<' '<<e<<' '<<f<<'\n';}}}};
   if(c){if(rhs%c==0&&has(rhs/c))test(rhs/c);}
   else if(d){rhs=b*b-b*e-b*f+2*c*d;if(rhs%d==0&&has(rhs/d))test(rhs/d);}
   else for(I a=0;a<=M;++a)test(a);
  };
  if(c!=d){I rhs=-d*(e-f);if(rhs%(c-d)==0&&has(rhs/(c-d)))finish(rhs/(c-d));}
  else if(d*(e-f)==0)for(I b=0;b<=M;++b)finish(b);
 }
 if(counts)for(I m=1;m<=M;++m)std::cout<<m<<' '<<sd[m]+ns[m]<<' '<<sd[m]<<' '<<ns[m]<<'\n';
}
