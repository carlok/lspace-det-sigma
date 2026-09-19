# K33: proof for L-space iterated torus knots

**Statement (K33).** For every L-space knot K: `det(K) <= 1 + |sigma(K)|`. (KnotInfo's chirality: a positive L-space
knot has `sigma < 0`, so the inequality is the one the engine printed, `det <= -sigma + 1`.)

**What is proved here.** K33 holds for every L-space knot that is an iterated torus knot; this includes all torus
knots and all algebraic knots. The hyperbolic case is not covered and stays open. Every numbered step was checked by
script on exact data; the scripts are in `verification/` (`lemma_L.py`, `induction_proof.py`, `proof_steps.py`,
`iterated.py`).

## 0. Notation and standard input

For coprime `2 <= p < q`, `T(p,q)` is the positive torus knot, `g(T(p,q)) = (p-1)(q-1)/2`. For a knot K and
coprime `p >= 2`, `q`, the cable `K_{p,q}` has pattern winding number p. Three standard facts are used, and all three
were verified on 4,088 cable instances in `induction_proof.py` (0 mismatches):

- **(F1)** `Delta_{K_{p,q}}(t) = Delta_K(t^p) * Delta_{T(p,q)}(t)`, hence, since `Delta_K(1) = 1`,
  `det(K_{p,q}) = det(K) * det(T(p,q))` for p odd and `det(K_{p,q}) = det(T(p,q))` for p even.
- **(F2)** Litherland's cabling formula for signatures: `sigma(K_{p,q}) = sigma_{(-1)^p}(K) + sigma(T(p,q))`, so
  `sigma(K_{p,q}) = sigma(K) + sigma(T(p,q))` for p odd and `= sigma(T(p,q))` for p even (`sigma_1 = 0`).
- **(F3)** `det(T(p,q)) = 1` if p and q are both odd, `= p` if q is even, `= q` if p is even.

Hedden and Hom: `K_{p,q}` is an L-space knot if and only if K is one and `q >= p(2g(K) - 1)`. Ozsvath-Szabo: an
L-space knot is fibered with `g = g_4 = tau`, so `|sigma| <= 2g`.

## 1. Lemma L: `|sigma(T(p,q))| >= g(T(p,q))`

By the Brieskorn / Gordon-Litherland-Murasugi count, `sigma(T(p,q)) = N_out - N_in` over the grid
`G = [1,p-1] x [1,q-1]`, where `(i,j)` is *in* when `1/2 < i/p + j/q < 3/2`. The involution `(i,j) -> (p-i, q-j)` of G
exchanges the two outside regions, so `N_out = 2 N_<` with `N_< = #{(i,j) in G : i/p + j/q < 1/2}`. Since
`N_in + N_out = 2g`, the claim `|sigma| >= g` is equivalent to

    N_< <= (p-1)(q-1)/8.

For fixed i the count is `#{j >= 1 : j < f(i)} = ceil(f(i)) - 1 <= f(i)`, where `f(i) = q/2 - i q / p`, and `f(i) > 0`
exactly for `i < p/2`. Summing over those i:

- p even, `m = p/2 - 1`: `N_< <= q(p-2)/8`, and `q(p-2) <= (p-1)(q-1)` reduces to `q >= p - 1`;
- p odd, `m = (p-1)/2`: `N_< <= q(p-1)^2/(8p)`, and `q(p-1)/p <= q - 1` reduces to `p <= q`.

Both hold because `q > p`. **Lemma L follows.** (`lemma_L.py`: 429 pairs `p <= 15, q < 60`, every step of this
argument checked, 0 failures; the bound also holds on `p <= 20, q < 200`.)

Lemma L is stronger than the general positive-braid bounds known to us (Feller, `-sigma > b_1/8`; Greene-Liechti,
`-sigma >= b_1/4`), but it is special to torus knots, where the count above is available.

## 2. Base case: torus knots

