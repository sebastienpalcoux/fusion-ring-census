// Checked wide integer products for fraction-free Gaussian elimination.
using Wide=__int128;
Wide wgcd(Wide a,Wide b){if(a<0)a=-a;if(b<0)b=-b;while(b){Wide c=a%b;a=b;b=c;}return a;}
Wide wmul(Wide a,Wide b){Wide c;if(__builtin_mul_overflow(a,b,&c))throw std::overflow_error("rational product overflow");return c;}
Wide wadd(Wide a,Wide b){Wide c;if(__builtin_add_overflow(a,b,&c))throw std::overflow_error("rational sum overflow");return c;}
Wide wsub(Wide a,Wide b){Wide c;if(__builtin_sub_overflow(a,b,&c))throw std::overflow_error("rational difference overflow");return c;}
