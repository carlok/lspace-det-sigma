# Two prompts for an external model, on the note `k33.tex`

Use them separately, in separate conversations. Prompt A is adversarial review of what is claimed to be proved.
Prompt B is an attempt at the open case. Give the model the LaTeX source `k33.tex`, not the PDF: no text is lost in
extraction, the formulas stay exact, and the model can quote precise strings. `prompt_A_review.md` and
`prompt_B_open_case.md` (built by `make_prompts.py`) already contain the prompt with the source inline, ready to paste
as a single message.

---

## Prompt A — review the note

You are reviewing a short mathematical note (LaTeX source below) on an inequality for L-space knots in S^3. Your job is to find
errors, not to be encouraging. The note was assembled with heavy computer assistance and one of its lemmas is proved
from scratch rather than cited, so treat every step as suspect until you have checked it yourself.

The claims to check, in order of importance:

1. **Lemma 1**: for coprime 2 <= p < q, |sigma(T(p,q))| >= g(T(p,q)) = (p-1)(q-1)/2. The proof uses the
   Brieskorn / Gordon-Litherland-Murasugi lattice count for the signature of a torus knot, an involution argument to
   get N_out = 2 N_<, and a per-column estimate ceil(f(i)) - 1 <= f(i). Verify each of these:
   - Is the counting formula stated with the right convention (which region counts positively, the role of the open
     interval (1/2, 3/2), what happens for lattice points exactly on the boundary)? Note that with the note's sign
     convention sigma(T(2,3)) = -2.
   - Does the involution really exchange the two outside regions, and is the resulting identity N_out = 2 N_< correct
     for all parities of p and q?
   - Is the per-column bound applied on the correct index range, and is the resulting closed form (q(p-2)/8 for p even,
     q(p-1)^2/(8p) for p odd) right?
   - Are the final reductions (q >= p-1 for p even, p <= q for p odd) correct, and do they cover all cases?
   If the lemma is already in the literature, say where; if it is false as stated, give a counterexample (p,q).

2. **Theorem 1** (K33 for L-space iterated torus knots), by induction over cabling. Check:
   - the cabling facts (F1), (F2), (F3) as stated, including chirality and sign conventions in Litherland's formula,
     and whether (F2) is being applied to the correct cable orientation;
   - the claim that sigma(K) and sigma(T(p,q)) have the same sign, which the proof uses to write |sigma(K_{p,q})| =
     A + B;
   - the case analysis by parities of p and q: is it exhaustive, given gcd(p,q) = 1 and p >= 2?
   - the reduction to q >= 4 g_K + 3 and the claim that the L-space condition q >= p(2 g_K - 1) supplies it when
     g_K >= 3;
   - whether the list of leftover small cases for g_K = 1 and g_K = 2 is complete. This is the step most likely to
     have a gap: recompute which pairs (p,q) with p odd, q even, gcd(p,q) = 1, q >= p(2 g_K - 1) are not covered by
     the inequality B >= (p-1)(q-1)/2, and check that the note lists all of them.
   - whether the induction is well founded (every L-space iterated torus knot is reached, and the base case is the
     right one).

3. **The reformulation** det = |2D + 1| with D = #odd gaps - #even gaps, derived from
   t^g Delta_K(t) = (1-t) sum_{s in S, s < 2g} t^s + t^{2g}. Check the derivation, including the symmetry
   s <-> 2g-1-s and the claim |S ∩ [0,2g)| = g.

4. **The background facts** attributed to Ozsvath-Szabo, Ni, Hedden, Hom: are they stated correctly and with the right
   attributions? Flag any citation that does not say what the note claims.

Report in this form:

```
verdict: CORRECT | CORRECT WITH GAPS | INCORRECT
errors: <numbered, each with the exact claim, why it fails, and a counterexample or corrected statement>
gaps: <steps that are true but not justified in the note>
known: <any part already in the literature, with a precise reference>
presentation: <at most five points, only if they affect correctness or readability>
confidence: high | medium | low, with a sentence on what you did not check
```

Do not invent references. If you are unsure whether a paper states something, say so and mark confidence low.

---

## Prompt B — attempt the open case

You are given a short note (LaTeX source below) proving the inequality

    det(K) <= 1 + |sigma(K)|

for every L-space knot in S^3 that is an iterated torus knot, and asking whether it holds for all L-space knots. Your
task is to settle the open case, or to make definite progress on it. Assume the note's Theorem 1 and Lemma 1 are
correct (they are reviewed separately); you may use them freely.

What is known, and what the data say:

