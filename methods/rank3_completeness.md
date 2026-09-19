# A complete Diophantine census in rank three

All isomorphisms below preserve the distinguished basis and its unit. No
categorifiability hypothesis or criterion is used. Let M >= 1.

## 1. The possible dualities

The unit is self-dual. Either both remaining basis elements X,Y are self-dual,
or X*=Y. These two types cannot be isomorphic.

### Self-dual type

Frobenius reciprocity and duality force a commutative multiplication table

    X^2 = 1 + m X + k Y,
    XY  = k X + l Y,
    Y^2 = 1 + l X + n Y,

with k,l,m,n nonnegative integers. Comparing (X^2)Y and X(XY) shows that
associativity is equivalent to the single equation

    k^2 + l^2 = 1 + l*m + k*n.                   (1)

The comparison X(Y^2)=(XY)Y gives the same equation. The remaining associativity
checks either involve the unit or are automatic from commutativity. Conversely,
every nonnegative integral solution of (1) gives a fusion ring: the unit,
duality, positivity, and reciprocity are visible in this table, and (1) checks
associativity.

The only possible nonidentity unit-fixing basis permutation swaps X,Y. On the
parameters it sends (k,l,m,n) to (l,k,n,m). Thus one representative is selected
by k<l, or k=l and m<=n.

### Non-self-dual type

Write X*=Y. The unit coefficient, duality, and the two Frobenius reciprocity
identities force, for nonnegative integers a,b,

    X^2 = a X + b Y,
    Y^2 = b X + a Y,
    XY = YX = 1 + a X + a Y.

The coefficient of X in (X^2)Y=X(XY) gives

    a^2+b^2 = 1+2a^2,

hence (b-a)(b+a)=1. Nonnegativity implies a=0,b=1. This is precisely the group
ring of C3. It has multiplicity 1, and contributes one class there.

## 2. Complete, nonredundant solution enumeration

We impose k<=l, using the symmetry already proved.

If k=0, equation (1) is l(l-m)=1. It follows that l=1,m=0, with arbitrary
0<=n<=M. The algorithm emits exactly these M+1 solutions.

If k=l, equation (1) gives k(2k-m-n)=1. Hence k=l=1 and m+n=1. Up to swapping
X,Y, only (k,l,m,n)=(1,1,0,1) is needed.

It remains to treat 1<=k<l<=M. Any common divisor of k,l would divide the left
side of (1) and both terms l*m,k*n, and would therefore divide 1. Consequently

    gcd(k,l)=1.

Put C=k^2+l^2-1. Let m0 be the unique solution in 0<=m0<k of

    l*m0 = C  (mod k),

and put n0=(C-l*m0)/k. For k=1, take m0=0. For k>1, find m0 using the extended
Euclidean algorithm. All integral solutions of l*m+k*n=C are exactly

    m=m0+k*t,   n=n0-l*t,                       (2)

for integral t. The simultaneous bounds 0<=m,n<=M are equivalent to

    max(0,ceil((n0-M)/l)) <= t
      <= min(floor((M-m0)/k),floor(n0/l)).       (3)

The program loops over the complete interval (3) and checks (1) and all
nonnegativity/bound conditions again before counting a solution. The strict
inequality k<l removes any remaining basis-swap duplication. Together with the
two boundary cases and C3, this proves completeness and nonredundancy.

## 3. Counts versus materialization

The multiplicity of a self-dual solution is max(1,k,l,m,n). Each solution
increments the corresponding exact-multiplicity counter. The program's
default output is one line `multiplicity count` for each multiplicity 1..M.
It does not need to retain the full list of solutions in memory. With `--emit`,
it instead writes `S k l m n` for each self-dual solution, and `C3` for the
non-self-dual ring. The exporter reconstructs every entry of the full tensor.

All arithmetic is exact integer arithmetic. The safety limit M<=1,000 enforces the requested
repository scope. None of these
programs takes an existing fusion-ring list as input.

## 4. Checks performed

The M=16 counts agree with an independent brute-force scan of all four
parameters and an independent quotient by swapping X,Y:

    4,3,4,6,5,9,6,10,12,9,10,20,9,13,16,25.

These also agree with the rank-three column of Vercleyen--Slingerland's v4
Table 2. Every small self-dual tensor from this brute-force scan was checked
for associativity directly, not just against (1).

The M=1,000 run gives 460,353 classes. Every one of these full tensors was
exported and independently checked for every fusion-ring axiom. Exhaustive
unit-fixing-permutation canonicalization found 460,353 distinct classes and
no repetitions.
