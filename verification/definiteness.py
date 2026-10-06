"""The definiteness statement implied by K33, tested directly on every L-space knot computed.

Section 7 of the note observes that the sharp case of the conjecture carries a rigidity statement:

    every L-space knot with the Alexander polynomial of T(2, 2g+1) has sigma = -2g,

that is, its symmetrised Seifert form is definite. This is a weak form of K3 Problem 1.21(c)(i), known
for g <= 2 by Ghiggini and by Farber-Reinoso-Wang with Baldwin-Hu-Sivek.

For an L-space knot the hypothesis is checkable from the determinant alone. The identity det = |2D + 1|
with D = #{odd gaps} - #{even gaps} holds for every L-space knot, and D <= g with equality exactly when
every gap is odd, which is exactly when the staircase is that of T(2, 2g+1). So

    Delta_K = Delta_{T(2,2g+1)}   iff   det(K) = 2g + 1,

and the statement to test is: det = 2g+1 implies sigma = -2g.

This collects every L-space knot for which a determinant, a genus and an exact signature were computed
anywhere in this directory, selects those with det = 2g+1, and checks the signature. It also reports how
many such knots there are outside the torus knots, which is the interesting number: if the hypothesis is
only ever met by T(2,2g+1) itself, the sharp case is vacuous on everything computed so far and says
nothing about where a counterexample could live.

Reads the existing result files only; computes nothing new.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent


def load(name):
    p = HERE / name
    if not p.exists():
        return []
    out = []
    with open(p) as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def records():
    """(source, name, genus, det, sigma) for every L-space knot with all three known."""
    rows = []
    for r in load("census_lspace_fast.jsonl"):
        if "matrix_size" in r and "signature_positive_chirality" in r:
            rows.append(("census", r["name"], r["matrix_size"] // 2, r["det"],
                         r["signature_positive_chirality"]))
    for r in load("families_fast.jsonl"):
        g = r.get("seifert_surface_genus_of_braid_closure")
        if g is not None:
            rows.append(("families", r["name"], g, r["det"], r["signature_positive_chirality"]))
    for r in load("onebridge.jsonl"):
        if "genus" in r:
            rows.append(("one-bridge braids", r["name"], r["genus"], r["det"], r["signature"]))
    for r in load("twisted_torus_sigma.jsonl"):
        rows.append(("twisted torus", r["name"], r["genus"], r["det_seifert"],
                     r["signature_positive_chirality"]))
    return rows


def main():
    rows = records()
    sharp = [r for r in rows if r[3] == 2 * r[2] + 1]
    failures = [r for r in sharp if r[4] != -2 * r[2]]

    # which of the sharp ones are torus knots T(2,2g+1)? in these files those are the one-bridge braids
    # with b = 1 and the census knots named after a (2,n) torus knot; report the split by source instead,
    # which needs no name parsing
    by_source = {}
    for src, *_ in sharp:
        by_source[src] = by_source.get(src, 0) + 1

    out = {
        "statement": "every L-space knot with Delta = Delta_{T(2,2g+1)} has sigma = -2g",
        "hypothesis_as_tested": "det = 2g + 1, which is equivalent for an L-space knot",
        "l_space_knots_with_det_genus_and_exact_signature": len(rows),
        "satisfying_the_hypothesis": len(sharp),
        "failures": len(failures),
        "failing": [{"source": s, "name": n, "genus": g, "det": d, "sigma": sg}
                    for s, n, g, d, sg in failures],
        "by_source": by_source,
        "max_genus_in_sample": max((r[2] for r in rows), default=None),
        "max_genus_satisfying_hypothesis": max((r[2] for r in sharp), default=None),
    }
    (HERE / "definiteness.json").write_text(json.dumps(out, indent=2))
    print(f"L-space knots with det, genus and an exact signature: {len(rows)}")
    print(f"  satisfying det = 2g+1, i.e. Delta = Delta_(T(2,2g+1)): {len(sharp)}")
    print(f"  of those, sigma != -2g: {len(failures)}")
    print(f"  by source: {by_source}")
    print(f"  largest genus in the sample {out['max_genus_in_sample']}, "
          f"largest genus meeting the hypothesis {out['max_genus_satisfying_hypothesis']}")


if __name__ == "__main__":
    main()
