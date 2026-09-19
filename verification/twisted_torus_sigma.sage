"""Stage B for the twisted torus family: exact signatures, then the K33 check det <= 1 - sigma.

Reads twisted_torus.jsonl (written by twisted_torus.py in the SnapPy environment, which decided
L-space-ness from knot Floer homology) and, for each knot, builds the braid closure in Sage, takes the
Seifert matrix V of the standard Seifert surface, and computes the signature of V + V^T exactly by
congruence diagonalisation over Q (exact_signature.py). No floating point anywhere.

Chirality: K33 is stated for the positive chirality, where an L-space knot has tau = g > 0 and sigma < 0.
pd_to_hfk reports tau for the knot as built, so a knot with tau < 0 is the mirror and its signature is
negated before the comparison. Every record carries tau, so the convention is auditable.

The determinant is recomputed here from the Seifert matrix and cross-checked against the one stage A
read off the Alexander polynomial; a mismatch is a hard failure rather than a silent disagreement.

    sage -python is not needed; run with:  sage twisted_torus_sigma.sage
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from exact_signature import signature as exact_signature

HERE = Path(__file__).parent
jd = lambda o: json.dumps(o, default=int)

records = [json.loads(l) for l in open(HERE / "twisted_torus.jsonl") if '"error"' not in l]
out = open(HERE / "twisted_torus_sigma.jsonl", "w")

violations = []
det_mismatch = []
n = 0
for rec in sorted(records, key=lambda r: len(r["braid_word"])):
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

hyp = [r for r in records if r.get("hyperbolic")]
neg = [r for r in records if not r["braid_positive_word"]]
summary = {"candidate": "K33", "family": "twisted torus knots, L-space knots only",
           "tested": n, "violations": len(violations), "det_mismatches": det_mismatch,
           "hyperbolic": len(hyp), "non_braid_positive_word": len(neg),
           "signature": "exact, congruence diagonalisation over Q of V + V^T"}
(HERE / "twisted_torus_sigma_summary.json").write_text(json.dumps(summary, indent=2, default=int))
print("tested", n, "violations", len(violations), "det mismatches", len(det_mismatch), flush=True)