- The inequality is sharp. Equality det = 1 + |sigma| holds for T(2,n), for the (2,q)-cables of the trefoil, and for
  every member tested (n = 1..25) of Baker and Kegel's family of hyperbolic L-space knots, the closures of
  [(2,1,3,2)^(2n+1), -1, 2, 1, 1, 2] (arXiv:2203.12013). So the open case contains the extremal examples.
- No counterexample exists among: all 632 L-space knots of the SnapPy census, 11,728 L-space iterated torus knots,
  and 68 knots of the non-braid-positive families (Baker-Kegel K_1..K_25, Himeno K_2..K_8, cables of T(2,3), T(2,5)).
- The hypothesis is essential: 25 census knots that are closures of positive or negative braids but are not L-space
  knots violate the inequality.
- Equivalent form: for an L-space knot with semigroup set S and gap set of size g,
  det = |2D + 1| with D = #(odd gaps) - #(even gaps), so the conjecture says |sigma| >= 2D when D >= 0.
- A termwise bound is too weak: det <= #(nonzero coefficients of Delta) combined with |sigma| >= #terms - 1 would
  suffice, but the latter is false, failing exactly on the knots where the conjecture is sharp.

Directions worth trying, in no particular order. You are not required to follow them.

1. Prove it for all L-space knots. The natural objects are the symmetrised Seifert form V + V^T of a fibered knot
   (unimodular V, so det(V + V^T) = det(I + monodromy)), the staircase complex, and the semigroup S.
2. Prove it under an extra hypothesis that covers the hyperbolic families, for instance for L-space knots that are
   closures of positive braids with one negative band, which is the shape of all known non-braid-positive examples.
3. Characterise the equality case. The known equality knots are T(2,n), their iterated (2,q)-cables and the
   Baker-Kegel family; a clean characterisation would probably reveal the mechanism.
4. Find a counterexample. Candidate sources: hyperbolic L-space knots of large genus outside the census, Himeno's
   family for larger even n, L-space knots with unusually small |sigma| relative to genus.
5. Decide whether the statement is already known. It was not found in a search of the literature, the zbMATH Open and
   arXiv APIs, or the K3 problem list (Ruberman-Baykur-Kirby, AMS Surveys 295, 2026). If you recognise it, say where
   it appears.

Report in this form:

```
outcome: PROVED | REFUTED | PARTIAL | NO PROGRESS | KNOWN
statement proved or refuted: <exact statement, with hypotheses>
argument: <complete proof, or the counterexample with every invariant value and how it is known>
what remains: <precisely what is still open>
references: <only sources you are confident exist>
confidence: high | medium | low
```

Rules: a counterexample must come with the invariant values and their justification (a theorem, a computation you
display, or a named database). Do not invent references. If you use a formula for the signature of a torus knot, a
cable, or a satellite, state it and say where it comes from. Partial results are welcome, as long as the hypotheses
are stated exactly.


---

## Prompt C — fresh pass for a third model (o2)

You are the third model to see this note (LaTeX source below). Two earlier passes are already folded into it, and their
contributions are marked in the text: one checked the proof and found six gaps, all now repaired; one contributed the
mod 4 congruence of Section 5, the one-bridge braid family in the table of Section 3, and the rigidity observation in
Section 7. Everything both of them computed was reproduced independently by the authors.

Do not redo their work. Two things are wanted from you.

**1. Errors.** Read the proof of Lemma 1 and of Theorem 1 as a referee would. Lemma 1 is not a citation: it is proved
here from the lattice count, and the whole induction rests on it. State any error with the exact claim and a
counterexample or a corrected statement. If a step is true but unjustified, say so separately.

**2. The open case.** Conjecture 1 is open for hyperbolic L-space knots, which is where equality occurs. Prove it,
refute it, or reduce it. Useful facts already established, so you do not repeat them: a counterexample needs
det >= |sigma| + 5 (Section 5); the conjecture restricted to Alexander polynomial Delta_{T(2,2g+1)} is a definiteness
statement and a weak form of Problem 1.21(c)(i) of the K3 list (Section 7); the cabling induction fails for hyperbolic
knots because no half-conductor is available (Section 7); no counterexample exists in 12,702 L-space knots computed.

Also say, if you know: is the inequality itself in the literature, and is the definiteness statement of Section 7 open
or a consequence of a known detection theorem?

Answer in this form:

```
errors: <numbered, or "none found", with what you checked>
open case: PROVED | REFUTED | PARTIAL | NO PROGRESS
argument: <proof, counterexample with all invariant values and how each is known, or the partial result with exact hypotheses>
literature: <references you are confident exist, or "none found">
confidence: high | medium | low, and what you did not check
```

Do not invent references. If you use a formula for a signature, a determinant, or a cable, state it and its source.


---

## Prompt D — one question: definiteness (single task)

