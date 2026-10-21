#!/usr/bin/env python3
"""Generate selected LaTeX companions from the certified census manifest.

Run with --compile to build PDFs. Sources and the retained rank-specific
mathematical derivations remain editable. No new census is performed here.
"""
from __future__ import annotations
import argparse,hashlib,json,re,shutil,subprocess,tempfile
from collections import Counter
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
\fancyhead[R]{\sffamily\small Rank \Rank}\fancyfoot[L]{\sffamily\footnotesize Computational companion \textbullet\ RELEASEMONTH}
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

A parallel run adaptively splits prefix subtrees into every bounded value of
the next unfixed coordinate. The resulting frontier subtrees are disjoint and
their union is the original tree. A run is marked complete only after every
frontier subtree finishes. A time limit is not a
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

Independent checks use the supplied tensors; they do not rerun enumeration.
The per-rank reports identify the verification environment and source revision,
and certify agreement with the established exact-multiplicity count prefix.
Hosted audits and local checks are identified separately in
\path{verification/README.md}; see \path{docs/PROVENANCE.md} for attribution.

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
EH_CONTEXT=r'''
\paragraph{A known categorical example.}
The census includes the Grothendieck ring of the Extended Haagerup fusion
category $\mathrm{EH}_1$, of rank six and fusion multiplicity seven.
For the fusion categories and their fusion rules, see Grossman, Morrison,
Penneys, Peters and Snyder~\cite{GMPPS}; the original planar-algebra
construction is due to Bigelow, Morrison, Peters and Snyder~\cite{BMPS}.
This identification is a categorical example within the census, not a
categorifiability filter on its enumeration.
'''
EH_BIB=r'''
\bibitem{BMPS} S. Bigelow, S. Morrison, E. Peters and N. Snyder,
\emph{Constructing the extended Haagerup planar algebra},
Acta Mathematica \textbf{209} (2012), no.~1, 29--82;
\href{https://doi.org/10.1007/s11511-012-0081-7}{doi:10.1007/s11511-012-0081-7}.
\bibitem{GMPPS} P. Grossman, S. Morrison, D. Penneys, E. Peters and N. Snyder,
\emph{The Extended Haagerup fusion categories},
Annales Scientifiques de l'\'Ecole Normale Sup\'erieure (4) \textbf{56} (2023),
no.~2, 589--664;
\href{https://doi.org/10.24033/asens.2541}{doi:10.24033/asens.2541};
\href{https://arxiv.org/abs/1810.06076}{arXiv:1810.06076}.
'''
RANK7_CLASSIFICATION_CONTEXT=r'''
\paragraph{Categorification in the companion project.}
As of 20 October 2026, the
\href{https://github.com/sebastienpalcoux/grothendieck-ring-classification}{companion classification}
resolves all 10,006 supplied tensors: 9,976 general exclusions, 30 known unitary
models and no unresolved rings. At exact multiplicity five, all 5,805 tensors
are resolved: 5,804 general exclusions and one known model,
\texttt{R7\_5\_5678}, namely
$\operatorname{Rep}(C_7\rtimes C_6)=\operatorname{Rep}(\operatorname{AGL}(1,7))$.
The update includes fifteen further exclusions with exact replay certificates.
In particular, coupled fourth and eighth rotations, all-order phase packets
and integral fusion-norm inequalities exclude both
\href{https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/rank7_m5_20261020/models/sqrt5/R3895_CYCLIC_CHAIN.md}{\texttt{R7\_5\_3895}} and
\href{https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/evidence/rank7_m5_20261020/models/sqrt5/R5039_CYCLIC_CHAIN.md}{\texttt{R7\_5\_5039}}
in the general complex scope. The first proof closes all 15 final cyclic
branches with 2,126 exact leaves; its complete source and branch coverage is
replayed independently. No new categorical model is claimed.
These categorification decisions do not alter the census tensors or the
enumeration-completeness qualification above. The companion project retains
the proof manuscripts, source identifiers and full decision ledger. The earlier
rank-six rings \texttt{R6\_4\_155} and \texttt{R6\_8\_1660} remain open;
the companion project's rank-eight frontier is recorded separately there.
'''

