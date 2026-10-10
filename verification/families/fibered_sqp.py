"""A fibered strongly quasipositive knot with u > g: the mirror of 12n_642.

  * fibered, genus 2, |tau| = 2 = g: knot Floer homology (which detects fiberedness and the genus). A fibered knot
    with tau = g is strongly quasipositive (Hedden, JKTR 19 (2010)), so the chirality with tau = +2 is.
  * not an L-space knot: knot Floer homology has total rank 37 > 2g + 1.
  * u >= 3: V + V^T has nullity 3 over F_3, so H_1 of the double branched cover has 3 generators (it is (Z/3)^3, the
    determinant being 27), and the unknotting number is at least that number of generators (Wendt).

    python fibered_sqp.py     # writes fibered_sqp.json
"""
import json
import snappy


def rank_mod_p(M, p):
    A = [[x % p for x in row] for row in M]
    r, rows, cols = 0, len(A), len(A[0])
    for c in range(cols):
        piv = next((i for i in range(r, rows) if A[i][c]), None)
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], -1, p)
        A[r] = [(x * inv) % p for x in A[r]]
        for i in range(rows):
            if i != r and A[i][c]:
                f = A[i][c]
                A[i] = [(a - f * b) % p for a, b in zip(A[i], A[r])]
        r += 1
    return r


def det_int(M):
    """Bareiss fraction-free determinant."""
    A = [list(r) for r in M]; n = len(A); sign, prev = 1, 1
    for k in range(n - 1):
        if A[k][k] == 0:
            sw = next((i for i in range(k + 1, n) if A[i][k]), None)
            if sw is None:
                return 0
            A[k], A[sw] = A[sw], A[k]; sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) // prev
        prev = A[k][k]
    return sign * A[-1][-1]


K = snappy.Link('K12n642')
h = K.knot_floer_homology()
V = K.seifert_matrix()
S = [[V[i][j] + V[j][i] for j in range(len(V))] for i in range(len(V))]
null3 = len(S) - rank_mod_p(S, 3)
out = dict(knot="12n_642", genus=h['seifert_genus'], tau=h['tau'], fibered=h['fibered'], L_space=h['L_space_knot'],
           hfk_rank=h['total_rank'], det=abs(det_int(S)), nullity_mod_3=null3, unknotting_lower_bound=null3)
print(json.dumps(out))
assert out['fibered'] and abs(out['tau']) == out['genus'] == 2 and out['det'] == 27 and null3 == 3
json.dump(out, open("fibered_sqp.json", "w"), indent=1)
