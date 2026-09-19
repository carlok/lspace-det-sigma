"""Twisted torus knots as a new test family for K33 (det <= 1 - sigma) and K32 (u = g).

Nothing checked so far covers them. The families already tested are the SnapPy census (632), one-bridge
braids (274), iterated torus knots (11,728) and the Baker-Kegel and Himeno families. Twisted torus knots
with *negative* twisting are the interesting case: they are not braid positive, and the open region for
both statements is exactly the hyperbolic, non-braid-positive L-space knots.

  K(p, q; r, s) = closure of (s_1 s_2 ... s_{p-1})^q (s_1 ... s_{r-1})^s   on p strands.

s > 0 gives a positive braid; s < 0 does not, and that is the half worth having.

L-space-ness is decided computationally, by the `L_space_knot` flag of knot Floer homology, rather than
by citing a classification. That also makes the family self-certifying: a knot enters the sample only if
its own HFK says it is an L-space knot.

This stage writes the knots and everything HFK gives, including the determinant, which for an L-space
knot is read off the Alexander polynomial: every HFK group has rank one and the signs alternate, so
det = |sum_i (-1)^i (-1)^{a_i}| over the Alexander gradings a_0 > a_1 > ... The signature needs a Seifert
matrix, so it is computed in Sage by twisted_torus_sigma.sage, which reads this file's output.

Single process, nice, bounded by --minutes.
"""
import argparse
import json
import time
from math import gcd
from pathlib import Path

import snappy
from knot_floer_homology import pd_to_hfk

HERE = Path(__file__).parent


def braid_word(p, q, r, s):
    """(s_1 ... s_{p-1})^q (s_1 ... s_{r-1})^s as a list of signed generator indices."""
    full = list(range(1, p))
    part = list(range(1, r))
    tail = part * s if s > 0 else [-x for x in reversed(part)] * (-s)
    return full * q + tail


def determinant_from_hfk(hfk):
    """|Delta(-1)| for an L-space knot, from the Alexander gradings of its HFK."""
    gradings = sorted({int(a) for a, _ in hfk["ranks"]}, reverse=True)
    # (-1)**a with a negative would be a float; the parity is all that matters
    sign = lambda k: 1 if k % 2 == 0 else -1
    return abs(sum(sign(i) * sign(a) for i, a in enumerate(gradings)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=40.0)
    ap.add_argument("--max-p", type=int, default=7)
    ap.add_argument("--max-q", type=int, default=9)
    ap.add_argument("--max-s", type=int, default=6)
    ap.add_argument("--max-braid", type=int, default=44)
    a = ap.parse_args()

    deadline = time.time() + 60 * a.minutes
    out = open(HERE / "twisted_torus.jsonl", "w")
    seen = set()
    n_built = n_lspace = n_neg = 0

    params = [(p, q, r, s)
              for p in range(3, a.max_p + 1)
              for q in range(2, a.max_q + 1)
              for r in range(2, p + 1)
              for s in list(range(-a.max_s, 0)) + list(range(1, a.max_s + 1))]
    params.sort(key=lambda t: len(braid_word(*t)))          # cheapest first

    for p, q, r, s in params:
        if time.time() > deadline:
            break
        w = braid_word(p, q, r, s)
        if len(w) > a.max_braid:
            continue
        try:
            K = snappy.Link(braid_closure=w)
            if len(K.link_components) != 1:
                continue
            K.simplify("global")
            if not K.crossings:
                continue
            pd = K.PD_code(KnotTheory=True)
            if pd in seen:
                continue
            seen.add(pd)
            hfk = pd_to_hfk(pd)
        except Exception as e:
            out.write(json.dumps({"p": p, "q": q, "r": r, "s": s, "error": str(e)[:150]}) + "\n")
            continue
        n_built += 1
        if not hfk.get("L_space_knot"):
            continue
        n_lspace += 1
        n_neg += s < 0
        rec = {"name": f"K({p},{q};{r},{s})", "p": p, "q": q, "r": r, "s": s,
               "braid_word": w, "strands": p, "crossings": len(K.crossings),
               "braid_positive_word": s > 0,
               "genus": int(hfk["seifert_genus"]), "tau": int(hfk["tau"]),
               "fibered": bool(hfk["fibered"]), "det": determinant_from_hfk(hfk),
               "total_rank": int(hfk["total_rank"])}
        # hyperbolic or not: the open region for K32 and K33 is the hyperbolic L-space knots, so
        # record which of these are genuinely outside the iterated-torus case already proved
        try:
            M = K.exterior()
            rec["solution_type"] = M.solution_type()
            rec["volume"] = float(M.volume())
            rec["hyperbolic"] = bool(M.solution_type() == "all tetrahedra positively oriented"
                                     and M.volume() > 0.9)
        except Exception as e:
            rec["solution_type"] = f"error: {str(e)[:60]}"
            rec["hyperbolic"] = None
        out.write(json.dumps(rec) + "\n")
        out.flush()
        print(f"  {rec['name']:<16} c={rec['crossings']:3d} g={rec['genus']:3d} "
              f"tau={rec['tau']:3d} det={rec['det']:5d} braid_positive={rec['braid_positive_word']}", flush=True)

    summary = {"candidate": "K33 and K32", "family": "twisted torus knots K(p,q;r,s)",
               "parameters": {"p": [3, a.max_p], "q": [2, a.max_q], "r": "2..p",
                              "s": f"-{a.max_s}..{a.max_s}, nonzero", "max_braid_length": a.max_braid},
               "L_space_test": "knot Floer homology L_space_knot flag, not a cited classification",
               "distinct_knots_built": n_built, "l_space_knots": n_lspace,
               "l_space_with_negative_twisting": n_neg, "note": "hyperbolicity recorded per knot"}
    (HERE / "twisted_torus_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\n{n_built} distinct knots built, {n_lspace} are L-space knots, "
          f"{n_neg} of those from a non-positive braid word")


if __name__ == "__main__":
    main()
