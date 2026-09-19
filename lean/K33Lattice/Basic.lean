/-
# The lattice inequality behind Lemma L of the K33 note

For coprime integers `2 ≤ p < q`, the signature of the torus knot `T(p,q)` is `N_out - N_in`, counted
over the grid `[1, p-1] × [1, q-1]`, where a point is "in" when `1/2 < i/p + j/q < 3/2`
(Brieskorn; Gordon-Litherland-Murasugi). The involution `(i,j) ↦ (p-i, q-j)` exchanges the two
outside regions, so `N_out = 2 * N_lt` with

  `N_lt = #{(i,j) ∈ [1,p-1] × [1,q-1] : i/p + j/q < 1/2}`,

and `|σ(T(p,q))| ≥ g(T(p,q)) = (p-1)(q-1)/2` reduces to the purely arithmetic statement proved here:

  `N_lt ≤ (p-1)(q-1)/8`.

That is the one step of the K33 note proved from scratch rather than cited, which is why it is the
first thing worth machine-checking. The knot theory stays outside: nothing below mentions a knot.

The proof, column by column:

* the points in column `i` are the `j ≥ 1` with `j < f i` where `f i = q/2 - i*q/p`, so there are
  `⌈f i⌉ - 1 ≤ f i` of them when `f i > 0`, and none otherwise;
* `f i > 0` exactly for `i < p/2`, so summing the columns gives
  `N_lt ≤ (q/(2p)) * ∑_{i < p/2} (p - 2i) = q*(p-2)/8` for even `p`, `q*(p-1)^2/(8p)` for odd `p`;
* `q*(p-2)/8 ≤ (p-1)*(q-1)/8` iff `q ≥ p - 1`, and `q*(p-1)^2/(8p) ≤ (p-1)*(q-1)/8` iff `p ≤ q`.
  Both hold because `p < q`.

The Python check `K33/verification/lemma_L.py` verifies every one of these steps on 429 coprime pairs
and the conclusion on 2166; this file is the unconditional version of the same argument.

## State

Complete. `card_below_le` is proved with no `sorry`, and `#print axioms` at the end of the file reports
only `propext`, `Classical.choice` and `Quot.sound`, so nothing is assumed beyond Lean's own axioms.
Coprimality of `p` and `q` is not needed; only `2 ≤ p < q`.

The supporting steps, each also complete: `card_below_eq_sum_columns` (the grid count is the sum of its
columns), `column_card_le` (a column has at most `max 0 (f i)` points, via `Nat.lt_ceil` and
`Nat.ceil_lt_add_one`), `max_f_eq_ite` (the cut at `(p-1)/2` in both parities), `sum_Icc_cast` (Gauss),
`sum_max_f` (the closed form), and `even_case` and `odd_case` (the two final comparisons).

What this does and does not certify: the arithmetic of Lemma L is now machine-checked, unconditionally.
The topology it is used with — the Gordon-Litherland-Murasugi lattice count for `σ(T(p,q))`, Litherland's
cabling formula, the Hedden/Hom criterion — is cited in the note and is not formalised here, because
Mathlib has no knot theory.
-/
import Mathlib

namespace K33Lattice

open Finset

variable (p q : ℕ)

/-- The lattice points below the line `i/p + j/q = 1/2` inside the grid `[1,p-1] × [1,q-1]`. -/
def below : Finset (ℕ × ℕ) :=
  (Icc 1 (p - 1) ×ˢ Icc 1 (q - 1)).filter fun ij => (ij.1 : ℚ) / p + (ij.2 : ℚ) / q < 1 / 2

/-- The column height: in column `i`, the points counted are the `j ≥ 1` with `j < f p q i`. -/
noncomputable def f (i : ℕ) : ℚ := (q : ℚ) / 2 - (i : ℚ) * q / p

/-- Column `i` of `below`, as a finset of second coordinates. -/
def column (i : ℕ) : Finset ℕ :=
  (Icc 1 (q - 1)).filter fun j => (i : ℚ) / p + (j : ℚ) / q < 1 / 2

theorem card_below_eq_sum_columns :
    (below p q).card = ∑ i ∈ Icc 1 (p - 1), (column p q i).card := by
  have h : below p q = (Icc 1 (p - 1)).biUnion fun i => {i} ×ˢ column p q i := by
    ext ⟨a, b⟩
    simp only [below, column, mem_filter, Finset.mem_product, mem_biUnion, mem_singleton]
    grind
  rw [h, card_biUnion]
  · exact Finset.sum_congr rfl fun i _ => by simp
  · intro x _ y _ hxy
    simp only [Finset.disjoint_left, Finset.mem_product, mem_singleton]
    grind

