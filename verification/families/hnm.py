"""The two-parameter family H(n,m), n >= 2, m odd: the closure of the 2n-braid X_n^m T_n, where

  X_n = L_0 L_1 ... L_{n-1} L_{n-2} ... L_0,   L_k = s_{n-k} s_{n-k+2} ... s_{n+k}   (letters of a layer commute),
  T_n = s_1^-1 ... s_{n-1}^-1 . s_n s_{n-1} ... s_1 . s_1 s_2 ... s_n.

X_n is the n-cable of a positive crossing of two n-strand bundles. Himeno's knots (arXiv:2506.22934) are H(n,3);
Baker and Kegel's knots K_k (arXiv:2203.12013) are H(2,2k+1), since X_2 = s2 s1 s3 s2 and T_2 = s1^-1 s2 s1 s1 s2."""


def layer(n, k):
    return list(range(n - k, n + k + 1, 2))


def X(n):
    up = [g for k in range(n) for g in layer(n, k)]
    down = [g for k in range(n - 2, -1, -1) for g in reversed(layer(n, k))]
    return up + down


def T(n):
    return [-i for i in range(1, n)] + list(range(n, 0, -1)) + list(range(1, n + 1))


def H(n, m):
    return X(n) * m + T(n)


def slice_bennequin(word, strands):
    """Rudolph's slice-Bennequin bound (w - strands + 1)/2 <= g_4 of the closure, w the writhe of the word."""
    w = sum(1 if x > 0 else -1 for x in word)
    return (w - strands + 1) // 2


def unknotting_flips(n, m):
    """The explicit unknotting: flip every letter of copies 2, 4, ..., m-1 of X_n, the second half (layers n-2..0) of
    the last copy, and the letter s_n of T_n at offset n-1. Returns (flipped word, number of flips)."""
    x = X(n)
    half = n * (n + 1) // 2                       # layers 0..n-1
    word, flips = [], 0
    for c in range(1, m + 1):
        if c % 2 == 0:
            word += [-g for g in x]; flips += len(x)
        elif c == m:
            word += x[:half] + [-g for g in x[half:]]; flips += len(x) - half
        else:
            word += x
    t = T(n); j = n - 1
    assert t[j] == n
    word += t[:j] + [-t[j]] + t[j + 1:]; flips += 1
    return word, flips
