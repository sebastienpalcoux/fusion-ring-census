// Weighted rank-four associativity with constant 2, for g fixing the other three basis elements.
void weighted(){
 auto has=[&](I x){return 0<=x&&x<=M;};
 const std::array<std::array<int,3>,10> tri{{{0,0,0},{0,0,1},{0,0,2},{0,1,1},{0,1,2},{0,2,2},{1,1,1},{1,1,2},{1,2,2},{2,2,2}}};
 auto emit=[&](std::array<I,10> p){
  std::vector<Vec> vv;std::array<int,3>perm{0,1,2};do{
   Vec v{};v[4]=v[7]=v[9]=1;for(int k=0;k<10;k++){std::array<int,3>q{perm[tri[k][0]],perm[tri[k][1]],perm[tri[k][2]]};std::sort(q.begin(),q.end());v[10+k]=p[std::find(tri.begin(),tri.end(),q)-tri.begin()];}vv.push_back(v);
  }while(std::next_permutation(perm.begin(),perm.end()));std::sort(vv.begin(),vv.end());vv.erase(std::unique(vv.begin(),vv.end()),vv.end());
  // This callback is itself called repeatedly under mixed-entry normalizations.
  // Retain the lexicographically least triple-tensor among permutations preserving minimal p[1].
  for(const Vec&v:vv){const auto*q=&v[10];if(q[1]!=p[1])continue;bool less=false;for(int k=0;k<10;k++){if(q[k]<p[k]){less=true;break;}if(q[k]>p[k])break;}if(less)return;}
  for(const Vec&v:vv)::emit(v);
 };
 // Every orbit has b=min(b,c,d,f,h,i). Positive minimal mixed entry.
 for(I b=1;b<=M;++b)for(I c=b;c<=M;++c)for(I d=b;d<=M;++d)
 for(I e=0;e<=M;++e)for(I f=b;f<=M;++f){
  I H0=e*(d+f)+b*c,G0=b*b+d*d+e*e-2,J0=c*c+e*e+f*f-2;
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
   if(step>1)a0=static_cast<I>((static_cast<__int128>(mod(-B0/div,step))*inv(C/div,step))%step);
   for(I a=a0;a<=M;a+=step){I rhs=-B0-C*a;if(rhs%A==0)finish(a,rhs/A);}
  }else if(C){if(B0%C==0&&has(-B0/C))for(I i=b;i<=M;++i)finish(-B0/C,i);}
  else if(B0==0)for(I a=0;a<=M;++a)for(I i=b;i<=M;++i)finish(a,i);
 }
 // b=0<c, e>0: i integrality gives a=d+f modulo c/gcd(c,e).
 for(I c=1;c<=M;++c)for(I d=0;d<=M;++d)for(I e=1;e<=M;++e){
  I step=c/std::gcd(c,e);
  for(I f=0;f<=M;++f){
   I lo=std::max<I>(0,d+f-c*M/e),hi=std::min<I>(M,d+f);
   auto restrict_a=[&](I q,I numerator){
    if(q){lo=std::max(lo,(numerator-c*M+q-1)/q);hi=std::min(hi,numerator/q);}
    else if(numerator<0||numerator>c*M){lo=1;hi=0;}
   };
   restrict_a(d,d*d+e*e-2);restrict_a(f,c*c+e*e+f*f-2);
   if(lo>hi)continue;
   I a0=lo+mod(d+f-lo,step);
   for(I a=a0;a<=hi;a+=step){
    I hh=d*d+e*e-a*d-2,ii=e*(d+f-a),jj=c*c+e*e+f*f-a*f-2;
    if(hh%c||ii%c||jj%c)continue;
    I h=hh/c,i=ii/c,j=jj/c;if(!has(h)||!has(i)||!has(j))continue;
    I gg=h*(d-f)+e*i-c*d;
    if(gg%e==0&&has(gg/e))emit({a,0,c,d,e,f,gg/e,h,i,j});
   }
  }
 }
 // b=0<c, e=0. Necessarily d>0 and h>0; h(d-f)=cd fixes f.
 for(I c=1;c<=M;++c)for(I d=1;d<=M;++d){
  I gg=std::gcd(c,d);if(2%gg)continue;I step=c/gg;
  I a0=step==1?0:mod(((d*d-2)/gg)*inv(d/gg,step),step);
  for(I a=a0;a<=M;a+=step){
   I hh=d*d-a*d-2;if(hh<=0||hh%c)continue;I h=hh/c;
   if(!has(h)||c*d%h)continue;I f=d-c*d/h;if(!has(f))continue;
   I jj=c*c+f*f-a*f-2;if(jj%c)continue;I j=jj/c;if(!has(j))continue;
   for(I g=0;g<=M;++g)emit({a,0,c,d,0,f,g,h,0,j});
  }
 }
 // b=c=0<e: a=d+f and df=e^2-2.
 for(I e=1;e<=M;++e)for(I d=0;d<=M;++d){
  I rhs=e*e-2;
  auto finish=[&](I f){I a=d+f;if(!has(f)||!has(a))return;
   for(I h=0;h<=M;++h)for(I i=0;i<=M;++i){
    I gg=h*(d-f)+e*i,jj=e*h+i*(f-d);
    if(gg%e==0&&jj%e==0&&has(gg/e)&&has(jj/e))emit({a,0,0,d,e,f,gg/e,h,i,jj/e});
   }
  };
  if(d){if(rhs%d==0)finish(rhs/d);}else if(rhs==0)for(I f=0;f<=M;++f)finish(f);
 }
 // b=c=e=0 forces a=1,d=f=2. Solve gi+hj=h^2+i^2-6.
 if(M>=2)
 for(I h=0;h<=M;++h)for(I i=0;i<=M;++i){
  I rhs=h*h+i*i-6;
  if(h){for(I g=0;g<=M;++g){I jj=rhs-g*i;if(jj%h==0&&has(jj/h))emit({1,0,0,2,0,2,g,h,i,jj/h});}}
  else if(i&&rhs%i==0&&has(rhs/i))for(I j=0;j<=M;++j)emit({1,0,0,2,0,2,rhs/i,0,i,j});
 }
}
