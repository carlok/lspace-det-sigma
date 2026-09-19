"""K33 (det <= 1 - sigma) on all 632 census L-space knots, from Baker-Kegel's braid words (arXiv:2203.12013, Appendix,
first table). Signature from the Seifert matrix V of the braid closure: eigenvalues of V + V^T computed numerically
(the matrix is nonsingular; the smallest |eigenvalue| is reported as a conditioning check), determinant |det(V + V^T)|
exactly. Orientation: a positive braid word gives the positive chirality, a negative word the mirror, so sigma is
negated for negative words. Numeric signatures are compared with Sage's exact signature() on every knot that the
earlier exact run (census_sage_native.jsonl) completed."""
import json
import numpy as np
jd = lambda o: json.dumps(o, default=int)
ls = json.load(open("bk_lspace_braids.json"))
exact = {json.loads(l)["name"]: json.loads(l) for l in open("census_sage_native.jsonl")}
out = open("census_lspace_fast.jsonl", "w")  # rerun records the conditioning bound
mismatch = agree = 0
for name, w in sorted(ls.items(), key=lambda t: len(t[1])):
    n = max(abs(x) for x in w) + 1
    K = Link(BraidGroup(n)([int(x) for x in w]))
    V = K.seifert_matrix(); S = V + V.transpose()
    ev = np.linalg.eigvalsh(np.array(S, dtype=float))
    sig = int((ev > 0).sum() - (ev < 0).sum())
    det = int(abs(S.det()))
    sign = 1 if w[0] > 0 else -1
    sig_pos = sig if sign > 0 else -sig
    r = dict(name=name, braid_length=len(w), strands=int(n), matrix_size=int(S.nrows()), positive=bool(sign > 0),
             signature_positive_chirality=sig_pos, det=det, bound=1 - sig_pos, holds=bool(det <= 1 - sig_pos),
             min_abs_eigenvalue=float(np.min(np.abs(ev))), max_abs_eigenvalue=float(np.max(np.abs(ev))),
             eigenvalue_error_bound=float(S.nrows() * np.finfo(float).eps * np.max(np.abs(ev))))
    e = exact.get(name)
    if e and "signature_positive_chirality" in e:
        same = e["signature_positive_chirality"] == sig_pos and e["det"] == det
        agree += same; mismatch += not same
        r["matches_exact_run"] = bool(same)
    out.write(jd(r) + "\n"); out.flush()
print("done: exact-run comparison agree", agree, "mismatch", mismatch, flush=True)