# Fill this immutable pin after the classification publication, then regenerate
# rank8.tex, README.md and docs/index.html before publishing this repository.
CLASSIFICATION_PUBLICATION_COMMIT = '822e84ec02e9a18d0fca0eb7c05f4ac6206788b5'

RANK8_CLASSIFICATION_SNAPSHOT = {'date': '2026-10-22',
 'exact': {'excluded': 3506, 'unitarily_realized': 15, 'unresolved': 6},
 'earlier': {'excluded': 896, 'unitarily_realized': 77, 'unresolved': 0},
 'ledger_sha256': '521b9b9fb16a86c7c4ba491b8c2c0ebad05de1e41aafb5bc225d6342c9477e4e',
 'classification_commit': CLASSIFICATION_PUBLICATION_COMMIT,
 'classification_stage': 'published_main_research_update',
 'r721_model': True,
 'r65_excluded': True,
 'r1795_excluded': True}

def rank8_classification(ledger=None):
    """Read an explicit companion ledger, or the last published snapshot.

    This describes categorification only. It never changes census counts.
    A supplied ledger must cover every released rank-eight tensor exactly once.
    """
    summary=json.loads(json.dumps(RANK8_CLASSIFICATION_SNAPSHOT))
    if ledger is not None:
        raw=Path(ledger).read_bytes();rows=json.loads(raw)
        if not isinstance(rows,list):
            raise ValueError('The companion classification ledger must be a list')
        census=json.loads((ROOT/'results/census.json').read_text())['ranks']['8']
        expected={int(m):n for m,n in census['counts'].items()}
        ids=set();counts=Counter();by_band={m:Counter() for m in expected}
        for row in rows:
            match=re.fullmatch(r'R8_(\d+)_(\d+)',row.get('id',''))
            if match is None or row['id'] in ids:
                raise ValueError('Invalid or repeated rank-eight ledger identity')
            m,index=map(int,match.groups())
            if (m not in expected or not 1<=index<=expected[m] or
                    row.get('rank',8)!=8 or row.get('multiplicity')!=m):
                raise ValueError('Ledger identity disagrees with the census band')
            status=row.get('status')
            if status not in {'excluded','unitarily_realized','unresolved'}:
                raise ValueError('Unsupported companion classification status')
            ids.add(row['id']);counts[m]+=1;by_band[m][status]+=1
        if dict(counts)!=expected or len(rows)!=census['classes']:
            raise ValueError('Companion ledger does not cover the released census')
        summary['exact']={k:by_band[3][k] for k in summary['exact']}
        summary['earlier']={k:sum(by_band[m][k] for m in expected if m<3)
                            for k in summary['earlier']}
        summary['r721_model']=any(row['id']=='R8_3_721' and
                                 row['status']=='unitarily_realized' for row in rows)
        summary['r65_excluded']=any(row['id']=='R8_3_65' and
                                   row['status']=='excluded' for row in rows)
        summary['r1795_excluded']=any(row['id']=='R8_3_1795' and
                                     row['status']=='excluded' for row in rows)
        ledger_sha256=hashlib.sha256(raw).hexdigest()
        if summary.get('ledger_sha256') not in (None,ledger_sha256):
            summary.pop('classification_commit',None)
            summary.pop('classification_stage',None)
        summary['ledger_sha256']=ledger_sha256
    summary['cumulative']={k:summary['exact'][k]+summary['earlier'][k]
                           for k in summary['exact']}
    for scope,total in (('exact',3527),('earlier',973),('cumulative',4500)):
        if (set(summary[scope])!={'excluded','unitarily_realized','unresolved'} or
                any(type(v) is not int or v<0 for v in summary[scope].values()) or
                sum(summary[scope].values())!=total):
            raise ValueError('Invalid companion classification snapshot')
    return summary

def rank8_classification_values(summary):
    return {f'{scope}_{key}':f'{value:,}' for scope in ('exact','earlier','cumulative')
            for key,value in summary[scope].items()}

