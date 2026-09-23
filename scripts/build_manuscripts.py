#!/usr/bin/env python3
"""Generate six explanatory LaTeX companions from the certified census manifest.

Run with --compile to build PDFs. Sources and the retained rank-specific
mathematical derivations remain editable. No new census is performed here.
"""
from __future__ import annotations
import argparse,json,shutil,subprocess,tempfile
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
M=ROOT/'manuscripts'
PREAMBLE=r'''\documentclass[11pt,a4paper]{article}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}\usepackage{lmodern}
\usepackage[margin=23mm,headheight=15pt]{geometry}
\usepackage{amsmath,amssymb,amsthm,mathtools,booktabs,longtable,array,microtype,xcolor}
\usepackage{hyperref,fancyhdr,listings,enumitem}
\definecolor{ink}{HTML}{163348}\definecolor{accent}{HTML}{147D83}
\hypersetup{colorlinks=true,linkcolor=ink,urlcolor=accent,citecolor=accent,pdfauthor={Sébastien Palcoux}}
\pagestyle{fancy}\fancyhf{}\fancyhead[L]{\sffamily\small FUSION RING CENSUS}
\fancyhead[R]{\sffamily\small Rank \Rank}\fancyfoot[L]{\sffamily\footnotesize Computational companion \textbullet\ September 2026}
\fancyfoot[R]{\sffamily\small\thepage}\renewcommand{\headrulewidth}{0.4pt}
\newtheorem{theorem}{Theorem}[section]\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}\newtheorem{corollary}[theorem]{Corollary}
\theoremstyle{definition}\newtheorem{definition}[theorem]{Definition}\newtheorem{remark}[theorem]{Remark}
\newcommand{\ZZ}{\mathbb Z}\newcommand{\CC}{\mathbb C}\newcommand{\Q}{\mathbb Q}
\newcommand{\NN}{\mathbb Z_{\geq0}}\newcommand{\FPdim}{\operatorname{FPdim}}
\setlength{\parindent}{0pt}\setlength{\parskip}{0.45em}\setlength{\emergencystretch}{3em}
\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,columns=fullflexible,frame=single,rulecolor=\color{accent},aboveskip=1em,belowskip=1em}
\setcounter{tocdepth}{2}
'''
DEFINITIONS=r'''
\section{Objects, equivalence and the counting convention}
A \emph{fusion ring} here is a free abelian group with a distinguished finite basis
$B=\{b_0,b_1,\ldots,b_{r-1}\}$, an associative multiplication with unit $b_0$,
and an involution $i\mapsto i^*$ fixing $0$. Its structure constants satisfy
\[
b_i b_j=\sum_k N_{ij}^{k}b_k,\qquad N_{ij}^{k}\in\NN,
\]
\begin{align}
N_{0j}^{k}=N_{j0}^{k}&=\delta_{jk},&N_{ij}^{0}&=\delta_{i^*,j},\\
N_{ij}^{k}&=N_{i^*k}^{j}=N_{kj^*}^{i}.&&\label{eq:reciprocity}
\end{align}
These conventions agree with the usual based-ring definition; see
\cite{EGNO,VS}. No assumption of categorifiability, commutativity or integrality
of Frobenius--Perron dimensions is imposed unless proved in the relevant rank.

A based isomorphism is a bijection of the distinguished bases preserving the
unit and multiplication. In tensor notation it is a permutation $q$ fixing $0$
such that
\[
 N_{ij}^{k}={N'}_{q(i)q(j)}^{q(k)}\quad\hbox{for every }i,j,k.
\]
The coefficient of the unit determines the involution, so such an isomorphism
automatically intertwines duality. The \emph{multiplicity} is the maximum entry
of the \emph{full} ordered multiplication tensor. It is at least one, including
for group rings. Put
\[
 c_r(m)=\#\{\text{rank-}r\text{ fusion rings of multiplicity exactly }m\}/\cong,
 \qquad C_r(M)=\sum_{m=1}^{M}c_r(m).
\]
A list through $M$ contains all rings of multiplicity at most $M$, not only
those of multiplicity equal to $M$. This distinction is essential when exporting
OEIS b-files.

\subsection{Why duality types can be searched separately}
An involution on the $r-1$ nonunit elements consists of $p$ disjoint transpositions
and $r-1-2p$ fixed points, with $0\leq p\leq\lfloor(r-1)/2\rfloor$. Fix one
representative $d_p$ of each type. An isomorphism between two tensors with
involution $d_p$ commutes with $d_p$. Hence it is sufficient to quotient that
stratum by the centralizer
\[
 Z_{S_{r-1}}(d_p),\qquad |Z_{S_{r-1}}(d_p)|=2^p p!(r-1-2p)!.
\]
Different $p$ cannot be isomorphic. Therefore a whole-rank census is complete
exactly when every required stratum has been searched exhaustively. Finishing
only the non-self-dual strata does not certify a whole-rank counting term.
'''
GENERAL=r'''
\section{An exhaustive finite-domain model}
\subsection{Coordinates directly from reciprocity}
On nonunit triples apply the two transformations
\[
(i,j,k)\longmapsto(i^*,k,j),\qquad
(i,j,k)\longmapsto(k,j^*,i).
\]
Assign one variable $x_O\in\{0,\ldots,M\}$ to each resulting orbit $O$.
The unit entries and $N_{ij}^0$ are already fixed. Thus every tensor satisfying
unit, duality and reciprocity occurs exactly once as an assignment of orbit
coordinates. Three successive reciprocity transformations give
$N_{ij}^{k}=N_{j^*i^*}^{k^*}$, so duality is an anti-involution. In particular,
the self-dual stratum is commutative, at every rank.

For every nonunit $i,j,k,\ell$ impose the integer polynomial
\begin{equation}
 \sum_s N_{ij}^{s}N_{sk}^{\ell}-\sum_s N_{jk}^{s}N_{is}^{\ell}=0.
 \label{eq:associativity}
\end{equation}
Associativity involving a unit is automatic. When $\ell=0$, the two sides
reduce to $N_{ij}^{k^*}$ and $N_{jk}^{i^*}$, which agree by reciprocity and the
anti-involution. Therefore these generated polynomials are necessary and
sufficient for associativity. Removing zero polynomials and normalizing signs
of repeated equations changes no solution.

\subsection{Safe pruning, including singular linear systems}
The baseline solver starts with a finite domain for every variable. It evaluates
an enclosing interval for each polynomial and rejects a branch only if that
interval excludes zero. If an equation contains at most two unfixed variables,
it tests every pair of values in their current domains and removes unsupported
values. These operations preserve every solution.

Equations that have become linear are row-reduced over $\mathbb F_{257}$.
An inconsistent modular system cannot have an integer solution. Consequences
involving one or two variables restrict their finite domains. Rank deficiency
by itself never rejects a branch: free variables remain in the exhaustive
search. Since $M\leq15<257$, a residue determines at most one permitted integer.
The final leaf is always checked against every original integer polynomial.

Lexicographic comparison with the duality centralizer retains the least
coordinate vector in each orbit. A comparison stops at its first undecided
coordinate; one cannot infer a later lexicographic inequality past an earlier
unknown entry. Any extra prefix inequalities are necessary conditions for the
same least representative.

\begin{theorem}[Conditional completeness of a terminated search]
Fix $r$, $M$ and a duality type. If the finite-domain solver terminates normally
and processes every branch of its search tree, it emits exactly one tensor from
each based-isomorphism class satisfying that type and bound. If every duality
type terminates normally, their union is the complete whole-rank census.
\end{theorem}
\begin{proof}
Every admissible tensor has an orbit-coordinate vector in the initial box.
Each pruning rule is a necessary condition, so the least representative of
that tensor is never deleted. At each unpruned node the first unfixed variable
is assigned every remaining value. Induction on the number of unfixed variables
therefore visits each feasible least vector. Leaf tests prove soundness, and
lexicographic minimality proves uniqueness. Finally, duality types are disjoint
and exhaust all possibilities.
\end{proof}

A parallel run partitions a fixed coordinate prefix into all bounded assignments.
The resulting subtrees are disjoint and their union is the original tree. A run
is marked complete only after every prefix finishes. A time limit is not a
mathematical rejection rule: a timeout leaves the larger census uncertified.
'''
FAST=r'''
\section{Self-dual reconstruction from one multiplication matrix}
Put $n=r-2$. Choosing a nonunit element gives a symmetric matrix
\[
 A=\begin{pmatrix}0&1&0\\1&a&u^{\mathsf T}\\0&u&Q\end{pmatrix},
 \qquad u\in\NN^n,\quad Q=Q^{\mathsf T}\in M_n(\NN).
\]
The remaining parameters are a symmetric cubic tensor on the $n$ tail indices.
Relabelling allows $u$ to be nondecreasing. If $b=u_1$ is the least mixed
repeated-index coefficient, then every such coefficient is at least $b$;
in particular $Q_{ii}\geq b$. Ties in $u$ allow the corresponding diagonal
entries of $Q$ to be sorted. These are necessary conditions on an orbit minimum,
not extra axioms imposed on the ring.

\subsection{The two contraction identities}
Let $R_i$ be the tail block of multiplication by the $i$th tail basis element.
Comparing the lower blocks of its commutator with $A$ gives
\begin{align}
 R_i u&=(Q^2+uu^{\mathsf T}-I-aQ)e_i,\\
 R_iQ&=QR_i-(Qe_i)u^{\mathsf T}+u(Qe_i)^{\mathsf T}.
 \label{eq:commutator}
\end{align}
Writing $s=\sum_j u_j$, each contraction lies in $[0,Ms]$ and is divisible
by $\gcd(u_1,\ldots,u_n)$, with zero required if $u=0$. Mixed-coefficient
bounds strengthen the diagonal lower bound to $b(s-u_i)$ and the off-diagonal
lower bound to $b(u_i+u_j)$. Partial sums of squares in $Q^2$ are enclosed by
letting each missing entry range over $[0,M]$. These necessary interval and
divisibility conditions eliminate many first matrices before cubic completion.

\subsection{A finite-field reconstruction with an exhaustive fallback}
Define
\[
 V_k=Q^ku,\quad K=[V_0,\ldots,V_{n-1}],\quad
 H_0=Q^2+uu^{\mathsf T}-I-aQ,
\]
\[
 H_{k+1}=QH_k-(u^{\mathsf T}V_k)Q+uV_{k+1}^{\mathsf T}.
\]
Induction using \eqref{eq:commutator} proves $R_iV_k=H_ke_i$.
Each $H_k$ is affine in $a$. If $K$ is invertible modulo a prime $p>M$, then
\[
 R_i=[H_0e_i,\ldots,H_{n-1}e_i]K^{-1}\pmod p.
\]
Each reconstructed residue has at most one representative in $[0,M]$.
Retaining only those representatives and then checking all original integer
equations gives an exact reconstruction, not an approximate numerical method.

The implementation tries $p=257$ and $p=17$. A preliminary row system can
reject values of $a$ without reconstructing all tail entries. If either system
has free coordinates, its compatibility equations are retained. With one or
two free coordinates, all their permitted values are tested. With more free
coordinates the general exhaustive completion is used. If neither prime gives
an invertible $K$, the solver searches every surviving integer value of $a$
and every compatible remaining coordinate. In particular, an integer matrix
that happens to be singular modulo a chosen prime is never lost.

\subsection{Folding a fixed invertible element}
When $u=0$, $a=0$ and $Q=I$, the chosen element $g$ satisfies $g^2=1$ and
$gX_i=X_i$ for all tail elements. The tail product then has the form
\[
 X_iX_j=\delta_{ij}(1+g)+\sum_k t_{ijk}X_k.
\]
Its associativity equations are the rank-$(r-1)$ symmetric equations with the
unit contribution changed from one to two. This is an auxiliary weighted
system, not a new fusion ring. Replace $I$ by $2I$ in the contraction formulae,
enumerate that smaller system, and unfold. Each unfolded tensor is minimized
under the original relabellings and checked against the original equations.

The distinguished pair $\{1,g\}$ is intrinsic: another invertible element
$h$ fixed by $g$ would yield $g=1$ after multiplying $gh=h$ by $h^{-1}$.
Thus folding introduces no hidden identifications. It is used only in this
proved case; weighted systems are not recursively folded under an unproved
extension of the argument.
'''
RANK3=r'''
\section{The classical rank-three Diophantine parameterization}
This companion does not claim a new theoretical rank-three classification.
It materializes the familiar parameterization through the requested bound.
In the self-dual basis $(1,X,Y)$, reciprocity gives
\[
X^2=1+mX+kY,\qquad XY=kX+lY,\qquad Y^2=1+lX+nY.
\]
Comparing $(X^2)Y$ with $X(XY)$ proves that associativity is equivalent to
\begin{equation}k^2+l^2=1+lm+kn.\label{eq:rankthree}\end{equation}
Exchanging $X,Y$ sends $(k,l,m,n)$ to $(l,k,n,m)$. Retain $k<l$, or $k=l$
with $m\leq n$.

If $X^*=Y$, reciprocity instead gives
\[
X^2=aX+bY,\quad Y^2=bX+aY,\quad XY=YX=1+aX+aY.
\]
Associativity implies $b^2-a^2=1$. Nonnegative integers force $a=0$, $b=1$,
which is exactly $\ZZ[C_3]$.

\subsection{Every boundary and every arithmetic progression}
For the self-dual part take $k\leq l$. If $k=0$, equation
\eqref{eq:rankthree} gives $l=1$, $m=0$, with $n$ arbitrary in $[0,M]$.
If $k=l$, it gives $k=l=1$ and $m+n=1$, leaving the representative $(1,1,0,1)$.
For $0<k<l$, a common divisor of $k,l$ would divide one, so $\gcd(k,l)=1$.
Set $C=k^2+l^2-1$ and choose $0\leq m_0<k$ with $lm_0\equiv C\pmod k$.
For $k=1$ take $m_0=0$. Then every integral solution is
\[
m=m_0+kt,\qquad n=n_0-lt,\qquad n_0=(C-lm_0)/k,
\]
where
\[
\max\left(0,\left\lceil\frac{n_0-M}{l}\right\rceil\right)
\leq t\leq
\min\left(\left\lfloor\frac{M-m_0}{k}\right\rfloor,
          \left\lfloor\frac{n_0}{l}\right\rfloor\right).
\]
The Euclidean algorithm finds the inverse of $l$ modulo $k$. This visits
every bounded solution exactly once. The two boundary cases and $\ZZ[C_3]$
complete the census. Every emitted solution is checked again in
\eqref{eq:rankthree}; the independent tensor verifier does not use that equation.

\subsection{The deliberate endpoint}
The repository hard-caps the rank-three generator at $M=1000$. It contains
all exact-multiplicity counts and all multiplication tensors through that
bound. There are no rank-three counts or searches beyond that endpoint in
the released data. The b-file belongs to OEIS A354471.
'''
SMALLCOMM=r'''
\section{Why the rank-four specialization is commutative}
The coefficient-of-unit functional $\tau$ gives the positive inner product
$\langle x,y\rangle=\tau(xy^*)$ on the complexified based ring. The basis is
orthonormal and multiplication is closed under adjoints. Consequently its
complexification is semisimple. The Frobenius--Perron dimension character is a
one-dimensional representation. A noncommutative semisimple complex algebra
with a one-dimensional representation has dimension at least $1+2^2=5$.
Thus a rank-four fusion ring is commutative. This justifies the specialization
below without any categorical assumption.
'''
AUDIT=r'''
\section{What the independent verification establishes}
The enumerator and verifier have separate mathematical tasks. Exhaustiveness
uses the complete coordinate parameterization, the safe-pruning proof and the
normal completion of every required branch. The verifier reads only the emitted
\emph{full tensors}; it neither reconstructs the parameterization nor trusts the
generator's polynomial list.

For every tensor it checks nonnegative integral coefficients, both unit laws,
uniqueness and involutivity of the dual, both reciprocity identities, and every
integer associativity identity for all four indices. It then canonicalizes
under \emph{every} unit-fixing basis permutation. A matching hash is only a
lookup aid: actual canonical tensors are compared. This detects both literal
repetitions and different labellings of an isomorphic based ring.

Passing these checks proves soundness and uniqueness of the emitted data; by
itself it would not prove that no ring was omitted. That is why normal completion
logs and the mathematical coverage argument are retained separately. Comparison
with the original ancillary file is an additional containment/regression test,
not an input to enumeration and not a replacement for an exhaustiveness proof.

\subsection{Provenance and reproducibility}
The retained Vercleyen--Slingerland v4 ancillary file has SHA-256
\begin{center}\footnotesize\ttfamily
b587c3f683157369da7cc090f762bbff0e18dcf11acc3f5031d6bc0c643843f8
\end{center}
Its 28,451 records contain 25,138 distinct classes. The 3,313 redundant records
occur at rank five and exact multiplicities 9--12. Their original and corrected
counts are respectively
\[
(1463,1794,2283,3049)\quad\longrightarrow\quad(863,1082,1383,1948).
\]
Every deletion has an explicit basis-permutation witness in the audit folder.
This audit does not establish completeness of the source's partial-search cells.

The primary manifest \path{results/census.json} records every released count,
bound, filename and checksum. Compressed tensors use the original line-per-ring,
nested-curly-brace format. An entry is $N[i][j][k]=N_{ij}^{k}$: the output index
has already been dualized where the internal parameter convention requires it.
The raw tensor needs no additional index conversion.

\subsection{Certified datasets and reproducibility}
The primary manifest gives the complete bound, exact counts and data checksums
for every rank. Each \path{verification/rankR/} directory records the independent
audit and source identity for that dataset. For the laptop censuses it also
retains the completed enumeration, commands, environment, phase timings and
nonempty subprocess logs. Every required duality stratum completed normally;
independent canonicalization found zero duplicate classes.

The independent checks of ranks five through eight ran on GitHub using the
supplied tensors. They did not rerun enumeration. The per-rank reports identify
the exact verification revision and run, and certify agreement with the established
exact-multiplicity count prefix. See \path{verification/README.md} for the evidence
index and \path{docs/PROVENANCE.md} for attribution.

The local launcher has no clock limit, while the manual hosted workflow uses a
finite shared deadline covering every computational phase. A timeout never
certifies the unfinished bound. Only a complete, independently verified whole-rank
candidate can enter the release; a later failed attempt cannot replace it.
Reproduction commands and supported limits are in \path{docs/REPRODUCIBILITY.md}.

\section{Reading and reusing the data}
The result files count based rings, not monoidal categories or realizations of
a ring. One tensor can admit several inequivalent categorifications, or none.
No number here is a classification of fusion categories. The rank-specific
count files use exact multiplicity; cumulative totals belong only in the
summary column. Proposed OEIS additions must be regenerated from a complete
manifest, not copied from an interrupted log.

The retained code was generated with AI assistance and is accompanied by explicit
mathematical coverage arguments and independent integer checks. These checks
are not a formal proof in a proof assistant. The present text is an explanatory
computational companion, not a claim of journal acceptance or external peer review.
'''
BIB=r'''
\begin{thebibliography}{9}\small\setlength{\itemsep}{2pt}
\bibitem{EGNO} P. Etingof, S. Gelaki, D. Nikshych and V. Ostrik,
\emph{Tensor Categories}, Mathematical Surveys and Monographs 205,
American Mathematical Society, 2015.
\bibitem{VS} G. Vercleyen and J. Slingerland,
\emph{On Low Rank Fusion Rings}, Journal of Mathematical Physics 64 (2023),
091703; \href{https://arxiv.org/abs/2205.15637v4}{arXiv:2205.15637v4}.
\bibitem{Ostrik} V. Ostrik, \emph{On formal codegrees of fusion categories},
Mathematical Research Letters 16 (2009), 895--901;
\href{https://arxiv.org/abs/0810.3242}{arXiv:0810.3242}.
\bibitem{DP} J. Dong and S. Palcoux, rank-four and rank-five census derivations,
project manuscripts and computational supplements, September 2026.
The relevant derivations are retained in the repository's \path{methods/} directory.
\bibitem{OEIS} OEIS Foundation Inc., \emph{The On-Line Encyclopedia of Integer
Sequences}, entries A348305, A354471, A354472, A354473, A354475, A354476
and A354477. Proposed updates in this repository are not submitted edits.
\end{thebibliography}
'''

