"""Which one-bridge braids that attain det = 1 + |sigma| close to hyperbolic knots? (None, so among the hyperbolic
L-space knots tested equality stays confined to the Baker-Kegel family.) A knot counts as hyperbolic if some
retriangulation of its exterior has all tetrahedra positively oriented and volume above 0.9.

    python onebridge_equality.py     # writes onebridge_equality.json
"""
import json, sys
sys.path.insert(0, "..")
import snappy
from distinct_knots import onebridge_word

rows = [json.loads(l) for l in open("../onebridge.jsonl")]
eq = [r for r in rows if r["equality"]]
hyp = []
for r in eq:
    L = snappy.Link(braid_closure=onebridge_word(r["w"], r["b"], r["t"])); L.simplify('global')
    M = L.exterior()
    for _ in range(6):
        if M.solution_type() == 'all tetrahedra positively oriented' and M.volume() > 0.9:
            hyp.append(r["name"]); break
        M.randomize()
out = dict(triples=len(rows), equality_triples=len(eq), hyperbolic_equality_triples=hyp)
json.dump(out, open("onebridge_equality.json", "w"), indent=1)
print(out)