def rank8_classification_provenance(summary,markup='markdown'):
    commit=summary.get('classification_commit')
    if commit is None:
        return 'Classification publication commit pending for this prepared research snapshot.'
    if re.fullmatch(r'[0-9a-f]{40}',commit) is None:
        raise ValueError('Invalid classification provenance commit')
    stage=summary.get('classification_stage')
    if stage not in {'reviewed_research_checkpoint','published_main_normal_verified','published_main_research_update','certified_release'}:
        raise ValueError('Invalid classification provenance stage')
    label={'reviewed_research_checkpoint':'reviewed research checkpoint',
           'published_main_normal_verified':'classification main snapshot',
           'published_main_research_update':'classification main snapshot',
           'certified_release':'classification release'}[stage]
    url='https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/'+commit
    if markup=='markdown':link=f'[{label} `{commit[:8]}`]({url})'
    elif markup=='html':link=f'<a href="{url}">{label} <code>{commit[:8]}</code></a>'
    elif markup=='tex':link=r'\href{'+url+'}{'+label+r' \texttt{'+commit[:8]+'}}'
    else:raise ValueError('Unsupported provenance markup')
    suffix={'reviewed_research_checkpoint':' Aggregate release verification is pending.',
            'published_main_normal_verified':
                ' The 108-check canonical normal replay passed; all 8 center checks passed in normal and optimized Python.'
                ' Optimized core and extracted-package full replays are pending.',
            'published_main_research_update':'',
            'certified_release':''}[stage]
    return 'These counts are bound to the '+link+'.'+suffix

def rank8_research_addendum(summary,markup='markdown'):
    """Reviewed research consequences; no additional model is asserted."""
    if not (summary.get('r65_excluded') or summary.get('r1795_excluded')):return ''
    ref=summary.get('classification_commit') or 'main'
    base='https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/'+ref
    def case(identifier):
        if markup=='markdown':return '`'+identifier+'`'
        if markup=='html':return '<code>'+identifier+'</code>'
        if markup=='tex':return r'\texttt{'+identifier.replace('_',r'\_')+'}'
        raise ValueError('Unsupported research markup')
    def link(label,path):
        url=base+path
        if markup=='markdown':return f'[{label}]({url})'
        if markup=='html':return f'<a href="{url}">{label}</a>'
        if markup=='tex':return r'\href{'+url+'}{'+label+'}'
        raise ValueError('Unsupported research markup')
    parts=[]
    if summary.get('r65_excluded'):
        proof=link('six exact certificates','/evidence/rank8_research_20261022/r65/PROOF.md')
        parts.append(f'The general exclusion of {case("R8_3_65")} uses pointed-induction '
                     f'phases and integral Fourier fibers; {proof} cover every pointed '
                     'associator class.')
    if summary.get('r1795_excluded'):
        proof=link('sixteen exact indicator branches','/evidence/rank8_research_20261022/pointed_followup/PROOF.md')
        parts.append(f'The new general exclusion of {case("R8_3_1795")} uses finite '
                     f'integer packing of the two pointed twist fibers; {proof} '
                     'exclude both pointed associator classes.')
    research=link('structural results','/manuscripts/rank8/paper/m3_research_20261022.tex')
    followup=link('followup restrictions','/manuscripts/rank8/paper/m3_pointed_followup.tex')
    parts.append('Every categorification of a remaining rank-eight case admits a '
                 'spherical structure and has a pseudo-unitary Galois conjugate, '
                 'and none is Morita equivalent to a braided category. '
                 f'Further {research} restrict module actions and distinguish '
                 f'possible centers. The {followup} force the nontrivial pointed '
                 f'associator for {case("R8_3_1768")} and constrain additional '
                 'twist-one central simples; no new categorification is supplied.')
    return ' '.join(parts)