/-- A column is empty once `f p q i ≤ 0`, that is once `2 * i ≥ p`. -/
theorem column_card_le (hp : 0 < p) (hq : 0 < q) (i : ℕ) :
    ((column p q i).card : ℚ) ≤ max 0 (f p q i) := by
  have hq' : (0 : ℚ) < q := by exact_mod_cast hq
  have hp' : (0 : ℚ) < p := by exact_mod_cast hp
  -- the defining condition of a column is exactly `(j : ℚ) < f p q i`
  have hmem : ∀ j ∈ column p q i, (j : ℚ) < f p q i := by
    intro j hj
    rw [column, mem_filter] at hj
    have h1 := hj.2
    have h2 : (j : ℚ) / q < 1 / 2 - (i : ℚ) / p := by linarith
    have h3 : (j : ℚ) < (1 / 2 - (i : ℚ) / p) * q := by
      calc (j : ℚ) = (j : ℚ) / q * q := by field_simp
        _ < (1 / 2 - (i : ℚ) / p) * q := mul_lt_mul_of_pos_right h2 hq'
    have h4 : (1 / 2 - (i : ℚ) / p) * q = (q : ℚ) / 2 - (i : ℚ) * q / p := by
      field_simp
    rw [f]
    linarith
  -- so the column sits inside `Ico 1 ⌈f⌉₊`
  have hsub : column p q i ⊆ Ico 1 ⌈f p q i⌉₊ := by
    intro j hj
    have h1 : 1 ≤ j := by
      rw [column, mem_filter, mem_Icc] at hj; exact hj.1.1
    exact mem_Ico.2 ⟨h1, Nat.lt_ceil.2 (hmem j hj)⟩
  have hcard : (column p q i).card ≤ ⌈f p q i⌉₊ - 1 := by
    have := card_le_card hsub
    simpa [Nat.card_Ico] using this
  by_cases hf : f p q i ≤ 0
  · have hz : ⌈f p q i⌉₊ = 0 := Nat.ceil_eq_zero.2 hf
    rw [hz] at hcard
    simp only [Nat.zero_sub, Nat.le_zero] at hcard
    rw [hcard, max_eq_left hf]
    simp
  · push_neg at hf
    have hceil : 1 ≤ ⌈f p q i⌉₊ := Nat.one_le_ceil_iff.2 hf
    have hlt : ((⌈f p q i⌉₊ : ℚ)) < f p q i + 1 := Nat.ceil_lt_add_one hf.le
    have : ((column p q i).card : ℚ) ≤ ((⌈f p q i⌉₊ : ℚ)) - 1 := by
      have := (Nat.cast_le (α := ℚ)).2 hcard
      rwa [Nat.cast_sub hceil, Nat.cast_one] at this
    rw [max_eq_right hf.le]
    linarith

/-- Gauss' formula in the form needed below. -/
theorem sum_Icc_cast (m : ℕ) : ∑ i ∈ Icc 1 m, (i : ℚ) = m * (m + 1) / 2 := by
  induction m with
  | zero => simp
  | succ n ih =>
      rw [Finset.sum_Icc_succ_top (by omega : 1 ≤ n + 1), ih]
      push_cast
      ring

/-- A column is nonempty exactly for `i ≤ (p-1)/2`: `f p q i ≥ 0` iff `2*i ≤ p`, and at the boundary
`2*i = p` the value is `0`, so the cut can be taken at `(p-1)/2` in both parities. -/
theorem max_f_eq_ite (hp : 2 ≤ p) (hq : 0 < q) (i : ℕ) :
    max 0 (f p q i) = if i ≤ (p - 1) / 2 then f p q i else 0 := by
  have hp0 : (0 : ℚ) < p := by exact_mod_cast (by omega : 0 < p)
  have hq0 : (0 : ℚ) < q := by exact_mod_cast hq
  have hf : f p q i = (q : ℚ) * ((p : ℚ) - 2 * i) / (2 * p) := by
    rw [f]; field_simp
  split_ifs with h
  · have h2 : 2 * i ≤ p := by omega
    have h2q : 2 * (i : ℚ) ≤ (p : ℚ) := by exact_mod_cast h2
    have hnn : 0 ≤ f p q i := by
      rw [hf]; apply div_nonneg (by nlinarith) (by linarith)
    exact max_eq_right hnn
  · have h2 : p ≤ 2 * i := by omega
    have h2q : (p : ℚ) ≤ 2 * (i : ℚ) := by exact_mod_cast h2
    have hnp : f p q i ≤ 0 := by
      rw [hf]; apply div_nonpos_of_nonpos_of_nonneg (by nlinarith) (by linarith)
    exact max_eq_left hnp

