# The lattice inequality, in Lean 4

`K33Lattice/Basic.lean` proves, with no `sorry`:

    for all integers 2 ≤ p < q,
    #{ (i,j) ∈ [1,p-1] × [1,q-1] : i/p + j/q < 1/2 }  ≤  (p-1)(q-1)/8

This is the combinatorial core of Lemma 1 of the note, the one step proved there from scratch rather
than cited. Coprimality of `p` and `q` is not needed.

`#print axioms K33Lattice.card_below_le` reports `propext`, `Classical.choice` and `Quot.sound` only.

What this does *not* formalise: the topology the lemma is used with — the Gordon–Litherland–Murasugi
lattice count for `σ(T(p,q))`, Litherland's cabling formula, the Hedden/Hom criterion. Mathlib has no
knot theory, so those stay citations in the note.

## Building

Pinned to Mathlib revision `0df444a360eaa60ab8c11dca51a86af692955474` with
`leanprover/lean4:v4.33.1`, as recorded in `lean-toolchain` and `lake-manifest.json`.

A Mathlib build is about 7 GB. If you already have one at this revision, point this project at it
instead of fetching another:

    mkdir -p .lake && ln -s /path/to/existing/.lake/packages .lake/packages
    lake build K33Lattice

Only your own files should compile; if thousands of Mathlib jobs build rather than replay, the manifest
or the toolchain does not match. Otherwise the usual `lake exe cache get && lake build K33Lattice`
applies, on a machine where no other project shares the packages directory.
