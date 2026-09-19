"""u = g on Himeno's knots K_n (arXiv:2506.22934): closure of the 2n-braid X_n^3 . [-1,...,-(n-1), n, n-1,...,1, 1, 2,...,n],
X_n = layers k = 0..n-1 of (n-k, n-k+2, ..., n+k), then layers k = n-2..0 again (generators in a layer commute).
For even n these are hyperbolic L-space knots that are not braid positive; K_2 = o9_30634."""
import json, sys, time
from multiprocessing import Pool
import snappy
from census_lspace import dfs

def X(n):
    layer = lambda k: list(range(n - k, n + k + 1, 2))
    up = [g for k in range(n) for g in layer(k)]
    down = [g for k in range(n - 2, -1, -1) for g in reversed(layer(k))]
    return up + down

def word(n):
    return X(n) * 3 + [-i for i in range(1, n)] + list(range(n, 0, -1)) + list(range(1, n + 1))

def run(n):
    t = time.time()
    L = snappy.Link(braid_closure=word(n)); L.simplify('global')
    pd = [list(map(int, c)) for c in L.PD_code()]
    h = L.knot_floer_homology()
    same_as_o9 = None
    if n == 2:
        same_as_o9 = L.exterior().is_isometric_to(snappy.Manifold('o9_30634'))
    path = dfs(pd, h['tau'], h['seifert_genus'], time.time() + 3000) if h['L_space_knot'] else None
    return dict(n=n, word_length=len(word(n)), crossings=len(pd), components=len(L.link_components), genus=h['seifert_genus'],
                tau=h['tau'], L_space=h['L_space_knot'], fibered=h['fibered'], isometric_to_o9_30634=same_as_o9,
                u_equals_g=path is not None, seconds=round(time.time() - t))

if __name__ == "__main__":
    print(word(2))
    ns = [int(x) for x in sys.argv[1:]]
    with Pool(len(ns)) as p, open("himeno.jsonl", "w") as f:
        for r in p.imap_unordered(run, ns):
            print(json.dumps(r), flush=True); f.write(json.dumps(r) + "\n"); f.flush()
