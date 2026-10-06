"""How many distinct knots are in each generated family?

The twisted torus family, the one-bridge braids and the random search were deduplicated by diagram (the PD code of the
simplified diagram), not by knot type. Different parameters or different braid words often close to the same knot:
B(4,2,1) and B(5,2,1) are both the trefoil, and the random search finds T(2,5) many times over. So their record counts
are counts of diagrams. This measures how many distinct knots, up to mirror image, they contain.

  hyperbolic:      the knot is determined by its complement up to mirror (Gordon-Luecke), and SnapPy's isometry
                   signature is a complete invariant of the hyperbolic complement, so equal signatures mean the same
                   knot and different signatures different knots. The count is exact.
  non-hyperbolic:  keyed by the knot Floer homology (Alexander and Maslov gradings, up to the mirror symmetry). Two
                   different knots can share it, so this count is a lower bound on the number of distinct knots.

Each hyperbolic representative is also looked up in SnapPy's censuses, which says whether a family adds any hyperbolic
knot beyond the census L-space knots already tested. The census (named census manifolds) and the iterated torus knots
(distinct cabling sequences) are distinct by construction and are not recounted here.
"""
import json
import sys
import time
from pathlib import Path

import snappy
from knot_floer_homology import pd_to_hfk

HERE = Path(__file__).parent


def twisted_word(p, q, r, s):
    full, part = list(range(1, p)), list(range(1, r))
    return full * q + (part * s if s > 0 else [-x for x in reversed(part)] * (-s))


def onebridge_word(w, b, t):
    return list(range(b, 0, -1)) + list(range(w - 1, 0, -1)) * t


def key_of(word):
    """(kind, key) for the knot closing this braid word."""
    K = snappy.Link(braid_closure=[int(x) for x in word])
    K.simplify("global")
    M = K.exterior()
    # hyperbolicity read off one triangulation depends on the diagram, so retriangulate a few times:
    # the knot counts as hyperbolic if any triangulation gives a positively oriented solution
    hyp = False
    for _ in range(6):
        if M.solution_type() == "all tetrahedra positively oriented" and M.volume() > 0.9:
            hyp = True
            break
        M.randomize()
    if hyp:
        for _ in range(6):
            try:
                return "hyperbolic", M.isometry_signature()
            except Exception:
                M.randomize()
    h = pd_to_hfk(K.PD_code(KnotTheory=True))
    g = sorted(h["ranks"].items())
    mirror = sorted(((-a, -m), r) for (a, m), r in h["ranks"].items())
    # normalise the bigradings up to an overall Maslov shift, then up to mirror
    def norm(items):
        m0 = min(m for (a, m), _ in items)
        return tuple(((a, m - m0), r) for (a, m), r in items)
    return ("hyperbolic-unresolved" if hyp else "non-hyperbolic"), min(norm(g), norm(mirror))


class Slow(Exception):
    pass


def _alarm(signum, frame):
    raise Slow()


def family(name, records, per_knot=20):
    """Distinct knots in one family. A knot whose isometry signature takes longer than per_knot seconds is counted
    as unresolved, so the distinct count is then a lower bound and says so."""
    import signal
    signal.signal(signal.SIGALRM, _alarm)
    t0 = time.time()
    keys, thin_keys, unresolved = {}, set(), 0
    for word, rec in records:
        signal.alarm(per_knot)
        try:
            kind, k = key_of(word)
        except (Slow, RuntimeError, ValueError):   # alarm surfacing from Cython; HFK refusing a diagram of girth > 20
            unresolved += 1
            continue
        finally:
            signal.alarm(0)
        keys.setdefault((kind, k), dict(rec, word=word))
        if rec.get("thin"):
            thin_keys.add((kind, k))
    by_kind = {}
    for kind, _ in keys:
        by_kind[kind] = by_kind.get(kind, 0) + 1
    # every hyperbolic representative is looked up in SnapPy's censuses
    census, not_census = 0, []
    for (kind, k), rec in keys.items():
        if kind != "hyperbolic":
            continue
        M = snappy.Link(braid_closure=[int(x) for x in rec["word"]]).exterior()
        ids = []
        for _ in range(6):
            try:
                ids = [str(x) for x in M.identify()]
                if ids:
                    break
            except Exception:
                pass
            M.randomize()
        if ids:
            census += 1
        else:
            not_census.append(rec.get("name"))
    out = {"family": name, "records": len(records), "distinct": len(keys), "distinct_by_kind": by_kind,
           "distinct_hyperbolic_in_census": census, "distinct_hyperbolic_not_in_census": not_census,
           "distinct_thin": len(thin_keys),
           "thin_genera": sorted({keys[k]["genus"] for k in thin_keys if "genus" in keys[k]}),
           "unresolved_timeouts": unresolved, "seconds": round(time.time() - t0)}
    print(json.dumps(out), flush=True)
    return out


def main():
    only = set(sys.argv[1:])
    results = []
    tt = [json.loads(l) for l in open(HERE / "twisted_torus_sigma.jsonl")]
    if not only or "twisted" in only: results.append(family("twisted torus", [
        (twisted_word(r["p"], r["q"], r["r"], r["s"]), {"name": r["name"], "genus": r["genus"], "thin": r["det_seifert"] == 2 * r["genus"] + 1}) for r in tt]))
    ob = [json.loads(l) for l in open(HERE / "onebridge.jsonl")]
    if not only or "onebridge" in only: results.append(family("one-bridge braids", [
        (onebridge_word(r["w"], r["b"], r["t"]), {"name": r["name"], "genus": r["genus"], "thin": r["det"] == 2 * r["genus"] + 1}) for r in ob]))
    words = {json.loads(l)["name"]: json.loads(l)["braid_word"] for l in open(HERE / "random_lspace.jsonl")}
    rs = [json.loads(l) for l in open(HERE / "random_lspace_sigma.jsonl")]
    if not only or "random" in only: results.append(family("random search", [
        (words[r["name"]], {"name": r["name"], "genus": r["genus"], "thin": r["det_seifert"] == 2 * r["genus"] + 1}) for r in rs]))
    out = HERE / "distinct_knots.json"
    prev = {r["family"]: r for r in (json.loads(out.read_text()) if out.exists() else [])}
    prev.update({r["family"]: r for r in results})
    out.write_text(json.dumps(list(prev.values()), indent=2))


if __name__ == "__main__":
    main()
