// Independent checks of the optimized necessary conditions.
// Build: g++ -O2 -std=c++17 -I code tests/audit_optimized_pruning.cpp -o audit_pruning
// Run: ./audit_pruning systems/system4sd.txt
#include "completion_solver.hpp"
#include <random>
#include <string>

static std::mt19937 rng(20261018);
static unsigned long long checked_assignments=0, checked_solutions=0;
static int draw(int n){return int(rng()%unsigned(n));}
static long long eval(const Equation&e,const std::vector<int>&x){
 long long ans=0;for(const auto&t:e.ts)ans+=(long long)t.c*(t.a<0?1:x[t.a])*(t.b<0?1:x[t.b]);return ans;
}
static void require(bool p,const char*s){if(!p)throw std::runtime_error(s);}

static void propagation_checks(const char*system){
 CompletionSolver c(system,15,1e9,std::chrono::steady_clock::now());
 require(c.nv>=9,"audit needs the standard rank-four self-dual system");
 c.perms.clear();c.symmetries_.clear();
 for(int trial=0;trial<30000;++trial){
  int M=1+draw(4),nactive=1+draw(4),offset=trial%2?5:0;
  c.M=M;c.dom.assign(c.nv,1);c.trail.clear();
  std::vector<int> planted(c.nv);
  for(int v=0;v<c.nv;++v){planted[v]=draw(M+1);c.dom[v]=1u<<planted[v];}
  for(int v=offset;v<offset+nactive;++v)
   for(int z=0;z<=M;++z)if(draw(2))c.dom[v]|=1u<<z;
  auto domains=c.dom;
  int ne=1+draw(5);c.eqs.assign(ne,{});c.inc.assign(c.nv,{});c.queued_.assign(ne,0);
  bool linear=trial%3==0;
  for(int ei=0;ei<ne;++ei){auto&e=c.eqs[ei];int nt=4+draw(13);
   for(int t=0;t<nt;++t){int a=draw(c.nv+1)-1,b=linear?-1:draw(c.nv+1)-1,coeff=draw(9)-4;
    e.ts.push_back({a,b,coeff});if(a>=0)e.vs.push_back(a);if(b>=0)e.vs.push_back(b);
   }
   e.ts.push_back({-1,-1,int(-eval(e,planted))});
   std::sort(e.vs.begin(),e.vs.end());e.vs.erase(std::unique(e.vs.begin(),e.vs.end()),e.vs.end());
   for(int v:e.vs)c.inc[v].push_back(ei);
  }
  std::vector<Mask> supported(c.nv,0);std::vector<int>x(c.nv);
  auto rec=[&](auto&&self,int v)->void{
   if(v==c.nv){++checked_assignments;for(const auto&e:c.eqs)if(eval(e,x))return;
    ++checked_solutions;for(int i=0;i<c.nv;++i)supported[i]|=1u<<x[i];return;}
   for(Mask d=domains[v];d;d&=d-1){x[v]=__builtin_ctz(d);self(self,v+1);}
  };rec(rec,0);
  require(c.propagate(-1),"propagation discarded a planted solution");
  for(int v=0;v<c.nv;++v)require((supported[v]&~c.dom[v])==0,"propagation discarded an exhaustively verified solution");
 }
 std::cout<<"PASS propagation: 30000 systems, "<<checked_assignments<<" assignments, "<<checked_solutions<<" exact solutions retained\n";
}

