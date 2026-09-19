"""The congruence 1 + |sigma| - det = 0 (mod 4).

It holds for every knot: Murasugi's Delta_K(-1) = 1 mod 4 together with sign Delta_K(-1) = (-1)^(sigma/2).
The consequence used in the note is that a counterexample to K33 needs det >= |sigma| + 5, so the
inequality cannot fail narrowly.

Checked here on every L-space knot computed in this directory, which needs no external database. A knot
table can be passed with --table for an additional check on knots that are not L-space knots; it is
optional, and nothing in the note depends on it.
"""
import argparse
import csv
import json
from pathlib import Path

HERE = Path(__file__).parent
FAMILIES = ("census_lspace_fast.jsonl", "families_fast.jsonl", "onebridge.jsonl",
            "twisted_torus_sigma.jsonl")


def load(name):
    p = HERE / name
    if not p.exists():
        return []
    with open(p) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--table", help="optional CSV of knot invariants, with determinant and signature columns")
    a = ap.parse_args()

    out = {"families": {}, "table": None}
    total = failures = 0
    for f in FAMILIES:
        rs = load(f)
        if not rs:
            continue
        key = "signature_positive_chirality" if "signature_positive_chirality" in rs[0] else "signature"
        dkey = "det_seifert" if "det_seifert" in rs[0] else "det"
        m = [1 + abs(r[key]) - r[dkey] for r in rs]
        bad = sum(x % 4 != 0 for x in m)
        out["families"][f] = {"knots": len(rs), "congruence_failures": bad,
                              "equalities": sum(x == 0 for x in m),
                              "min_positive_margin": min([x for x in m if x] or [0])}
        total += len(rs)
        failures += bad
    out["l_space_knots"] = total
    out["l_space_failures"] = failures

    if a.table:
        rows = list(csv.DictReader(open(a.table)))
        keys = list(rows[0])
        col = lambda c: next(x for x in keys if x.split(":")[0] == c)
        n = bad = 0
        for r in rows:
            d, s = r[col("determinant")], r[col("signature")]
            if not d or not s or ".." in d or ".." in s:
                continue
            d, s = int(float(d)), int(float(s))
            n += 1
            bad += (1 + abs(s) - d) % 4 != 0
        out["table"] = {"source": a.table, "knots": n, "failures": bad}

    (HERE / "congruence.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
