"""u = g for the L-space (2,q)-cables of T(2,2k+1) that are not positive braids.

The (2,q)-cable of T(2,2k+1) is the closure of X_2^(2k+1) s1^e, e = q - 2(2k+1), and it is an L-space knot exactly
when q >= 2(2k-1) (Hedden; Hom), i.e. e in {-3, -1, 1, 3, ...}. For e >= 1 the word is positive (Rudolph).
e = -1: flip k palindromic copies of X_2 (4k flips) to reach X_2 s1^-1, whose closure is the unknot; g = 4k.
e = -3: flip k-1 copies (4k-4 flips) to reach X_2^3 s1^-3, the (2,3)-cable of T(2,3), unknotted by flipping the
first three letters; g = 4k-1. Here: flips = genus (knot Floer homology) and the flipped word closes to the unknot.

    python cables.py 8     # writes cables.json
"""
import json, sys
import snappy
from unknotting import is_unknot

X2 = [2, 1, 3, 2]


def flipped(k, e):
    w = []
    for c in range(2 * k + 1):
        cancel = c % 2 == 1 and (e == -1 or c < 2 * k - 1)
        w += [-x for x in X2] if cancel else X2
    flips = 4 * k if e == -1 else 4 * (k - 1)
    if e == -3:
        s = 4 * (2 * k - 2)
        w[s:s + 3] = [-x for x in w[s:s + 3]]; flips += 3
    return w + [-1] * abs(e), flips


rows = []
for k in range(1, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 9):
    for e in (-1, -3):
        word = X2 * (2 * k + 1) + [-1] * abs(e)
        L = snappy.Link(braid_closure=word); L.simplify('global')
        h = L.knot_floer_homology()
        fw, flips = flipped(k, e)
        rows.append(dict(k=k, q=2 * (2 * k + 1) + e, genus=h['seifert_genus'], L_space=h['L_space_knot'], flips=flips,
                         flips_equal_genus=flips == h['seifert_genus'], flipped_is_unknot=is_unknot(fw)))
        print(json.dumps(rows[-1]), flush=True)
json.dump(dict(rows=rows, all_ok=all(r['L_space'] and r['flips_equal_genus'] and r['flipped_is_unknot'] for r in rows)),
          open("cables.json", "w"), indent=1)
