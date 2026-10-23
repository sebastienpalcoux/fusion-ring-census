// Independent exhaustive support check for partial-dot masks at M=1.
#define main census_main_not_used
#include "../code/enumerate_selfdual_fast.cpp"
#undef main
#include <random>
#include <stdexcept>

static uint64_t cases=0, completions=0;
static std::mt19937 rng(20261023);

template<int N> void audit(const std::string& system){
 for(int C:{1,2}){
  Worker<N> w(system.c_str(),1,C);
  for(int ones=0;ones<=N;ones++){
   for(int i=0;i<N;i++)w.u[i]=(i>=N-ones);
   w.b=w.u[0];w.sum=ones;w.g=ones?1:0;w.prepare_masks();
   for(int trial=0;trial<3;trial++){
    for(int i=0;i<N;i++)for(int j=i;j<N;j++)w.Q[i][j]=w.Q[j][i]=rng()%2;
    for(int filled=0;filled<=w.E;filled++)for(int i=0;i<N;i++){
     bool complete=true;
     for(int k=0;k<N;k++)if(k!=i&&w.edge_index[i][k]>=filled)complete=false;
     if(!complete)continue;
     for(int j=0;j<N;j++)if(j!=i){
      auto got=w.partial_dot_filter(i,j,filled,3);
      std::vector<int> unknown,original;
      for(int k=0;k<N;k++)if(k!=j&&w.edge_index[k][j]>=filled){unknown.push_back(k);original.push_back(w.Q[k][j]);}
      uint32_t expected=0;
      for(unsigned bits=0;bits<(1u<<unknown.size());bits++){
       for(size_t k=0;k<unknown.size();k++)w.Q[unknown[k]][j]=w.Q[j][unknown[k]]=(bits>>k)&1;
       expected|=w.dot_filter(i,j,3);++completions;
      }
      for(size_t k=0;k<unknown.size();k++)w.Q[unknown[k]][j]=w.Q[j][unknown[k]]=original[k];
      if(got!=expected){std::cerr<<"FAIL N="<<N<<" C="<<C<<" ones="<<ones<<" trial="<<trial<<" filled="<<filled<<" i="<<i<<" j="<<j<<" got="<<got<<" expected="<<expected<<'\n';throw std::logic_error("partial-dot support mismatch");}
      for(unsigned mask=0;mask<4;mask++)if(w.partial_dot_filter(i,j,filled,mask)!=(expected&mask))throw std::logic_error("mask intersection mismatch");
      ++cases;
     }
    }
   }
  }
 }
 std::cout<<"PASS rank="<<N+2<<" cumulative_cases="<<cases<<" cumulative_completions="<<completions<<'\n';
}

int main(int argc,char**argv){
 if(argc!=2)return 2;system_dir=argv[1];allowance=1e9;began=Clock::now();
 audit<7>(system_dir+"/system9sd.txt");
 audit<8>(system_dir+"/system10sd.txt");
 audit<9>(system_dir+"/system11sd.txt");
 std::cout<<"PASS all partial-dot supports, M=1 C=1,2 all sorted binary u, all lex-prefix lengths, all complete-row pairs, seed=20261023\n";
}
