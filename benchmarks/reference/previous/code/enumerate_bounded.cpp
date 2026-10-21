// The serial frontend shares the same exact solver as parallel completion.
#include "completion_solver.hpp"
int main(int argc,char**argv){
 if(argc!=4){std::cerr<<"usage: enumerate_general SYSTEM MAX_MULTIPLICITY MAX_SECONDS\n";return 2;}
 try{
  int M=std::stoi(argv[2]);double seconds=std::stod(argv[3]);
  if(seconds<=0)return 2;
  auto began=std::chrono::steady_clock::now();
  CompletionSolver c(argv[1],M,seconds,began);c.search();
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count();
  std::cerr<<"rank "<<c.rank_<<" pairs "<<c.pairs_<<" bound "<<M<<" complete "<<(!c.stopped)<<" nodes "<<c.nodes<<" classes "<<c.sols<<" seconds "<<sec<<" counts";
  for(int m=1;m<=M;m++)std::cerr<<' '<<c.counts[m];std::cerr<<'\n';
  if(!std::cout){std::cerr<<"Output write failed\n";return 2;}return c.stopped?3:0;
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 2;}
}