def results_section(r,item):
    text=f"\\section{{The certified release at rank {r}}}\n"
    text+=f"The released bound is $M={item['bound']}$ and the cumulative number of classes is $C_{{{r}}}({item['bound']})={item['classes']:,}$. "
    text+="Every duality type is included. The accompanying full tensor file has one record per based-isomorphism class.\n\n"
    if r==8:
        text+="The rank-eight implementation extends the general solver, not the commutative rank-five specialization. Its self-dual system has 84 variables and 231 equations. The inherited fixed-size arrays were therefore replaced by dynamically sized linear-algebra workspaces before this rank was enabled. All four duality types are included in the release.\n\n"
    if r in (6,7,8):
        text+=r'\begin{center}\begin{tabular}{rrrr}\toprule Dual pairs & Variables & Equations & Relabellings\\\midrule'+'\n'
        for p in range((r-1)//2+1):
            filename=f'system{r}sd.txt' if p==0 else f'rank{r}_pairs{p}.txt'
            a=list(map(int,(ROOT/'systems'/filename).read_text().splitlines()[0].split()))
            text+=f'{p} & {a[2]} & {a[3]} & {a[4]}\\\\\n'
        text+=r'\bottomrule\end{tabular}\end{center}'+'\n'
    if r!=3:
        text+='\n'+r'\begin{center}\begin{tabular}{rr}\toprule Exact multiplicity $m$ & $c_{\Rank}(m)$\\\midrule'+'\n'
        for m,c in item['counts'].items():
            if r==4 and int(m)>16:continue
            text+=f'{m} & {c:,}\\\\\n'
        text+=r'\bottomrule\end{tabular}\end{center}'+'\n'
        if r==4:text+='The complete table through the released bound appears in Appendix A.\n'
    else:text+='The first sixteen terms are $4,3,4,6,5,9,6,10,12,9,10,20,9,13,16,25$. The complete 1,000-term file is supplied as \\path{oeis/b354471.txt}.\n'
    text+=f'\nThe data and their checksums are recorded in \\path{{results/census.json}}. The corresponding completed-run evidence and independent audit are under \\path{{verification/rank{r}/}}.\n'
    return text

def build_sources():
    data=json.loads((ROOT/'results/census.json').read_text());M.mkdir(exist_ok=True)
    release_date=date.fromisoformat(data['release_date']).strftime('%d %B %Y')
    for r in range(3,9):
        item=data['ranks'][str(r)];body=PREAMBLE+f'\\newcommand{{\\Rank}}{{{r}}}\n\\begin{{document}}\n'
        body+=r'\thispagestyle{empty}{\sffamily\small\color{accent} EXACT ENUMERATION / DATA / VERIFICATION}\par\vspace{1cm}'+'\n'
        body+=f'{{\\sffamily\\Huge\\bfseries\\color{{ink}} Rank-{r} fusion rings\\par}}\n\\vspace{{0.35cm}}\n'
        body+=f'{{\\sffamily\\Large A reproducible census through multiplicity {item["bound"]}\\par}}\n'
        body+=(r'\vspace{0.65cm}{\large Sébastien Palcoux}\par{\small BIMSA}\par\vspace{0.35cm}{\small Computational companion, RELEASEDATE}\par\vspace{0.8cm}').replace('RELEASEDATE',release_date)+'\n'
        body+=r'\begin{abstract}'+'\n'
        body+=f'We explain the exact enumeration of all based fusion rings of rank {r} through multiplicity {item["bound"]}, comprising {item["classes"]:,} isomorphism classes. '
        body+='The account separates the mathematical coverage argument, the completed search, and independent verification of the emitted tensors. '
        body+='All duality types are included, and no categorifiability filter is applied. Code, machine-readable counts, full multiplication tensors and provenance records accompany the text.\n'
        body+=r'\end{abstract}\vspace{0.4cm}\noindent\textbf{AI assistance and verification.} GPT-6 Astra Pro assisted with code, exposition and computational checks. Exhaustive-search arguments and exact independent tensor verification are recorded separately; no proof-assistant certification or peer-reviewed acceptance is claimed.\vfill\noindent\textbf{Scope.} A census of based rings, not a classification of tensor categories. Only completed whole-rank results are released.\newpage\tableofcontents\newpage'+'\n'
        body+=DEFINITIONS+results_section(r,item)
        if r==3:body+=RANK3
        elif r==4:
            s=(ROOT/'methods/rank4_completeness.tex').read_text()
            s=s.replace('In this appendix','In this section').replace('Commutativity follows from Section 3 of the accompanying completeness.md;','Commutativity was proved above;')
            s=s.replace('through multiplicity $128$ produces $889530$',f'through multiplicity ${item["bound"]}$ produces ${item["classes"]}$')
            body+=SMALLCOMM+s
        elif r==5:
            s=(ROOT/'methods/rank5_specialized_derivation.tex').read_text()
            s=s.replace('The following elementary argument also supplies the commutativity needed\nfor every signed sphericalization search. The unsigned assertion also follows from the proof below.','The following based-ring argument justifies the commutative specialization. Formal-codegree facts used here are recalled in \\cite{Ostrik}.')
            s=s.replace('Every rank-five fusion ring is commutative. A rank-five signed Frobenius\nbased ring admitting a nonzero, dual-equal dimension character is also\ncommutative.','Every rank-five fusion ring is commutative.')
            s=s.replace('(possibly signed) ','').replace('For a fusion ring this character is FP; in the signed assertion it is\nthe given dimension character. In either case','This character is the Frobenius--Perron dimension character. Its values are positive. Consequently')
            body+=s
            body+=r'''\subsection{The modular prefilter does not change the solution set}
In the nonsingular branch each reconstructed coefficient has the form
$(A+Ba)/D$. When $D$ is invertible modulo $257$, an allowed integer coefficient
must have a residue in $[0,M]$. Intersecting precomputed masks for two such
coefficients eliminates impossible $a$ values. Every retained value still
undergoes exact divisibility and the original integer checks. If $257\mid D$,
the original gcd/congruence calculation is used. All integer-singular branches
are unchanged. This is a necessary-condition speedup, not an assumption that
a generic determinant is nonzero.
'''
        else:body+=GENERAL+FAST
        body+=AUDIT
        body+='\n\\par\\noindent\\begin{minipage}{\\linewidth}\n\\section{Reproduction commands}\nFrom the repository root on a local computer, request a complete run with no clock limit. An interruption does not certify a smaller census.\n'
        body+='\\begin{lstlisting}\n'+f'python3 scripts/run_laptop.py --rank {r} --bound {item["bound"]}\n'+'\\end{lstlisting}\n'
        body+='To verify the supplied release without recomputing it:\n\\begin{lstlisting}\npython3 scripts/check_release.py --full\n\\end{lstlisting}\n'
        body+='For a shared-budget frontier search, use \\path{scripts/extend_census.py}. For ranks five through eight it starts at the released bound plus one and restarts the unfinished bound without claiming checkpoint resumption. The local command above verifies all tensors and the old count prefix before packaging a result. The separate timed frontier wrapper bounds every phase. Rank three is instead capped at 1000.\n'
        body+='\n\\end{minipage}\\par\n'
        if r==4:
            body+='\\clearpage\\appendix\n\\section{All exact-multiplicity rank-four counts}\n\\begin{longtable}{rr@{\\hspace{1.1cm}}rr@{\\hspace{1.1cm}}rr@{\\hspace{1.1cm}}rr}\n\\toprule $m$ & $c_4(m)$ & $m$ & $c_4(m)$ & $m$ & $c_4(m)$ & $m$ & $c_4(m)$\\\\\\midrule\\endhead\n'
            values=list(item['counts'].items())
            for i in range(0,len(values),4):
                fields=[]
                for j in range(4):
                    if i+j<len(values):a,c=values[i+j];fields += [a,f'{c:,}']
                    else:fields += ['','']
                body+=' & '.join(fields)+'\\\\\n'
            body+='\\bottomrule\\end{longtable}\n'
        body+=BIB+'\\end{document}\n'
        body=body.replace('\\begin{lstlisting}', '\\par\\noindent\\begin{minipage}{\\linewidth}\n\\begin{lstlisting}').replace('\\end{lstlisting}', '\\end{lstlisting}\n\\end{minipage}\\par')
        (M/f'rank{r}.tex').write_text(body)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--compile',action='store_true');a=ap.parse_args()
    build_sources()
    if a.compile:
        # Build away from released PDFs, then replace only completed output.
        for r in range(3,9):
            with tempfile.TemporaryDirectory(prefix=f'fusion-manuscript-{r}-') as tmp:
                tmp=Path(tmp);shutil.copy2(M/f'rank{r}.tex',tmp/f'rank{r}.tex')
                with (M/f'rank{r}.build.txt').open('w') as log:
                    subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-pdflatex=pdflatex -no-shell-escape %O %S',f'rank{r}.tex'],cwd=tmp,check=True,stdout=log,stderr=subprocess.STDOUT)
                pdf=(tmp/f'rank{r}.pdf').read_bytes()
                if not pdf.startswith(b'%PDF-') or b'%%EOF' not in pdf[-100:]:
                    raise RuntimeError(f'Incomplete PDF output for rank {r}; previous PDF retained')
                staged=M/f'rank{r}.pdf.next';staged.write_bytes(pdf)
                staged.replace(M/f'rank{r}.pdf')
            print(f'Built rank{r}.pdf',flush=True)
if __name__=='__main__':main()
