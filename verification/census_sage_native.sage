"""K33 on census knots from Baker-Kegel braid words (arXiv:2203.12013, Appendix), using Sage's own Link (Seifert matrix).
Only braid words of uniform sign are used: by Baker-Kegel every census L-space knot except o9_30634 (checked separately in
hyperbolic.jsonl) has such a word. K33 is evaluated on every uniform-sign knot (a superset of the L-space ones), orienting by the sign of the braid
(positive braid: positive chirality). Any violation must then be confirmed to be an L-space knot with knot Floer homology."""
import json
jd = lambda o: json.dumps(o, default=int)
from pathlib import Path
words = json.load(open("bk_census_braids.json"))
uni = sorted(((n, v) for n, v in words.items() if all(x > 0 for x in v) or all(x < 0 for x in v)), key=lambda x: len(x[1]))
outp = Path("census_sage_native.jsonl")
done = {json.loads(l)["name"] for l in open(outp)} if outp.exists() else set()
out = open(outp, "a")
for name, w in uni:
    if name in done: continue
    n = max(abs(x) for x in w) + 1
    B = BraidGroup(n)
    K = Link(B([int(x) for x in w]))
    if K.number_of_components() != 1:
        out.write(jd(dict(name=name, error="not a knot")) + "\n"); continue
    sign = 1 if w[0] > 0 else -1
    try:
        alarm(120)
        sig = int(K.signature()); det = int(abs(K.determinant()))
        cancel_alarm()
    except AlarmInterrupt:
        out.write(jd(dict(name=name, braid_length=len(w), skipped="signature over 120 s")) + "\n"); out.flush(); continue
    sig_pos = sig if sign > 0 else -sig
    bound = 1 - sig_pos
    out.write(jd(dict(name=name, braid_length=len(w), strands=int(n), positive=sign > 0, 
                              signature_positive_chirality=sig_pos, det=det, bound=bound, holds=bool(det <= bound))) + "\n")
    out.flush()
print("done", flush=True)