- p, q both odd: `det = 1 <= 1 + |sigma|`.
- q even (so p odd): `det = p`, and Lemma L gives `|sigma| >= (p-1)(q-1)/2 >= 3(p-1)/2` (as `q >= 4`), so
  `1 + |sigma| >= 1 + 3(p-1)/2 >= p`.
- p even (so q odd): `det = q`. For `p = 2`, `|sigma(T(2,q))| = q - 1`, so `1 + |sigma| = q = det`: equality. For
  `p >= 4`, Lemma L gives `|sigma| >= 3(q-1)/2 >= q - 1`.

## 3. Induction step

Let K be an L-space knot with `det(K) <= 1 + A`, `A = |sigma(K)| <= 2 g_K`, and let `K_{p,q}` be an L-space cable, so
`q >= p(2g_K - 1)`. Write `B = |sigma(T(p,q))|`. Signatures of positive torus knots and of K are both negative, so
(F2) gives `|sigma(K_{p,q})| = A + B` for p odd and `= B` for p even.

- **Case p even** (q odd). By (F1), (F3): `det(K_{p,q}) = det(T(p,q)) = q`. This is the base case computation above,
  which gives `q <= 1 + B`. Equality exactly when `p = 2`.
- **Case p, q both odd.** `det(K_{p,q}) = det(K) <= 1 + A <= 1 + A + B = 1 + |sigma(K_{p,q})|`.
- **Case p odd, q even.** `det(K_{p,q}) = p * det(K) <= p(1 + A)`, and the claim is `p(1+A) <= 1 + A + B`, i.e.
  `(p-1)(1+A) <= B`. Lemma L gives `B >= (p-1)(q-1)/2`, so it suffices that `q >= 2A + 3`, and since `A <= 2g_K` it
  suffices that `q >= 4 g_K + 3`. As `p >= 3`, the L-space condition gives `q >= 3(2g_K - 1) = 6g_K - 3`, which is
  `>= 4g_K + 3` exactly when `g_K >= 3`. The remaining cases are finite and explicit:
  - `g_K = 1`: `A <= 2`, so the requirement is `(p-1)*3 <= B`, and `q >= p`, q even. Only `(p,q) = (3,4)` and `(5,6)`
    are not already covered by `B >= (p-1)(q-1)/2`; there `B = 6 >= 6` and `B = 16 >= 12`.
  - `g_K = 2`: `A <= 4`, requirement `(p-1)*5 <= B`, `q >= 3p`, q even. The only uncovered pair is `(3,10)`, where
    `B = 14 >= 10`.

  (The three signature values are computed in `lemma_L.py`.)

**Theorem.** Every L-space knot that is an iterated torus knot satisfies `det <= 1 + |sigma|`. In particular K33 holds
for all torus knots and all algebraic knots. `induction_proof.py` also checks the step directly, with worst-case
`A = 2g_K` and `det(K) = 1 + A`, over `g_K <= 11`, `p <= 11` and the full L-space range of q: 0 failures.

## 4. What the proof does not cover, and where equality lives

The induction only reaches iterated torus knots. The hyperbolic L-space knots are untouched, and they are exactly
where the inequality is sharp: `det = 1 + |sigma|` for every Baker-Kegel `K_n`, `n = 1..25` (`families_fast.sage`),
which are hyperbolic and not braid positive. So the open part of K33 is not a technicality; it is the case with the
extremal examples.

A useful reformulation for that case (`proof_steps.py`, checked on 11,728 knots, 0 mismatches). For an L-space knot
with semigroup set S (complement of the g gaps in `[0, 2g)`),

    det = |2D + 1|,   D = #(odd gaps) - #(even gaps),

so K33 is equivalent to `|sigma| >= 2D` when `D >= 0` (and `|sigma| >= 2|D| - 2` when `D < 0`). The naive route
through `det <= #(terms of Delta)` fails: the implied lemma `|sigma| >= #terms - 1` is false on 401 of the 11,728
iterated torus knots, precisely the ones where K33 is tight.
