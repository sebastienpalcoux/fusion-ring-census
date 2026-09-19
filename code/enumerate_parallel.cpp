// Disjoint prefix partition of the complete bounded-domain search.
#include <atomic>
#include <omp.h>
#include "completion_solver.hpp"
int main(int argc,char**argv){
 if(argc!=6){std::cerr<<"usage: enumerate_parallel SYSTEM M SECONDS THREADS PREFIX_LENGTH\n";return 2;}
 int M=std::stoi(argv[2]),threads=std::stoi(argv[4]),depth=std::stoi(argv[5]);double secs=std::stod(argv[3]);
 if(M<1||M>15||threads<1||depth<0||depth>8||secs<=0)return 2;
 uint64_t nj=1;for(int i=0;i<depth;++i)nj*=M+1;if(nj>2000000)return 2;
 auto began=std::chrono::steady_clock::now();std::atomic<bool> stopped(false);uint64_t done=0,nodes=0,sols=0;
 std::vector<uint64_t> counts(M+1);omp_set_num_threads(threads);
 #pragma omp parallel
 {
  CompletionSolver c(argv[1],M,secs,began);
  if(depth>c.nv)std::abort();
  #pragma omp for schedule(dynamic,1)
  for(uint64_t j=0;j<nj;++j){if(stopped.load(std::memory_order_relaxed))continue;
   std::vector<int> p(depth);uint64_t z=j;for(int k=depth-1;k>=0;--k){p[k]=z%(M+1);z/=M+1;}
   c.complete_prefix(p);if(c.stopped)stopped=true;else{
    #pragma omp atomic update
    ++done;
   }
  }
  #pragma omp critical(stats)
  {nodes+=c.nodes;sols+=c.sols;for(int m=1;m<=M;++m)counts[m]+=c.counts[m];}
 }
 bool complete=!stopped&&done==nj;
 std::cerr<<"FINAL bound "<<M<<" complete "<<complete<<" jobs "<<done<<" / "<<nj<<" nodes "<<nodes<<" classes "<<sols<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()<<" counts";
 for(int m=1;m<=M;++m)std::cerr<<' '<<counts[m];std::cerr<<'\n';if(!std::cout)return 2;return complete?0:3;
}
