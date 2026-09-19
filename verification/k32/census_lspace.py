"""u = g test on SnapPy census knots that are L-space knots. For each: diagram from the exterior, tau and
genus from HFK, then a depth-first search over crossing changes of the sign of tau that lower |tau| by exactly
1 at each step (necessary for an unknotting in g = |tau| steps). Success certificate: final diagram simplifies
to 0 crossings or has HFK rank 1."""
import json, sys, time
from multiprocessing import Pool
import snappy, spherogram
from unknot3 import flip

def hfk(pd):
    L = spherogram.Link(pd); L.simplify('global')
    if len(L.crossings) == 0:
        return 0, 1, []
    h = L.knot_floer_homology()
    return h['tau'], h['total_rank'], [list(map(int, c)) for c in L.PD_code()]

def dfs(pd, tau, budget, deadline):
    if time.time() > deadline: return None
    if tau == 0:
        _, rank, _ = hfk(pd)
        return [] if rank == 1 else None
    sign = 1 if tau > 0 else -1
    Lp = spherogram.Link(pd)
    signs = {tuple(sorted(map(int, c))): x.sign for c, x in zip(Lp.PD_code(), Lp.crossings)}
    tried = set()
    for i, c in enumerate(pd):
        if signs.get(tuple(sorted(c))) != sign: continue
        t2, rank, pd2 = hfk(flip(pd, [i]))
        if abs(t2) != abs(tau) - 1: continue
        key = (len(pd2), rank)
        if pd2 and key in tried: continue
        tried.add(key)
        if t2 == 0 and rank == 1: return [i]
        if not pd2: continue
        rest = dfs(pd2, t2, budget - 1, deadline)
        if rest is not None: return [i] + rest
    return None

def work(name):
    try:
        M = snappy.Manifold(name)
        L = M.exterior_to_link(); L.simplify('global')
        pd = [list(map(int, c)) for c in L.PD_code()]
        h = L.knot_floer_homology()
        if not h['L_space_knot']:
            return None
        g, tau = h['seifert_genus'], h['tau']
        path = dfs(pd, tau, g, time.time() + 300)
        return dict(name=name, crossings=len(pd), genus=g, tau=tau, u_equals_g=path is not None, steps=None if path is None else len(path))
    except Exception as e:
        return dict(name=name, error=repr(e)[:200])

def work_named(name):
    return name, work(name)

if __name__ == "__main__":
    names = [M.name() for M in snappy.CensusKnots()]
    try:
        done = {json.loads(l)["name"] for l in open("census_lspace.jsonl")}
        done |= {l.strip() for l in open("census_seen.txt")}
    except FileNotFoundError:
        done = set()
    names = [n for n in names if n not in done]
    print(len(names), "census knots to do", flush=True)
    t = time.time()
    seen = open("census_seen.txt", "a")
    with Pool(10) as p, open("census_lspace.jsonl", "a") as f:
        for n, r in p.imap_unordered(work_named, names, chunksize=1):
            if r: f.write(json.dumps(r) + "\n"); f.flush()
            seen.write(n + "\n"); seen.flush()
    print("done", f"{time.time()-t:.0f}s", flush=True)
