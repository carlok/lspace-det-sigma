"""K32 (u = g) on more L-space knots that are not braid positive, or not known to be:
Baker-Kegel K_7..K_10, Himeno K_5..K_6, and minimal-twist cables K_{p,q} with q = p(2g(K)-1) (the smallest q for which
the cable is an L-space knot, by Hedden and Hom; larger q give braid positive cables when K is braid positive).
u >= g holds for every L-space knot; a depth-first search looks for g crossing changes to the unknot, each lowering
|tau| by exactly 1. Success certifies u = g; failure within the time cap certifies nothing."""
import json, time, sys
import snappy
from census_lspace import dfs

def bk(n): return [2, 1, 3, 2] * (2 * n + 1) + [-1, 2, 1, 1, 2]
def X(n):
    layer = lambda k: list(range(n - k, n + k + 1, 2))
    return [g for k in range(n) for g in layer(k)] + [g for k in range(n - 2, -1, -1) for g in reversed(layer(k))]
def him(n): return X(n) * 3 + [-i for i in range(1, n)] + list(range(n, 0, -1)) + list(range(1, n + 1))
def cable(word, p, q, framing):  # p-cable of the closure of `word` with parameter q; framing = writhe of the word
    out = []
    for x in word:
        i = abs(x); s = 1 if x > 0 else -1
        block = []
        for a in range(p):
            for b in range(p - 1, -1, -1) if s > 0 else range(p):
                pass
        # p-cable of sigma_i: the (p x p) block of the braid, standard pattern
        blk = []
        for a in range(p):
            blk += [s * (p * (i - 1) + p - a + c) for c in range(p)][:0]
        out.append(None)
    return None

jobs = []  # Baker-Kegel K_7..K_10 done in hunt.json; Himeno K_5, K_6 skipped: knot Floer homology of an 89-letter
# braid on 10 strands did not finish in hours
# minimal-twist 2-cables: (2, 2g-1) cable of T(2,2k+1), genus g = k; braid (2,1,3,2)^(2k+1) then s1^(q - 2*(2k+1))
for k in (2, 3, 4, 5):
    q = 2 * (2 * k - 1) + 1  # odd, >= 2*(2g-1) with g = k
    w = [2, 1, 3, 2] * (2 * k + 1) + ([1] * (q - 2 * (2 * k + 1)) if q >= 2 * (2 * k + 1) else [-1] * (2 * (2 * k + 1) - q))
    jobs.append((f"(2,{q})-cable of T(2,{2*k+1})", w))

out = []
for name, w in jobs:
    t = time.time()
    L = snappy.Link(braid_closure=w); L.simplify('global')
    pd = [list(map(int, c)) for c in L.PD_code()]
    h = L.knot_floer_homology()
    if not h['L_space_knot']:
        r = dict(knot=name, L_space=False); print(r, flush=True); out.append(r); continue
    path = dfs(pd, int(h['tau']), int(h['seifert_genus']), time.time() + 1800)
    r = dict(knot=name, L_space=True, crossings=len(pd), genus=int(h['seifert_genus']), u_equals_g=path is not None, seconds=round(time.time() - t))
    out.append(r); print(r, flush=True)
    json.dump(out, open("hunt.json", "w"), indent=1)
