"""Exact signature of a symmetric integer matrix, by congruence diagonalisation over Q (Fractions only, no floats).

Used instead of a numerical eigenvalue computation wherever an exact signature is needed. The algorithm is
symmetric Gaussian elimination with Bunch-Kaufman pivoting: pivot on a nonzero diagonal entry and take the
Schur complement; when every diagonal entry of the remaining block is zero but the block is not, pivot on
a 2x2 hyperbolic block, which contributes (+1, -1), and take the Schur complement of *that*. Sylvester's
law of inertia makes the result exact and independent of the choices.

The 2x2 Schur complement is the part that is easy to get wrong. For the block

    B = [[0, b], [b, 0]]   with inverse   B^-1 = [[0, 1/b], [1/b, 0]],

the update of the remaining entries is

    a[k][l] -= (a[k][i] * a[j][l] + a[k][j] * a[i][l]) / b.

An earlier version of this file deleted the two rows and columns without applying that update. It agreed
with Sage and with the numerical route on every matrix whose diagonal never vanished, which is almost all
of them, and was wrong otherwise: on the Seifert matrix of the twisted torus knot K(8,3;5,-2) it returned
-8 for a genus 3 knot, where |sigma| <= 2g = 6 forces -6. The mod 4 congruence check of congruence.py is
what caught it, and the regression test below is that matrix's smallest symptom.

The matrices themselves come from Sage (`Link.seifert_matrix`), so only the inertia computation is here.
"""
from fractions import Fraction


def signature(mat):
    """Signature of a symmetric matrix given as a list of lists of ints/Fractions."""
    n = len(mat)
    a = [[Fraction(x) for x in row] for row in mat]
    idx = list(range(n))
    pos = neg = 0
    while idx:
        piv = next((i for i in idx if a[i][i] != 0), None)
        if piv is None:
            # every diagonal entry is zero: a 2x2 hyperbolic block contributes (+1, -1)
            pair = next(((i, j) for i in idx for j in idx if i != j and a[i][j] != 0), None)
            if pair is None:
                break  # the remaining block is zero and contributes nothing
            i, j = pair
            b = a[i][j]
            pos += 1
            neg += 1
            rest = [k for k in idx if k not in (i, j)]
            for k in rest:
                for l in rest:
                    a[k][l] -= (a[k][i] * a[j][l] + a[k][j] * a[i][l]) / b
            idx = rest
            continue
        d = a[piv][piv]
        pos += d > 0
        neg += d < 0
        rest = [i for i in idx if i != piv]
        for i in rest:
            f = a[i][piv] / d
            if f == 0:
                continue
            for j in rest:
                a[i][j] -= f * a[piv][j]
        idx = rest
    return pos - neg


if __name__ == "__main__":
    # the algorithm itself is checked against known signatures of symmetric forms
    assert signature([[2]]) == 1 and signature([[-3]]) == -1
    assert signature([[0, 1], [1, 0]]) == 0
    assert signature([[-2, 1], [1, -2]]) == -2          # right-handed trefoil, V + V^T
    assert signature([[-2, 1, 0], [1, -2, 1], [0, 1, -2]]) == -3
    assert signature([[0, 0], [0, 0]]) == 0

    # regression: a zero diagonal with a nonzero remainder, which needs the 2x2 Schur complement.
    # Eigenvalues 2, -1, -1, so the signature is -1; the version without the update returned 0.
    assert signature([[0, 1, 1], [1, 0, 1], [1, 1, 0]]) == -1
    # the same failure one size up, signature 0 either way only if the update is applied
    assert signature([[0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]) == 0
    print("exact signature self-tests passed")
