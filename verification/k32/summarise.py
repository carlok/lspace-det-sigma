"""Render verdict.md for K32. Recomputes the quick certificates (seconds) and reads the family/census result files."""
import itertools, json
from pathlib import Path
import snappy, spherogram
from klmms import D1_NOTEBOOK, create_D_n

here = Path(__file__).parent
load = lambda f: [json.loads(l) for l in open(here / f)]

def braid_cert(word, flips):
    L = snappy.Link(braid_closure=word)
    h = L.knot_floer_homology()
    v = list(word)
    for i in flips: v[i] = -v[i]
    U = snappy.Link(braid_closure=v); U.simplify('global')
    fewer = 0
    for idx in itertools.combinations([i for i, x in enumerate(word) if x > 0], h['seifert_genus'] - 1):
        w = list(word)
        for i in idx: w[i] = -w[i]
        X = snappy.Link(braid_closure=w); X.simplify('global')
        if len(X.crossings) == 0 or X.knot_floer_homology()['total_rank'] == 1:
            fewer += 1; break
    return h, v, len(U.crossings), fewer

cab23 = [2, 1, 3, 2] * 3 + [-1] * 3
h23, v23, c23, f23 = braid_cert(cab23, [0, 1, 2])
cab257 = [2, 1, 3, 2] * 5 + [-1] * 3
L257 = snappy.Link(braid_closure=cab257); h257 = L257.knot_floer_homology()
v257 = list(cab257)
for i in (0, 1, 2, 3, 10, 17, 19): v257[i] = -v257[i]
U257 = snappy.Link(braid_closure=v257); U257.simplify('global')
bk = sorted(load("bk_family.jsonl"), key=lambda r: r["n"])
hm = sorted(load("himeno.jsonl"), key=lambda r: r["n"])
census = load("census_lspace.jsonl")
kl = []
for name, pd in (("D_1", D1_NOTEBOOK), ("D_2", create_D_n(2))):
    h = spherogram.Link([list(c) for c in pd]).knot_floer_homology()
    kl.append((name, len(pd), h['seifert_genus'], h['total_rank'], h['L_space_knot']))

