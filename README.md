# An inequality between determinant and signature for L-space knots

For every L-space knot `K`, is

    det(K) ≤ 1 + |σ(K)| ?

This repository holds the note, its proof for iterated torus knots, the computations behind it, and a
Lean 4 formalisation of the one lemma proved here from scratch. A second statement, `u(K) = g(K)` for
L-space knots, is carried along with the same evidence.

The statement was produced by a program that fits linear inequalities to a table of knot invariants and
discards the ones its own checks refute. It survived those checks, and then survived everything below.
It is a conjecture, not a theorem, except where stated.

## What is proved

* **Theorem.** The inequality holds for every L-space knot that is an iterated torus knot, in particular
  for every algebraic knot. The proof is an induction over cabling using Litherland's formula and the
  bound `|σ(T(p,q))| ≥ g(T(p,q))`, which is proved here from the lattice count for torus knot signatures.
* **Machine-checked.** The combinatorial core of that lemma — `N_< ≤ (p-1)(q-1)/8` for all integers
  `2 ≤ p < q` — is formalised in Lean 4 against Mathlib in `lean/`, with no `sorry`. `#print axioms`
  reports only `propext`, `Classical.choice` and `Quot.sound`.
* **Open.** The hyperbolic case. That is also where the inequality is sharp.

## Layout

    note/           the note (k33.tex, k33.pdf), its generator, and proof.md
    verification/   every computation, each writing the JSON or JSONL its numbers are read from
    verification/k32/  the same for u = g
    lean/           the Lean 4 formalisation of the lattice inequality
    pictures/       diagrams of the knots that appear in the note

Every number in the note is substituted from a result file by `note/make_tex.py`. None is typed by hand.

## Reproducing

The Python and Sage scripts are independent of each other and each writes its own result file. Tools:
SnapPy 3.3.2 with `knot_floer_homology`, Sage 10.7, khoca 1.5.

    python3 verification/iterated.py            # L-space iterated torus knots, exact formulas
    python3 verification/lemma_L.py             # every step of the lattice lemma
    python3 verification/twisted_torus.py       # the twisted torus family, via knot Floer homology
    sage   verification/twisted_torus_sigma.sage    # its exact signatures, and the check
    python3 verification/random_lspace.py       # an unbiased search for L-space knots
    sage   verification/random_lspace_sigma.sage    # its exact signatures, and the check
    python3 verification/congruence.py          # the mod 4 congruence, on everything computed
    python3 verification/definiteness.py        # the sharp case across all families

For the Lean part, see `lean/README.md`: it needs a Mathlib build at the pinned revision, and on a
machine with several Lean projects that build should be shared rather than repeated.

## Data that is not here

Two things were deliberately left out; see `DATA.md` for the detail.

* The braid words for the 632 census L-space knots, which are Baker and Kegel's published table. The
  scripts that use them say where to get them.
* Anything derived from KnotInfo. The note names KnotInfo as the source of the candidate and follows its
  sign conventions, and reproduces none of its data.

## Licence

Apache-2.0, in `LICENSE`.
