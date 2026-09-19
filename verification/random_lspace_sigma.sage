"""Stage B for the unbiased search: exact signatures for the random L-space knots, then the K33 check.

Reads random_lspace.jsonl, written in the SnapPy environment, where each knot's own knot Floer homology
decided that it is an L-space knot. For each, the braid closure is rebuilt in Sage, the Seifert matrix V
of the standard Seifert surface is taken, and the signature of V + V^T is computed exactly by congruence
diagonalisation over Q (exact_signature.py). No floating point.

Chirality as elsewhere: K33 is stated for the positive chirality, where an L-space knot has tau = g > 0,
so a knot with tau < 0 is the mirror and its signature is negated before the comparison.

Two cross-checks per knot, both hard failures rather than silent disagreements: the determinant from the
Seifert matrix against the determinant read off the Alexander polynomial in stage A, and the mod 4
congruence 1 + |sigma| - det = 0, which holds for every knot and is what caught the bug in the 2x2 branch
of exact_signature.py.

Shortest braid words first, with a wall-clock cap, so a partial run is still a valid sample.

    sage random_lspace_sigma.sage [minutes]
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from exact_signature import signature as exact_signature

HERE = Path(__file__).parent
jd = lambda o: json.dumps(o, default=int)
MINUTES = float(sys.argv[1]) if len(sys.argv) > 1 else 25.0

records = [json.loads(l) for l in open(HERE / "random_lspace.jsonl") if l.strip()]
records.sort(key=lambda r: (len(r["braid_word"]), r["crossings"]))
out = open(HERE / "random_lspace_sigma.jsonl", "w")

deadline = time.time() + 60 * MINUTES
violations, det_mismatch, cong_fail = [], [], []
n = 0
for rec in records:
    if time.time() > deadline:
        break
    w = [int(x) for x in rec["braid_word"]]
    nstrands = max(abs(x) for x in w) + 1
    K = Link(BraidGroup(nstrands)([int(x) for x in w]))
    V = K.seifert_matrix()
    S = V + V.transpose()
    sig = exact_signature([[int(S[i][j]) for j in range(S.ncols())] for i in range(S.nrows())])
    det = int(abs(S.det()))
    sig_pos = sig if rec["tau"] > 0 else -sig
    if det != rec["det"]:
        det_mismatch.append({"name": rec["name"], "seifert": det, "alexander": rec["det"]})
    if (1 + abs(sig_pos) - det) % 4 != 0:
        cong_fail.append({"name": rec["name"], "sigma": sig_pos, "det": det})
    bound = 1 - sig_pos
    holds = det <= bound
    r = dict(rec)
    r.pop("braid_word", None)
    r.update(signature_positive_chirality=sig_pos, det_seifert=det, bound=bound, holds=bool(holds),
             equality=bool(det == bound), matrix_size=int(S.nrows()))
    out.write(jd(r) + "\n")
    out.flush()
    n += 1
    if not holds:
        violations.append(r)
        print("VIOLATION:", jd(r), flush=True)

done = [json.loads(l) for l in open(HERE / "random_lspace_sigma.jsonl")]
hyp = [r for r in done if r.get("hyperbolic")]
summary = {"candidate": "K33", "family": "unbiased random search, L-space knots only",
           "available": len(records), "tested": n, "violations": len(violations),
           "det_mismatches": det_mismatch, "congruence_failures": cong_fail,
           "hyperbolic": len(hyp), "equalities": sum(1 for r in done if r["equality"]),
           "hyperbolic_equalities": sum(1 for r in hyp if r["equality"]),
           "max_genus": max((r["genus"] for r in done), default=None),
           "signature": "exact, congruence diagonalisation over Q of V + V^T"}
(HERE / "random_lspace_sigma_summary.json").write_text(json.dumps(summary, indent=2, default=int))
print("tested", n, "of", len(records), "| violations", len(violations),
      "| det mismatches", len(det_mismatch), "| congruence failures", len(cong_fail), flush=True)
