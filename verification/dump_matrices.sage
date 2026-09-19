"""Dump S = V + V^T for every census L-space knot (Baker-Kegel braid words) as integer lists, for exact inertia."""
import json
ls = json.load(open("bk_lspace_braids.json"))
out = {}
for name, w in ls.items():
    K = Link(BraidGroup(max(abs(x) for x in w) + 1)([int(x) for x in w]))
    V = K.seifert_matrix(); S = V + V.transpose()
    out[name] = [[int(x) for x in row] for row in S.rows()]
json.dump(out, open("census_matrices.json", "w"))
print("dumped", len(out), "matrices; largest", max(len(m) for m in out.values()))
