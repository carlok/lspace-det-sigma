"""Does K33 follow from: (a) det <= #terms of Delta (true for L-space knots: coefficients +-1) and
(b) |sigma| >= #terms - 1?  Test (b) and the sharper det <= |sigma| + 1 on L-space iterated torus knots."""
import json, math
from iterated import knot_torus, cable, ev, check
rows, bad_b, bad_k33, worst = 0, [], [], None
bases = [knot_torus(p, q) for p in range(2, 8) for q in range(p + 1, 40) if math.gcd(p, q) == 1]
level = bases
for depth in range(3):
    nxt = []
    for K in level:
        terms = sum(1 for c in K['alex'] if c)
        det, bound, ok = check(K)
        sig = abs(K['sigma'])
        rows += 1
        if sig < terms - 1: bad_b.append((K['name'], terms, sig))
        if not ok: bad_k33.append(K['name'])
        slack = sig - (terms - 1)
        if worst is None or slack < worst[0]: worst = (slack, K['name'], terms, sig, det)
        if depth < 2 and K['g'] <= 60:
            for p in range(2, 6):
                qmin = p * (2 * K['g'] - 1)
                for q in range(qmin, qmin + 12):
                    if math.gcd(p, q) == 1: nxt.append(cable(K, p, q))
    level = nxt
print("tested", rows, "| lemma |sigma| >= terms - 1 fails on", len(bad_b), bad_b[:5])
print("K33 fails on", len(bad_k33))
print("tightest case (slack, knot, terms, |sigma|, det):", worst)
json.dump(dict(tested=rows, lemma_failures=bad_b[:50], k33_failures=bad_k33[:50], tightest=worst), open("lemma.json", "w"), indent=1)
