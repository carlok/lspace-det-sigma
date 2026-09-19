"""K33 (det <= 1 - sigma, for positive L-space knots; for negative ones apply to the mirror: det <= 1 + sigma)
on hyperbolic L-space knots: SnapPy census, Baker-Kegel K_n, Himeno K_n, and 14/15-crossing non-alternating knots
that are fibered with |tau| = g (then the knot Floer L-space test decides). Signature and determinant from Sage
via SnapPy; L-space and tau from SnapPy's knot Floer homology. Run: sage hyperbolic.sage <snappy site-packages> <out>"""
import sys, json, time
sys.path.append(sys.argv[1])
import snappy

out = open(sys.argv[2], "w")
def record(source, name, L):
    h = L.knot_floer_homology()
    if not h['L_space_knot']:
        return None
    sig, det = int(L.signature()), int(L.determinant())
    sign = int(1) if int(h['tau']) > int(0) else int(-1)
    bound = int(1) - sign * sig
    r = dict(source=source, name=name, crossings=len(L.crossings), genus=int(h['seifert_genus']), tau=int(h['tau']),
             signature=sig, det=det, bound=bound, holds=bool(det <= bound))
    out.write(json.dumps(r) + "\n"); out.flush()
    return r

def bk(n): return [2, 1, 3, 2] * (2 * n + 1) + [-1, 2, 1, 1, 2]
def X(n):
    layer = lambda k: list(range(n - k, n + k + 1, 2))
    return [g for k in range(n) for g in layer(k)] + [g for k in range(n - 2, -1, -1) for g in reversed(layer(k))]
def him(n): return X(n) * 3 + [-i for i in range(1, n)] + list(range(n, 0, -1)) + list(range(1, n + 1))

t = time.time(); rs = []
for n in range(1, 7): rs.append(record("baker-kegel", f"K_{n}", snappy.Link(braid_closure=bk(n))))
for n in (2, 3, 4): rs.append(record("himeno", f"K_{n}", snappy.Link(braid_closure=him(n))))
print("families done", time.time() - t, flush=True)
for name in json.load(open(sys.argv[3])):
    rs.append(record("HT 14-15 crossings", name, snappy.Link(name)))
print("14/15 done", time.time() - t, flush=True)
for M in snappy.CensusKnots():
    try:
        L = M.exterior_to_link(); L.simplify('global')
        rs.append(record("census", M.name(), L))
    except Exception as e:
        out.write(json.dumps(dict(source="census", name=M.name(), error=repr(e)[:200])) + "\n")
rs = [r for r in rs if r]
print("L-space knots tested", len(rs), "violations", [r for r in rs if not r['holds']][:10], "time", round(time.time() - t), flush=True)
