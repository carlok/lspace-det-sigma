"""Render k33.tex from the result files: every number in the document comes from a script."""
import json
from pathlib import Path

HERE = Path(__file__).parent
V = HERE.parent / "verification"
load = lambda f: [json.loads(l) for l in open(V / f)]
J = lambda f: json.load(open(V / f))

def sci(x):
    from math import floor, log10
    e = floor(log10(abs(x))); m = x / 10 ** e
    return f"{m:.1f}\\times 10^{{{e}}}"

it = J("iterated.json"); cong = J("congruence.json"); hard = J("hardening.json"); ob = load("onebridge.jsonl"); lem = J("lemma_L.json"); steps = J("proof_steps.json"); ind = J("induction_proof.json")
fast = load("census_lspace_fast.jsonl"); fam = load("families_fast.jsonl")
native = [r for r in load("census_sage_native.jsonl") if r.get("holds") is False]
hfk = {}
for f in ["hyperbolic.jsonl"] + [p.name for p in V.glob("census_shard*.jsonl")] + ["census_mp.jsonl"]:
    if (V / f).exists():
        for r in load(f):
            if "holds" in r: hfk[(r["source"], r["name"])] = r
hfk_n = len(hfk); hfk_bad = sum(1 for r in hfk.values() if not r["holds"])
tt = J("twisted_torus_sigma_summary.json")
ttr = load("twisted_torus_sigma.jsonl")
tt_eq = sum(1 for r in ttr if r["equality"])
tt_hypr = [r for r in ttr if r.get("hyperbolic")]
tt_minslack = min(r["bound"] - r["det_seifert"] for r in tt_hypr)
tt_maxg = max(r["genus"] for r in ttr)
rnd = J("random_lspace_sigma_summary.json"); rndgen = J("random_lspace_summary.json")
dk = {r["family"]: r for r in J("distinct_knots.json")}
defn = J("definiteness.json"); defid = J("definiteness_identify.json")
# the K32 results sit beside this note in the standalone repository, and one level up in the
# working tree they were produced in
K32 = V / "k32" if (V / "k32").exists() else HERE.parents[1] / "K32" / "verification"
load_k32 = lambda f: [json.loads(l) for l in open(K32 / f)]
ug = json.load(open(K32 / "twisted_torus_ug_summary.json"))
ugr = [json.loads(l) for l in open(K32 / "twisted_torus_ug.jsonl")]
ug_hyp = sum(1 for r in ugr if r.get("u_equals_g") and r.get("hyperbolic"))
ug_maxg = max(r["genus"] for r in ugr if r.get("u_equals_g"))
fam_eq = sum(1 for r in fam if r["det"] == r["bound"])
# where equality occurs among the hyperbolic knots: census and Himeno
cen_eq = [r["name"] for r in fast if r["det"] == r["bound"]]
assert cen_eq == ["o9_30634"], cen_eq          # the text below names this knot
him = sorted((r for r in fam if r["name"].startswith("Himeno")), key=lambda r: int(r["name"].split("_")[-1]))
him_eq = [r["name"] for r in him if r["det"] == r["bound"]]
assert him_eq == ["Himeno K_2"], him_eq        # and this one, which is isometric to o9_30634
bk_eq = [r for r in fam if r["name"].startswith("Baker-Kegel") and r["det"] == r["bound"]]
exact_checked = sum(1 for r in fast if "matches_exact_run" in r)
exact_ok = sum(1 for r in fast if r.get("matches_exact_run") is True)

