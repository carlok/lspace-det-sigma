"""Seifert matrices (SnapPy, braid surface) of every braid-presented L-space knot used by sigma_by_alex.sage, and the
iterated torus knots' exact (Delta, sigma), so that the Sage step only takes determinants.

    python alex_inputs.py BK_BRAIDS_JSON     # writes alex_inputs.json (large; not committed)
"""
import json, math, sys
sys.path.insert(0, "..")
import snappy
import iterated as it
from hnm import H
from distinct_knots import twisted_word, onebridge_word

load = lambda f: [json.loads(l) for l in open(f)]
seif = lambda w: [[int(x) for x in r] for r in snappy.Link(braid_closure=[int(x) for x in w]).seifert_matrix()]
out = {"iterated": [], "braids": []}
bases = [it.knot_torus(p, q) for p in range(2, 8) for q in range(p + 1, 40) if math.gcd(p, q) == 1]
level = bases
for depth in range(3):
    nxt = []
    for K in level:
        out["iterated"].append(dict(name=K["name"], alex=K["alex"], sigma=K["sigma"]))
        if depth < 2 and K["g"] <= 60:
            for p in range(2, 6):
                qmin = p * (2 * K["g"] - 1)
                for q in range(qmin, qmin + 12):
                    if math.gcd(p, q) == 1: nxt.append(it.cable(K, p, q))
    level = nxt
ex = {r["name"]: r for r in load("../exact_census.jsonl")}
for name, w in json.load(open(sys.argv[1])).items():
    out["braids"].append(dict(source="census", name=name, sigma=ex[name]["signature_positive_chirality"], V=seif(w)))
for r in load("../onebridge.jsonl"):
    out["braids"].append(dict(source="one-bridge", name=r["name"], sigma=r["signature"], V=seif(onebridge_word(r["w"], r["b"], r["t"]))))
for r in load("../twisted_torus_sigma.jsonl"):
    out["braids"].append(dict(source="twisted torus", name=r["name"], sigma=r["signature_positive_chirality"],
                              V=seif(twisted_word(r["p"], r["q"], r["r"], r["s"]))))
sig = {(r["n"], r["m"]): r for r in load("signatures.jsonl")}
for r in load("lspace.jsonl"):
    k = (r["n"], r["m"])
    if r.get("L_space") is True and k in sig and k[0] >= 3:
        out["braids"].append(dict(source="H(n,m)", name="H(%d,%d)" % k, sigma=sig[k]["sigma"], V=seif(H(*k))))
for k in range(1, 26):
    out["braids"].append(dict(source="Baker-Kegel", name="K_%d" % k, sigma=sig[(2, 2 * k + 1)]["sigma"], V=seif(H(2, 2 * k + 1))))
json.dump(out, open("alex_inputs.json", "w"))
print("iterated", len(out["iterated"]), "braids", len(out["braids"]))