/-- `∑_{i=1}^{p-1} max 0 (f p q i)` in closed form, split on the parity of `p`. -/
theorem sum_max_f (hp : 2 ≤ p) (hq : 0 < q) :
    ∑ i ∈ Icc 1 (p - 1), max 0 (f p q i)
      = if p % 2 = 0 then (q : ℚ) * (p - 2) / 8 else (q : ℚ) * (p - 1) ^ 2 / (8 * p) := by
  have hp0 : (0 : ℚ) < p := by exact_mod_cast (by omega : 0 < p)
  rw [Finset.sum_congr rfl fun i _ => max_f_eq_ite p q hp hq i]
  -- the columns past (p-1)/2 contribute nothing, so the sum runs over Icc 1 m
  have hfilter : ((Icc 1 (p - 1)).filter fun i => i ≤ (p - 1) / 2) = Icc 1 ((p - 1) / 2) := by
    ext x
    simp only [mem_filter, mem_Icc]
    omega
  rw [← Finset.sum_filter, hfilter]
  -- Gauss
  have hlin : ∀ i : ℕ, f p q i = (q : ℚ) / 2 - ((q : ℚ) / p) * i := by
    intro i; rw [f]; field_simp
  rw [Finset.sum_congr rfl fun i _ => hlin i, Finset.sum_sub_distrib, ← Finset.mul_sum,
      sum_Icc_cast, Finset.sum_const, Nat.card_Icc, nsmul_eq_mul]
  set m := (p - 1) / 2 with hm
  push_cast
  -- substitute the parity relation between m and p
  by_cases hpar : p % 2 = 0
  · rw [if_pos hpar]
    have h : 2 * m + 2 = p := by omega
    have hq' : 2 * (m : ℚ) + 2 = (p : ℚ) := by exact_mod_cast h
    have : (m : ℚ) = ((p : ℚ) - 2) / 2 := by linarith
    rw [this]
    field_simp
    ring
  · rw [if_neg hpar]
    have h : 2 * m + 1 = p := by omega
    have hq' : 2 * (m : ℚ) + 1 = (p : ℚ) := by exact_mod_cast h
    have : (m : ℚ) = ((p : ℚ) - 1) / 2 := by linarith
    rw [this]
    field_simp
    ring

/-- The even case of the final comparison: `q*(p-2)/8 ≤ (p-1)*(q-1)/8` when `p - 1 ≤ q`. -/
theorem even_case (hp : 2 ≤ p) (hpq : p < q) :
    (q : ℚ) * (p - 2) / 8 ≤ ((p : ℚ) - 1) * ((q : ℚ) - 1) / 8 := by
  have hp' : (2 : ℚ) ≤ p := by exact_mod_cast hp
  have hpq' : (p : ℚ) < q := by exact_mod_cast hpq
  rw [div_le_div_iff_of_pos_right (by norm_num : (0:ℚ) < 8)]
  nlinarith

/-- The odd case: `q*(p-1)^2/(8p) ≤ (p-1)*(q-1)/8` when `p ≤ q`. -/
theorem odd_case (hp : 2 ≤ p) (hpq : p < q) :
    (q : ℚ) * ((p : ℚ) - 1) ^ 2 / (8 * p) ≤ ((p : ℚ) - 1) * ((q : ℚ) - 1) / 8 := by
  have hp' : (2 : ℚ) ≤ p := by exact_mod_cast hp
  have hpq' : (p : ℚ) < q := by exact_mod_cast hpq
  have hp0 : (0 : ℚ) < p := by linarith
  -- the difference factors as (p-1)(q-p)/(8p), which is nonnegative because 1 < p < q
  have key : ((p : ℚ) - 1) * ((q : ℚ) - 1) / 8 - (q : ℚ) * ((p : ℚ) - 1) ^ 2 / (8 * p)
      = ((p : ℚ) - 1) * ((q : ℚ) - (p : ℚ)) / (8 * p) := by
    field_simp
    ring
  have hnn : 0 ≤ ((p : ℚ) - 1) * ((q : ℚ) - (p : ℚ)) / (8 * p) :=
    div_nonneg (mul_nonneg (by linarith) (by linarith)) (by linarith)
  linarith

/-- **The lattice inequality.** For `2 ≤ p < q`, the number of grid points strictly below the line
`i/p + j/q = 1/2` is at most `(p-1)(q-1)/8`. Coprimality is not needed. -/
theorem card_below_le (hp : 2 ≤ p) (hpq : p < q) :
    ((below p q).card : ℚ) ≤ ((p : ℚ) - 1) * ((q : ℚ) - 1) / 8 := by
  have hp0 : 0 < p := by omega
  have hq0 : 0 < q := by omega
  calc ((below p q).card : ℚ)
      = ∑ i ∈ Icc 1 (p - 1), ((column p q i).card : ℚ) := by
        rw [card_below_eq_sum_columns]; push_cast; ring
    _ ≤ ∑ i ∈ Icc 1 (p - 1), max 0 (f p q i) :=
        Finset.sum_le_sum fun i _ => column_card_le p q hp0 hq0 i
    _ = if p % 2 = 0 then (q : ℚ) * (p - 2) / 8 else (q : ℚ) * (p - 1) ^ 2 / (8 * p) :=
        sum_max_f p q hp hq0
    _ ≤ ((p : ℚ) - 1) * ((q : ℚ) - 1) / 8 := by
        split_ifs with h
        · exact even_case p q hp hpq
        · exact odd_case p q hp hpq

end K33Lattice

-- No `sorry` anywhere below the main theorem: this prints the three standard axioms only.
#print axioms K33Lattice.card_below_le
