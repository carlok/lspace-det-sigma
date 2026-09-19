## Verification by computation and literature (ragusa session, not the external model)

verdict: OPEN in general; IMPLIED (known theorem) for every braid positive L-space knot; verified by computation on every non-braid-positive L-space knot we could find in the literature

**The external model missed a theorem.** For braid positive knots u = g is a theorem of Rudolph (L. Rudolph, *Braided surfaces and Seifert ribbons for closed braids*, Comment. Math. Helv. 58 (1983), 1-37), quoted and reproved in M. Kegel, L. Lewark, N. Manikandan, F. Misev, L. Mousseau, M. Silvero, *On unknotting fibered positive knots and braids*, arXiv:2312.07339 (abstract and Theorem 1.2: every positive braid diagram of a genus g knot has g crossings whose change gives the unknot). With g <= u for all L-space knots (tau = g <= g_4 <= u), K32 holds for every L-space knot that is braid positive: all positive torus knots, and 631 of the 632 hyperbolic L-space knots of the SnapPy census (K. Baker, M. Kegel, *Census L-space knots are braid positive, except for one that is not*, arXiv:2203.12013). What remains open is K32 for L-space knots that are not braid positive.

**Computation on the L-space knots that are not (or not known to be) braid positive.** An unknotting in g crossing changes was found for each; certificate: after the changes, SnapPy simplifies the diagram to 0 crossings (or knot Floer homology has rank 1). Since u >= g, each gives u = g.

| knot | crossings (diagram used) | genus = tau | L-space (HFK) | unknotted in g changes |
|---|---:|---:|---|---|
| (2,3)-cable of the right-handed trefoil, braid [2, 1, 3, 2, 2, 1, 3, 2, 2, 1, 3, 2, -1, -1, -1] (not braid positive, Baker-Kegel Example 1) | 15 | 3 | True | yes: flipped braid [-2, -1, -3, 2, 2, 1, 3, 2, 2, 1, 3, 2, -1, -1, -1] simplifies to 0 crossings; unknottings with g - 1 changes among positive letters: 0 |
| (2,7)-cable of T(2,5), braid [2, 1, 3, 2, 2, 1, 3, 2, 2, 1, 3, 2, 2, 1, 3, 2, 2, 1, 3, 2, -1, -1, -1] | 23 | 7 | True | yes: flipped braid [-2, -1, -3, -2, 2, 1, 3, 2, 2, 1, -3, 2, 2, 1, 3, 2, 2, -1, 3, -2, -1, -1, -1] simplifies to 0 crossings |
| Baker-Kegel K_1 | 17 | 6 | True | yes |
| Baker-Kegel K_2 | 25 | 10 | True | yes |
| Baker-Kegel K_3 | 33 | 14 | True | yes |
| Baker-Kegel K_4 | 41 | 18 | True | yes |
| Baker-Kegel K_5 | 49 | 22 | True | yes |
| Baker-Kegel K_6 | 57 | 26 | True | yes |
| Himeno K_2 (= o9_30634) (proven not braid positive) | 17 | 6 | True | yes |
| Himeno K_3 | 35 | 13 | True | yes |
| Himeno K_4 (proven not braid positive) | 59 | 23 | True | yes |

Baker-Kegel K_n = closure of [(2,1,3,2)^(2n+1), -1, 2, 1, 1, 2] (their Section 2; hyperbolic L-space knots for n >= 1, braid positivity unknown for n >= 2). Himeno K_n = closure of X_n^3 [-1..-(n-1), n..1, 1..n] (K. Himeno, *Non-braid positive hyperbolic L-space knots*, arXiv:2506.22934, Theorem 1.1: for even n, hyperbolic L-space knots that are not braid positive); the transcription is checked by K_2 being isometric to o9_30634.

**Census.** Before the braid positivity argument made it redundant, the same search certified u = g on 59 census L-space knots (genus 5 to 35), with 0 failures; the run was stopped there.

**Near miss checked.** Kegel et al. conjecture that a fibered positive knot of genus 7 (their diagram D_1) has u = 9, a counterexample to Stoimenow's conjecture u = g for fibered positive knots. It is not an L-space knot, so it does not bear on K32: D_1: 24 crossings, genus 7, HFK rank 559, L-space False, D_2: 40 crossings, genus 12, HFK rank 31929, L-space False (an L-space knot has HFK rank at most 2g + 1).

**Corrections to the external model's answer.** (1) u = g for positive braid knots is known (Rudolph 1983), so K32 is IMPLIED for braid positive L-space knots, including every census L-space knot but one. (2) The two cases it left undecided, the (2,3)-cable of the trefoil (u in {3, 4}) and the (2,7)-cable of T(2,5) (naive u <= 8), have u = g = 3 and u = g = 7. (3) The candidate is open only for non-braid-positive L-space knots; every such knot tested satisfies it, so "u = g for all L-space knots" stands as a conjecture with a precise frontier, not a data artefact. A short web search found no statement of it; a proper literature check is still to do.

What would settle it: a proof that every L-space knot can be unknotted in g(K) crossing changes (Rudolph's argument needs a positive braid; the hyperbolic examples above are positive braids with one negative crossing), or an obstruction to u <= g on a non-braid-positive L-space knot such as Himeno's K_n for large even n.

Reproduce: `bk_family.py 6`, `himeno.py 2 3 4`, `census_lspace.py` (optional), then `summarise.py`; versions in `VERSIONS.txt`.

**Further tests (2026-09-18).** u = g certified for 8 more L-space knots that are not braid positive, or not
known to be: Baker-Kegel K_7 (genus 30), Baker-Kegel K_8 (genus 34), Baker-Kegel K_9 (genus 38), Baker-Kegel K_10 (genus 42), (2,7)-cable of T(2,5) (genus 7), (2,11)-cable of T(2,7) (genus 11), (2,15)-cable of T(2,9) (genus 15), (2,19)-cable of T(2,11) (genus 19). No counterexample. Script `hunt.py`.
Himeno K_5 and K_6 were dropped: the knot Floer homology of an 89-letter braid on 10 strands did not finish.

**What class the unknotting stays in.** Rudolph's proof for braid positive knots works by unknotting through braid
positive knots of genus one less. The optimal unknottings found here leave the L-space knots after the first crossing
change, so that class is not preserved. They do stay inside the fibered strongly quasipositive knots, with the genus
dropping by exactly one at every step, for 6 of the 8 knots tested, namely
Baker-Kegel K_1, Baker-Kegel K_2, Baker-Kegel K_3, Baker-Kegel K_4, Himeno K_2, Himeno K_3; the two cable examples leave even that class. Fibered plus strongly
quasipositive is tested by Hedden's characterisation (fibered and tau = g). Note that fibered strongly quasipositive
does not imply u = g in general (Kegel-Lewark-Manikandan-Misev-Mousseau-Silvero, arXiv:2312.07339, Figure 2), so an
induction over that class alone cannot prove K32; something sharper about these knots is needed. Script `induction.py`.
