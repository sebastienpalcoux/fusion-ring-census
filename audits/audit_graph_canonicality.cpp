// Independent brute-force audit of actual Worker<N> graph canonicality.
#define main census_main_not_used
#include "../code/enumerate_selfdual_fast.cpp"
#undef main
#include <random>
#include <stdexcept>

static std::mt19937 rng(20261023);
static uint64_t cases=0,permutations_checked=0,prefix_checks=0;

template<int N> void check(Worker<N>&w){
 std::vector<std::vector<int>> cells;
 for(int i=0;i<N;i++){
  if(!i||w.u[i]!=w.u[i-1]||w.Q[i][i]!=w.Q[i-1][i-1])cells.emplace_back();
  cells.back().push_back(i);
 }
 std::array<int,N> p{},best_p{};std::iota(p.begin(),p.end(),0);
 std::vector<int> original,best,key;
 for(auto[i,j]:w.edge)original.push_back(w.Q[i][j]);
 auto visit=[&](auto&&self,size_t c,int offset)->void{
  if(c==cells.size()){
   ++permutations_checked;key.clear();
   for(auto[i,j]:w.edge)key.push_back(w.Q[p[i]][p[j]]);
   if(best.empty()||key<best){best=key;best_p=p;}return;
  }
  auto cell=cells[c];
  do{for(size_t k=0;k<cell.size();k++)p[offset+k]=cell[k];self(self,c+1,offset+cell.size());}
  while(std::next_permutation(cell.begin(),cell.end()));
 };visit(visit,0,0);
 bool expected=(original==best);
 w.prepare_stabilizers();
 if(w.canonical_matrix()!=expected||w.canonical_edges(w.E)!=expected){
  std::cerr<<"FAIL original N="<<N<<" M="<<w.M<<" case="<<cases<<" expected="<<expected<<'\n';
  throw std::logic_error("canonical predicate mismatch");
 }
 int copy[N][N];
 for(int i=0;i<N;i++)for(int j=0;j<N;j++)copy[i][j]=w.Q[best_p[i]][best_p[j]];
 for(int i=0;i<N;i++)for(int j=0;j<N;j++)w.Q[i][j]=copy[i][j];
 if(!w.canonical_matrix()||!w.canonical_edges(w.E))throw std::logic_error("rejected brute canonical matrix");
 for(int filled=0;filled<=w.E;filled++){
  if(!w.canonical_edges(filled))throw std::logic_error("partial test rejected brute canonical matrix");
  ++prefix_checks;
 }
 ++cases;
}

template<int N> void audit(const std::string&system){
 for(int M:{1,2,3}){
  Worker<N>w(system.c_str(),M);
  int trials=N<=7?300:30;
  for(int t=0;t<trials;t++){
   std::vector<std::pair<int,int>> color;
   for(int i=0;i<N;i++)color.emplace_back(t%5?int(rng()%(M+1)):0,t%5?int(rng()%(M+1)):0);
   std::sort(color.begin(),color.end());
   for(int i=0;i<N;i++){w.u[i]=color[i].first;w.Q[i][i]=color[i].second;}
   for(auto[i,j]:w.edge)w.Q[i][j]=w.Q[j][i]=rng()%(M+1);
   check(w);
  }
  // Highly symmetric graphs stress twin handling and equality branches.
  for(int pattern=0;pattern<6;pattern++){
   for(int i=0;i<N;i++){w.u[i]=0;w.Q[i][i]=0;}
   for(auto[i,j]:w.edge){int z=0;
    if(pattern==1)z=1;
    if(pattern==2)z=(j==i+1||(i==0&&j==N-1));
    if(pattern==3)z=(i%2==0&&j==i+1);
    if(pattern==4)z=(i/3==j/3);
    if(pattern==5)z=((i<N/2)!=(j<N/2));
    w.Q[i][j]=w.Q[j][i]=z;
   }
   check(w);
  }
 }
 std::cout<<"PASS N="<<N<<" cumulative_cases="<<cases<<" permutations="<<permutations_checked<<" prefixes="<<prefix_checks<<'\n';
}

int main(int argc,char**argv){
 if(argc!=2)return 2;system_dir=argv[1];allowance=1e9;began=Clock::now();
 audit<2>(system_dir+"/system4sd.txt");audit<3>(system_dir+"/system5sd.txt");
 audit<4>(system_dir+"/system6sd.txt");audit<5>(system_dir+"/system7sd.txt");
 audit<6>(system_dir+"/system8sd.txt");audit<7>(system_dir+"/system9sd.txt");
 audit<8>(system_dir+"/system10sd.txt");audit<9>(system_dir+"/system11sd.txt");
 std::cout<<"PASS actual C++ canonical_matrix and canonical_edges(E); M=1..3; seed=20261023\n";
}
