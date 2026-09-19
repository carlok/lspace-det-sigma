"""K33 on the non-braid-positive L-space knot families, beyond the SnapPy census:
Baker-Kegel K_n = closure of [(2,1,3,2)^(2n+1), -1, 2, 1, 1, 2] (arXiv:2203.12013, Section 2), hyperbolic L-space knots
for n >= 1 (K_1 = o9_30634); Himeno K_n = closure of X_n^3 [-1..-(n-1), n..1, 1..n] (arXiv:2506.22934), hyperbolic
L-space knots, not braid positive, for even n; and the (2,q)-cables of T(2,3) and of T(2,5) (L-space by Hedden/Hom).
Signature from the Seifert matrix of the braid closure (numeric eigenvalues, with the error bound recorded),
determinant exactly. The L-space property for the families is by the cited theorems; for the cables by q/p >= 2g-1."""
import json
import numpy as np
jd = lambda o: json.dumps(o, default=int)

def X(n):
    layer = lambda k: list(range(n - k, n + k + 1, 2))
    return [g for k in range(n) for g in layer(k)] + [g for k in range(n - 2, -1, -1) for g in reversed(layer(k))]

fams = {}
for n in range(1, 26):
    fams[f"Baker-Kegel K_{n}"] = [2, 1, 3, 2] * (2 * n + 1) + [-1, 2, 1, 1, 2]
for n in range(2, 9):
    fams[f"Himeno K_{n}"] = X(n) * 3 + [-i for i in range(1, n)] + list(range(n, 0, -1)) + list(range(1, n + 1))
for q in range(3, 40, 2):
    fams[f"(2,{q})-cable of T(2,3)"] = [2, 1, 3, 2] * 3 + ([1] * (q - 6) if q >= 6 else [-1] * (6 - q))
for q in range(7, 40, 2):
    fams[f"(2,{q})-cable of T(2,5)"] = [2, 1, 3, 2] * 5 + ([1] * (q - 10) if q >= 10 else [-1] * (10 - q))

out = open("families_fast.jsonl", "w")
bad = 0
for name, w in fams.items():
    K = Link(BraidGroup(max(abs(x) for x in w) + 1)([int(x) for x in w]))
    if K.number_of_components() != 1:
        out.write(jd(dict(name=name, error="not a knot")) + "\n"); continue
    V = K.seifert_matrix(); S = V + V.transpose()
    ev = np.linalg.eigvalsh(np.array(S, dtype=float))
    sig = int((ev > 0).sum() - (ev < 0).sum())
    det = int(abs(S.det()))
    sig_pos = sig if sum(1 for x in w if x > 0) >= sum(1 for x in w if x < 0) else -sig
    r = dict(name=name, braid_length=len(w), seifert_surface_genus_of_braid_closure=int(S.nrows() // 2), signature_positive_chirality=sig_pos,
             det=det, bound=1 - sig_pos, holds=bool(det <= 1 - sig_pos),
             min_abs_eigenvalue=float(np.min(np.abs(ev))), eigenvalue_error_bound=float(S.nrows() * np.finfo(float).eps * np.max(np.abs(ev))))
    bad += not r["holds"]
    out.write(jd(r) + "\n"); out.flush()
print("families done; violations", bad, flush=True)
