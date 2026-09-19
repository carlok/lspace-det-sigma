"""K33 on one-bridge braids B(w,b,t) = closure of (s_b ... s_1)(s_{w-1} ... s_1)^t in B_w, 1 <= b <= w-2,
1 <= t <= w-1 (Gabai's parametrisation; L-space knots by Greene-Lewallen-Vafaee, (1,1) L-space knots).
Independent recomputation of the family proposed by an external model. Signature from the Seifert matrix of the
braid closure (numeric eigenvalues plus error bound), determinant exactly; these are positive braids, so the
braid-closure surface is a minimal genus Seifert surface and g = (length - w + 1)/2."""
import json
import numpy as np
jd = lambda o: json.dumps(o, default=int)

def word(w, b, t):
    return list(range(b, 0, -1)) + list(range(w - 1, 0, -1)) * t

out = open("onebridge.jsonl", "w")
rows = []
for w in range(3, 16):
    for b in range(1, w - 1):
        for t in range(1, w):
            ws = word(w, b, t)
            K = Link(BraidGroup(w)(ws))
            if K.number_of_components() != 1: continue
            V = K.seifert_matrix(); S = V + V.transpose()
            ev = np.linalg.eigvalsh(np.array(S, dtype=float))
            sig = int((ev > 0).sum() - (ev < 0).sum())
            det = int(abs(S.det()))
            g = int(S.nrows() // 2)
            r = dict(name=f"B({w},{b},{t})", w=w, b=b, t=t, braid_length=len(ws), genus=g, signature=sig, det=det,
                     bound=1 - sig, holds=bool(det <= 1 - sig), equality=bool(det == 1 - sig),
                     margin=int(1 - sig - det), min_abs_eigenvalue=float(np.min(np.abs(ev))))
            rows.append(r); out.write(jd(r) + "\n")
out.flush()
viol = [r for r in rows if not r["holds"]]
eq = [r for r in rows if r["equality"]]
print("one-bridge braid knots:", len(rows), "| violations:", len(viol), "| equalities:", len(eq),
      "| all margins 0 or >= 4:", all(r["margin"] == 0 or r["margin"] >= 4 for r in rows), flush=True)
for name in ("B(9,2,3)", "B(10,3,4)", "B(10,5,8)"):
    r = next((x for x in rows if x["name"] == name), None)
    print("  sample", name, "->", {k: r[k] for k in ("genus", "det", "signature")} if r else "not a knot", flush=True)
