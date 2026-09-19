"""K32 (u = g for L-space knots) on the twisted torus family, which nothing tested so far covers.

The knots and their L-space-ness come from K33/verification/twisted_torus.jsonl, where the decision is
made by the `L_space_knot` flag of knot Floer homology rather than by a cited classification. The ones
worth the compute are those whose braid word is not positive: for a braid positive L-space knot, u = g
is Rudolph's theorem and there is nothing to test.

u >= g holds for every L-space knot, since u >= g_4 = g there. So the whole question is u <= g, and the
certificate is an explicit unknotting in g steps. `dfs` from census_lspace.py does the search: at each
step it changes a crossing of the sign of tau and keeps only the changes that lower |tau| by exactly 1,
which is necessary for an unknotting of length |tau|. Reaching HFK rank 1 certifies u = g; running out of
time certifies nothing, and is reported as such.

Single process, nice, with a per-knot time cap.
"""
import argparse
import json
import time
from pathlib import Path

import snappy
from census_lspace import dfs

HERE = Path(__file__).parent
SOURCE = HERE.parents[1] / "K33" / "verification" / "twisted_torus.jsonl"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--minutes", type=float, default=35.0)
    ap.add_argument("--per-knot", type=float, default=180.0, help="seconds per knot")
    ap.add_argument("--max-genus", type=int, default=12)
    ap.add_argument("--include-positive", action="store_true",
                    help="also test braid positive words, where Rudolph already gives u = g")
    a = ap.parse_args()

    records = [json.loads(l) for l in open(SOURCE) if '"error"' not in l]
    todo = [r for r in records
            if (a.include_positive or not r["braid_positive_word"]) and r["genus"] <= a.max_genus]
    todo.sort(key=lambda r: (r["genus"], r["crossings"]))
    print(f"{len(records)} L-space twisted torus knots, {len(todo)} to test "
          f"(genus <= {a.max_genus}, non-positive braid word only: {not a.include_positive})")

    deadline = time.time() + 60 * a.minutes
    out = open(HERE / "twisted_torus_ug.jsonl", "w")
    certified = attempted = failed = 0
    for r in todo:
        if time.time() > deadline:
            break
        try:
            L = snappy.Link(braid_closure=[int(x) for x in r["braid_word"]])
            L.simplify("global")
            pd = [list(map(int, c)) for c in L.PD_code()]
            h = L.knot_floer_homology()
            g, tau = int(h["seifert_genus"]), int(h["tau"])
            t0 = time.time()
            path = dfs(pd, tau, g, min(time.time() + a.per_knot, deadline))
            rec = {"name": r["name"], "genus": g, "tau": tau, "crossings": len(pd),
                   "braid_positive_word": r["braid_positive_word"],
                   "hyperbolic": r.get("hyperbolic"), "det": r["det"],
                   "u_equals_g": path is not None, "steps": None if path is None else len(path),
                   "seconds": round(time.time() - t0, 1)}
        except Exception as e:
            rec = {"name": r["name"], "error": str(e)[:150]}
        attempted += 1
        certified += bool(rec.get("u_equals_g"))
        failed += rec.get("u_equals_g") is False
        out.write(json.dumps(rec) + "\n")
        out.flush()
        print(f"  {rec['name']:<16} g={rec.get('genus','?'):>3} "
              f"{'u = g CERTIFIED' if rec.get('u_equals_g') else 'not certified in the time cap'} "
              f"({rec.get('seconds','-')}s)", flush=True)

    summary = {"candidate": "K32", "statement": "For every prime knot that is l space: g = u.",
               "family": "twisted torus knots K(p,q;r,s), L-space knots, non-positive braid word",
               "source": str(SOURCE.name), "per_knot_seconds": a.per_knot, "max_genus": a.max_genus,
               "attempted": attempted, "u_equals_g_certified": certified,
               "not_certified_in_time": failed, "counterexamples": 0,
               "note": "u >= g is automatic for L-space knots; failure to certify u <= g within the cap "
                       "is a search failure, not a counterexample"}
    (HERE / "twisted_torus_ug_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"\n{attempted} attempted, {certified} certified u = g, {failed} not certified in the cap")


if __name__ == "__main__":
    main()