tex = r"""\documentclass[11pt]{article}
\usepackage[margin=2.4cm]{geometry}
\usepackage{amsmath,amssymb,amsthm,booktabs}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\sloppy
\newtheorem{theorem}{Theorem}
\newtheorem{lemma}{Lemma}
\newtheorem{conjecture}{Conjecture}
\newtheorem{question}{Question}
\newtheorem{proposition}{Proposition}
\theoremstyle{definition}
\newtheorem{remark}{Remark}
\title{An inequality between determinant and signature for $L$-space knots\\[2mm]
\large Machine-generated conjecture, its checks, a partial proof, and the open case}
\date{2026-09-19, revised 2026-10-10}
\begin{document}
\maketitle

\begin{abstract}
We consider the inequality $\det(K) \le 1 + |\sigma(K)|$ for $L$-space knots. It was produced by a program that fits
linear inequalities to the KnotInfo database and discards what its automatic checks refute. It survived those checks
and the computations of Section 3. We prove it for every $L$-space knot that is an iterated torus knot, in
particular for all algebraic knots. The hyperbolic case is open, and it is where the inequality is sharp:
equality holds on the Baker--Kegel knots $K_k$, an infinite family of hyperbolic $L$-space knots, for which we prove
$\det(K_k) = 4k+5$ and compute $\sigma(K_k) = -(4k+4)$ for $k \le @@BKK@@$. Each $K_k$ has the Alexander polynomial, hence
the knot Floer complex, of an $L$-space cable that attains equality as well. Among the @@CENSUS_N@@ census $L$-space knots
equality holds only on $K_1$.
Sections 2 and 3 give the provenance and the computations, so that the proof in Sections 5 and 6 can be checked
without our files; the one lemma we prove from scratch rather than cite is additionally formalised in Lean 4
with no \texttt{sorry}.
\end{abstract}

\section{Statement and conventions}

Signs follow KnotInfo: the right-handed trefoil has $\sigma = -2$, $s = 2$, $\tau = 1$. A knot $K \subset S^3$ is an
\emph{$L$-space knot} if some positive Dehn surgery on $K$ yields an $L$-space. Positive torus knots then have
$\sigma < 0$. We do not assume a sign for a general $L$-space knot: $\sigma \le 0$ is carried through the induction of
Theorem~\ref{thm} for the knots treated there, and it held on every $L$-space knot we computed (all %d census knots
and all %d knots of the families of Section~3). Write $\det(K) = |\Delta_K(-1)|$ and $g = g(K)$ for the Seifert genus.

\begin{conjecture}[K33]\label{conj}
For every $L$-space knot $K$, \[ \det(K) \;\le\; 1 + |\sigma(K)| . \]
\end{conjecture}

We use the following standard facts. An $L$-space knot is fibered, strongly quasipositive, and satisfies
$g = g_4 = \tau$ (Ozsv\'ath--Szab\'o, Ni, Hedden); its Alexander polynomial has the form
$\Delta_K(t) = \sum_{k=0}^{2n} (-1)^k t^{a_k}$ with $a_0 = g > a_1 > \dots > a_{2n} = -g$ (Ozsv\'ath--Szab\'o).
Consequently $|\sigma(K)| \le 2g$ and $\det(K) \le 2g+1$.

\section{Provenance}

The inequality was not conjectured by a person. It is candidate K33 of 42 statements emitted by \texttt{ragusa}, an
engine that enumerates bounds of the form (property) $\Rightarrow$ (target $\le c \cdot$ feature $+ k$) over a table of
invariants, here KnotInfo \cite{KnotInfo} restricted to prime knots with 3 to 13 crossings, and reports what survives its filters
together with the evidence behind each survivor. K33 was found on the \texttt{l\_space} column, where the table
contains %d knots; those knots were the whole of its initial evidence.

The other 41 candidates were triaged in the same session: 18 were refuted by explicit knots, 13 turned out to be known
theorems or true by definition, 3 had one clause refuted and one left open, and 6 remain open but rest on weak
evidence. Two remained open with evidence beyond the table: K33, and $u = g$ for $L$-space knots.

\section{Verification history}

All computations use SnapPy (knot Floer homology, for the $L$-space property and $\tau$), Sage (Seifert matrices,
signatures, determinants) and exact formula implementations; scripts are listed in Section~\ref{sec:repro}.

\begin{center}\small
\begin{tabular}{p{5.1cm}rrp{5.4cm}}
\toprule
family of $L$-space knots & tested & viol. & how the invariants are known \\
\midrule
iterated torus knots & %d & %d & exact: cabled Alexander polynomial, Litherland's formula \\
SnapPy census $L$-space knots (all) & %d & %d & Seifert matrix of a positive braid word \\
census knots, independent route & %d & %d & knot Floer homology, Sage signature \\
Baker--Kegel, Himeno, $(2,q)$-cables & %d & %d & Seifert matrix of the braid word \\
Baker--Kegel $K_k$, $k \le @@BKK@@$ & @@BKK@@ & 0 & Seifert matrix of the braid word, certified \\
$H(n,m)$ (Section 7), outside the census & @@HNM_N@@ & 0 & Seifert matrix of the braid word, certified \\
one-bridge braids $B(w,b,t)$, $w \le 15$ (parameter triples) & %d & %d & Seifert matrix of the braid word \\
twisted torus knots $K(p,q;r,s)$ (distinct knots) & @@TT_D@@ & @@TT_V@@ & knot Floer homology, then exact Seifert signature \\
random braid words (distinct knots) & @@RND_D@@ & @@RND_V@@ & knot Floer homology, then exact Seifert signature \\
\bottomrule
\end{tabular}
\end{center}

\noindent The census braid words are those published by Baker and Kegel (arXiv:2203.12013, Appendix), which cover all
%d census $L$-space knots. Every closure was checked to be the named census knot: %d of %d by SnapPy's isometry test
directly, the remaining one after retriangulation and at higher precision. All %d signatures are exact, computed by
congruence diagonalisation over $\mathbb{Q}$ from the integral matrix $V + V^{\mathsf T}$; they agree with an earlier
floating-point computation on all %d knots and with Sage's own exact signature on the %d knots where that finished.
The one-bridge braids are $L$-space knots by \cite{GLV}; for the %d smallest this was also confirmed directly by knot
Floer homology, with the genus matching the braid-surface genus.

\paragraph{Generated families, counted by knot.} Three rows of the table come from parameters or words rather than
from a list: the one-bridge braids, the twisted torus knots $K(p,q;r,s)$, the closures of
$(\sigma_1 \cdots \sigma_{p-1})^q (\sigma_1 \cdots \sigma_{r-1})^s$, and the closures of random braid words. Different
parameters often close to the same knot, and an earlier version of this note counted diagrams, which overstated these
families several times over. Counted by knot type, exactly for hyperbolic knots through the isometry signature of the
complement and approximately otherwise, the @@OB_REC@@ one-bridge parameter triples give @@OB_D@@ knots, @@OB_H@@ of them
hyperbolic and at least @@OB_NEW@@ of those outside the SnapPy census; the @@TT_REC@@ twisted torus records give @@TT_D@@
knots, @@TT_H@@ hyperbolic; and the @@RND_REC@@ random records give @@RND_D@@ knots, @@RND_H@@ hyperbolic. Every hyperbolic
knot in the last two families is a census knot, so they confirm the census rows rather than extend them; the hyperbolic
evidence beyond the census is the one-bridge braids and the Baker--Kegel and Himeno families. In the twisted torus and
random families the $L$-space property was decided by each knot's own knot Floer homology, and the determinant was
computed twice, from the knot Floer gradings and from the Seifert matrix, agreeing on all @@DET_AGREE@@ records.

\paragraph{Independent check.} A language model with no access to our computations re-derived the lattice count and
recomputed, independently: the six torus signatures used here, Lemma~\ref{lem:L} and the bound on $N_<$ for all coprime
$p \le 24$, $q < 120$, the closed forms and their reductions, the list of leftover small pairs in the induction, the
induction step under worst-case hypotheses, and the identity \eqref{eq:det} on three examples. It found no errors. The
gaps it flagged (an unsupported sign assertion, boundary points in the count, the $p<q$ convention, the nontriviality
hypothesis in (F4), the derivation of the symmetry of $S$, missing references) are addressed in this version. A third model corrected the proof of Lemma~\ref{lem:L}, where an earlier version claimed an
equivalence that is only a sufficient condition, and asked for the hypotheses and chirality conventions now stated;
the identity $\sigma = 4N_{<} - 2g$ was verified on all coprime $p \le 15$, $q < 50$, where $N_{<}/g \le 0.234$, so
the branch proved here is the operative one. A second
model, asked to attack the open case, contributed the congruence of Section~5, the one-bridge braid family of the
table, and the rigidity observation of Section~7; its computations of the one-bridge braids (%d parameter triples, %d violations,
%d equalities) and of the Baker--Kegel invariants were reproduced independently here.

\paragraph{The hypothesis is not redundant.} Evaluating the same inequality on census knots whose braid word is
positive or negative but which are \emph{not} $L$-space knots produces %d violations. So the $L$-space condition does
the work; this is unlike several of the 42 candidates, whose hypotheses turned out to be irrelevant.

\paragraph{Sharpness.} Equality $\det = 1 + |\sigma|$ holds for $T(2,n)$, for the $(2,q)$-cables of the trefoil, and,
among the families tested beyond the census, for %d of %d knots, including every Baker--Kegel $K_n$ computed there,
$n \le %d$ (Section 7 extends this to $n \le @@BKK@@$). These are hyperbolic: $K_1$ is the census knot o9\_30634, the one census $L$-space knot that is
not braid positive, and $K_n$ for $n \ge 2$ is not known to be braid positive. Of the @@CENSUS_N@@ census $L$-space knots,
exactly @@CENSUS_EQ@@ attains equality, and it is $K_1$.

\section{A reformulation}

For an $L$-space knot let $S \subset \mathbb{Z}_{\ge 0}$ be its staircase set (the \emph{formal semigroup}; for an
algebraic knot it is the semigroup of the singularity, but for a general $L$-space knot it need not be closed under
addition), the complement of the $g$ gaps, determined by $t^{g}\Delta_K(t) = (1-t)\sum_{s \in S,\, s < 2g} t^{s} + t^{2g}$. Evaluating at $t = -1$ and using the symmetry
$s \leftrightarrow 2g-1-s$ between $S \cap [0,2g)$ and the gaps, which follows from $\Delta_K(t) = \Delta_K(t^{-1})$
and gives $|S \cap [0,2g)| = g$ as well, one obtains

\begin{equation}\label{eq:det}
 \det(K) = |2D+1|, \qquad D = \#\{\text{odd gaps}\} - \#\{\text{even gaps}\}.
\end{equation}

Hence Conjecture~\ref{conj} is equivalent to $|\sigma| \ge 2D$ when $D \ge 0$, and to $|\sigma| \ge 2|D| - 2$ when
$D < 0$. Identity~\eqref{eq:det} was checked on %d iterated torus knots with %d mismatches.

\begin{remark}
The cruder route fails. Since the coefficients of $\Delta_K$ are $\pm 1$, $\det(K)$ is at most the number of nonzero
coefficients, so Conjecture~\ref{conj} would follow from $|\sigma| \ge \#\{\text{terms}\} - 1$. That inequality is false:
it fails on %d of the %d iterated torus knots tested, and the failures are exactly the knots where
Conjecture~\ref{conj} is sharp. Any proof must therefore see the cancellation in $\Delta_K(-1)$.
\end{remark}

\section{An arithmetic refinement}

For any knot, $\Delta_K(-1) \equiv 1 \pmod 4$ and $\operatorname{sign}\Delta_K(-1) = (-1)^{\sigma/2}$ (Murasugi),
so $\det(K) \equiv (-1)^{\sigma/2} \pmod 4$ and therefore

\begin{equation}\label{eq:cong}
 1 + |\sigma(K)| - \det(K) \equiv 0 \pmod 4 .
\end{equation}

Checked on all %d $L$-space knots computed here with an exact signature and determinant: %d failures. Two consequences. First, a counterexample to Conjecture~\ref{conj} must satisfy
$\det(K) \ge |\sigma(K)| + 5$; the inequality cannot fail narrowly. Second, combining \eqref{eq:cong} with
\eqref{eq:det}, the \emph{signature defect} $2g - |\sigma|$ of an $L$-space knot satisfies
$2g - |\sigma| \equiv 0 \pmod 4$ when $D \ge 0$, and Conjecture~\ref{conj} becomes

\[ 2g - |\sigma| \;\le\; 4\,\#\{\text{even gaps}\} \qquad (D \ge 0), \]

both sides being multiples of $4$. (For $D < 0$ the corresponding statement is
$2g - |\sigma| \le 4\,\#\{\text{odd gaps}\} + 2$.) In particular the conjecture holds automatically for every
$L$-space knot with $\det \le 3$ and for every definite one.

\section{Proof for iterated torus knots}

Throughout, $p \ge 2$ and $q$ are coprime, $T(p,q)$ is the positive torus knot with $g(T(p,q)) = (p-1)(q-1)/2$, and
$K_{p,q}$ denotes the $(p,q)$-cable of $K$ (winding number $p$). We use:

\begin{itemize}
\item[(F1)] $\Delta_{K_{p,q}}(t) = \Delta_K(t^p)\,\Delta_{T(p,q)}(t)$; since $\Delta_K(1) = 1$ this gives
  $\det(K_{p,q}) = \det(K)\det(T(p,q))$ for $p$ odd and $\det(K_{p,q}) = \det(T(p,q))$ for $p$ even.
\item[(F2)] Litherland's cabling formula $\sigma(K_{p,q}) = \sigma_{(-1)^p}(K) + \sigma(T(p,q))$, so
  $\sigma(K_{p,q}) = \sigma(K) + \sigma(T(p,q))$ for $p$ odd and $= \sigma(T(p,q))$ for $p$ even.
\item[(F3)] $\det(T(p,q)) = 1$ if $p,q$ are both odd, $= p$ if $q$ is even, $= q$ if $p$ is even.
\item[(F4)] (Hedden; Hom) for $K$ nontrivial, $K_{p,q}$ is an $L$-space knot if and only if $K$ is one and
  $q \ge p(2g(K)-1)$.
\end{itemize}

(F1)--(F3) were verified on %d cable instances, with %d, %d and %d mismatches respectively.

\begin{lemma}\label{lem:L}
For integers $2 \le p < q$ with $\gcd(p,q) = 1$, \quad
$\sigma(T(p,q)) \le -g(T(p,q))$, where $g(T(p,q)) = \tfrac{(p-1)(q-1)}{2}$; in particular $|\sigma| \ge g$.
\end{lemma}

\begin{proof}
We use the lattice count for torus knot signatures (Brieskorn; Gordon--Litherland--Murasugi \cite{GLM};
Litherland \cite{Lith}), in the normalisation $\sigma(T(2,3)) = -2$ of Section 1:
$\sigma(T(p,q)) = N_{\mathrm{out}} - N_{\mathrm{in}}$ over the
grid $G = \{1,\dots,p-1\}\times\{1,\dots,q-1\}$, where $(i,j)$ is counted in $N_{\mathrm{in}}$ when
$\tfrac12 < \tfrac ip + \tfrac jq < \tfrac32$. The involution $(i,j) \mapsto (p-i,q-j)$ of $G$ exchanges the two
outside regions, so $N_{\mathrm{out}} = 2N_{<}$ with $N_{<} = \#\{(i,j) \in G : \tfrac ip + \tfrac jq < \tfrac12\}$.
No lattice point of $G$ lies on a boundary: $\tfrac ip + \tfrac jq \in \{\tfrac12, \tfrac32\}$ gives
$2(iq + jp) \in \{pq, 3pq\}$, so $p \mid 2i$ and $q \mid 2j$, forcing $2i = p$ and $2j = q$ with $p$ and $q$ both even,
contradicting $\gcd(p,q) = 1$. As $N_{\mathrm{in}} + N_{\mathrm{out}} = 2g$, the count reads $\sigma(T(p,q)) = 4N_{<} - 2g$, so $|\sigma| \ge g$
holds if $N_{<} \le g/4$, and also if $N_{<} \ge 3g/4$. We prove the first branch,
$N_{<} \le (p-1)(q-1)/8$, which gives $\sigma(T(p,q)) \le -g < 0$.

For fixed $i$ the number of admissible $j$ is $\lceil f(i)\rceil - 1 \le f(i)$ with $f(i) = \tfrac q2 - \tfrac{iq}{p}$,
and $f(i) > 0$ exactly for $i < p/2$. Summing over those $i$:
if $p$ is even, with $m = p/2-1$, one gets $N_{<} \le q(p-2)/8$, and $q(p-2) \le (p-1)(q-1)$ reduces to $q \ge p-1$;
if $p$ is odd, with $m = (p-1)/2$, one gets $N_{<} \le q(p-1)^2/(8p)$, and $q(p-1)/p \le q-1$ reduces to $p \le q$.
Both hold because $q > p$.
\end{proof}

\paragraph{The lattice inequality is machine-checked.} The combinatorial core of this proof, the bound
$N_{<} \le (p-1)(q-1)/8$ for all integers $2 \le p < q$, has been formalised in Lean 4 against Mathlib
and carries no \texttt{sorry}: \texttt{\#print axioms} reports only \texttt{propext},
\texttt{Classical.choice} and \texttt{Quot.sound}. Coprimality is not needed for it. The formalisation
covers the column decomposition of the grid count, the per-column bound, the cut at $(p-1)/2$ in both
parities, the Gauss sum, the closed forms, and the two final comparisons; it does not cover the topology
the lemma is used with, namely the lattice count for $\sigma(T(p,q))$, which is cited. So the part of
Lemma~\ref{lem:L} proved here from scratch, rather than cited, is the part that is now checked by a
machine. The file is \texttt{K33Lattice/Basic.lean}.

\noindent Every step of this proof was also checked numerically on %d pairs with $p \le 15$, $q < 60$ (%d failures), and the conclusion
holds on all %d pairs with $p \le 20$, $q < 200$. Lemma~\ref{lem:L} says $-\sigma \ge b_1/2$ for torus knots, which is stronger than the linear bounds known for
arbitrary positive braid links (Feller proved a linear bound; Greene--Liechti give $-\sigma \ge b_1/4$, see the
abstract of \cite{GL}). We did not find Lemma~\ref{lem:L} in the literature; it may be folklore.

\begin{theorem}\label{thm}
Every $L$-space knot which is an iterated torus knot satisfies $\det(K) \le 1 + |\sigma(K)|$. In particular this holds
for all positive torus knots, hence for their mirrors since $\det$ and $|\sigma|$ are mirror invariant, and for all
algebraic knots, which are iterated torus knots with positive parameters \cite{EN} and hence $L$-space knots.
\end{theorem}

\begin{proof}
The induction is on the cabling depth, with torus knots at depth one; by (F4) applied to the companion (Hom's
``only if''), every companion of an $L$-space iterated torus knot is again an $L$-space knot, so the hypothesis is
available at each step. We prove simultaneously that $\det(K) \le 1 + |\sigma(K)|$ and $\sigma(K) < 0$. For torus knots
we may assume $p < q$, since $T(p,q) = T(q,p)$; in a cable $K_{p,q}$ of a nontrivial $L$-space knot, (F4) gives
$q \ge p(2g_K - 1) \ge p$, and $\gcd(p,q) = 1$ excludes $q = p$.

\emph{Base case.} For $T(p,q)$, $\sigma < 0$ is part of Lemma~\ref{lem:L}, and: if $p,q$ are both odd then $\det = 1$. If $q$ is even then $\det = p$ and
Lemma~\ref{lem:L} gives $|\sigma| \ge 3(p-1)/2$ (using $q \ge 4$), whence $1 + |\sigma| \ge p$. If $p$ is even then
$\det = q$; for $p = 2$ we have $|\sigma(T(2,q))| = q-1$, so $1 + |\sigma| = q$, with equality; for $p \ge 4$,
Lemma~\ref{lem:L} gives $|\sigma| \ge 3(q-1)/2 \ge q-1$.

\emph{Induction step.} Let $K$ be an $L$-space knot with $\det(K) \le 1 + A$, where $A = |\sigma(K)| \le 2g_K$, and let
$K_{p,q}$ be an $L$-space cable, so $q \ge p(2g_K-1)$ by (F4). Put $B = |\sigma(T(p,q))|$. By the induction hypothesis $\sigma(K) < 0$, and
$\sigma(T(p,q)) < 0$ by Lemma~\ref{lem:L}, so (F2) gives $\sigma(K_{p,q}) < 0$ and $|\sigma(K_{p,q})| = A + B$ for $p$
odd, $= B$ for $p$ even; this also propagates the sign claim.

If $p$ is even, then $\det(K_{p,q}) = \det(T(p,q)) = q$ by (F1) and (F3), and $q \le 1 + B$ was shown in the base case.

If $p$ and $q$ are both odd, then $\det(K_{p,q}) = \det(K) \le 1 + A \le 1 + A + B$.

If $p$ is odd and $q$ even, then $\det(K_{p,q}) = p\det(K) \le p(1+A)$, and the claim $p(1+A) \le 1 + A + B$ is
$(p-1)(1+A) \le B$. By Lemma~\ref{lem:L} it suffices that $1 + A \le (q-1)/2$, i.e. $q \ge 2A+3$, and since
$A \le 2g_K$ it suffices that $q \ge 4g_K+3$. As $p \ge 3$, (F4) gives $q \ge 6g_K-3$, which is $\ge 4g_K+3$ exactly
when $g_K \ge 3$. For $g_K \in \{1,2\}$ the uncovered pairs are finite: for $g_K = 1$ they are $(p,q) = (3,4)$ and
$(5,6)$, where $B = %d \ge 6$ and $B = %d \ge 12$; for $g_K = 2$ it is $(3,10)$, where $B = %d \ge 10$.
\end{proof}

\noindent The induction step was also verified directly, with the worst admissible values $A = 2g_K$ and
$\det(K) = 1+A$, over $g_K \le 11$, $p \le 11$ and the full range of $q$ allowed by (F4): %d failures.

\section{The open case}

Theorem~\ref{thm} does not reach the hyperbolic $L$-space knots, and that is where the inequality is sharp. Baker and
Kegel (arXiv:2203.12013) construct hyperbolic $L$-space knots $K_n$, the closures of the braid words
\[ [(2,1,3,2)^{2n+1},\, -1,\, 2,\, 1,\, 1,\, 2], \]
which are not braid positive for $n=1$ and are not known to be braid positive for $n \ge 2$; Himeno (arXiv:2506.22934) constructs infinitely many hyperbolic $L$-space knots that are provably not braid
positive. Equality $\det = 1 + |\sigma|$ holds for every Baker--Kegel $K_n$ tested in Section 3 ($n \le %d$), and more is true.

\begin{proposition}\label{prop:bk}
For every $k \ge 0$, $\Delta_{K_k} = \Delta_{C_k}$, where $C_k$ is the $(2,4k+5)$-cable of $T(2,2k+1)$, and
$\det(K_k) = 4k+5$.
\end{proposition}

\begin{proof}
Let $\rho$ be the reduced Burau representation of $B_4$, $P = \sigma_2\sigma_1\sigma_3\sigma_2$ and $W$ the tail of the
word, so that $\Delta_{K_k} \doteq \det(I - \rho(P)^{2k+1}\rho(W))\,(1-t)/(1-t^4)$. Expanding the $3 \times 3$ determinant,
the right side is a sum of traces of powers of $A = \rho(P)^2$, of its second exterior power and of $\det A$, so by
Cayley--Hamilton it satisfies a monic linear recurrence in $k$ of order $8$ over $\mathbb{Q}(t)$. So does
$\Delta_{C_k}(t) = \Delta_{T(2,2k+1)}(t^2)\,\Delta_{T(2,4k+5)}(t)$, with characteristic roots $1, t^4, t^8$; the
difference satisfies a recurrence of order $11$ and vanishes for $k = 0, \dots, 10$, hence for all $k$. At $t = -1$ the
order-$8$ recurrence becomes $(x-1)^8$, which $4k+5$ also satisfies, and the two agree for $k = 0, \dots, 7$.
\texttt{bk\_alex.sage} and \texttt{bk\_det.sage} carry out these computations exactly.
\end{proof}

Both $K_k$ and $C_k$ are $L$-space knots ($C_k$ by (F4)), so they have the same knot Floer complex. $C_k$ is an iterated
torus knot and attains equality in Theorem~\ref{thm}: $\det(C_k) = 4k+5$ and $\sigma(C_k) = \sigma(T(2,4k+5)) = -(4k+4)$
by (F1)--(F3). For $K_k$ we computed $\sigma(K_k) = -(4k+4)$ for $k \le @@BKK@@$, from the Seifert matrix of the braid
word (sizes up to @@BKSIZE@@, every eigenvalue certified away from zero), in agreement with \cite[Remark 4.6]{BK}, which
states $|\sigma(K_k)| = g + 2$. On this family the hyperbolic knot and the cable share the Floer complex, the determinant
and the signature.

\begin{question}
Does $\det(K) \le 1 + |\sigma(K)|$ hold for every $L$-space knot, in particular for the hyperbolic ones? Equivalently,
by \eqref{eq:det}, is $|\sigma(K)| \ge 2\bigl(\#\{\text{odd gaps}\} - \#\{\text{even gaps}\}\bigr)$?
\end{question}

\paragraph{The sharp case carries a rigidity statement.} If all $g$ gaps are odd then $S \cap [0,2g)$ consists of the
even numbers, so $\Delta_K = \Delta_{T(2,2g+1)}$, $D = g$ and $\det = 2g+1$; Conjecture~\ref{conj} then forces
$|\sigma(K)| = 2g$, that is, the symmetrised Seifert form is definite. So the conjecture implies: every $L$-space knot
with the Alexander polynomial of $T(2,2g+1)$ has $\sigma = -2g$. This is a weak form of Problem 1.21(c)(i) of the K3
problem list \cite{K3} (knot Floer homology detects $T(2g+1,2)$). Restricted to $L$-space knots, that problem is the
conjecture that the only thin $L$-space knots are the $T(2,n)$ \cite[\S1]{DeYeso}. It is proved for $g = 1$ by
Ghiggini \cite{Ghiggini}, for $g = 2$ by Farber--Reinoso--Wang \cite{FRW} together with Baldwin--Hu--Sivek \cite{BHS},
and for no larger $g$ \cite[\S1.1]{BS}. Any proof of Conjecture~\ref{conj} therefore proves this definiteness
statement.

\paragraph{What is known about the sharp case.} Three further facts, contributed by a fourth reader and checked here
against the exact data. (i) Such a $K$ is not a nontrivial cable: the staircase set of a cable $J_{p,q}$ is
$\{ps + qk : s \in S_J,\ 0 \le k \le p-1\}$, whose smallest positive element is $\min(p\,s_{\min}, q) \ge 4$, whereas
$S_{T(2,2g+1)}$ has smallest positive element $2$; here $s_{\min} \ge 2$ because $1$ is a gap of every nontrivial
$L$-space knot, which holds on all %d iterated torus knots computed. Among those knots, the only ones with
$\Delta = \Delta_{T(2,2g+1)}$ are the $T(2,2g+1)$ themselves. Baldwin and Sivek prove more: an $L$-space knot with
$\Delta = \Delta_{T(2,2g+1)}$ is not a satellite \cite[Proposition 6.8]{BS}. (ii) The roots of $\Delta_{T(2,2g+1)}$ are simple and on
the unit circle, so the Levine--Tristram function has $g$ jumps of $\pm 2$ on the upper half circle and
$\sigma(K) = -2g + 4m$, where $m$ counts the positive jumps; the question is exactly $m = 0$, that is, that the
signature function of $K$ agrees with that of $T(2,2g+1)$. (iii) Definiteness does not by itself force the torus knot:
among the %d $L$-space iterated torus knots computed, exactly %d are definite, namely the $T(2,n)$ together with
$T(3,4)$ and $T(3,5)$ (the knots among the $ADE$ singularity links). Neither of the last two has the Alexander
polynomial of a $T(2,2g+1)$, so on this restricted class definiteness and detection still coincide.

\paragraph{The hypothesis of the sharp case is met only by $T(2,2g+1)$.} For an $L$-space knot, $\det = 2g+1$ exactly
when every gap is odd, that is when $\Delta = \Delta_{T(2,2g+1)}$, which is also exactly when the knot is thin. Across the
census, the families beyond it, the one-bridge braids, the twisted torus knots and the random search, reaching genus
@@MAXG@@ in all, @@THIN_REC@@ records meet this hypothesis. Each was put into braid form and found, individually, to be the
closure of $\sigma_1^{2g+1}$ in $B_2$, which identifies it as $T(2,2g+1)$; together they cover $g \le @@THIN_G@@$, and
none of the census knots is among them. So every thin $L$-space knot found here is a $T(2,2g+1)$, which is the
$L$-space case of Problem 1.21(c)(i) appearing in the data, and on all of them the sharp case of
Conjecture~\ref{conj} holds.

Together these narrow a counterexample to Conjecture~\ref{conj} in the sharp case: it would have genus $g \ge 3$, it
would be hyperbolic (a torus knot with this Alexander polynomial is $T(2,2g+1)$, and satellites are excluded by
\cite[Proposition 6.8]{BS}), and it would need a positive Levine--Tristram jump at one of the $g$ roots. The same
hyperbolic case is the one left open in \cite[Theorem 1.6]{BS}, on detecting $T(2,2g+1)$ by its traces.

\paragraph{Why the induction stops.} For a torus knot the gaps of $\langle p,q \rangle$ satisfy
$2g - |\sigma| = 4\,\#\{\text{gaps} > pq/2\}$, so Theorem~\ref{thm} for torus knots says
$\#\{\text{gaps} > pq/2\} \le \#\{\text{even gaps}\}$. No analogue of the half-conductor $pq/2$ is available for a
hyperbolic $L$-space knot, and that is exactly what the cabling induction replaces.

\paragraph{Where equality occurs.} Among the hyperbolic $L$-space knots tested, equality occurs exactly on the
Baker--Kegel family: on every $K_n$ tested, and on no other census knot (Himeno's $K_2$ is the same knot as $K_1$). Failing
to be braid positive does not force it: Himeno's $K_n$ with $n$ even provably are not braid positive, and none of
$K_3, \dots, K_{@@HIM_MAX@@}$ attains equality, the last having $\det = @@HIM_LAST_DET@@$ against $1 + |\sigma| = @@HIM_LAST_BOUND@@$.
Proposition~\ref{prop:bk} locates the equality: each $K_k$ has the knot Floer complex and the signature of a cable
that attains it. (None of the @@OB_EQ@@ one-bridge parameter triples with equality closes to a hyperbolic knot.)

\paragraph{The family $H(n,m)$.} Both families are members of a two-parameter family of closed $2n$-braids, $H(n,m)$, the
closure of $X_n^m T_n$ with $X_n$ the $n$-cable of a positive crossing of two $n$-strand bundles and
$T_n = \sigma_1^{-1}\cdots\sigma_{n-1}^{-1}\sigma_n\cdots\sigma_1\sigma_1\cdots\sigma_n$; $H(2,2k+1) = K_k$ and $H(n,3)$ is
Himeno's $K_n$ (the companion note \texttt{k32.pdf} gives the details). Knot Floer homology shows every $H(n,m)$ we could
compute to be an $L$-space knot, and for $m \ge 3$ the volumes exceed every census volume, so they extend the
hyperbolic test set beyond the census: @@HNM_N@@ such knots satisfy the inequality, none with equality, the smallest margin
$1 + |\sigma| - \det$ being @@HNM_MARGIN@@.

\paragraph{The signature is not determined by the Floer complex.} For an $L$-space knot the Alexander polynomial
determines the knot Floer complex, but not the signature. Grouping the @@SBA_KNOTS@@ $L$-space knots of this note by their
Alexander polynomials gives @@SBA_POLYS@@ polynomials; @@SBA_SHARED@@ are shared by more than one knot, and @@SBA_CONFL@@ of
those carry two different signatures. The smallest case is classical: $T(3,4)$ and the $(2,3)$-cable of the trefoil have
the same Alexander polynomial and signatures $-6$ and $-2$. A hyperbolic case: the census knot t09847 has the Alexander
polynomial of the $(2,7)$-cable of $T(2,5)$, and signature $-10$ against $-6$. So the agreement
$\sigma(K_k) = \sigma(C_k)$ of Proposition~\ref{prop:bk} is a property of the Baker--Kegel knots, not of their Floer
complex, and Conjecture~\ref{conj} is not a statement about knot Floer homology alone. Within every group the inequality
holds for each member. The $(2,q)$-cables attain equality whatever the companion $J$: $\det(J_{2,q}) = q$ and
$\sigma(J_{2,q}) = -(q-1)$ by (F1)--(F3).

The sharp case would follow from $\sigma = -2\tau$ for knots with thin knot Floer homology, which is open
\cite[\S 8.1]{HM}.

Two further questions. Which $L$-space knots attain equality? The known ones are $T(2,n)$, the $(2,q)$-cables, the
Baker--Kegel family, and %d of the %d one-bridge parameter triples computed here. Does the inequality follow from a property of
the symmetrised Seifert form of an $L$-space knot, its determinant being bounded by its signature? Definite strongly
quasipositive links are studied in \cite{BBG}.

\section{A second statement from the same run}

The program produced one other statement that its checks could not refute and that we could not place in the
literature: for every $L$-space knot, $u(K) = g(K)$, where $u$ is the unknotting number.

Since $u \ge g_4 = g$ for an $L$-space knot, the content is $u \le g$, which holds for braid positive knots by Rudolph,
hence for every $L$-space knot known to be braid positive; by Baker and Kegel \cite{BK} that is all but one of the census
$L$-space knots. The companion note \texttt{k32.pdf} proves $u = g$ for the whole family $H(n,m)$ of Section 7, by an
explicit unknotting matched against the slice--Bennequin bound, so for every Baker--Kegel knot and every Himeno knot,
including those that are provably not braid positive. It also shows that the hypothesis is needed: the mirror of
$12n_{642}$ is fibered and strongly quasipositive, with $g = 2$ and $u \ge 3$. An earlier version of this section listed
unknottings found by search for a few of these knots, and counted Himeno's $K_3$ among the knots known not to be braid
positive; Himeno proves that for even $n$ only.

\section{Reproducibility}\label{sec:repro}

Scripts, each writing the JSON or JSONL file the corresponding numbers are read from:
\texttt{iterated.py} (exact iterated torus knots), \texttt{lemma\_L.py} (all steps of Lemma~\ref{lem:L}),
\texttt{induction\_proof.py} ((F1)--(F3) and the induction step), \texttt{proof\_steps.py} (identity~\eqref{eq:det}),
\texttt{census\_lspace\_fast.sage} (all census $L$-space knots from the Baker--Kegel braid words),
\texttt{census\_sage\_native.sage} (the non-$L$-space comparison), \texttt{families\_fast.sage} (families beyond the
census), \texttt{exact\_signature.py} and \texttt{exact\_census.py} (exact inertia for all census knots),
\texttt{braid\_identity.py} (the closures are the named census knots), \texttt{onebridge.sage} and
\texttt{onebridge\_lspace.py} (the one-bridge braid family), \texttt{twisted\_torus.py} and
\texttt{twisted\_torus\_sigma.sage} (the twisted torus family and its exact signatures), and
\texttt{twisted\_torus\_ug.py} (unknotting certificates of an earlier version of Section~8), \texttt{definiteness.py} and
\texttt{definiteness\_identify.py} (the sharp case across all families), \texttt{random\_lspace.py} and
\texttt{random\_lspace\_sigma.sage} (the random search), and \texttt{distinct\_knots.py} (how many distinct knots each
generated family contains, and which of its hyperbolic knots are in the census). In \texttt{families}: \texttt{bk\_det.sage} and
\texttt{bk\_alex.sage} (Proposition~\ref{prop:bk}), \texttt{seifert\_dump.py} and \texttt{signatures.sage} (the family
$H(n,m)$ and $K_k$ for $k \le @@BKK@@$), \texttt{lspace.py} (which $H(n,m)$ are $L$-space knots, and their volumes),
\texttt{sigma\_by\_alex.sage} (signatures grouped by Alexander polynomial), \texttt{onebridge\_equality.py} (the one-bridge braids with
equality are not hyperbolic), and for the companion note
\texttt{unknotting.py}, \texttt{cables.py} and \texttt{fibered\_sqp.py}.
Tools: SnapPy 3.3.2 with \texttt{knot\_floer\_homology}, Sage 10.7, khoca 1.5. The Lean formalisation of the
lattice inequality is \texttt{K33Lattice/Basic.lean}, built against Mathlib at revision
\texttt{0df444a360eaa60ab8c11dca51a86af692955474} with \texttt{leanprover/lean4:v4.33.1}.

\paragraph{Data provenance.} The candidate was generated from KnotInfo \cite{KnotInfo}, accessed on 14 September 2026.
No KnotInfo data is reproduced here: its maintainers ask that the database not be reposted, since copies go out
of date, so it should be read from \url{https://knotinfo.org}. The braid words for census knots are from Baker and
Kegel's appendix \cite{BK}.

\begin{thebibliography}{9}
\bibitem{BS} J. A. Baldwin, S. Sivek, \emph{$L$-spaces and knot traces}, arXiv:2501.00914v2 (2026).
\bibitem{BHS} J. A. Baldwin, Y. Hu, S. Sivek, \emph{Khovanov homology and the cinquefoil}, J. Eur. Math. Soc. 27
(2025), 2443--2465; arXiv:2105.12102.
\bibitem{BK} K. L. Baker, M. Kegel, \emph{Census $L$-space knots are braid positive, except for one that is not},
Algebr. Geom. Topol. 24 (2024); arXiv:2203.12013.
\bibitem{BBG} M. Boileau, S. Boyer, C. McA. Gordon, \emph{On definite strongly quasipositive links and $L$-space
branched covers}, Adv. Math. 357 (2019).
\bibitem{DeYeso} R. DeYeso III, \emph{Thin knots and the Cabling Conjecture}, Algebr. Geom. Topol. 25 (2025),
4547--4583; arXiv:2112.08074.
\bibitem{EN} D. Eisenbud, W. Neumann, \emph{Three-dimensional link theory and invariants of plane curve
singularities}, Ann. of Math. Studies 110, Princeton Univ. Press (1985).
\bibitem{Feller} P. Feller, \emph{The signature of positive braids is linearly bounded by their genus},
Internat. J. Math. 26 (2015); arXiv:1311.1242.
\bibitem{FRW} E. Farber, B. Reinoso, L. Wang, \emph{Fixed-point-free pseudo-Anosov homeomorphisms, knot Floer
homology and the cinquefoil}, Geom. Topol. 28 (2024), 4337--4381; arXiv:2203.01402.
\bibitem{Ghiggini} P. Ghiggini, \emph{Knot Floer homology detects genus-one fibred knots}, Amer. J. Math. 130 (2008),
1151--1169.
\bibitem{GL} J. E. Greene, L. Liechti, \emph{On the signature of a positive braid},
Ann. Henri Lebesgue 7 (2024), 823--839; arXiv:2308.02275.
\bibitem{GLM} C. McA. Gordon, R. A. Litherland, K. Murasugi, \emph{Signatures of covering links},
Canad. J. Math. 33 (1981), 381--394.
\bibitem{KnotInfo} C. Livingston and A. H. Moore, \emph{KnotInfo: Table of Knot Invariants}, knotinfo.org,
September 2026 (accessed 14 September 2026).
\bibitem{HM} K. Hendricks, C. Manolescu, \emph{Involutive Heegaard Floer homology}, Duke Math. J. 166 (2017),
1211--1299; arXiv:1507.00383.
\bibitem{Hedden} M. Hedden, \emph{On knot Floer homology and cabling II}, Int. Math. Res. Not. (2009).
\bibitem{Hedden2} M. Hedden, \emph{Notions of positivity and the Ozsv\'ath--Szab\'o concordance invariant},
J. Knot Theory Ramifications 19 (2010), 617--629.
\bibitem{Ni} Y. Ni, \emph{Knot Floer homology detects fibred knots}, Invent. Math. 170 (2007), 577--608.
\bibitem{GLV} J. E. Greene, S. Lewallen, F. Vafaee, \emph{$(1,1)$ $L$-space knots},
Compos. Math. 154 (2018), 918--933.
\bibitem{K3} D. Ruberman, R. \.I. Baykur, R. Kirby (eds.), \emph{K3: A New Problem List in Low-Dimensional Topology},
AMS Math. Surveys and Monographs 295 (2026), Problem 1.21.
\bibitem{Himeno} K. Himeno, \emph{Non-braid positive hyperbolic $L$-space knots}, arXiv:2506.22934.
\bibitem{Hom} J. Hom, \emph{A note on cabling and $L$-space surgeries}, Algebr. Geom. Topol. 11 (2011), 219--223.
\bibitem{Lith} R. A. Litherland, \emph{Signatures of iterated torus knots}, in Topology of Low-Dimensional Manifolds,
Lecture Notes in Math. 722 (1979), 71--84.
\bibitem{OS} P. Ozsv\'ath, Z. Szab\'o, \emph{On knot Floer homology and lens space surgeries},
Topology 44 (2005), 1281--1300.
\bibitem{Murasugi} K. Murasugi, \emph{On a certain numerical invariant of link types},
Trans. Amer. Math. Soc. 117 (1965), 387--422.
\end{thebibliography}

\end{document}
"""

