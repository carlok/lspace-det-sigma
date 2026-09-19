"""An unbiased search for L-space knots, as a check on K33 and K32 that carries no family bias.

Every test so far picked a family first: the census, one-bridge braids, iterated torus knots,
Baker-Kegel, Himeno, twisted torus knots. A statement can survive all of them and still fail on an
L-space knot nobody thought to parametrise. This instead generates random braid words, closes them, and
keeps whatever knot Floer homology calls an L-space knot. The sample is whatever the generator reaches,
not a family.

On Berge knots specifically, which would be the other natural family: Berge types I and II are torus
knots and types III to VI are the Berge-Gabai knots, the 1-bridge braids in a solid torus, and by
Greene-Lewallen-Vafaee the (1,1) L-space knots are exactly the 1-bridge braids. Those 274 are already in
the table of the note. What is left, types VII to XII, sits in the fibre surface of the trefoil and the
figure-eight and in sporadic families, and generating them needs machinery this project does not have.
An unbiased search reaches whichever of them happen to be small, without having to parametrise any.

Writes the knots and everything knot Floer homology gives, including the determinant read off the
Alexander polynomial. Signatures come afterwards from Sage, as for the twisted torus family.

Single process, nice, bounded by --minutes.
"""
import argparse
import json
import random
import time
from pathlib import Path

import snappy
from knot_floer_homology import pd_to_hfk

HERE = Path(__file__).parent


def determinant_from_hfk(hfk):
    """|Delta(-1)| for an L-space knot, from the Alexander gradings of its knot Floer homology."""
    gradings = sorted({int(a) for a, _ in hfk["ranks"]}, reverse=True)
    sign = lambda k: 1 if k % 2 == 0 else -1
    return abs(sum(sign(i) * sign(a) for i, a in enumerate(gradings)))


def random_word(rng, strands, length, negative_rate):
    """A random braid word. Mostly positive: L-space knots are strongly quasipositive, so a word with
    many negative letters almost never closes to one, and the search would spend its time on misses."""
    w = []
    for _ in range(length):
        g = rng.randrange(1, strands)
        w.append(-g if rng.random() < negative_rate else g)
    return w


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=30.0)
    ap.add_argument("--seed", type=int, default=20260919)
    ap.add_argument("--max-crossings", type=int, default=24)
    a = ap.parse_args()

    rng = random.Random(a.seed)
    deadline = time.time() + 60 * a.minutes
    out = open(HERE / "random_lspace.jsonl", "w")
    seen = set()
    tried = knots = lspace = 0

    while time.time() < deadline:
        tried += 1
        strands = rng.randrange(3, 8)
        length = rng.randrange(strands + 2, 3 * strands + 10)
        w = random_word(rng, strands, length, rng.choice([0.0, 0.0, 0.05, 0.12]))
        try:
            K = snappy.Link(braid_closure=w)
            if len(K.link_components) != 1:
                continue
            K.simplify("global")
            if not 3 <= len(K.crossings) <= a.max_crossings:
                continue
            pd = K.PD_code(KnotTheory=True)
            if pd in seen:
                continue
            seen.add(pd)
            hfk = pd_to_hfk(pd)
        except Exception:
            continue
        knots += 1
        if not hfk.get("L_space_knot"):
            continue
        lspace += 1
        rec = {"name": f"random-{lspace}", "braid_word": w, "crossings": len(K.crossings),
               "braid_positive_word": all(x > 0 for x in w),
               "genus": int(hfk["seifert_genus"]), "tau": int(hfk["tau"]),
               "fibered": bool(hfk["fibered"]), "det": determinant_from_hfk(hfk)}
        try:
            M = K.exterior()
            rec["solution_type"] = M.solution_type()
            rec["volume"] = float(M.volume())
            rec["hyperbolic"] = bool(M.solution_type() == "all tetrahedra positively oriented"
                                     and M.volume() > 0.9)
        except Exception:
            rec["hyperbolic"] = None
        out.write(json.dumps(rec) + "\n")
        out.flush()
        print(f"  {rec['name']:<12} c={rec['crossings']:3d} g={rec['genus']:3d} det={rec['det']:5d} "
              f"hyp={rec['hyperbolic']} positive={rec['braid_positive_word']}", flush=True)

    summary = {"candidate": "K33 and K32", "method": "random braid words, closed, filtered by the "
                                                     "L_space_knot flag of knot Floer homology",
               "seed": a.seed, "minutes": a.minutes, "words_tried": tried,
               "distinct_knots": knots, "l_space_knots": lspace}
    (HERE / "random_lspace_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\n{tried} words, {knots} distinct knots, {lspace} L-space knots")


if __name__ == "__main__":
    main()