One mathematical question. Do not review the note, do not re-verify its computations; it is attached only as
background, and its Sections 1, 4 and 7 are the relevant ones.

**Question.** Let K be an L-space knot in S^3 of genus g whose Alexander polynomial equals that of the torus knot
T(2,2g+1), that is Delta_K(t) = sum_{k=0}^{2g} (-1)^k t^{g-k}. Prove or refute: sigma(K) = -2g, equivalently the
symmetrised Seifert form V + V^T is definite.

Why this and nothing else: it is the sharp case of the note's Conjecture 1, which implies it, and it is the smallest
piece of that conjecture not covered by the note's Theorem 1. A proof would remove the main obstacle to proving the
conjecture in general; a counterexample would refute the conjecture outright.

What is available:

- An L-space knot is fibered and strongly quasipositive with g = g_4 = tau, and its Alexander polynomial has
  coefficients +-1 with alternating signs (Ozsvath-Szabo, Ni, Hedden). For any knot |sigma| <= 2g, so the question is
  whether the maximum is attained.
- Under the hypothesis, the knot Floer complex is the staircase of T(2,2g+1), det(K) = 2g+1, and in the gap language of
  the note all g gaps are odd.
- sigma is not determined by the Alexander polynomial in general, not even for fibered knots, so the content of the
  question is whether the L-space condition forces the signature here.
- For g = 1 and g = 2 the answer is yes, because knot Floer homology detects T(2,3) (Ghiggini) and T(2,5)
  (Farber-Reinoso-Wang), so K is the torus knot itself. For g >= 3, that detection statement is Problem 1.21(c)(i) of
  the K3 problem list and is open. The question asked here is weaker than detection: it asks only for the signature.
- Computational status, and this matters: among 11,728 L-space iterated torus knots, all 632 census L-space knots, 274
  one-bridge braids and 68 knots of the Baker-Kegel and Himeno families, every knot satisfying the hypothesis is
  T(2,2g+1) itself. So there is no non-trivial test data, and any counterexample would also refute detection.

Directions, not requirements: the Seifert form of a fibered knot has unimodular V, so det(V + V^T) = +-det(I + h) for
the monodromy h; the branched double cover has H_1 = Z/(2g+1), which connects to A. Moore's conjecture (K3 Problem
1.22) that Sigma_2 of a hyperbolic L-space knot is not an L-space; Boileau, Boyer and Gordon classify definite strongly
quasipositive links and relate them to L-space branched covers; the Upsilon function of an L-space knot is determined
by its Alexander polynomial (Borodzik-Livingston), which the signature is not.

Note on provenance, since it may affect how much you trust the surrounding material: the note has been read by three
language models from two AI labs. The first checked the proof and found six gaps, all repaired. The second contributed
the mod 4 congruence, the one-bridge braid family and the rigidity observation that led to this question. The third
corrected an error in the statement of Lemma 1 (an equivalence that is only a sufficient condition). None of the three
made progress on the question asked here, and none found the inequality in the literature.

Answer in this form:

```
outcome: PROVED | REFUTED | PARTIAL | NO PROGRESS | KNOWN
statement: <exact statement you proved or refuted, with hypotheses>
argument: <complete proof; or a counterexample with all invariant values and how each is known; or the partial result>
what remains: <precisely what is still open>
references: <only sources you are confident exist, with the exact result used>
confidence: high | medium | low, and what you did not check
```

Do not invent references. If you use a formula or a detection theorem, state it and its source. If you conclude the
question is equivalent to, or strictly harder than, a known open problem, say which and why.


---

## Prompt E — next model, after four passes

Use this only if a fifth model is wanted before a person. It is Prompt D with the state updated; the question is the
same, and the point of the extra paragraph is to stop the model repeating four dead ends.

Four language models from two AI labs have read the note. Between them they: verified every computation
independently; found six presentational gaps and one real error (an equivalence in Lemma 1 that is only a sufficient
condition), all repaired; contributed the mod 4 congruence, the one-bridge braid family, and the reduction of the
sharp case to a definiteness statement; excluded cables from that sharp case; and reformulated it as the vanishing of
the positive Levine-Tristram jumps. None proved or refuted anything, and none found the inequality in the literature.

What is therefore already known about a counterexample in the sharp case: it is not a cable, it is not braid positive
(the definite positive braid knots in our data are the T(2,n) together with T(3,4) and T(3,5), the knots among the ADE
singularity links, and neither of the last two has the Alexander polynomial of a T(2,2g+1)), and it must have a
positive Levine-Tristram jump at one of the g roots of Delta on the upper half circle. It would have to be hyperbolic
or a satellite with a non-cable pattern.

Answer the question of Prompt D in the same format. If your best contribution is to identify which known theorem
settles it, that is a full answer; say which and quote it.
