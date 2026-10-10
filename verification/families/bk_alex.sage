# Proof that Delta(K_k) = Delta(C_k) for every k >= 0, where K_k is the Baker-Kegel knot (closure of P^(2k+1) W) and
# C_k is the (2,4k+5)-cable of T(2,2k+1): Delta(C_k)(t) = Delta_{T(2,2k+1)}(t^2) * Delta_{T(2,4k+5)}(t).
# Both sides, suitably normalised, are linear recurrence sequences in k over Q(t); the difference satisfies the
# product recurrence, of order r, so r consecutive zeros force it to vanish identically.
B = BraidGroup(4)
Rt.<t> = PolynomialRing(QQ)
F = FractionField(Rt)
P = B([2, 1, 3, 2]); W = B([-1, 2, 1, 1, 2])
rP = P.burau_matrix(reduced=True).change_ring(F); rW = W.burau_matrix(reduced=True).change_ring(F)
I3 = identity_matrix(F, 3)
A = rP^2
def s(k):            # det(I - rho(beta_k)), beta_k = P^(2k+1) W
    return (I3 - rP^(2*k + 1) * rW).determinant()
def burau_alex(k):   # Delta up to a unit
    return F(s(k) * (1 - t) / (1 - t^4))
def tor2(m):         # Delta_{T(2,m)}(t) = (t^m + 1)/(t + 1), m odd
    return F((t^m + 1) / (t + 1))
def cable_alex(k):
    return F(tor2(2*k + 1).subs(t=t^2) * tor2(4*k + 5))
# normalise: Delta_K = u_k * cable with u_k a unit +-t^e; find e(k)
def unit_ratio(k):
    r = burau_alex(k) / cable_alex(k)
    num, den = r.numerator(), r.denominator()
    assert num.is_monomial() or (-num).is_monomial(), ("not a unit", k, r)
    assert den.is_monomial() or (-den).is_monomial(), ("not a unit", k, r)
    return r
ratios = [unit_ratio(k) for k in range(12)]
print("ratio Delta_Burau / Delta_cable for k = 0..11:", ratios)
# the ratio is c * t^(a k + b): read a, b, c from k = 0, 1 and check on all 12
c0 = ratios[0]; step = ratios[1] / ratios[0]
assert all(ratios[k] == c0 * step^k for k in range(12)), "ratio is not geometric in k"
print("ratio = (%s) * (%s)^k on k = 0..11" % (c0, step))
# recurrence: chi = chi_A * chi_{L2 A} * (x - det A) * (x - 1) for s_k; the cable side times c0*step^k has char roots
# step * {1, t^4, t^8} (from (t^(4k+2)+1)(t^(4k+5)+1)); the difference satisfies the product, of order 8 + 3 = 11.
x = polygen(F, 'x')
idx = [(0, 1), (0, 2), (1, 2)]
L2 = matrix(F, 3, 3, [A.matrix_from_rows_and_columns(list(r_), list(c_)).determinant() for r_ in idx for c_ in idx])
chi = A.charpoly('x').change_ring(F)(x) * L2.charpoly('x').change_ring(F)(x) * (x - A.determinant()) * (x - 1)
chi_cable = (x - step) * (x - step * t^4) * (x - step * t^8)
order = chi.degree() + chi_cable.degree()
diff = [burau_alex(k) - c0 * step^k * cable_alex(k) for k in range(order)]
assert all(d == 0 for d in diff)
# guard: the cable side really satisfies chi_cable (direct check of the claimed char roots)
cc = chi_cable.list()
for k in range(4):
    assert sum(cc[j] * c0 * step^(k + j) * cable_alex(k + j) for j in range(len(cc))) == 0
print("PROVED: Delta(K_k) = Delta(C_k) up to units for every k >= 0 (difference sequence of order %d vanishes on %d initial terms)" % (order, order))
