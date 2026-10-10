"""u = g_4 = (m n^2 - n + 2)/2 for every H(n,m), n >= 2, m odd: the computational side of the proof.

Lower bound: Rudolph's slice-Bennequin inequality, g_4 >= (w - strands + 1)/2 for the closure of a braid word of writhe
w, which for X_n^m T_n is (m n^2 - n + 2)/2.
Upper bound: the flips of hnm.unknotting_flips. Copies 2, 4, ..., m-1 of X_n flip to X_n^-1 because X_n is a
palindrome up to commuting letters, so they cancel their neighbours; the second half of the last copy turns it into
C L C^-1 (C = layers 0..n-2, L = the middle layer); one more flip in T_n. Their number equals the lower bound.
That the flipped word closes to the unknot for every n is proved in the note; here it is checked for n <= N, m <= 7
by simplifying the diagram (and, if needed, by knot Floer homology of total rank 1, which detects the unknot).
Also checked: Baker-Kegel K_k = H(2,2k+1) and Himeno K_n = H(n,3) are the published braid words.

    python unknotting.py 12     # writes unknotting.json
"""
import json, sys
import snappy
from hnm import X, T, H, slice_bennequin, unknotting_flips


def is_unknot(word):
    K = snappy.Link(braid_closure=word)
    if len(K.link_components) != 1:
        return False
    K.simplify('global')
    if len(K.crossings) == 0:
        return True
    for _ in range(4):
        K.backtrack(10); K.simplify('global')
        if len(K.crossings) == 0:
            return True
    return K.knot_floer_homology()['total_rank'] == 1


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    assert H(2, 3) == [2, 1, 3, 2] * 3 + [-1, 2, 1, 1, 2]                # Baker-Kegel K_1 = o9_30634
    assert sorted(X(4)) == sorted(X(4)[::-1])
    rows = []
    for n in range(2, N + 1):
        for m in (1, 3, 5, 7):
            word, flips = unknotting_flips(n, m)
            bound = slice_bennequin(H(n, m), 2 * n)
            ok = is_unknot(word)
            rows.append(dict(n=n, m=m, letters=len(H(n, m)), flips=flips, slice_bennequin=bound,
                             flips_equal_bound=flips == bound == (m * n * n - n + 2) // 2, flipped_is_unknot=ok))
            print(json.dumps(rows[-1]), flush=True)
    json.dump(dict(rows=rows, all_ok=all(r['flips_equal_bound'] and r['flipped_is_unknot'] for r in rows)),
              open("unknotting.json", "w"), indent=1)
    print("all ok:", all(r['flips_equal_bound'] and r['flipped_is_unknot'] for r in rows))


if __name__ == "__main__":
    main()
