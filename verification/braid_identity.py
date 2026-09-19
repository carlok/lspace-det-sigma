"""Check that each Baker-Kegel braid word really is the named census knot: the closure's exterior is compared with the
census manifold by SnapPy's isometry test. Run in the scratch venv (SnapPy)."""
import json, time
import snappy
words = json.load(open("bk_lspace_braids.json"))
out, t0 = [], time.time()
for i, (name, w) in enumerate(sorted(words.items())):
    try:
        E = snappy.Link(braid_closure=w).exterior()
        ok = E.is_isometric_to(snappy.Manifold(name))
        r = dict(name=name, isometric=bool(ok))
    except Exception as e:
        r = dict(name=name, error=repr(e)[:150])
    out.append(r)
    if i % 100 == 0: print(i, f"{time.time()-t0:.0f}s", flush=True)
with open("braid_identity.jsonl", "w") as f:
    for r in out: f.write(json.dumps(r) + "\n")
ok = sum(r.get("isometric") is True for r in out)
print("checked", len(out), "| isometric", ok, "| not isometric", sum(r.get("isometric") is False for r in out),
      "| errors", sum("error" in r for r in out), f"| {time.time()-t0:.0f}s")
