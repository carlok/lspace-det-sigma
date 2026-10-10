# Is the signature of an L-space knot determined by its Alexander polynomial? Every L-space knot of this project is
# grouped by its Alexander polynomial (normalised: symmetric, Delta(1) = 1) and the signatures in each group compared.
#   iterated torus knots: Delta and sigma exact (cabling formula, Litherland), as enumerated in iterated.py
#   census L-space knots: Baker-Kegel braid words, exact signatures (exact_census.jsonl)
#   one-bridge braids (L-space knots by Greene-Lewallen-Vafaee) and twisted torus L-space knots: signatures on record
#   H(n,m) shown by knot Floer homology to be L-space knots, and Baker-Kegel K_k: certified signatures
# For braids, Delta = det(t V - V^T) with V the braid-surface Seifert matrix from alex_inputs.py, by integer
# determinants at N+1 points and exact interpolation.
# Signs: KnotInfo convention throughout.
#
#   python alex_inputs.py BK_BRAIDS_JSON && sage sigma_by_alex.sage     # writes sigma_by_alex.json
import json
from collections import defaultdict
R.<t> = PolynomialRing(ZZ)

def norm(d):
    d = {int(e): int(c) for e, c in d.items() if c}
    lo, hi = min(d), max(d)
    out = tuple(sorted((2 * e - lo - hi, c) for e, c in d.items()))
    return out if sum(c for _, c in out) > 0 else tuple((e, -c) for e, c in out)

D = json.load(open("alex_inputs.json"))
groups = defaultdict(list)
for K in D["iterated"]:
    groups[norm(dict(enumerate(K["alex"])))].append(("iterated torus", K["name"], int(K["sigma"])))
QX = PolynomialRing(QQ, 'x')

def alex_from_seifert(V):
    # det(t V - V^T) has degree <= N: integer determinants at N+1 points, then exact Lagrange interpolation
    N = V.nrows()
    pts = [ZZ(i) - N // 2 for i in range(N + 1)]
    P = QX.lagrange_polynomial([(x, (x * V - V.transpose()).det()) for x in pts])
    assert all(c in ZZ for c in P.list())
    return P

for K in D["braids"]:
    V = matrix(ZZ, K["V"])
    p = alex_from_seifert(V)
    groups[norm(dict(enumerate(p.list())))].append((K["source"], K["name"], int(K["sigma"])))
knots = sum(len(v) for v in groups.values())
conflicts = [v for v in groups.values() if len({m[2] for m in v}) > 1]
shared = [v for v in groups.values() if len(v) > 1]
beyond = [v for v in shared if any(m[0] != "iterated torus" for m in v)]
cross = [v for v in beyond if len({m[0] for m in v}) > 1]
out = dict(knots=knots, polynomials=len(groups), polynomials_with_several_knots=len(shared),
           polynomials_shared_beyond_iterated=len(beyond), polynomials_shared_across_families=len(cross),
           conflicts=conflicts, shared_examples=beyond[:80])
json.dump(out, open("sigma_by_alex.json", "w"), indent=1)
print("knots", knots, "| polynomials", len(groups), "| shared", len(shared), "| shared beyond iterated torus", len(beyond),
      "| across families", len(cross), "| CONFLICTS", len(conflicts))
for c in conflicts[:12]: print("  conflict:", c[:6])
for s in cross[:30]: print("  across:", s[:4])
