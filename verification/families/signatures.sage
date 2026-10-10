# det (exact integer determinant) and signature (certified) of S = V + V^T for the matrices of seifert_dump.py.
# Certification: eigenvalues from numpy, accepted only if every |eigenvalue| exceeds 10 * N * eps * ||S||_F, a bound on
# the floating-point error (Weyl). Signs follow KnotInfo (right-handed trefoil -2): SnapPy's matrices are negated.
#
#   sage signatures.sage     # writes signatures.jsonl
import json, numpy as np
D = json.load(open("seifert_matrices.json"))

def inertia(V):
    S = matrix(ZZ, V); S = S + S.transpose()
    A = np.array(S, dtype=float); ev = np.linalg.eigvalsh(A)
    err = A.shape[0] * np.finfo(float).eps * np.linalg.norm(A) * 10
    return abs(S.det()), int((ev > 0).sum() - (ev < 0).sum()), bool(np.min(np.abs(ev)) > err)

d0, s0, ok0 = inertia(D.pop("trefoil"))
assert (d0, s0, ok0) == (3, 2, True)          # SnapPy convention: +2 for the right-handed trefoil
rows = []
for key, r in D.items():
    d, s, ok = inertia(r["V"])
    sigma = -s
    rows.append(dict(n=int(r["n"]), m=int(r["m"]), letters=int(r["letters"]), det=int(d), sigma=sigma, certified=ok,
                     K33=bool(d <= 1 + abs(sigma)), equality=bool(d == 1 + abs(sigma))))
with open("signatures.jsonl", "w") as f:
    for r in rows: f.write(json.dumps(r) + "\n")
bk = sorted((r for r in rows if r["n"] == 2), key=lambda r: r["m"])
print("rows", len(rows), "| uncertified", sum(not r["certified"] for r in rows), "| K33 failures", sum(not r["K33"] for r in rows))
print("Baker-Kegel k = 0..%d: det = 4k+5 and sigma = -(4k+4) for all:" % (len(bk) - 1),
      all(r["det"] == 2*r["m"] + 3 and r["sigma"] == -(2*r["m"] + 2) for r in bk))