def rank8_classification_addendum(summary,markup='markdown'):
    """Current research and separately labelled construction/replay history."""
    research=rank8_research_addendum(summary,markup)
    if not summary.get('r721_model'):return research
    proof='https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/'+(summary.get('classification_commit') or 'main')+'/evidence/rank8_next_20261021/r721/r721_qsystem_model.tex'
    historical='https://github.com/sebastienpalcoux/grothendieck-ring-classification/tree/95f38175256ba852b6634f88a055b674e920f941'
    if markup=='markdown':
        model='`R8_3_721`';algebra='`1 + rho`';groups=('`C2`','`C8`')
        proof_link=f'[construction proof]({proof})';history_link=f'[snapshot `95f38175`]({historical})'
    elif markup=='html':
        model='<code>R8_3_721</code>';algebra='<code>1 + rho</code>';groups=('<code>C2</code>','<code>C8</code>')
        proof_link=f'<a href="{proof}">construction proof</a>';history_link=f'<a href="{historical}">snapshot <code>95f38175</code></a>'
    elif markup=='tex':
        model=r'\texttt{R8\_3\_721}';algebra=r'$\mathbf 1\oplus\rho$';groups=('$C_2$','$C_8$')
        proof_link=r'\href{'+proof+'}{construction proof}';history_link=r'\href{'+historical+r'}{snapshot \texttt{95f38175}}'
    else:raise ValueError('Unsupported construction markup')
    return ((research+' ') if research else '')+(f'The known model {model} is the Morita dual of the inherited Q-system '
            f'{algebra} in the {groups[0]} de-equivariantization of the known unitary '
            f'{groups[1]} generalized-Haagerup category. The {proof_link} includes '
            'an exact fusion-coefficient bound and identification across all 4,500 '
            'supplied rank-eight tensors. '
            f'Historical verification at {history_link}: the 108-check canonical normal '
            'replay passed; all 8 center checks passed in normal and optimized Python. '
            'At that checkpoint, optimized core and extracted-package full replays were pending.')

def rank8_classification_readme(summary):
    v=rank8_classification_values(summary)
    return f'''At rank eight, the exact-multiplicity-three band has **{v['exact_excluded']} general
exclusions, {v['exact_unitarily_realized']} unitary models and {v['exact_unresolved']} unresolved categorification candidates**
among its 3,527 supplied rings. Together with the earlier {v['earlier_excluded']} exclusions and
{v['earlier_unitarily_realized']} unitary models through multiplicity two, this gives **{v['cumulative_excluded']} general
exclusions, {v['cumulative_unitarily_realized']} unitary models and {v['cumulative_unresolved']} unresolved rings** among 4,500 supplied
rank-eight rings. The candidates are not asserted fusion categories or
established exotic examples. The general questions `R6_4_155` and
`R6_8_1660` also remain open; see the [current classification account](https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/docs/RESEARCH_STATUS.md)
for the precise proof scope and individual attempt records.
{rank8_classification_provenance(summary)}
{rank8_classification_addendum(summary)}'''

def sync_rank8_readme(summary):
    path=ROOT/'README.md';text=path.read_text()
    pattern=r'At rank eight,.*?(?=\n\nAt rank seven)'
    if len(re.findall(pattern,text,flags=re.S))!=1:
        raise ValueError('Expected exactly one rank-eight README paragraph')
    path.write_text(re.sub(pattern,lambda _:rank8_classification_readme(summary),text,flags=re.S))

RANK8_CLASSIFICATION_CONTEXT=r'''
\paragraph{Categorification in the companion project.}
As of @@classification_date@@, the
\href{https://github.com/sebastienpalcoux/grothendieck-ring-classification/blob/main/docs/RESEARCH_STATUS.md}{companion classification}
records @@exact_excluded@@ general complex exclusions, @@exact_unitarily_realized@@ unitary constructions and @@exact_unresolved@@
unresolved categorification candidates among the 3,527 supplied rings of
exact multiplicity three. The earlier classification through multiplicity
two retains its @@earlier_excluded@@ exclusions and @@earlier_unitarily_realized@@ unitary models. Thus the cumulative
inventory of 4,500 supplied rank-eight rings consists of @@cumulative_excluded@@ general
exclusions, @@cumulative_unitarily_realized@@ unitary models and @@cumulative_unresolved@@ unresolved cases.
Each remaining tensor has an individual attempt record. These candidates
are not asserted fusion categories or established exotic examples;
a unitary-only exclusion leaves the general complex question unresolved.
The companion project records full model tensors, exact certificates and
the hypotheses of the categorical reductions. These categorification
decisions do not alter the census or its enumeration-completeness
qualification above.
'''

