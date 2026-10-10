"""Seifert matrices (braid surface, SnapPy) of the family H(n,m): Baker-Kegel K_k = H(2,2k+1) for k <= 60, and
H(n,m) for 3 <= n <= 8, m in {1,3,5,7,9}. SnapPy's matrix gives the right-handed trefoil signature +2, the opposite
of the KnotInfo convention used in the note, so signatures from it are negated downstream (checked on the trefoil).

    python seifert_dump.py     # writes seifert_matrices.json (large; not committed)
"""
import json
import snappy
from hnm import H

tre = snappy.Link(braid_closure=[1, 1, 1]).seifert_matrix()
jobs = [(2, 2 * k + 1) for k in range(61)] + [(n, m) for n in range(3, 9) for m in (1, 3, 5, 7, 9)]
out = {"trefoil": [[int(x) for x in r] for r in tre]}
for n, m in jobs:
    out[f"{n},{m}"] = dict(n=n, m=m, letters=len(H(n, m)),
                           V=[[int(x) for x in r] for r in snappy.Link(braid_closure=H(n, m)).seifert_matrix()])
json.dump(out, open("seifert_matrices.json", "w"))
print("matrices:", len(jobs))
