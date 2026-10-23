// Exact deduplication of Vercleyen--Slingerland fusion-ring tables.
// C++17; no external libraries. See README.md for proof and conventions.
// MIT license, 2026. Generated with AI assistance; independently testable.
#include <algorithm>
#include <array>
#include <chrono>
#include <cctype>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
namespace fs = std::filesystem;
using V = std::vector<int>;
constexpr int MAX_RANK = 32;
constexpr int MAX_COEFF = 1000000; // ensures rank * MAX_COEFF^2 fits uint64_t
struct Hash {
    size_t operator()(const V& a) const noexcept {
        uint64_t h = 1469598103934665603ULL;
        for (int x : a) { h ^= uint32_t(x); h *= 1099511628211ULL; }
        return size_t(h);
    }
}; // Hashes accelerate lookup ONLY: std::vector equality always decides.
struct Ring {
    int n = 0, m = 0;
    V a, dual;
    int operator()(int i,int j,int k) const { return a[(i*n+j)*n+k]; }
};
struct Parser {
    const std::string& s; size_t pos = 0;
    void ws() { while(pos<s.size() && std::isspace((unsigned char)s[pos])) ++pos; }
    [[noreturn]] void bad(const std::string& why) const {
        throw std::runtime_error("column " + std::to_string(pos+1) + ": " + why);
    }
    char begin() {
        ws(); if(pos==s.size() || (s[pos]!='{' && s[pos]!='[')) bad("expected { or [");
        return s[pos++]=='{' ? '}' : ']';
    }
    bool more(char close) {
        ws(); if(pos==s.size()) bad("unterminated list");
        if(s[pos]==close) { ++pos; return false; }
        if(s[pos++]!=',') bad("expected comma or matching closing bracket");
        return true;
    }
    int integer() {
        ws(); if(pos==s.size() || !std::isdigit((unsigned char)s[pos])) bad("expected nonnegative integer");
        int x=0;
        while(pos<s.size() && std::isdigit((unsigned char)s[pos])) {
            int d=s[pos++]-'0'; if(x>(MAX_COEFF-d)/10) bad("coefficient exceeds safety limit"); x=10*x+d;
        }
        return x;
    }
    Ring parse() {
        Ring r; std::vector<std::vector<V>> t;
        char c0=begin();
        do {
            if(t.size()>=MAX_RANK) bad("rank exceeds safety limit");
            std::vector<V> mat; char c1=begin();
            do {
                if(mat.size()>=MAX_RANK) bad("too many rows");
                V row; char c2=begin();
                do { if(row.size()>=MAX_RANK) bad("too many columns"); row.push_back(integer()); } while(more(c2));
                mat.push_back(std::move(row));
            } while(more(c1));
            t.push_back(std::move(mat));
        } while(more(c0));
        ws(); if(pos!=s.size()) bad("trailing material after tensor");
        r.n=int(t.size());
        for(const auto& mat:t) {
            if(int(mat.size())!=r.n) bad("tensor is not n x n x n");
            for(const auto& row:mat) {
                if(int(row.size())!=r.n) bad("tensor is not n x n x n");
                for(int x:row) { r.a.push_back(x); r.m=std::max(r.m,x); }
            }
        }
        return r;
    }
};
void validate(Ring& r, bool associative) {
    int n=r.n; r.dual.assign(n,-1);
    auto fail=[](const std::string& s){throw std::runtime_error("invalid fusion ring: "+s);};
    for(int i=0;i<n;++i) for(int j=0;j<n;++j) {
        if(r(0,i,j)!=(i==j) || r(i,0,j)!=(i==j)) fail("basis element 0 is not the two-sided unit");
        int v=r(i,j,0);
        if(v) { if(v!=1 || r.dual[i]!=-1) fail("nonunique dual or wrong unit coefficient"); r.dual[i]=j; }
    }
    for(int i=0;i<n;++i) if(r.dual[i]<0) fail("missing dual");
    for(int i=0;i<n;++i) if(r.dual[r.dual[i]]!=i) fail("duality is not an involution");
    for(int i=0;i<n;++i) for(int j=0;j<n;++j) for(int k=0;k<n;++k)
        if(r(i,j,k)!=r(r.dual[i],k,j) || r(i,j,k)!=r(k,r.dual[j],i)) fail("Frobenius reciprocity");
    if(associative) for(int i=0;i<n;++i) for(int j=0;j<n;++j)
        for(int k=0;k<n;++k) for(int l=0;l<n;++l) {
            uint64_t a=0,b=0;
            for(int s=0;s<n;++s) {
                a+=uint64_t(r(i,j,s))*r(s,k,l);
                b+=uint64_t(r(j,k,s))*r(i,s,l);
            }
            if(a!=b) fail("associativity at ("+std::to_string(i)+","+std::to_string(j)+","+std::to_string(k)+","+std::to_string(l)+")");
        }
}
// A basis-isomorphism invariant signature attached to each nonunit element.
// The sorted slice and the sorted joint diagonal data retain exact integers.
V signature(const Ring& r,int i) {
    int n=r.n;
    V s={int(r.dual[i]==i),r(i,i,i)};
    V slice; slice.reserve(n*n);
    for(int j=0;j<n;++j) for(int k=0;k<n;++k) slice.push_back(r(i,j,k));
    std::sort(slice.begin(),slice.end()); s.insert(s.end(),slice.begin(),slice.end());
    std::vector<std::array<int,6>> pairs;
    for(int j=0;j<n;++j) pairs.push_back({r(i,j,j),r(j,i,j),r(j,j,i),r(i,i,j),r(i,j,i),r(j,i,i)});
    std::sort(pairs.begin(),pairs.end());
    for(const auto& p:pairs) s.insert(s.end(),p.begin(),p.end());
    return s;
}
struct Canon { V tensor, perm; uint64_t leaves=0; };
Canon canonical(const Ring& r,bool exhaustive) {
    int n=r.n; std::vector<V> cells;
    if(exhaustive) { V c(n-1); std::iota(c.begin(),c.end(),1); if(!c.empty()) cells.push_back(c); }
    else {
        std::map<V,V> groups;
        for(int i=1;i<n;++i) groups[signature(r,i)].push_back(i);
        for(auto& g:groups) cells.push_back(std::move(g.second));
    }
    V p(n); p[0]=0; Canon best;
    auto consider=[&]() {
        ++best.leaves;
        if(!best.tensor.empty()) {
            size_t t=0; int cmp=0;
            for(int i:p) { for(int j:p) { for(int k:p) {
                int v=r(i,j,k), old=best.tensor[t++];
                if(v!=old) {cmp=v<old?-1:1; break;}
            } if(cmp) break; } if(cmp) break; }
            if(cmp>=0) return;
        }
        best.perm=p; best.tensor.clear(); best.tensor.reserve(r.a.size());
        for(int i:p) for(int j:p) for(int k:p) best.tensor.push_back(r(i,j,k));
    };
    std::function<void(size_t,int)> visit=[&](size_t c,int offset) {
        if(c==cells.size()) {consider(); return;}
        V& cell=cells[c]; // initially sorted; next_permutation restores sorting on false
        do {std::copy(cell.begin(),cell.end(),p.begin()+offset); visit(c+1,offset+int(cell.size()));}
        while(std::next_permutation(cell.begin(),cell.end()));
    };
    visit(0,1); return best;
}
struct Rep { size_t line,clean_line; Ring r; V perm; };
struct Count { size_t records=0,distinct=0,literal=0,relabelled=0,commutative=0,noncommutative=0; };
bool commute(const Ring& r) {
    for(int i=0;i<r.n;++i) for(int j=0;j<i;++j) for(int k=0;k<r.n;++k)
        if(r(i,j,k)!=r(j,i,k)) return false;
    return true;
}
void write_perm(std::ostream& o,const V& p) {for(size_t i=0;i<p.size();++i) {if(i)o<<';';o<<p[i];}}
int main(int argc,char** argv) {
    if(argc<3) {std::cerr<<"Usage: dedup_fusion INPUT OUTPUT_DIRECTORY [--exhaustive] [--skip-associativity]\n";return 2;}
    auto start=std::chrono::steady_clock::now();
    bool full=true,exhaustive=false;
    for(int i=3;i<argc;++i) {std::string opt=argv[i]; if(opt=="--exhaustive")exhaustive=true;
        else if(opt=="--skip-associativity")full=false;else{std::cerr<<"Unknown option: "<<opt<<"\n";return 2;}}
    size_t lineno=0;
    try {
        std::ifstream in(argv[1]); if(!in)throw std::runtime_error("cannot open input");
        fs::path out(argv[2]);
        if(fs::exists(out) && !fs::is_empty(out))throw std::runtime_error("output directory is not empty; choose a new directory");
        fs::create_directories(out);
        std::ofstream clean(out/"FusionRingMultiplicationTables.deduplicated");
        std::ofstream mapping(out/"line_map.csv"),dups(out/"duplicates.csv");
        if(!clean||!mapping||!dups)throw std::runtime_error("cannot open output files");
        std::string header="source_line,representative_source_line,clean_line,rank,multiplicity,kind,permutation_source_to_representative\n";
        mapping<<header;dups<<header;
        std::unordered_map<V,size_t,Hash> classes;
        std::unordered_set<V,Hash> literal;
        std::vector<Rep> reps;
        classes.reserve(32768);literal.reserve(32768);reps.reserve(32768);
        std::map<std::pair<int,int>,Count> counts;
        size_t records=0,literal_dups=0,relab_dups=0;uint64_t leaves=0;
        std::string line;
        while(std::getline(in,line)) {
            ++lineno;
            if(std::all_of(line.begin(),line.end(),[](unsigned char c){return std::isspace(c);}))continue;
            Ring r=Parser{line}.parse();validate(r,full);
            ++records;auto& cnt=counts[{r.n,r.m}];++cnt.records;
            bool repeated=!literal.insert(r.a).second;
            Canon c=canonical(r,exhaustive);leaves+=c.leaves;
            auto it=classes.find(c.tensor);size_t index;V q(r.n);std::string kind;
            if(it==classes.end()) {
                index=reps.size();classes.emplace(std::move(c.tensor),index);
                std::iota(q.begin(),q.end(),0);kind="retained";
                clean<<line<<'\n';++cnt.distinct;
                if(commute(r))++cnt.commutative;else ++cnt.noncommutative;
                reps.push_back({lineno,reps.size()+1,std::move(r),std::move(c.perm)});
            } else {
                index=it->second;const Rep& rep=reps[index];
                for(int k=0;k<r.n;++k)q[c.perm[k]]=rep.perm[k];
                // Verify the witness against the ORIGINAL tensors, not hashes or canonical keys.
                if(q[0]!=0)throw std::runtime_error("internal error: witness moves unit");
                V sq=q;std::sort(sq.begin(),sq.end());
                for(int k=0;k<r.n;++k)if(sq[k]!=k)throw std::runtime_error("internal error: witness not bijective");
                for(int i=0;i<r.n;++i)for(int j=0;j<r.n;++j)for(int k=0;k<r.n;++k)
                    if(r(i,j,k)!=rep.r(q[i],q[j],q[k]))throw std::runtime_error("internal error: invalid isomorphism witness");
                if(repeated){kind="literal_repeat";++literal_dups;++cnt.literal;}
                else{kind="new_labelling";++relab_dups;++cnt.relabelled;}
            }
            const Rep& rep=reps[index];
            auto emit=[&](std::ostream& o){o<<lineno<<','<<rep.line<<','<<rep.clean_line<<','<<rep.r.n<<','<<rep.r.m<<','<<kind<<',';write_perm(o,q);o<<'\n';};
            emit(mapping);if(kind!="retained")emit(dups);
        }
        if(in.bad())throw std::runtime_error("input read error");
        if(!records)throw std::runtime_error("input has no tensors");
        clean.close();mapping.close();dups.close();
        if(!clean||!mapping||!dups)throw std::runtime_error("output write error");
        std::ofstream tab(out/"counts.csv");
        tab<<"rank,multiplicity,source_records,distinct_rings,duplicates,literal_repeats,new_labellings,commutative,noncommutative\n";
        for(const auto& kv:counts) {
            const auto& c=kv.second;tab<<kv.first.first<<','<<kv.first.second<<','<<c.records<<','<<c.distinct<<','<<c.records-c.distinct<<','<<c.literal<<','<<c.relabelled<<','<<c.commutative<<','<<c.noncommutative<<'\n';
        }
        tab.close();if(!tab)throw std::runtime_error("counts write error");
        double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::ofstream js(out/"summary.json");
        js<<std::setprecision(10)<<"{\n  \"input_records\": "<<records<<",\n  \"input_physical_lines\": "<<lineno
          <<",\n  \"distinct_rings\": "<<reps.size()<<",\n  \"duplicates\": "<<records-reps.size()
          <<",\n  \"literal_repeats\": "<<literal_dups<<",\n  \"new_labellings\": "<<relab_dups
          <<",\n  \"associativity_checked\": "<<(full?"true":"false")
          <<",\n  \"canonical_mode\": \""<<(exhaustive?"all unit-fixing permutations":"invariant-cell permutations")
          <<"\",\n  \"permutations_examined\": "<<leaves<<",\n  \"elapsed_seconds\": "<<sec<<"\n}\n";
        js.close();if(!js)throw std::runtime_error("summary write error");
        std::cout<<records<<" source records; "<<reps.size()<<" distinct rings; "<<records-reps.size()<<" duplicates ("<<literal_dups<<" literal repeats, "<<relab_dups<<" additional labellings).\n"
          <<"All witnesses checked. Associativity "<<(full?"checked":"NOT checked")<<". Time: "<<sec<<" seconds.\n";
    } catch(const std::exception& e) {
        std::cerr<<"ERROR near input line "<<lineno<<": "<<e.what()<<"\nPartial outputs must NOT be used; no successful summary is issued.\n";return 1;
    }
}