def rank8_classification_context(summary):
    text=RANK8_CLASSIFICATION_CONTEXT.replace('@@classification_date@@',
           date.fromisoformat(summary['date']).strftime('%d %B %Y'))
    for key,value in rank8_classification_values(summary).items():
        text=text.replace('@@'+key+'@@',value)
    if '@@' in text:
        raise ValueError('Unexpanded companion classification field')
    addendum=rank8_classification_addendum(summary,'tex')
    if addendum:
        addendum='\\par\\noindent\\begin{minipage}{\\linewidth}\n'+addendum+'\n\\end{minipage}\\par\n'
    return text+'\n'+rank8_classification_provenance(summary,'tex')+'\n'+addendum

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
    audit_path=ROOT/f'verification/rank{r}/audit.json'
    if audit_path.exists():
        audit=json.loads(audit_path.read_text())
        if audit.get('verification_environment')=='local workspace':
            text+=f"\nThe fresh audit for this dataset ran locally, checking {audit['independent_verification']['permutations_examined']:,} unit-fixing permutations across all {item['classes']:,} tensors. It found no duplicate classes and confirmed every exact-multiplicity count. This audit did not rerun enumeration, and no hosted audit is claimed for this dataset.\n"
    if r==7 and item.get('independent_enumeration_rerun') is False:
        text+=r'''
\subsection{Source qualification for the multiplicity-five extension}
The new band consists of $5,805$ tensors. By number of nontrivial dual pairs
$p=0,1,2,3$, its stratum counts are respectively $4,654$, $1,012$, $138$ and $1$;
nine tensors are noncommutative. The supplied producer record reports normal
completion of all four strata in $77,046$ seconds (about $21.4$ hours).

The producer used modified local enumeration sources. The source commit,
hashes and logs are retained in \path{verification/rank7/}. The complete optimized source archive was supplied separately
on 21 October 2026; its aggregate code hash matches the producer run. Numerical
C++ sources are integrated unchanged and finite pruning audits are available.
Completeness nevertheless remains producer-reported: this release does not
independently repeat the full search.

The fresh checks do establish the fusion-ring axioms and uniqueness of all
$10,006$ supplied tensors under every unit-fixing permutation. Re-exporting
the supplied parameters with the repository exporter gives byte-identical
tensors, and the tensor set of multiplicity at most four is exactly the
previous $4,201$-class release. Equation systems, exporter and independent
verifier match the supplied source hashes. The producer receipt and prior
audit remain in \path{verification/rank7/}; no enumeration was rerun.
'''
    if r==8 and item.get('independent_enumeration_rerun') is False:
        text+=r'''
\subsection{Source qualification and optimized enumeration}
The new multiplicity-three band consists of $3,527$ tensors. By number of
nontrivial dual pairs $p=0,1,2,3$, its counts are $2,152$, $972$, $362$ and
$41$; $85$ are noncommutative. The producer reports normal completion in
$62,292$ seconds, including $61,908$ seconds for the self-dual stratum.
These are producer timings, not timings from the independent check.

The complete optimized enumeration source was supplied. Its aggregate code
hash matches the producer records for both rank seven through five and rank
eight through three. Numerical C++ sources are integrated unchanged; only
launcher executable-cache handling was adjusted. Necessary finite-domain
support projections and self-dual moment identities are documented in
\path{methods/OPTIMIZATIONS.md}, \path{methods/SELFDUAL_PROOF.md} and
\path{methods/GAUSSIAN_AUDIT.md}. Witness resource caps disable pruning
for the branch; truncated witness lists cannot reject a solution.

Fresh independent checks establish the fusion axioms and uniqueness of all
$4,500$ tensors under $22,680,000$ unit-fixing permutations. Parameter re-export
is byte-identical. Filtering to multiplicity at most two recovers all $973$
previous tensors and parameter records in their original order. Full exhaustive
enumeration was not independently rerun; completeness remains producer-reported.
The fresh and producer checks are preserved separately under
\path{verification/rank8/}.
'''
    return text