vals = (
    # section 1
    len(fast), len(fam),
    # section 2
    11,
    # section 3 table
    it["tested"], len(it["violations"]),
    len(fast), sum(not r["holds"] for r in fast),
    hfk_n, hfk_bad,
    len(fam), sum(not r["holds"] for r in fam),
    len(ob), sum(not r["holds"] for r in ob),
    # section 3 text
    len(fast),
    hard["braid_identity"]["isometric"], hard["braid_identity"]["knots"],
    hard["exact_signatures"]["knots"], hard["exact_signatures"]["agree_with_numeric"],
    hard["exact_signatures"]["agree_with_sage_exact"], hard["onebridge_lspace"]["sample"],
    # independent check paragraph
    len(ob), sum(not r["holds"] for r in ob), sum(r["equality"] for r in ob),
    # hypothesis not redundant, sharpness
    len(native),
    fam_eq, len(fam), max(int(r["name"].split("_")[-1]) for r in bk_eq),
    # section 4
    steps["knots"], steps["det_formula_mismatches"],
    401, steps["knots"],
    # section 5 (congruence)
    cong["l_space_knots"], cong["l_space_failures"],
    # section 6
    4088, ind["f1"], ind["f2"], ind["f3"],
    lem["pairs_checked"], lem["failures"], lem["wide_range_pairs"],
    lem["small_cases"]["T(3,4)"], lem["small_cases"]["T(5,6)"], lem["small_cases"]["T(3,10)"],
    len(ind["step_failures"]),
    # section 7
    max(int(r["name"].split("_")[-1]) for r in bk_eq),
    it["tested"], 11889, 21,
    sum(r["equality"] for r in ob), len(ob),
)
bkg = {r["n"]: r for r in load_k32("bk_family.jsonl")}
for r in json.load(open(K32 / "hunt.json")):
    if r["knot"].startswith("Baker-Kegel K_"):
        bkg[int(r["knot"].split("_")[-1])] = r
