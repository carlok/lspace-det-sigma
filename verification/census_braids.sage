"""K33 on the 632 census L-space knots from Baker-Kegel's braid words (arXiv:2203.12013, Appendix), one process.
For a sample of 25 the closure is checked to be isometric to the named census manifold."""
import sys, json, random
from pathlib import Path
sys.path.append(sys.argv[1])
import snappy
words = json.load(open("bk_census_braids.json"))
done = {json.loads(l)["name"] for l in open("census_braids.jsonl")} if Path("census_braids.jsonl").exists() else set()
out = open("census_braids.jsonl", "a")
random.seed(int(0)); sample = set(random.sample(sorted(words), int(25)))
bad = 0
for name, w in sorted(words.items()):
    if name in done: continue
    L = snappy.Link(braid_closure=w); L.simplify('global')
    cs = [c for c in L.alexander_polynomial().coefficients(sparse=False) if c != 0]
    if not (all(abs(c) == 1 for c in cs) and all(cs[i] == -cs[i + 1] for i in range(len(cs) - 1))):
        out.write(json.dumps(dict(source="census (Baker-Kegel braids)", name=name, L_space=False, reason="Alexander polynomial not of L-space form")) + "\n"); out.flush(); continue
    h = L.knot_floer_homology()
    sig, det = int(L.signature()), int(L.determinant())
    tau = int(h['tau']); sign = int(1) if tau > int(0) else int(-1)
    bound = int(1) - sign * sig
    r = dict(source="census (Baker-Kegel braids)", name=name, L_space=bool(h['L_space_knot']), genus=int(h['seifert_genus']), tau=tau,
             signature=sig, det=det, bound=bound, holds=bool(det <= bound))
    if name in sample:
        r["isometric_to_census"] = bool(L.exterior().is_isometric_to(snappy.Manifold(name)))
    out.write(json.dumps(r) + "\n"); out.flush()
    bad += r["L_space"] and not r["holds"]
print("done", len(words), "knots; violations among L-space knots", bad, flush=True)
