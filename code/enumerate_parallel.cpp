// Disjoint, propagated-domain frontier: no enumeration of impossible raw prefixes.
// A split replaces one domain box by every value of its first unfixed variable.
// Necessary propagation may discard boxes; no solutions are emitted in this phase.
#include <atomic>
#include <deque>
#include <omp.h>
#include "completion_solver.hpp"
int main(int argc,char**argv){
 if(argc!=6){std::cerr<<"usage: enumerate_parallel SYSTEM M SECONDS THREADS TARGET_JOBS\n";return 2;}
 try{
 int M=std::stoi(argv[2]),threads=std::stoi(argv[4]),target=std::stoi(argv[5]);double secs=std::stod(argv[3]);
 if(M<1||M>15||threads<1||threads>64||target<1||target>200000||!(secs>0))return 2;
 auto began=std::chrono::steady_clock::now();
 CompletionSolver seed(argv[1],M,secs,began);
 if(threads==1){
  seed.search();
  std::cerr<<"FINAL bound "<<M<<" complete "<<!seed.stopped<<" jobs "<<!seed.stopped<<" / 1 nodes "<<seed.nodes<<" classes "<<seed.sols<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()<<" counts";
  for(int m=1;m<=M;++m)std::cerr<<' '<<seed.counts[m];std::cerr<<'\n';std::cout.flush();return !std::cout?2:seed.stopped?3:0;
 }
 std::deque<std::vector<Mask>> queue;std::vector<std::vector<Mask>> jobs;
 uint64_t frontier_nodes=1;
 if(seed.propagate(-1))queue.push_back(seed.dom);
 while(!queue.empty()&&queue.size()+jobs.size()<size_t(target)&&!seed.stopped){
  auto box=std::move(queue.front());queue.pop_front();int x=-1;
  for(int v=0;v<seed.nv;++v)if(!seed.single(box[v])){x=v;break;}
  if(x<0){jobs.push_back(std::move(box));continue;}
  for(Mask a=box[x];a&&!seed.stopped;a&=a-1){
   seed.dom=box;seed.dom[x]=a&-a;seed.trail.clear();++frontier_nodes;
   // The box was already propagated to a fixed point. Only x has changed.
   if(seed.propagate(x))queue.push_back(seed.dom);
  }
 }
 while(!queue.empty()){jobs.push_back(std::move(queue.front()));queue.pop_front();}
 if(seed.stopped){std::cerr<<"FINAL bound "<<M<<" complete 0 frontier timeout\n";return 3;}
 const uint64_t nj=jobs.size();
 std::cerr<<"frontier jobs "<<nj<<" preparation_nodes "<<frontier_nodes<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()<<'\n';
 std::atomic<bool> stopped(false);uint64_t done=0,nodes=0,sols=0;
 std::vector<uint64_t> counts(M+1);omp_set_num_threads(threads);
 #pragma omp parallel
 {
  // The frontier already parsed and validated this immutable equation system.
  // Copy it once per worker rather than reparsing the same files in parallel.
  CompletionSolver c=seed;c.nodes=0;c.sols=0;c.stopped=false;
  std::fill(c.counts.begin(),c.counts.end(),0);c.trail.clear();
  #pragma omp for schedule(dynamic,1)
  for(uint64_t j=0;j<nj;++j){if(stopped.load(std::memory_order_relaxed))continue;
   c.dom=jobs[j];c.trail.clear();c.search();
   if(c.stopped)stopped=true;else{
    #pragma omp atomic update
    ++done;
   }
  }
  #pragma omp critical(stats)
  {nodes+=c.nodes;sols+=c.sols;for(int m=1;m<=M;++m)counts[m]+=c.counts[m];}
 }
 bool complete=!stopped&&done==nj;
 std::cerr<<"FINAL bound "<<M<<" complete "<<complete<<" jobs "<<done<<" / "<<nj<<" nodes "<<nodes<<" frontier_nodes "<<frontier_nodes<<" classes "<<sols<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()<<" counts";
 for(int m=1;m<=M;++m)std::cerr<<' '<<counts[m];std::cerr<<'\n';std::cout.flush();if(!std::cout)return 2;return complete?0:3;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