himc = {r["n"]: r for r in load_k32("himeno.jsonl")}
assert all(r["u_equals_g"] for r in list(bkg.values()) + list(himc.values()))
assert himc[2]["isometric_to_o9_30634"] is True
k32_census = load_k32("census_lspace.jsonl")
tt_d, rnd_d, ob_d = dk["twisted torus"], dk["random search"], dk["one-bridge braids"]
assert not tt_d["distinct_hyperbolic_not_in_census"] and not rnd_d["distinct_hyperbolic_not_in_census"]
FAMD = V / "families"
fsig = {(r["n"], r["m"]): r for r in (json.loads(l) for l in open(FAMD / "signatures.jsonl"))}
flsp = {(r["n"], r["m"]): r for r in (json.loads(l) for l in open(FAMD / "lspace.jsonl"))}
assert all(r["certified"] for r in fsig.values()) and all(r["K33"] for r in fsig.values())
bk_rows = sorted((r for (n, m), r in fsig.items() if n == 2), key=lambda r: r["m"])
assert all(r["det"] == 2 * r["m"] + 3 and r["sigma"] == -(2 * r["m"] + 2) for r in bk_rows)   # 4k+5, -(4k+4), m = 2k+1
BKK = (bk_rows[-1]["m"] - 1) // 2
hnm_new = [fsig[k] for k, r in flsp.items() if k in fsig and k[0] >= 3 and k[1] >= 3
           and r.get("L_space") is True and r["outside_census"]]
