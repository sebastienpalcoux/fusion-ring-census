// Deterministic, lossless rank-four parameter sorting and full tensor export.
// C++17, no external libraries. The separate verifier checks all ring axioms.
#include <algorithm>
#include <array>
#include <charconv>
#include <chrono>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
struct Row { char tag; std::array<int,10> v{}; };
int main(int argc,char**argv){
 if(argc!=4){std::cerr<<"usage: export_rank4 INPUT SORTED_PARAMETERS FULL_TABLES\n";return 2;}
 auto start=std::chrono::steady_clock::now();
 try{
  std::ifstream in(argv[1]);if(!in)throw std::runtime_error("cannot open input");
  std::vector<Row> rows;rows.reserve(1000000);Row row;
  while(in>>row.tag){row.v.fill(0);int n=row.tag=='S'?10:row.tag=='N'?6:0;
   if(!n)throw std::runtime_error("invalid record tag");
   for(int i=0;i<n;++i)if(!(in>>row.v[i])||row.v[i]<0||row.v[i]>1000)throw std::runtime_error("invalid parameter");
   rows.push_back(row);
  }
  if(!in.eof()||rows.empty())throw std::runtime_error("invalid or empty input");
  auto less=[](const Row&a,const Row&b){return a.tag!=b.tag?a.tag<b.tag:a.v<b.v;};
  std::sort(rows.begin(),rows.end(),less);
  std::ofstream params(argv[2]),out(argv[3]);if(!params||!out)throw std::runtime_error("cannot open outputs");
  const std::array<std::array<int,3>,10> tri{{{1,1,1},{1,1,2},{1,1,3},{1,2,2},{1,2,3},{1,3,3},{2,2,2},{2,2,3},{2,3,3},{3,3,3}}};
  std::array<std::string,1001> number;for(int i=0;i<=1000;++i)number[i]=std::to_string(i);
  std::string line;line.reserve(300);
  for(size_t nr=0;nr<rows.size();++nr){const Row&r=rows[nr];
   if(nr&&r.tag==rows[nr-1].tag&&r.v==rows[nr-1].v)throw std::runtime_error("duplicate parameter record");
   params<<r.tag;for(int i=0;i<(r.tag=='S'?10:6);++i)params<<' '<<r.v[i];params<<'\n';
   int t[4][4][4]{};for(int i=0;i<4;++i)t[0][i][i]=t[i][0][i]=1;
   if(r.tag=='S'){
    for(int i=1;i<4;++i)t[i][i][0]=1;
    for(int k=0;k<10;++k){auto p=tri[k];do{t[p[0]][p[1]][p[2]]=r.v[k];}while(std::next_permutation(p.begin(),p.end()));}
   }else{
    int a=r.v[0],b=r.v[1],c=r.v[2],d=r.v[3],e=r.v[4],f=r.v[5];
    int x[4][4]={{0,1,0,0},{1,a,b,b},{0,b,c,d},{0,b,d,c}};
    int y[4][4]={{0,0,1,0},{0,b,c,d},{0,d,e,f},{1,c,e,e}};
    for(int j=0;j<4;++j)for(int k=0;k<4;++k){t[1][j][k]=x[j][k];t[2][j][k]=y[j][k];t[3][j][k]=y[k][j];}
   }
   line="{";
   for(int i=0;i<4;++i){if(i)line+=',';line+='{';for(int j=0;j<4;++j){if(j)line+=',';line+='{';for(int k=0;k<4;++k){if(k)line+=',';line+=number[t[i][j][k]];}line+='}';}line+='}';}line+="}\n";out<<line;
  }
  out.close();params.close();if(!out||!params)throw std::runtime_error("output write failed");
  std::cerr<<"records "<<rows.size()<<" seconds "<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
 }catch(const std::exception&e){std::cerr<<"ERROR: "<<e.what()<<"; partial outputs invalid.\n";return 1;}
}