def build_sources(ranks=range(3,9),classification=None):
    classification=rank8_classification() if classification is None else classification
    data=json.loads((ROOT/'results/census.json').read_text());M.mkdir(exist_ok=True)
    release_date=date.fromisoformat(data['release_date']).strftime('%d %B %Y')
    for r in ranks:
        item=data['ranks'][str(r)];body=PREAMBLE.replace('RELEASEMONTH',date.fromisoformat(data['release_date']).strftime('%B %Y'))+f'\\newcommand{{\\Rank}}{{{r}}}\n\\begin{{document}}\n'
        body+=r'\thispagestyle{empty}{\sffamily\small\color{accent} EXACT ENUMERATION / DATA / VERIFICATION}\par\vspace{1cm}'+'\n'
        body+=f'{{\\sffamily\\Huge\\bfseries\\color{{ink}} Rank-{r} fusion rings\\par}}\n\\vspace{{0.35cm}}\n'
        subtitle='A verified dataset' if item.get('independent_enumeration_rerun') is False else 'A reproducible census'
        body+=f'{{\\sffamily\\Large {subtitle} through multiplicity {item["bound"]}\\par}}\n'
        body+=(r'\vspace{0.65cm}{\large Sébastien Palcoux}\par{\small BIMSA}\par\vspace{0.35cm}{\small Computational companion, RELEASEDATE}\par\vspace{0.8cm}').replace('RELEASEDATE',release_date)+'\n'
        body+=r'\begin{abstract}'+'\n'
        if item.get('independent_enumeration_rerun') is False:
            body+=f'We document {item["classes"]:,} verified based-isomorphism classes of fusion rings of rank {r} through multiplicity {item["bound"]}, including {item["counts"][str(item["bound"])]:,} at the maximum multiplicity. The producer reports a complete enumeration. The complete optimized source is supplied and hash-matched, but full enumeration has not been independently reproduced. '
        else:
            body+=f'We explain the exact enumeration of all based fusion rings of rank {r} through multiplicity {item["bound"]}, comprising {item["classes"]:,} isomorphism classes. '
        body+='The account separates the mathematical coverage argument, the completed search, and independent verification of the emitted tensors. '
        body+='All duality types are included, and no categorifiability filter is applied. Code, machine-readable counts, full multiplication tensors and provenance records accompany the text.\n'
        body+=r'\end{abstract}\vspace{0.4cm}\noindent\textbf{AI-generated research \textperiodcentered\ independent verification pending.} This manuscript, its code and data were developed with AI assistance. Independent human verification and Lean formalization are pending. Treat the results with caution: exact computational checks establish only their stated scope.\vfill\noindent\textbf{Scope.} A census of based rings, not a classification of tensor categories. Only completed whole-rank results are released.\newpage\tableofcontents\newpage'+'\n'
        body+=DEFINITIONS+results_section(r,item)
        if r==6:body+=EH_CONTEXT
        if r==7:body+=RANK7_CLASSIFICATION_CONTEXT
        if r==8:body+=rank8_classification_context(classification)
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
        if item.get('independent_enumeration_rerun') is False:
            body+='\nThe completed-search and source qualification in Section 2 applies throughout: the complete optimized source is supplied and hash-matched, but independent output checks do not replace a fresh exhaustive enumeration.\n'
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
        body+=(BIB.replace(r'\end{thebibliography}',EH_BIB+r'\end{thebibliography}') if r==6 else BIB)+'\\end{document}\n'
        body=body.replace('\\begin{lstlisting}', '\\par\\noindent\\begin{minipage}{\\linewidth}\n\\begin{lstlisting}').replace('\\end{lstlisting}', '\\end{lstlisting}\n\\end{minipage}\\par')
        (M/f'rank{r}.tex').write_text(body)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--compile',action='store_true')
    ap.add_argument('--ranks',type=int,nargs='+',choices=range(3,9),default=list(range(3,9)),help='Regenerate only these ranks (default: all).')
    ap.add_argument('--classification-ledger',type=Path,help='Validate and use this explicit companion rank-eight classification ledger.')
    ap.add_argument('--sync-readme',action='store_true',help='Also synchronize the rank-eight companion classification paragraph in README.md.')
    a=ap.parse_args();selected=sorted(set(a.ranks))
    classification=rank8_classification(a.classification_ledger)
    build_sources(selected,classification)
    if a.sync_readme:sync_rank8_readme(classification)
    if a.compile:
        # Build away from released PDFs, then replace only completed output.
        for r in selected:
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
