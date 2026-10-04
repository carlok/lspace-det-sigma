# Data provenance, and what is deliberately absent

## The candidate came from KnotInfo, and none of KnotInfo is here

The inequality was found by fitting linear relations to KnotInfo, restricted to prime knots with 3 to
13 crossings, accessed on 14 September 2026. Cite it as its maintainers ask:

> C. Livingston and A. H. Moore, *KnotInfo: Table of Knot Invariants*, knotinfo.org, September 2026.

The note follows KnotInfo's chirality convention: the right-handed trefoil has `σ = -2`, `s = 2`,
`τ = 1`.

No KnotInfo data is reproduced in this repository. Every knot tested here is built from a braid word, a
cabling formula or a pretzel presentation, and every invariant is computed. Where a script names a
KnotInfo knot, it is naming a knot, not quoting a row: `iterated.py` compares its output against six
classical determinant and signature values for torus knots and cables, which are textbook facts.

Why none of it is here: KnotInfo asks to be cited, and a copy of the database goes out of date. Read
it from https://knotinfo.org.

## The Baker–Kegel braid words are not here

`census_lspace_fast.sage`, `census_sage_native.sage`, `exact_census.py` and `braid_identity.py` read
`bk_lspace_braids.json` and `bk_census_braids.json`, the braid words of the 632 census L-space knots.
Those are the table in the appendix of

> K. L. Baker, M. Kegel, *Census L-space knots are braid positive, except for one that is not*,
> Algebr. Geom. Topol. 24 (2024); arXiv:2203.12013.

Reproducing a published table of 632 words is the authors' to permit, not ours to assume, so the files
are absent and the scripts will not run without them. What *is* here is the output of our own
computations on those knots — names, determinants, exact signatures — in `census_lspace_fast.jsonl`,
`census_sage_native.jsonl` and `exact_census.jsonl`. To rerun from scratch, take the words from the
paper's appendix.

`census_matrices.json`, a 26 MB dump of the Seifert matrices of those closures, is left out for size.
`exact_census.py` regenerates it.

## Everything else is computed here

The twisted torus family, the unbiased random search, the one-bridge braids, the iterated torus knots,
the Baker–Kegel and Himeno families as *generated from their published braid word formulas* (a formula,
not a table), and the alternating pretzels: all built and measured by the scripts in `verification/`.
Where a family's membership of the L-space class matters, it is decided by each knot's own knot Floer
homology rather than by citing a classification.
