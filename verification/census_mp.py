"""K33 on SnapPy census knots in one process with a fork pool (run with `sage -python census_mp.py <snappy site-packages>`).
Resumes from census_done.json plus earlier shard outputs; appends to census_mp.jsonl."""
import sys, json, glob, multiprocessing as mp
sys.path.append(sys.argv[1])
from sage.all import *  # noqa: signature needs Sage
import snappy

def work(name):
    try:
        M = snappy.Manifold(name)
        cs = [c for c in M.alexander_polynomial().coefficients(sparse=False) if c != 0]
        if not (all(abs(c) == 1 for c in cs) and all(cs[i] == -cs[i + 1] for i in range(len(cs) - 1))):
            return dict(source="census", name=name, L_space=False, reason="Alexander polynomial not of L-space form")
        L = M.exterior_to_link(); L.simplify('global')
        h = L.knot_floer_homology()
        if not h['L_space_knot']:
            return dict(source="census", name=name, L_space=False)
        sig, det = int(L.signature()), int(L.determinant())
        sign = 1 if int(h['tau']) > 0 else -1
        bound = 1 - sign * sig
        return dict(source="census", name=name, crossings=len(L.crossings), genus=int(h['seifert_genus']), tau=int(h['tau']),
                    signature=sig, det=det, bound=bound, holds=bool(det <= bound))
    except Exception as e:
        return dict(source="census", name=name, error=repr(e)[:200])

if __name__ == "__main__":
    done = set(json.load(open("census_done.json")))
    for f in glob.glob("census_shard*.jsonl") + glob.glob("census_mp.jsonl"):
        for l in open(f):
            try: done.add(json.loads(l)["name"])
            except Exception: pass
    names = [M.name() for M in snappy.CensusKnots() if M.name() not in done]
    print(len(names), "to do", flush=True)
    with mp.get_context("fork").Pool(6) as pool, open("census_mp.jsonl", "a") as out:
        for i, r in enumerate(pool.imap_unordered(work, names, chunksize=1)):
            out.write(json.dumps(r) + "\n"); out.flush()
            if i % 50 == 0: print("progress", i, flush=True)
    print("census done", flush=True)
