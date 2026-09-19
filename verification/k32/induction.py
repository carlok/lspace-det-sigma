"""Does the unknotting of a non-braid-positive L-space knot stay inside the L-space knots (Rudolph-style induction)?
For each knot, take the depth-first unknotting used earlier (each crossing change lowers |tau| by exactly 1) and record
for every intermediate knot: genus, tau, whether it is an L-space knot, and whether it is fibered."""
import json, sys, time
import snappy, spherogram
from census_lspace import hfk  # simplify + knot Floer data
from unknot3 import flip

def steps(pd, tau, deadline):
    """Greedy/DFS path as in census_lspace.dfs, but recording the intermediate knots."""
    from census_lspace import dfs
    path = dfs(pd, tau, abs(tau), deadline)
    if path is None: return None
    out, cur = [], pd
    for i in path:
        cur = flip(cur, [i])
        L = spherogram.Link([list(c) for c in cur]); L.simplify('global')
        if len(L.crossings) == 0:
            out.append(dict(crossings=0, genus=0, tau=0, L_space=True, fibered=True, unknot=True)); break
        h = L.knot_floer_homology()
        cur = [list(map(int, c)) for c in L.PD_code()]
        out.append(dict(crossings=len(cur), genus=int(h['seifert_genus']), tau=int(h['tau']),
                        L_space=bool(h['L_space_knot']), fibered=bool(h['fibered']), unknot=False))
    return out

def bk(n): return [2, 1, 3, 2] * (2 * n + 1) + [-1, 2, 1, 1, 2]
def X(n):
    layer = lambda k: list(range(n - k, n + k + 1, 2))
    return [g for k in range(n) for g in layer(k)] + [g for k in range(n - 2, -1, -1) for g in reversed(layer(k))]
def him(n): return X(n) * 3 + [-i for i in range(1, n)] + list(range(n, 0, -1)) + list(range(1, n + 1))

jobs = [(f"Baker-Kegel K_{n}", bk(n)) for n in (1, 2, 3, 4)] + [(f"Himeno K_{n}", him(n)) for n in (2, 3)] \
     + [("(2,3)-cable of T(2,3)", [2, 1, 3, 2] * 3 + [-1] * 3), ("(2,7)-cable of T(2,5)", [2, 1, 3, 2] * 5 + [-1] * 3)]
out = []
for name, w in jobs:
    L = snappy.Link(braid_closure=w); L.simplify('global')
    pd = [list(map(int, c)) for c in L.PD_code()]
    h = L.knot_floer_homology()
    seq = steps(pd, int(h['tau']), time.time() + 900)
    r = dict(knot=name, genus=int(h['seifert_genus']), sequence=seq,
             all_L_space=None if seq is None else all(s["L_space"] for s in seq),
             genus_drops_by_one=None if seq is None else all(seq[i]["genus"] == int(h['seifert_genus']) - i - 1 for i in range(len(seq))))
    out.append(r)
    print(name, "genus", r["genus"], "| intermediates L-space:", r["all_L_space"], "| genus drops by 1 each step:", r["genus_drops_by_one"],
          "|", [(s["genus"], s["L_space"]) for s in (seq or [])][:6], flush=True)
json.dump(out, open("induction.json", "w"), indent=1)
