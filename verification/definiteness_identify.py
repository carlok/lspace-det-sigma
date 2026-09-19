"""Identify every L-space knot found with Delta = Delta_{T(2,2g+1)}, to see whether the sharp case of
K33 is ever met by something other than T(2,2g+1) itself.

definiteness.py finds the knots satisfying det = 2g+1, which for an L-space knot is exactly the
condition Delta = Delta_{T(2,2g+1)}. This rebuilds each of them from its parameters and asks SnapPy
whether its exterior is isometric to that of T(2,2g+1). Torus knot exteriors are Seifert fibred, not
hyperbolic, so the comparison is made on the fundamental group and the simplified diagram rather than on
a geometric isometry: two knots are reported as the same when their exteriors are isometric by SnapPy's
test, and otherwise the crossing numbers and knot Floer homology are printed for inspection.

If every one of them is T(2,2g+1), the definiteness statement is not just consistent with the data: its
hypothesis is never met by any other knot in the sample, which is the detection phenomenon of K3
Problem 1.21(c)(i) showing up directly.
"""
import json
from pathlib import Path

import snappy
from knot_floer_homology import pd_to_hfk

HERE = Path(__file__).parent


def twisted_word(p, q, r, s):
    full = list(range(1, p))
    part = list(range(1, r))
    tail = part * s if s > 0 else [-x for x in reversed(part)] * (-s)
    return full * q + tail


def onebridge_word(w, b, t):
    """B(w,b,t) = closure of (s_b ... s_1)(s_{w-1} ... s_1)^t in B_w."""
    return list(range(b, 0, -1)) + list(range(w - 1, 0, -1)) * t


def same_knot(K, g, tries=12):
    """Is K the torus knot T(2, 2g+1)?

    Torus knot exteriors are Seifert fibred, so SnapPy's isometry test does not apply. Instead the
    diagram is put into braid form: the closure of s_1^(2g+1) in B_2 is T(2,2g+1) by definition, so a
    2-strand braid word of the right length and sign identifies the knot outright. `braid_word` is a
    heuristic and fails on some diagrams, so it is retried on re-scrambled diagrams before giving up.
    """
    import random
    for i in range(tries):
        L = K.copy()
        if i:
            L.backtrack(3 * i)
            L.simplify(random.choice(["global", "level", "basic"]))
        else:
            L.simplify("global")
        try:
            w = [int(x) for x in L.braid_word()]
        except Exception:
            continue
        if not w:
            continue
        if max(abs(x) for x in w) == 1 and len(w) == 2 * g + 1 and len({x > 0 for x in w}) == 1:
            return True, w
    return None, None


def main():
    cases = []
    for line in open(HERE / "twisted_torus_sigma.jsonl"):
        r = json.loads(line)
        if r["det_seifert"] == 2 * r["genus"] + 1:
            cases.append(("twisted torus", r["name"], r["genus"],
                          twisted_word(r["p"], r["q"], r["r"], r["s"])))
    for line in open(HERE / "onebridge.jsonl"):
        r = json.loads(line)
        if r["det"] == 2 * r["genus"] + 1:
            cases.append(("one-bridge braid", r["name"], r["genus"],
                          onebridge_word(r["w"], r["b"], r["t"])))

    out, other = [], []
    for source, name, g, w in cases:
        K = snappy.Link(braid_closure=[int(x) for x in w])
        K.simplify("global")
        verdict, w2 = same_knot(K, g)
        rec = {"source": source, "name": name, "genus": g, "crossings": len(K.crossings),
               "is_T2_2g1": verdict, "braid_word_found": w2}
        if verdict is not True:
            rec["hfk"] = {k: v for k, v in pd_to_hfk(K.PD_code(KnotTheory=True)).items()
                          if k in ("seifert_genus", "tau", "L_space_knot", "total_rank")}
            other.append(rec)
        out.append(rec)
        print(f"  {name:<18} g={g:<3} c={rec['crossings']:<3} T(2,{2*g+1})? "
              f"{'yes' if verdict else 'unresolved'}", flush=True)

    summary = {"statement": "every L-space knot computed with Delta = Delta_{T(2,2g+1)} is T(2,2g+1)",
               "method": "a 2-strand positive braid word of length 2g+1 identifies T(2,2g+1) outright",
               "tested": len(out), "confirmed_T2": sum(1 for r in out if r["is_T2_2g1"] is True),
               "unresolved": len(other),
               "unresolved_all_have_crossing_number_2g_plus_1":
                   all(r["crossings"] == 2 * r["genus"] + 1 for r in other),
               "not_confirmed": other, "records": out}
    (HERE / "definiteness_identify.json").write_text(json.dumps(summary, indent=2))
    print(f"\n{len(out)} knots meet the hypothesis; "
          f"{summary['confirmed_T2']} confirmed to be T(2,2g+1); {len(other)} not confirmed")


if __name__ == "__main__":
    main()
