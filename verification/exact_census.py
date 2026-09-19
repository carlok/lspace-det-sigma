"""K33 on all 632 census L-space knots with exact arithmetic only: signature by congruence diagonalisation over Q
(exact_signature.py) on the matrices S = V + V^T dumped from Sage, determinant already exact. Compares with the
numerical run (census_lspace_fast.jsonl) and with Sage's exact signature where that finished (census_sage_native.jsonl)."""
import json, time
from exact_signature import signature

M = json.load(open("census_matrices.json"))
num = {json.loads(l)["name"]: json.loads(l) for l in open("census_lspace_fast.jsonl")}
sage_exact = {json.loads(l)["name"]: json.loads(l) for l in open("census_sage_native.jsonl")}
words = json.load(open("bk_lspace_braids.json"))

out, t0 = [], time.time()
for name in sorted(M):
    S = M[name]
    sig = signature(S)
    w = words[name]
    sign = 1 if w[0] > 0 else -1
    sig_pos = sig if sign > 0 else -sig
    det = num[name]["det"]                      # |det(V + V^T)|, computed exactly by Sage
    r = dict(name=name, matrix_size=len(S), signature_positive_chirality=sig_pos, det=det,
             bound=1 - sig_pos, holds=bool(det <= 1 - sig_pos),
             matches_numeric=bool(sig_pos == num[name]["signature_positive_chirality"]))
    e = sage_exact.get(name)
    if e and "signature_positive_chirality" in e:
        r["matches_sage_exact"] = bool(sig_pos == e["signature_positive_chirality"])
    out.append(r)
with open("exact_census.jsonl", "w") as f:
    for r in out: f.write(json.dumps(r) + "\n")
viol = [r for r in out if not r["holds"]]
mism_num = [r for r in out if not r["matches_numeric"]]
sage_cmp = [r for r in out if "matches_sage_exact" in r]
print(f"{len(out)} census L-space knots, all signatures exact in {time.time()-t0:.0f}s")
print("K33 violations:", len(viol), "| equalities:", sum(r['det'] == r['bound'] for r in out))
print("disagreements with the numerical run:", len(mism_num))
print("compared with Sage exact where available:", len(sage_cmp), "| disagreements:", sum(not r["matches_sage_exact"] for r in sage_cmp))
