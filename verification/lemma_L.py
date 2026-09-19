"""Lemma L: |sigma(T(p,q))| >= g(T(p,q)) = (p-1)(q-1)/2 for coprime 2 <= p < q, with each step of the proof checked.

sigma(T(p,q)) = N_out - N_in over the grid G = [1,p-1] x [1,q-1], where a point is "in" if 1/2 < i/p + j/q < 3/2
(Brieskorn; Gordon-Litherland-Murasugi). The map (i,j) -> (p-i, q-j) is an involution of G exchanging the two outside
regions, so N_out = 2 N_<, N_< = #{(i,j) in G : i/p + j/q < 1/2}, and |sigma| >= g  <=>  N_< <= (p-1)(q-1)/8.

Per column i, the count is #{j >= 1 : j < f(i)} = ceil(f(i)) - 1 <= f(i) where f(i) = q/2 - i q / p, and f(i) > 0
exactly for i < p/2. Summing:
  p even, m = p/2 - 1:   N_< <= q (p - 2) / 8,        and q(p-2) <= (p-1)(q-1) <=> q >= p - 1.
  p odd,  m = (p-1)/2:   N_< <= q (p-1)^2 / (8 p),    and q(p-1)/p <= q - 1 <=> p <= q.
Both hold since q > p, so Lemma L follows."""
import math
from fractions import Fraction
from iterated import torus_sigma

def counts(p, q):
    N_lt = N_gt = N_in = 0
    for i in range(1, p):
        for j in range(1, q):
            x = Fraction(i, p) + Fraction(j, q)
            if x < Fraction(1, 2): N_lt += 1
            elif x > Fraction(3, 2): N_gt += 1
            else: N_in += 1
    return N_lt, N_gt, N_in

bad = []
for p in range(2, 16):
    for q in range(p + 1, 60):
        if math.gcd(p, q) != 1: continue
        N_lt, N_gt, N_in = counts(p, q)
        g = (p - 1) * (q - 1) // 2
        sig = torus_sigma(p, q)
        checks = {
            "symmetry N_< = N_>": N_lt == N_gt,
            "sigma = N_out - N_in": sig == (N_lt + N_gt) - N_in,
            "column bound": N_lt <= sum(max(0, Fraction(q, 2) - Fraction(i * q, p)) for i in range(1, p)),
            "closed form": N_lt <= (Fraction(q * (p - 2), 8) if p % 2 == 0 else Fraction(q * (p - 1) ** 2, 8 * p)),
            "N_< <= (p-1)(q-1)/8": N_lt <= Fraction((p - 1) * (q - 1), 8),
            "Lemma L": abs(sig) >= g,
        }
        for k, v in checks.items():
            if not v: bad.append((p, q, k))
import json
pairs = sum(1 for p in range(2, 16) for q in range(p + 1, 60) if math.gcd(p, q) == 1)
wide = sum(1 for p in range(2, 21) for q in range(p + 1, 200) if math.gcd(p, q) == 1
           and abs(torus_sigma(p, q)) >= (p - 1) * (q - 1) / 2)
wide_all = sum(1 for p in range(2, 21) for q in range(p + 1, 200) if math.gcd(p, q) == 1)
json.dump(dict(pairs_checked=pairs, failures=len(bad), wide_range_pairs=wide_all, wide_range_holds=wide,
               small_cases={"T(3,4)": abs(torus_sigma(3, 4)), "T(5,6)": abs(torus_sigma(5, 6)), "T(3,10)": abs(torus_sigma(3, 10))}),
          open("lemma_L.json", "w"), indent=1)
print("pairs checked:", pairs)
print("failures:", len(bad), bad[:5])
print("small cases needed in the induction: |sigma(T(3,4))| =", abs(torus_sigma(3, 4)), ">= 6 ;",
      "|sigma(T(5,6))| =", abs(torus_sigma(5, 6)), ">= 12 ;", "|sigma(T(3,10))| =", abs(torus_sigma(3, 10)), ">= 10")
