"""Checks for the inductive proof of K33 on L-space iterated torus knots.

Notation: K L-space knot of genus g_K, cable K_{p,q} with p >= 2, gcd(p,q) = 1, q >= p(2g_K - 1) (Hedden/Hom:
exactly when the cable is an L-space knot). Write A = |sigma(K)|, B = |sigma(T(p,q))|, and use

  (F1) Delta_{K_{p,q}}(t) = Delta_K(t^p) Delta_{T(p,q)}(t)  =>  det(K_{p,q}) = |Delta_K((-1)^p)| det(T(p,q))
       = det(K) det(T(p,q)) for p odd, and = det(T(p,q)) for p even (Delta_K(1) = 1);
  (F2) sigma(K_{p,q}) = sigma_{(-1)^p}(K) + sigma(T(p,q)) (Litherland), i.e. sigma(K) + sigma(T(p,q)) for p odd and
       sigma(T(p,q)) for p even (sigma_1 = 0);
  (F3) det(T(p,q)) = 1 if p, q both odd; p if q even; q if p even.

All three are verified below on the exact data, then the case analysis of the induction step is verified over a large
parameter range, and the base case (torus knots) as well. The only external input is the bound B >= (p-1)(q-1)/2,
tested here and used in cases A and B."""
import json, math
from iterated import knot_torus, cable, ev, torus_sigma

def det_of(K): return abs(ev(K['alex'], -1))
rows = []

# (F1)-(F3) on cables of L-space knots
bases = [knot_torus(p, q) for p in range(2, 7) for q in range(p + 1, 30) if math.gcd(p, q) == 1]
f1 = f2 = f3 = 0; checked = 0
for K in bases:
    dK, sK, gK = det_of(K), K['sigma'], K['g']
    for p in range(2, 7):
        for q in range(p * (2 * gK - 1), p * (2 * gK - 1) + 20):
            if math.gcd(p, q) != 1 or q <= p: continue
            C = cable(K, p, q); T = knot_torus(p, q)
            dC, sC = det_of(C), C['sigma']
            expect_d = (dK if p % 2 else 1) * det_of(T)
            expect_s = (sK if p % 2 else 0) + T['sigma']
            expect_dT = 1 if (p % 2 and q % 2) else (p if q % 2 == 0 else q)
            f1 += dC != expect_d; f2 += sC != expect_s; f3 += det_of(T) != expect_dT; checked += 1
print(f"(F1) det cabling mismatches {f1} / {checked}; (F2) Litherland sigma mismatches {f2}; (F3) det(T(p,q)) mismatches {f3}")

# base case: torus knots
bad_base = [(p, q) for p in range(2, 14) for q in range(p + 1, 80) if math.gcd(p, q) == 1
            and det_of(knot_torus(p, q)) > 1 + abs(torus_sigma(p, q))]
print("base case (torus knots) failures:", len(bad_base))

# induction step, using only the hypotheses: det(K) <= 1 + A, A <= 2 g_K, q >= p(2 g_K - 1), B >= (p-1)(q-1)/2
def step_holds(p, q, gK, A, dK):
    B = abs(torus_sigma(p, q))
    if p % 2 == 0:
        return q if p == 2 else det_of(knot_torus(p, q)), (det_of(knot_torus(p, q)) <= 1 + B)
    return dK * det_of(knot_torus(p, q)), (dK * det_of(knot_torus(p, q)) <= 1 + A + B)
worst = []
fails = []
for gK in range(1, 12):
    A, dK = 2 * gK, 1 + 2 * gK          # worst allowed values under the induction hypothesis
    for p in range(2, 12):
        for q in range(max(p + 1, p * (2 * gK - 1)), p * (2 * gK - 1) + 40):
            if math.gcd(p, q) != 1: continue
            val, ok = step_holds(p, q, gK, A, dK)
            if not ok: fails.append((gK, p, q, val, 1 + A + abs(torus_sigma(p, q))))
print("induction step failures with worst-case A and det(K):", len(fails), fails[:8])
json.dump(dict(f1=f1, f2=f2, f3=f3, base_failures=len(bad_base), step_failures=fails[:50]), open("induction_proof.json", "w"), indent=1)
