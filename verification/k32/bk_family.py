"""u = g on Baker-Kegel's family K_n = closure of [(2,1,3,2)^(2n+1), -1, 2, 1, 1, 2] (arXiv:2203.12013, Sec. 2),
hyperbolic L-space knots for n >= 1 that are not known to be braid positive (K_1 = o9_30634)."""
import json, sys, time
from multiprocessing import Pool
import snappy
from census_lspace import dfs

def word(n):
    return [2, 1, 3, 2] * (2 * n + 1) + [-1, 2, 1, 1, 2]

def run(n):
    t = time.time()
    L = snappy.Link(braid_closure=word(n)); L.simplify('global')
    pd = [list(map(int, c)) for c in L.PD_code()]
    h = L.knot_floer_homology()
    path = dfs(pd, h['tau'], h['seifert_genus'], time.time() + 1800)
    return dict(n=n, crossings=len(pd), genus=h['seifert_genus'], tau=h['tau'], L_space=h['L_space_knot'],
                fibered=h['fibered'], u_equals_g=path is not None, seconds=round(time.time() - t))

if __name__ == "__main__":
    ns = list(range(1, int(sys.argv[1]) + 1))
    with Pool(len(ns)) as p, open("bk_family.jsonl", "w") as f:
        for r in p.imap_unordered(run, ns):
            print(json.dumps(r), flush=True); f.write(json.dumps(r) + "\n"); f.flush()