// Compare the new scalar-moment expression against the former vector recurrence,
// independently of whether random Q,u happen to extend to fusion rings.
static void moment_checks(){
 for(int trial=0;trial<100000;++trial){
  int N=2+draw(5),P=trial%2?17:257,C=1+draw(2),M=1+draw(15);
  std::vector<std::vector<int>>Q(N,std::vector<int>(N)),V(N+1,std::vector<int>(N));
  std::vector<int>u(N),mom(N),h(N),d(N),w(N+2),e(N);e[0]=1;
  for(int i=0;i<N;++i){u[i]=draw(M+1);V[0][i]=u[i];for(int j=0;j<=i;++j)Q[i][j]=Q[j][i]=draw(M+1);}
  auto mv=[&](const std::vector<int>&x){std::vector<int>y(N);for(int i=0;i<N;++i)for(int j=0;j<N;++j)y[i]=(y[i]+Q[i][j]*x[j])%P;return y;};
  for(int k=1;k<=N;++k)V[k]=mv(V[k-1]);
  for(int k=0;k<N;++k)for(int j=0;j<N;++j)mom[k]=(mom[k]+u[j]*V[k][j])%P;
  for(int k=0;k<=N+1;++k){w[k]=e[0];e=mv(e);}
  for(int j=0;j<N;++j){int z=u[j]*u[0]-C*(j==0);for(int l=0;l<N;++l)z+=Q[j][l]*Q[l][0];h[j]=(z+P*P)%P;d[j]=(P-Q[j][0])%P;}
  for(int k=0;k<N;++k){
   long long z=(N+2)*P*P+w[k+2]-C*w[k];
   for(int t=0;t<=k;++t)z+=V[t][0]*V[k-t][0];
   for(int t=0;t<k;++t)z-=mom[t]*w[k-t];
   require(z>=0,"moment expression offset is too small");
   require(z%P==h[0],"moment identity disagrees with former vector recurrence");
   require((P-w[k+1])%P==d[0],"linear moment coefficient disagrees");
   if(k+1<N){auto nh=mv(h),nd=mv(d);for(int j=0;j<N;++j)nh[j]=(nh[j]+P*P-mom[k]*Q[j][0]+u[j]*V[k+1][0])%P;h=nh;d=nd;}
  }
  // Independently check the half-power symmetry shortcut used to form w.
  int L=(N+2)/2;std::vector<std::vector<int>>W(L+1,std::vector<int>(N));W[0][0]=1;
  for(int k=1;k<=L;++k)W[k]=mv(W[k-1]);
  for(int k=0;k<=N+1;++k){int z=0;for(int j=0;j<N;++j)z+=W[k/2][j]*W[(k+1)/2][j];require(z%P==w[k],"half-power moment mismatch");}
 }
 std::cout<<"PASS moments: 100000 random symmetric matrices, ranks 4--8, both primes, weights 1 and 2\n";
}

static void reachable_checks(){
 for(int trial=0;trial<10000;++trial){
  int N=2+draw(5),M=1+draw(4),C=1+draw(2),b=draw(M+1);std::vector<int>u(N);int sum=0;
  for(int&i:u){i=b+draw(M-b+1);sum+=i;}
  int i=draw(N),j=draw(N),cap=M*sum,lower=-M*M-C,width=cap-lower+1;
  std::vector<unsigned char>reach(cap+1),next(cap+1);reach[0]=1;int used=0;
  for(int k=0;k<N;++k){std::fill(next.begin(),next.end(),0);int lo=i==j?(k!=i?b:0):(k==i||k==j?b:0);
   for(int z=0;z<=used;++z)if(reach[z])for(int x=lo;x<=M;++x)next[z+u[k]*x]=1;
   used+=M*u[k];reach.swap(next);
  }
  std::vector<unsigned char>brute(cap+1);
  auto rec=[&](auto&&self,int k,int z)->void{if(k==N){brute[z]=1;return;}int lo=i==j?(k!=i?b:0):(k==i||k==j?b:0);for(int x=lo;x<=M;++x)self(self,k+1,z+u[k]*x);};rec(rec,0,0);
  require(reach==brute,"reachable tail DP disagrees with exhaustive sums");
  std::vector<unsigned char>feasible(N*width);for(int z=0;z<=cap;++z)feasible[z-lower]=reach[z];
  for(int left=1;left<N;++left)for(int z=lower;z<=cap;++z)
   for(int x=0;x<=M&&z+x*x<=cap;++x)if(feasible[(left-1)*width+z+x*x-lower]){feasible[left*width+z-lower]=1;break;}
  int left=draw(N);std::vector<int>squares;
  auto sq=[&](auto&&self,int k,int z)->void{if(k==left){squares.push_back(z);return;}for(int x=0;x<=M;++x)self(self,k+1,z+x*x);};sq(sq,0,0);
  for(int z=lower;z<=cap;++z){bool ok=false;for(int s:squares)if(z+s>=0&&z+s<=cap&&brute[z+s]){ok=true;break;}require(bool(feasible[left*width+z-lower])==ok,"square-completion DP disagrees with exhaustive sums");}
 }
 std::cout<<"PASS reachable masks: 10000 random domains compared with exhaustive tail and square sums\n";
}
int main(int argc,char**argv){
 try{if(argc!=2)throw std::runtime_error("usage: audit_pruning systems/system4sd.txt");propagation_checks(argv[1]);moment_checks();reachable_checks();}
 catch(const std::exception&e){std::cerr<<"FAIL: "<<e.what()<<'\n';return 1;}
}
