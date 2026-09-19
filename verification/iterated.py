"""K33 (det <= 1 - sigma for L-space knots) on iterated torus knots, by classical formulas only.

Conventions as KnotInfo: positive torus knots have negative signature (T(2,3): sigma = -2).
- Torus knot T(p,q), p,q > 1 coprime: sigma = #{(i,j): 1<=i<p, 1<=j<q, i/p+j/q outside [1/2,3/2]} - #{inside}
  (Brieskorn / Gordon-Litherland-Murasugi); Delta = (t^pq - 1)(t - 1)/((t^p - 1)(t^q - 1)).
- Cable K_{p,q} (p > 1 longitudinal): Delta(t) = Delta_K(t^p) Delta_{T(p,q)}(t), genus g = p g(K) + (p-1)(q-1)/2,
  sigma(K_{p,q}) = sigma_{(-1)^p}(K) + sigma(T(p,q)) (Litherland 1979), and sigma at +1 is 0, so the first term
  is sigma(K) for odd p and 0 for even p.
- L-space: K_{p,q} is an L-space knot iff K is one and q/p >= 2 g(K) - 1 (Hedden 2009, Hom 2011).
det = |Delta(-1)|, computed from the polynomial."""
import itertools, json, math
from fractions import Fraction

def pdiv(num, den):  # exact division of integer polynomials, coefficient lists low -> high
    num = list(num); out = [0] * (len(num) - len(den) + 1)
    for k in range(len(out) - 1, -1, -1):
        c = num[k + len(den) - 1] // den[-1]; out[k] = c
        for j, d in enumerate(den): num[k + j] -= c * d
    assert not any(num), "inexact division"
    return out

def torus_sigma(p, q):
    s = 0
    for i in range(1, p):
        for j in range(1, q):
            x = Fraction(i, p) + Fraction(j, q)
            s += 1 if (x < Fraction(1, 2) or x > Fraction(3, 2)) else -1
    return s

def torus_alex(p, q):
    tn = lambda n: [-1] + [0] * (n - 1) + [1]
    return pdiv(mul(tn(p * q), tn(1)), mul(tn(p), tn(q)))

def subst(poly, p):  # Delta(t^p)
    out = [0] * ((len(poly) - 1) * p + 1)
    for k, c in enumerate(poly): out[k * p] = c
    return out

def mul(a, b):
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b): out[i + j] += x * y
    return out

def ev(poly, t): return sum(c * t ** k for k, c in enumerate(poly))

def knot_torus(p, q):
    return dict(name=f"T({p},{q})", alex=torus_alex(p, q), g=(p - 1) * (q - 1) // 2, sigma=torus_sigma(p, q))

def cable(K, p, q):
    T = knot_torus(p, q)
    return dict(name=f"{K['name']};{p},{q}", alex=mul(subst(K['alex'], p), T['alex']),
                g=p * K['g'] + (p - 1) * (q - 1) // 2, sigma=(K['sigma'] if p % 2 else 0) + T['sigma'])

def check(K):
    det = abs(ev(K['alex'], -1))
    return det, 1 - K['sigma'], det <= 1 - K['sigma']

if __name__ == "__main__":
    # validation against KnotInfo values (13n_4639 = T(2,3;2,5), 13n_4587 = T(2,3;2,7), 8_19 = T(3,4), 10_124 = T(3,5))
    tre = knot_torus(2, 3)
    for K, (d, s) in [(tre, (3, -2)), (knot_torus(3, 4), (3, -6)), (knot_torus(3, 5), (1, -8)), (knot_torus(2, 13), (13, -12)),
                      (cable(tre, 2, 5), (5, -4)), (cable(tre, 2, 7), (7, -6))]:
        print("check", K['name'], "det", abs(ev(K['alex'], -1)), "sigma", K['sigma'], "genus", K['g'], "expected", d, s)
    results, violations = [], []
    bases = [knot_torus(p, q) for p in range(2, 8) for q in range(p + 1, 40) if math.gcd(p, q) == 1]
    level = bases
    for depth in range(3):
        nxt = []
        for K in level:
            det, bound, ok = check(K)
            results.append(dict(name=K['name'], genus=K['g'], det=det, one_minus_sigma=bound, holds=ok))
            if not ok: violations.append(results[-1])
            if depth < 2 and K['g'] <= 60:
                for p in range(2, 6):
                    qmin = p * (2 * K['g'] - 1)
                    for q in range(qmin, qmin + 12):
                        if math.gcd(p, q) == 1: nxt.append(cable(K, p, q))
        level = nxt
    json.dump(dict(tested=len(results), violations=violations), open("iterated.json", "w"), indent=1)
    print("tested", len(results), "L-space iterated torus knots; violations", len(violations))
    for v in sorted(violations, key=lambda v: v['genus'])[:10]: print(" ", v)
