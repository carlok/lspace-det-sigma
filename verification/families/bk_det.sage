# det(K_k) = 4k + 5 for every Baker-Kegel knot K_k = closure of P^(2k+1) W, P = s2 s1 s3 s2, W = s1^-1 s2 s1 s1 s2.
#
# Proof. Let rho be the reduced Burau representation of B_4 and s_k(t) = det(I - rho(P)^(2k+1) rho(W)). Then
# Delta_k = s_k (1 - t)/(1 - t^4) is the Alexander polynomial of K_k up to a unit (checked against Sage for k <= 4).
# With A = rho(P)^2 and B = rho(P) rho(W), s_k = 1 - tr(A^k B) + tr(L2(A)^k L2(B)) - det(A)^k det(B) for 3x3
# matrices, so by Cayley-Hamilton s_k satisfies the monic recurrence chi = chi_A * chi_{L2 A} * (x - det A) * (x - 1)
# of order 8 over Q(t), and so does Delta_k. Its coefficients are regular at t = -1, so d_k = Delta_k(-1) satisfies
# the integer recurrence chi(-1; x), which is (x - 1)^8. The sequence 4k + 5 satisfies it too, and the two agree on
# k = 0..7, so they agree for every k.
#
#   sage bk_det.sage
B = BraidGroup(4)
Rt.<t> = PolynomialRing(QQ)
F = FractionField(Rt)
P = B([2, 1, 3, 2]); W = B([-1, 2, 1, 1, 2])
rP = P.burau_matrix(reduced=True).change_ring(F); rW = W.burau_matrix(reduced=True).change_ring(F)
I3 = identity_matrix(F, 3)


def s(k):
    return (I3 - rP^(2*k + 1) * rW).determinant()


def alex(k):
    return F(s(k) * (1 - t) / (1 - t^4))


# the Burau normalisation agrees with Sage's Alexander polynomial up to units
for k in range(5):
    r = alex(k) / F(Link(P^(2*k + 1) * W).alexander_polynomial().subs(t=t))
    assert r.numerator().is_monomial() or (-r.numerator()).is_monomial()
    assert r.denominator().is_monomial() or (-r.denominator()).is_monomial()

A = rP^2
x = polygen(F, 'x')
idx = [(0, 1), (0, 2), (1, 2)]
L2 = matrix(F, 3, 3, [A.matrix_from_rows_and_columns(list(r_), list(c_)).determinant() for r_ in idx for c_ in idx])
chi = A.charpoly('x').change_ring(F)(x) * L2.charpoly('x').change_ring(F)(x) * (x - A.determinant()) * (x - 1)
c = chi.list(); r = chi.degree()
assert r == 8 and c[-1] == 1
for k in range(4):                                   # guard on the algebra; Cayley-Hamilton gives it for all k
    assert sum(c[j] * alex(k + j) for j in range(r + 1)) == 0
cm1 = [Rt(cj.numerator())(-1) / Rt(cj.denominator())(-1) for cj in c]
y = polygen(QQ, 'y')
assert sum(cm1[j] * y^j for j in range(r + 1)) == (y - 1)^8
d = [alex(k)(-1) for k in range(r)]
assert d == [4*k + 5 for k in range(r)], d
print("det(K_k) = 4k + 5 for every k >= 0: proved (initial values", d, ")")
