"""Steps of a proof attempt for K33 (det <= 1 + |sigma| for L-space knots), each checked on the exact
iterated-torus dataset.

Step 1. For an L-space knot, Delta~(t) = t^g Delta(t) = (1 - t) R(t) + t^(2g) with R(t) = sum over s in S, s < 2g,
        where S is the semigroup set (complement of the g gaps). Hence det = |Delta(-1)| = |2(E - O) + 1| with
        E, O the even/odd elements of S below 2g; by the symmetry s <-> 2g-1-s, E = #odd gaps, O = #even gaps.
Step 2. So K33 is equivalent to |sigma| >= 2D (D = E - O >= 0) resp. |sigma| >= 2|D| - 2 (D < 0).
Step 3. Candidate lower bounds for |sigma(T(p,q))| used by the cable induction.
"""
import json, math
from iterated import knot_torus, cable, ev, torus_sigma

def semigroup_from_alex(alex, g):
    """S ∩ [0, 2g) from the normalised Alexander polynomial (coefficients of t^(a+g))."""
    poly = {}
    for e, c in enumerate(alex):
        if c: poly[e] = c          # alex is already t^0..t^2g (iterated.py stores it that way)
    run, S = 0, []
    for e in range(0, 2 * g):
        run += poly.get(e, 0)
        if run == 1: S.append(e)
        elif run != 0: return None  # not an L-space-type staircase
    return S

def stats(K):
    g = K['g']; alex = K['alex']
    S = semigroup_from_alex(alex, g)
    if S is None: return None
    E = sum(1 for s in S if s % 2 == 0); O = len(S) - E
    det = abs(ev(alex, -1))
    return dict(g=g, S_size=len(S), E=E, O=O, D=E - O, det_formula=abs(2 * (E - O) + 1), det=det, sigma=K['sigma'])

bases = [knot_torus(p, q) for p in range(2, 8) for q in range(p + 1, 40) if math.gcd(p, q) == 1]
level, rows = bases, []
for depth in range(3):
    nxt = []
    for K in level:
        s = stats(K)
        if s: rows.append((K['name'], s))
        if depth < 2 and K['g'] <= 60:
            for p in range(2, 6):
                qmin = p * (2 * K['g'] - 1)
                for q in range(qmin, qmin + 12):
                    if math.gcd(p, q) == 1: nxt.append(cable(K, p, q))
    level = nxt

bad_formula = [(n, s) for n, s in rows if s['det_formula'] != s['det']]
bad_size = [(n, s) for n, s in rows if s['S_size'] != s['g']]
print("step 1: knots", len(rows), "| det formula mismatches", len(bad_formula), "| |S cap [0,2g)| != g:", len(bad_size))
eq = [(n, s) for n, s in rows if s['det'] == 1 + abs(s['sigma'])]
print("step 2: K33 equality on", len(eq), "of", len(rows), "| examples", [n for n, _ in eq[:6]])
viol = [(n, s) for n, s in rows if s['det'] > 1 + abs(s['sigma'])]
print("       violations", len(viol))
defect = sorted(rows, key=lambda t: (1 + abs(t[1]['sigma'])) - t[1]['det'])[:5]
print("       tightest:", [(n, dict(det=s['det'], sigma=s['sigma'], D=s['D'], g=s['g'])) for n, s in defect])
print("step 3: torus knot signature bounds")
for name, f in (("(p-1)(q-1)/2 = g", lambda p, q: (p - 1) * (q - 1) / 2),
                ("pq/2 - (p+q)/2", lambda p, q: p * q / 2 - (p + q) / 2),
                ("pq/2 - p - q + 2", lambda p, q: p * q / 2 - p - q + 2)):
    bad = [(p, q, abs(torus_sigma(p, q)), f(p, q)) for p in range(2, 12) for q in range(p + 1, 60)
           if math.gcd(p, q) == 1 and abs(torus_sigma(p, q)) < f(p, q)]
    print(f"   |sigma(T(p,q))| >= {name}: failures {len(bad)}", bad[:3])
json.dump(dict(knots=len(rows), det_formula_mismatches=len(bad_formula), equality=len(eq), violations=len(viol)),
          open("proof_steps.json", "w"), indent=1)
