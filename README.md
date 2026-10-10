# An inequality between determinant and signature for L-space knots

For every L-space knot `K`, is

    det(K) ≤ 1 + |σ(K)| ?

This repository holds the note, its proof for iterated torus knots, the computations behind it, and a
Lean 4 formalisation of the one lemma proved here from scratch. A second statement, `u(K) = g(K)` for
L-space knots, has its own short note (`note/k32.pdf`).

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
* **Baker-Kegel family.** For their hyperbolic L-space knots `K_k`, their formula for the Alexander polynomial is
  that of the (2,4k+5)-cable of T(2,2k+1), so `det(K_k) = 4k+5` for every k (rechecked by exact Burau recurrences). `σ(K_k) = -(4k+4)`
  is computed for k ≤ 60, so equality holds there, as it does for the cable.
* **Unknotting number (second note).** `u = g_4` for a two-parameter family of closed braids that contains the
  Baker-Kegel and Himeno knots, by an explicit unknotting. So `u = g` holds for both families, including the
  knots that are provably not braid positive. Fibered and strongly quasipositive is not enough: as Bode and Truöl
  observe, the mirror of 12n_642 has `g = 2` and `u ≥ 3`.
* **Open.** The hyperbolic case of the inequality, where it is sharp, and `u = g` for L-space knots in general.
  The signature of an L-space knot is not determined by its knot Floer complex (T(3,4) and the (2,3)-cable of
  the trefoil), so the inequality is not a statement about knot Floer homology alone.

## Layout

    note/           the notes (k33.tex/pdf on the inequality, k32.tex/pdf on u = g), their generators, proof.md
    verification/   every computation, each writing the JSON or JSONL its numbers are read from
    verification/k32/       earlier unknotting searches for u = g
    verification/families/  the family H(n,m) (Baker-Kegel, Himeno), the u = g proof checks, 12n_642
    lean/           the Lean 4 formalisation of the lattice inequality
    pictures/       diagrams of the knots that appear in the note

Every number in the notes is substituted from a result file by `note/make_tex.py` and `note/make_k32.py`.
None is typed by hand.

## Reproducing

The Python and Sage scripts are independent of each other and each writes its own result file. Tools:
SnapPy 3.3.2 with `knot_floer_homology`, Sage 10.7, khoca 1.5.

    python3 verification/iterated.py            # L-space iterated torus knots, exact formulas
    python3 verification/lemma_L.py             # every step of the lattice lemma
    python3 verification/twisted_torus.py       # the twisted torus family, via knot Floer homology
    sage   verification/twisted_torus_sigma.sage    # its exact signatures, and the check
    python3 verification/random_lspace.py       # a random search for L-space knots
    sage   verification/random_lspace_sigma.sage    # its exact signatures, and the check
    python3 verification/congruence.py          # the mod 4 congruence, on everything computed
    python3 verification/definiteness.py        # the sharp case across all families
    python3 verification/distinct_knots.py      # distinct knots per generated family, and census lookup
    python3 verification/k32/twisted_torus_ug.py    # unknotting certificates for u = g (earlier search)
    sage   verification/families/bk_det.sage         # det(K_k) = 4k+5 for every k
    sage   verification/families/bk_alex.sage        # Delta(K_k) = Delta of the cable, for every k
    python3 verification/families/unknotting.py 12  # the explicit unknotting of H(n,m), n <= 12
    python3 verification/families/cables.py 8       # the non-positive L-space (2,q)-cables
    python3 verification/families/fibered_sqp.py    # 12n_642: fibered, SQP, u >= 3
    python3 verification/families/lspace.py         # which H(n,m) are L-space knots, and their volumes
    python3 verification/families/seifert_dump.py && sage verification/families/signatures.sage
    python3 verification/families/alex_inputs.py BK_BRAIDS && sage verification/families/sigma_by_alex.sage

`note/make_tex.py` and `note/make_k32.py` regenerate `note/k33.tex` and `note/k32.tex` from the result
files, and two `pdflatex` passes give each PDF. The families scripts run from their own directory. `note/make_prompts.py` inlines the note into the review prompts in `PROMPTS.md`; its output is
generated and not tracked.

For the Lean part, see `lean/README.md`: it needs a Mathlib build at the pinned revision, and on a
machine with several Lean projects that build should be shared rather than repeated.

## Data that is not here

Two things were deliberately left out; see `DATA.md` for the detail.

* The braid words for the 632 census L-space knots, which are Baker and Kegel's published table. The
  scripts that use them say where to get them.
* KnotInfo itself. The note cites KnotInfo as the source of the candidate and follows its sign
  conventions; its maintainers ask that the database not be reposted, so it is read from
  https://knotinfo.org rather than copied here.

## Licence

Apache-2.0, in `LICENSE`.
