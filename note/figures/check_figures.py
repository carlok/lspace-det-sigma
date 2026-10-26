"""Checks that the figures show what the note proves. Run with SnapPy's Python.

1. The PD code of the drawn H(2,3), built from make_figures' crossing convention, is the knot SnapPy builds from the
   braid word, with the same chirality, and is census o9_30634 (same tau, so same chirality; signature needs Sage).
2. The drawn diagram with the circled crossings changed simplifies to the unknot.
3. Step 4 in the drawing's convention: after Step 2 and Step 3, each strand A_i with i >= 2, followed once around the
   closed braid from its crossing in the middle layer L, lies on the same side of every strand it meets, so it can be
   lifted off. Prints which side, so the email can say it in the picture's terms."""

import sys

import snappy

from make_figures import H, X, changed_letters, unknotting_flips


def pd_code(word):
    """PD code of the drawn closed braid: strands run left to right, position 1 at the bottom, and in a positive
    letter the falling strand (from position i+1) is over. Edges are numbered along the knot."""
    n_letters, labels = len(word), {}
    label, p, k = 1, 1, 0
    for _ in range(2 * n_letters):
        while abs(word[k]) not in (p, p - 1):
            k = (k + 1) % n_letters
        side = "lo" if abs(word[k]) == p else "hi"
        labels[(k, side, "in")] = label
        label += 1
        labels[(k, side, "out")] = label
        p = p + 1 if side == "lo" else p - 1
        k = (k + 1) % n_letters
    while k != 0:                                                   # run on to the left end of the braid
        assert abs(word[k]) not in (p, p - 1), "a crossing met three times"
        k = (k + 1) % n_letters
    assert p == 1, "not a knot: the walk did not close"
    wrap = lambda c: 1 if c == 2 * n_letters + 1 else c
    pd = []
    for k, g in enumerate(word):
        il, ol, ih, oh = (wrap(labels[(k, s, d)]) for s, d in (("lo", "in"), ("lo", "out"), ("hi", "in"), ("hi", "out")))
        pd.append((il, oh, ol, ih) if g > 0 else (ih, il, oh, ol))
    return pd


def side_of_lifted_strands(n):
    """Step 4 on the word after Steps 2 and 3 (m = 1; for larger m Step 1 has already cancelled the other copies)."""
    word, _ = unknotting_flips(n, 1)
    middle = range(n * (n - 1) // 2, n * (n - 1) // 2 + n)       # the letters of L_{n-1}
    out = {}
    for a in range(2, n + 1):
        p, k = a, 0
        while not (k in middle and abs(word[k]) in (p, p - 1)):
            if abs(word[k]) in (p, p - 1):
                p = p + 1 if abs(word[k]) == p else p - 1
            k += 1
        start = k
        p = p + 1 if abs(word[k]) == p else p - 1
        k = (k + 1) % len(word)
        sides = []
        while k != start:
            g = word[k]
            if abs(g) in (p, p - 1):
                rising = abs(g) == p
                over = (g > 0) != rising                          # positive letter: the falling strand is over
                sides.append("over" if over else "under")
                p = p + 1 if rising else p - 1
            k = (k + 1) % len(word)
        back_at_crossing = abs(word[start]) in (p, p - 1)
        out[a] = (sorted(set(sides)), len(sides), back_at_crossing)
    return out


def main():
    word = H(2, 3)
    drawn = snappy.Link(pd_code(word))
    ref = snappy.Link(braid_closure=word)
    writhe = sum(c.sign for c in drawn.crossings)
    hd, hr = drawn.knot_floer_homology(), ref.knot_floer_homology()
    print("drawn H(2,3): crossings", len(drawn.crossings), "writhe", writhe, "tau", hd["tau"], "genus",
          hd["seifert_genus"], "L-space", hd["L_space_knot"], "| SnapPy braid closure: tau", hr["tau"])
    assert hd["tau"] == hr["tau"] == hd["seifert_genus"] == 6, "chirality differs from SnapPy's closure"
    assert writhe == sum(1 if g > 0 else -1 for g in word), "drawn crossings are not right-handed for positive letters"
    E = drawn.exterior()
    print("isometric to SnapPy's closure:", bool(E.is_isometric_to(ref.exterior())), "| identify:", E.identify())

    flipped, _ = unknotting_flips(2, 3)
    assert changed_letters(word, flipped)
    u = snappy.Link(pd_code(flipped))
    u.simplify("global")
    print("drawn diagram with the circled crossings changed: crossings after simplify =", len(u.crossings))

    for n in (2, 3, 4, 5):
        res = side_of_lifted_strands(n)
        print(f"n={n}: strand A_i -> (sides met, crossings met, back at its L crossing):", res)
        assert all(sides in ([], ["over"]) and back for sides, _, back in res.values()), "Step 4 fails in the drawing"
    return 0


if __name__ == "__main__":
    sys.exit(main())