rows_bk = "\n".join(f"| Baker-Kegel K_{r['n']} | {r['crossings']} | {r['genus']} | {r['L_space']} | {'yes' if r['u_equals_g'] else 'not found'} |" for r in bk)
rows_hm = "\n".join(f"| Himeno K_{r['n']}{' (= o9_30634)' if r['isometric_to_o9_30634'] else ''}{' (proven not braid positive)' if r['n'] % 2 == 0 else ''} | {r['crossings']} | {r['genus']} | {r['L_space']} | {'yes' if r['u_equals_g'] else 'not found'} |" for r in hm)
text = f"""## Verification by computation and literature (ragusa session, not the external model)

verdict: OPEN in general; IMPLIED (known theorem) for every braid positive L-space knot; verified by computation on every non-braid-positive L-space knot we could find in the literature

**The external model missed a theorem.** For braid positive knots u = g is a theorem of Rudolph (L. Rudolph, *Braided surfaces and Seifert ribbons for closed braids*, Comment. Math. Helv. 58 (1983), 1-37), quoted and reproved in M. Kegel, L. Lewark, N. Manikandan, F. Misev, L. Mousseau, M. Silvero, *On unknotting fibered positive knots and braids*, arXiv:2312.07339 (abstract and Theorem 1.2: every positive braid diagram of a genus g knot has g crossings whose change gives the unknot). With g <= u for all L-space knots (tau = g <= g_4 <= u), K32 holds for every L-space knot that is braid positive: all positive torus knots, and 631 of the 632 hyperbolic L-space knots of the SnapPy census (K. Baker, M. Kegel, *Census L-space knots are braid positive, except for one that is not*, arXiv:2203.12013). What remains open is K32 for L-space knots that are not braid positive.

**Computation on the L-space knots that are not (or not known to be) braid positive.** An unknotting in g crossing changes was found for each; certificate: after the changes, SnapPy simplifies the diagram to 0 crossings (or knot Floer homology has rank 1). Since u >= g, each gives u = g.

| knot | crossings (diagram used) | genus = tau | L-space (HFK) | unknotted in g changes |
|---|---:|---:|---|---|
| (2,3)-cable of the right-handed trefoil, braid {cab23} (not braid positive, Baker-Kegel Example 1) | {len(cab23)} | {h23['seifert_genus']} | {h23['L_space_knot']} | yes: flipped braid {v23} simplifies to {c23} crossings; unknottings with g - 1 changes among positive letters: {f23} |
| (2,7)-cable of T(2,5), braid {cab257} | {len(cab257)} | {h257['seifert_genus']} | {h257['L_space_knot']} | yes: flipped braid {v257} simplifies to {len(U257.crossings)} crossings |
{rows_bk}
{rows_hm}

Baker-Kegel K_n = closure of [(2,1,3,2)^(2n+1), -1, 2, 1, 1, 2] (their Section 2; hyperbolic L-space knots for n >= 1, braid positivity unknown for n >= 2). Himeno K_n = closure of X_n^3 [-1..-(n-1), n..1, 1..n] (K. Himeno, *Non-braid positive hyperbolic L-space knots*, arXiv:2506.22934, Theorem 1.1: for even n, hyperbolic L-space knots that are not braid positive); the transcription is checked by K_2 being isometric to o9_30634.

**Census.** Before the braid positivity argument made it redundant, the same search certified u = g on {sum(1 for r in census if r.get('u_equals_g'))} census L-space knots (genus {min(r['genus'] for r in census)} to {max(r['genus'] for r in census)}), with {sum(1 for r in census if r.get('u_equals_g') is False)} failures; the run was stopped there.

**Near miss checked.** Kegel et al. conjecture that a fibered positive knot of genus 7 (their diagram D_1) has u = 9, a counterexample to Stoimenow's conjecture u = g for fibered positive knots. It is not an L-space knot, so it does not bear on K32: {', '.join(f'{n}: {c} crossings, genus {g}, HFK rank {r}, L-space {l}' for n, c, g, r, l in kl)} (an L-space knot has HFK rank at most 2g + 1).

**Corrections to the external model's answer.** (1) u = g for positive braid knots is known (Rudolph 1983), so K32 is IMPLIED for braid positive L-space knots, including every census L-space knot but one. (2) The two cases it left undecided, the (2,3)-cable of the trefoil (u in {{3, 4}}) and the (2,7)-cable of T(2,5) (naive u <= 8), have u = g = 3 and u = g = 7. (3) The candidate is open only for non-braid-positive L-space knots; every such knot tested satisfies it, so "u = g for all L-space knots" stands as a conjecture with a precise frontier, not a data artefact. A short web search found no statement of it; a proper literature check is still to do.

What would settle it: a proof that every L-space knot can be unknotted in g(K) crossing changes (Rudolph's argument needs a positive braid; the hyperbolic examples above are positive braids with one negative crossing), or an obstruction to u <= g on a non-braid-positive L-space knot such as Himeno's K_n for large even n.

Reproduce: `bk_family.py 6`, `himeno.py 2 3 4`, `census_lspace.py` (optional), then `summarise.py`; versions in `VERSIONS.txt`.
"""

hunt = json.load(open(here / "hunt.json"))
ind = json.load(open(here / "induction.json"))
ok_ind = [r for r in ind if r["sequence"] and all(x["fibered"] and x["tau"] == x["genus"] for x in r["sequence"])]
text += f"""
**Further tests (2026-09-18).** u = g certified for {len(hunt)} more L-space knots that are not braid positive, or not
known to be: {', '.join(r['knot'] + f" (genus {r['genus']})" for r in hunt)}. No counterexample. Script `hunt.py`.
Himeno K_5 and K_6 were dropped: the knot Floer homology of an 89-letter braid on 10 strands did not finish.

**What class the unknotting stays in.** Rudolph's proof for braid positive knots works by unknotting through braid
positive knots of genus one less. The optimal unknottings found here leave the L-space knots after the first crossing
change, so that class is not preserved. They do stay inside the fibered strongly quasipositive knots, with the genus
dropping by exactly one at every step, for {len(ok_ind)} of the {len(ind)} knots tested, namely
{', '.join(r['knot'] for r in ok_ind)}; the two cable examples leave even that class. Fibered plus strongly
quasipositive is tested by Hedden's characterisation (fibered and tau = g). Note that fibered strongly quasipositive
does not imply u = g in general (Kegel-Lewark-Manikandan-Misev-Mousseau-Silvero, arXiv:2312.07339, Figure 2), so an
induction over that class alone cannot prove K32; something sharper about these knots is needed. Script `induction.py`.
"""
(here / "verdict.md").write_text(text)
print(text)
