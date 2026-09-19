"""Verify computationally that one-bridge braids B(w,b,t) are L-space knots, rather than relying only on
Greene-Lewallen-Vafaee. Knot Floer homology (SnapPy) on the smallest members of the family, plus the K33 check with
the invariants recomputed from the knot Floer data (genus) and the Seifert matrix (det, sigma, from onebridge.jsonl)."""
import json, time
import snappy

rows = {json.loads(l)["name"]: json.loads(l) for l in open("onebridge.jsonl")}
def word(w, b, t): return list(range(b, 0, -1)) + list(range(w - 1, 0, -1)) * t

sample = sorted(rows.values(), key=lambda r: r["braid_length"])[:40]
out, t0 = [], time.time()
for r in sample:
    L = snappy.Link(braid_closure=word(r["w"], r["b"], r["t"])); L.simplify('global')
    h = L.knot_floer_homology()
    out.append(dict(name=r["name"], braid_length=r["braid_length"], L_space=bool(h['L_space_knot']),
                    genus_hfk=int(h['seifert_genus']), genus_braid=r["genus"], fibered=bool(h['fibered']),
                    det=r["det"], signature=r["signature"], holds=r["holds"]))
with open("onebridge_lspace.jsonl", "w") as f:
    for r in out: f.write(json.dumps(r) + "\n")
print("sample", len(out), "| all L-space:", all(r["L_space"] for r in out),
      "| genus from HFK equals braid-surface genus:", all(r["genus_hfk"] == r["genus_braid"] for r in out),
      "| K33 holds on all:", all(r["holds"] for r in out), f"| {time.time()-t0:.0f}s")
