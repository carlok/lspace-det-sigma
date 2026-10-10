"""Render k32.tex from the result files in verification/families: every number in the document comes from a script."""
import json
from pathlib import Path

HERE = Path(__file__).parent
F = HERE.parent / "verification" / "families"
J = lambda f: json.load(open(F / f))
L = lambda f: [json.loads(l) for l in open(F / f)]

unk = J("unknotting.json"); cab = J("cables.json"); sqp = J("fibered_sqp.json"); ls = L("lspace.jsonl")
assert unk["all_ok"] and cab["all_ok"]
N_MAX = max(r["n"] for r in unk["rows"]); M_LIST = sorted({r["m"] for r in unk["rows"]})
N_CASES = len(unk["rows"]); MAX_FLIPS = max(r["flips"] for r in unk["rows"])
K_MAX = max(r["k"] for r in cab["rows"]); CAB_N = len(cab["rows"])
assert sqp["fibered"] and abs(sqp["tau"]) == sqp["genus"] == 2 and sqp["det"] == 27 and sqp["nullity_mod_3"] == 3
lsp = {(r["n"], r["m"]): r for r in ls}
him_odd = [n for n in (3, 5) if lsp.get((n, 3), {}).get("L_space") is True]
assert him_odd == [3, 5], him_odd
him_odd_g = {n: lsp[(n, 3)]["genus"] for n in him_odd}
assert all(him_odd_g[n] == (3 * n * n - n + 2) // 2 for n in him_odd)
assert all(r["genus"] == (r["m"] * r["n"] ** 2 - r["n"] + 2) // 2 for r in ls)
LS_N = len(ls)

tex = r"""\documentclass[11pt]{article}
\usepackage[margin=2.4cm]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\sloppy
\newtheorem{theorem}{Theorem}
\newtheorem{corollary}{Corollary}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{question}{Question}
\title{Unknotting number equals genus for the Baker--Kegel and Himeno $L$-space knots}
\date{2026-10-10}
\begin{document}
\maketitle

\begin{abstract}
For an $L$-space knot $u \ge g_4 = g$. We show $u = g$ for two infinite families of hyperbolic $L$-space knots that
are not braid positive, or not known to be: the knots $K_k$ of Baker and Kegel and the knots $K_n$ of Himeno. Both are
members of a two-parameter family $H(n,m)$ of closed $2n$-braids, and $u = g = g_4 = (mn^2-n+2)/2$ for every
$H(n,m)$, by an explicit unknotting and a braided Seifert surface. The same argument settles the $L$-space $(2,q)$-cables of $T(2,2k+1)$ that are not positive braids.
The $L$-space hypothesis is not superfluous: as Bode and Tru\"ol observe, the mirror of $12n_{642}$ is fibered and
strongly quasipositive, with $g = 2$ and $u \ge 3$.
\end{abstract}

\section{Context}

An $L$-space knot is fibered and strongly quasipositive, and $g = g_4 = \tau$ \cite{OS, Ni, Hedden2}. Since
$u \ge g_4$ for every knot, $u \ge g$, and the statement $u = g$ for every $L$-space knot is the statement $u \le g$.
It was produced as candidate K32 by a program that fits inequalities to the KnotInfo table \cite{KnotInfo}; the
companion note on $\det \le 1 + |\sigma|$ describes the program. We have not found the statement in the literature.

It holds for braid positive knots: $u \le g$ is due to Rudolph \cite{Rud83}, and Kegel, Lewark, Manikandan, Misev,
Mousseau and Silvero show that every positive braid diagram of a genus $g$ knot has $g$ crossings whose change gives
the unknot \cite{KLMMMS}. This covers the torus knots, the $(1,1)$ $L$-space knots, which are closures of positive
braids \cite[Theorem 2]{Nie}, and all $L$-space knots of the SnapPy census but one \cite{BK}. It also holds for
strongly quasipositive $3$-braid knots \cite{LeeLee}. What remains are the $L$-space knots that are not braid positive.
The ones we know are the families of Baker--Kegel \cite{BK} and Himeno \cite{Himeno} and some iterated torus knots,
such as the $(2,3)$-cable of the trefoil \cite[Example 1]{BK}.

\section{The family}

Fix $n \ge 2$. In the braid group $B_{2n}$ let
\[ L_k = \sigma_{n-k}\,\sigma_{n-k+2}\cdots\sigma_{n+k} \quad (0 \le k \le n-1), \qquad
   X_n = L_0 L_1 \cdots L_{n-1} L_{n-2} \cdots L_0, \]
\[ T_n = \sigma_1^{-1}\cdots\sigma_{n-1}^{-1}\;\sigma_n\sigma_{n-1}\cdots\sigma_1\;\sigma_1\sigma_2\cdots\sigma_n, \]
and for odd $m \ge 1$ let $H(n,m)$ be the closure of $X_n^m T_n$. The letters of each $L_k$ commute. $X_n$ is the
$n$-cable of a positive crossing between two bundles of $n$ strands. The closure is a knot: the permutation of $X_n^m$
exchanges $i$ and $n+i$, that of $T_n$ is an $n$-cycle on $1, \dots, n$, and their product is a $2n$-cycle.

Since $X_2 = \sigma_2\sigma_1\sigma_3\sigma_2$ and $T_2 = \sigma_1^{-1}\sigma_2\sigma_1\sigma_1\sigma_2$, the knot
$H(2,2k+1)$ is the knot $K_k$ of Baker and Kegel \cite{BK}, a hyperbolic $L$-space knot of genus $4k+2$ for $k \ge 1$,
not braid positive for $k = 1$ ($K_1$ is the census knot o9\_30634) and not known to be braid positive for $k \ge 2$.
The knot $H(n,3)$ is the knot $K_n$ of Himeno \cite{Himeno}, hyperbolic for $n \ge 2$, and for even $n$ an $L$-space
knot of genus $(3n^2-n)/2+1$ that is not braid positive.

\section{The theorem}

\begin{theorem}\label{thm}
For $n \ge 2$ and odd $m \ge 1$, \quad $u(H(n,m)) = g(H(n,m)) = g_4(H(n,m)) = (mn^2-n+2)/2$.
\end{theorem}

\begin{corollary}
$u = g$ for every Baker--Kegel knot $K_k$ and every Himeno knot $K_n$. These are $L$-space knots for all $k$
\cite{BK}, for even $n$ \cite{Himeno}, and for $n = 3, 5$ by knot Floer homology, so for them this is an instance of
the statement $u = g$ for $L$-space knots.
\end{corollary}

\begin{proof}[Proof of Theorem~\ref{thm}]
\emph{Lower bound.} The word $X_n^m T_n$ has $mn^2 + 2n$ positive and $n-1$ negative letters, so writhe
$w = mn^2+n+1$, on $2n$ strands. Rudolph's slice--Bennequin inequality \cite{Rud93} gives
$g_4 \ge (w - 2n + 1)/2 = (mn^2-n+2)/2$, and $u \ge g_4$.

\emph{Genus.} $T_n = a\,\sigma_1\cdots\sigma_n$ with $a = (\sigma_n\cdots\sigma_2)\,\sigma_1\,(\sigma_n\cdots\sigma_2)^{-1}$
(Step 4 below), a positive half-twisted band joining the first and the $(n+1)$-st strand that passes on one side of the
strands between them. So $X_n^m T_n$ is a product of $mn^2+n+1$ positive bands, and its closure bounds the braided
surface with one disk per strand and one band per factor \cite{Rud83}, a Seifert surface of genus
$(mn^2+n+1-2n+1)/2 = (mn^2-n+2)/2$. Hence $g \le (mn^2-n+2)/2 \le g_4 \le g$.

\emph{Upper bound.} A crossing change in the closed braid replaces a letter $\sigma_i^{\pm 1}$ by $\sigma_i^{\mp 1}$. We
make $(mn^2-n+2)/2$ of them and reach the unknot. Matching explicit crossing changes against the slice--Bennequin bound
is a standard way to compute unknotting numbers of closed braids \cite[\S 4]{Stoimenow}, \cite[\S 2]{KLMMMS}; what is
specific here is the cancellation of the palindromic blocks.

\emph{Step 1.} Read backwards, $X_n$ is $L_0 \cdots L_{n-2} L_{n-1} L_{n-2} \cdots L_0$ with the letters of each layer
permuted, so it represents the same braid; hence the word obtained from $X_n$ by inverting every letter represents
$X_n^{-1}$. Changing all crossings of the second, fourth, \dots, $(m-1)$-st copy of $X_n$ turns $X_n^m T_n$ into
$X_n T_n$, with $n^2(m-1)/2$ changes.

\emph{Step 2.} Write $X_n = C L_{n-1} \bar C$ with $C = L_0\cdots L_{n-2}$ and $\bar C = L_{n-2}\cdots L_0$. Changing the
$n(n-1)/2$ crossings of $\bar C$ replaces it by $C^{-1}$.

\emph{Step 3.} $T_n = a\,\sigma_1\cdots\sigma_n$ with $a = (\sigma_{n-1}\cdots\sigma_1)^{-1}\sigma_n(\sigma_{n-1}\cdots\sigma_1)$.
Changing the crossing $\sigma_n$ inside $a$ replaces $a$ by $a^{-1}$. In all,
$n^2(m-1)/2 + n(n-1)/2 + 1 = (mn^2-n+2)/2$ changes, giving the braid $C L_{n-1} C^{-1} R$ with
$R = a^{-1}\sigma_1\cdots\sigma_n \in B_{n+1}$.

\emph{Step 4: the closure of $C L_{n-1} C^{-1} R$ is the unknot.} It is the closure of the conjugate
$L_{n-1}\cdot C^{-1} R\, C$. Call the strands at the top of $X_n$ $A_1, \dots, A_n$ (positions $1, \dots, n$) and
$B_1, \dots, B_n$ (positions $n+1, \dots, 2n$). Every crossing of $X_n$ is between an $A$ strand and a $B$ strand, with
the $A$ strand on the same side, say over, every time. $C$ performs the crossings of $A_i$ with $B_j$ for $j < i$, after
which $A_i$ is at position $2i-1$ and $B_i$ at $2i$, and $L_{n-1}$ crosses $A_i$ with $B_i$. In the conjugate, after
$L_{n-1}$ the strand $B_i$ is at position $2i-1$ and $A_i$ at $2i$. The word $C^{-1}$ moves the strands at odd positions
back to positions $1, \dots, n$ and those at even positions to $n+1, \dots, 2n$; since $C^{-1}$ undoes $C$, the strand
coming from an even position passes under every strand it meets, in $C^{-1}$ and again in $C$. So $R$ acts on
$B_1, \dots, B_n, A_1$ and leaves $A_2, \dots, A_n$ alone, and each $A_i$ with $i \ge 2$, followed from its crossing in
$L_{n-1}$ once around the closed braid back to that crossing, lies under every strand it meets. Pushing that arc below
the diagram and shrinking it removes the strand and its crossing. After doing so for $i = n, \dots, 2$ the closure is
that of
\[ \sigma_1\cdot(\sigma_2^{-1}\cdots\sigma_n^{-1})\cdot R\cdot(\sigma_n\cdots\sigma_2) \in B_{n+1}, \]
where $\sigma_1$ is the crossing of $A_1$ with $B_1$, the factor before $R$ moves $A_1$ to position $n+1$ under
$B_2, \dots, B_n$, and the factor after $R$ moves the strand then in position $n+1$ back in the same way. Conjugating by $\sigma_n\cdots\sigma_2$ and using
$\sigma_n\cdots\sigma_2\,\sigma_1\,\sigma_2^{-1}\cdots\sigma_n^{-1} = (\sigma_{n-1}\cdots\sigma_1)^{-1}\sigma_n(\sigma_{n-1}\cdots\sigma_1) = a$,
which follows by induction from $\sigma_{i+1}\sigma_i\sigma_{i+1}^{-1} = \sigma_i^{-1}\sigma_{i+1}\sigma_i$, the closure is
that of $a R = \sigma_1\sigma_2\cdots\sigma_n \in B_{n+1}$, the unknot.
\end{proof}

\noindent Without the change in Step 3 the same reduction gives the closure of $a^2\sigma_1\cdots\sigma_n$, a knot of
genus one (its braided surface has $n+2$ bands on $n+1$ disks); the change in Step 3 unknots it.

\section{Cables}

\begin{corollary}
Every $L$-space $(2,q)$-cable of $T(2,2k+1)$ has $u = g$.
\end{corollary}

\begin{proof}
The cable is the closure of $X_2^{2k+1}\sigma_1^{e}$ with $e = q - 2(2k+1)$, and it is an $L$-space knot exactly when
$q \ge 2(2k-1)$ \cite{Hedden, Hom}, that is $e \in \{-3, -1, 1, 3, \dots\}$. For $e \ge 1$ the word is positive. For $e = -1$,
Step 1 with $k$ cancelled copies of $X_2$ ($4k$ changes) leaves $X_2\sigma_1^{-1}$, whose closure is the unknot, and
$g = 4k$. For $e = -3$, cancelling $k-1$ copies ($4k-4$ changes) leaves $X_2^3\sigma_1^{-3}$, the $(2,3)$-cable of the
trefoil, which three changes unknot (its first three letters); $g = 4k-1$.
\end{proof}

\section{The hypothesis is needed}

\begin{proposition}[Bode--Tru\"ol \cite{BT}]
The mirror of $12n_{642}$ is fibered and strongly quasipositive, has genus $2$, is not an $L$-space knot, and has
unknotting number at least $3$.
\end{proposition}

\noindent This is \cite[\S 2.7.2 and Example 6.1]{BT}; we include the computation as a check.

\begin{proof}
Knot Floer homology gives genus $2$, fiberedness and $|\tau| = 2$; the chirality with $\tau = g$ is strongly
quasipositive, since a fibered knot with $\tau = g$ is \cite{Hedden2}. Its total rank is @@HFKRANK@@, more than $2g+1$,
so it is not an $L$-space knot. A Seifert matrix $V$ has $\det(V+V^T) = \pm 27$ and $V + V^T$ has nullity $3$ over
$\mathbb{F}_3$, so the first homology of the double branched cover is $(\mathbb{Z}/3)^3$ and needs three generators;
by Wendt \cite{Wendt} this is a lower bound for the unknotting number.
\end{proof}

\noindent KnotInfo lists $u(12n_{642}) \in \{3, 4\}$. So $u = g$ fails for fibered strongly quasipositive knots, holds
for braid positive ones, and for fibered positive knots is Stoimenow's conjecture, open, with a likely counterexample
of genus $7$ in \cite{KLMMMS}.

\section{Computations}

All in \texttt{verification/families}. \texttt{unknotting.py}: for $2 \le n \le @@NMAX@@$ and $m \in \{@@MLIST@@\}$
(@@NCASES@@ cases, up to @@MAXFLIPS@@ changes) the number of changes equals the slice--Bennequin bound and the changed word
closes to the unknot (SnapPy simplification to no crossings, or knot Floer homology of total rank $1$).
\texttt{cables.py}: the two non-positive cases for $1 \le k \le @@KMAX@@$ (@@CABN@@ cables), with the genus from knot Floer
homology. \texttt{fibered\_sqp.py}: the proposition. \texttt{lspace.py}: which $H(n,m)$ are $L$-space knots by knot Floer
homology; for the @@LS_N@@ members computed, the genus it gives equals $(mn^2-n+2)/2$. Tools: SnapPy 3.3.2 with \texttt{knot\_floer\_homology}.

\section{Questions}

\begin{question}
Is $u = g$ known, or expected, for every $L$-space knot?
\end{question}

\begin{question}
Besides the two families above and some iterated torus knots, which $L$-space knots are known not to be braid positive?
\end{question}

\begin{thebibliography}{9}
\bibitem{BT} B. Bode, P. Tru\"ol, \emph{On $\mathcal{T}$-positive links}, arXiv:2605.10502.
\bibitem{BK} K. L. Baker, M. Kegel, \emph{Census $L$-space knots are braid positive, except for one that is not},
Algebr. Geom. Topol. 24 (2024); arXiv:2203.12013.
\bibitem{Hedden} M. Hedden, \emph{On knot Floer homology and cabling II}, Int. Math. Res. Not. (2009).
\bibitem{Hom} J. Hom, \emph{A note on cabling and $L$-space surgeries}, Algebr. Geom. Topol. 11 (2011), 219--223.
\bibitem{Hedden2} M. Hedden, \emph{Notions of positivity and the Ozsv\'ath--Szab\'o concordance invariant},
J. Knot Theory Ramifications 19 (2010), 617--629.
\bibitem{Himeno} K. Himeno, \emph{Non-braid positive hyperbolic $L$-space knots}, arXiv:2506.22934.
\bibitem{KLMMMS} M. Kegel, L. Lewark, N. Manikandan, F. Misev, L. Mousseau, M. Silvero, \emph{On unknotting fibered
positive knots and braids}, arXiv:2312.07339.
\bibitem{KnotInfo} C. Livingston and A. H. Moore, \emph{KnotInfo: Table of Knot Invariants}, knotinfo.org
(accessed 14 September 2026).
\bibitem{LeeLee} E.-K. Lee, S.-J. Lee, \emph{Unknotting number and genus of $3$-braid knots}, J. Knot Theory
Ramifications 22 (2013), 1350047; arXiv:1305.3455.
\bibitem{Ni} Y. Ni, \emph{Knot Floer homology detects fibred knots}, Invent. Math. 170 (2007), 577--608.
\bibitem{Nie} Z. Nie, \emph{An explicit description of $(1,1)$ $L$-space knots, and non-left-orderable surgeries},
arXiv:2102.10891.
\bibitem{OS} P. Ozsv\'ath, Z. Szab\'o, \emph{On knot Floer homology and lens space surgeries}, Topology 44 (2005),
1281--1300.
\bibitem{Rud83} L. Rudolph, \emph{Braided surfaces and Seifert ribbons for closed braids}, Comment. Math. Helv. 58
(1983), 1--37.
\bibitem{Rud93} L. Rudolph, \emph{Quasipositivity as an obstruction to sliceness}, Bull. Amer. Math. Soc. 29 (1993),
51--59.
\bibitem{Stoimenow} A. Stoimenow, \emph{Positive knots, closed braids and the Jones polynomial}, Ann. Sc. Norm. Super.
Pisa Cl. Sci. (5) 2 (2003), 237--285; arXiv:math/9805078.
\bibitem{Wendt} H. Wendt, \emph{Die gordische Aufl\"osung von Knoten}, Math. Z. 42 (1937), 680--696.
\end{thebibliography}
\end{document}
"""

for tok, val in {"HIMODD": "$ and $K_".join(map(str, him_odd)), "HFKRANK": sqp["hfk_rank"], "NMAX": N_MAX,
                 "MLIST": ", ".join(map(str, M_LIST)), "NCASES": N_CASES, "MAXFLIPS": MAX_FLIPS, "KMAX": K_MAX,
                 "CABN": CAB_N, "LS_N": LS_N}.items():
    tex = tex.replace(f"@@{tok}@@", str(val))
assert "@@" not in tex
(HERE / "k32.tex").write_text(tex)
print("wrote k32.tex")