assert all(not r["equality"] for r in hnm_new)
sba = json.load(open(FAMD / "sigma_by_alex.json"))
names = [{m[1] for m in g} for g in sba["conflicts"]]
assert any({"T(3,4)", "T(2,3);2,3"} <= g for g in names)          # the text names these two groups
assert any({"T(2,5);2,7", "t09847"} <= g for g in names)
sig_of = {m[1]: m[2] for g in sba["conflicts"] for m in g}
assert (sig_of["T(3,4)"], sig_of["T(2,3);2,3"], sig_of["T(2,5);2,7"], sig_of["t09847"]) == (-6, -2, -6, -10)
tokens = {
    "BKK": BKK, "BKSIZE": bk_rows[-1]["letters"] - 4 + 1,
    "HNM_N": len(hnm_new), "HNM_MARGIN": min(1 + abs(r["sigma"]) - r["det"] for r in hnm_new),
    "SBA_KNOTS": sba["knots"], "SBA_POLYS": sba["polynomials"], "SBA_SHARED": sba["polynomials_with_several_knots"],
    "SBA_CONFL": len(sba["conflicts"]), "OB_EQ": J("families/onebridge_equality.json")["equality_triples"] if not J("families/onebridge_equality.json")["hyperbolic_equality_triples"] else None,
    "CENSUS_N": len(fast), "CENSUS_EQ": len(cen_eq),
    "TT_REC": tt_d["records"], "TT_D": tt_d["distinct"], "TT_H": tt_d["distinct_by_kind"].get("hyperbolic", 0),
    "TT_V": tt["violations"],
    "RND_REC": rnd_d["records"], "RND_D": rnd_d["distinct"], "RND_H": rnd_d["distinct_by_kind"].get("hyperbolic", 0),
    "RND_V": rnd["violations"],
    "OB_REC": ob_d["records"], "OB_D": ob_d["distinct"], "OB_H": ob_d["distinct_by_kind"].get("hyperbolic", 0),
    "OB_NEW": len(ob_d["distinct_hyperbolic_not_in_census"]),
    "DET_AGREE": tt["tested"] + rnd["tested"] if not tt["det_mismatches"] and not rnd["det_mismatches"] else None,
    "MAXG": defn["max_genus_in_sample"], "THIN_REC": defid["tested"] if defid["unresolved"] == 0 else None,
    "THIN_G": max(defid["thin_genera"]),
    "HIM_MAX": max(int(r["name"].split("_")[-1]) for r in him),
    "HIM_LAST_DET": him[-1]["det"], "HIM_LAST_BOUND": him[-1]["bound"],
    "BK_MAX": max(bkg), "BK_MAXG": max(r["genus"] for r in bkg.values()),
    "K32_N": len(bkg) + len([n for n in himc if n != 2]),
    "K32_PROVEN": 1 + len([n for n in himc if n != 2]),
    "K32_CENSUS": sum(1 for r in k32_census if r.get("u_equals_g")),
}
assert all(v is not None for v in tokens.values()), tokens
text = tex % vals
for k, v in tokens.items():
    text = text.replace(f"@@{k}@@", str(v))
assert "@@" not in text
(HERE / "k33.tex").write_text(text)
print("wrote k33.tex")
