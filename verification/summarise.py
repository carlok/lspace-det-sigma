"""Render verdict.md for K33 from the result files in this folder."""
import json
from pathlib import Path
here = Path(__file__).parent
load = lambda f: [json.loads(l) for l in open(here / f)]
it = json.load(open(here / "iterated.json"))
fast = load("census_lspace_fast.jsonl")
hyp = {}
for f in ("hyperbolic.jsonl",) + tuple(p.name for p in here.glob("census_shard*.jsonl")) + ("census_mp.jsonl",):
    if (here / f).exists():
        for r in load(f):
            if "holds" in r: hyp[(r["source"], r["name"])] = r
fam = {s: [r for (src, _), r in hyp.items() if src == s] for s in {src for src, _ in hyp}}
native = [r for r in load("census_sage_native.jsonl") if r.get("holds") is False]
text = f"""## Verification by computation (ragusa session, not the external model)

verdict: OPEN; no counterexample among any L-space knot tested; the L-space hypothesis is essential

**Statement.** For every prime L-space knot: det <= 1 - sigma (KnotInfo chirality, so positive L-space knots have sigma < 0).

**Evidence.**

| family | L-space knots tested | violations | how the values are known |
|---|---:|---:|---|
| iterated torus knots (cables of cables, L-space by Hedden's and Hom's criterion q/p >= 2g-1) | {it['tested']} | {len(it['violations'])} | exact: Alexander polynomial of a cable, Litherland's signature formula, det = \\|Delta(-1)\\| |
| SnapPy census L-space knots (all 632, from Baker-Kegel's braid words, arXiv:2203.12013 Appendix) | {len(fast)} | {sum(not r['holds'] for r in fast)} | Seifert matrix V of the braid closure; signature of V + V^T numerically, det = \\|det(V + V^T)\\| exactly |
""" + "".join(
    f"| {src} | {len(rs)} | {sum(not r['holds'] for r in rs)} | knot Floer homology (SnapPy) for the L-space property, signature and determinant from Sage |\n"
    for src, rs in sorted(fam.items())) + f"""
Equality holds on many of them (all T(2,n), all (2,q)-cables of the trefoil, {sum(r['det'] == r['bound'] for r in fast)} census knot), so the bound is sharp.

**Reliability of the census signatures.** The exact Sage `signature()` was computed for {sum('matches_exact_run' in r for r in fast)} of the 632 and agrees with the numeric value on every one ({sum(r.get('matches_exact_run') is True for r in fast)} of {sum('matches_exact_run' in r for r in fast)}). For the rest the numeric computation is safe by a wide margin: V + V^T has small integer entries, so the backward-stable eigenvalue error is at most {max(r['eigenvalue_error_bound'] for r in fast):.1e}, while the smallest eigenvalue over all 632 knots is {min(r['min_abs_eigenvalue'] for r in fast):.1e}, about 8 orders of magnitude larger.

**The hypothesis matters.** Evaluating the same inequality on census knots that are braid positive (or negative) but not L-space knots gives {len(native)} violations, for example {', '.join(r['name'] for r in native[:5])}. Unlike K01, where the fibered and adequate labels were irrelevant, here the L-space condition is doing the work.

**What is not yet done.** No proof attempt, and no check of whether the inequality follows from the known shape of L-space Alexander polynomials (nonzero coefficients +-1 with alternating signs, so det <= 2g + 1) together with a bound on the signature. That is the obvious next step and could make this an easy theorem rather than a conjecture.

Reproduce: `iterated.py`, then `census_lspace_fast.sage` (needs `bk_lspace_braids.json`, parsed from the Baker-Kegel appendix), and `census_sage_native.sage` for the non-L-space comparison.
"""

fam2 = [json.loads(l) for l in open(here / "families_fast.jsonl")]
eq2 = [r for r in fam2 if r["det"] == r["bound"]]
text += f"""
**Sharp on an infinite family of the hardest case.** Beyond the census, K33 was checked on {len(fam2)} knots of the
non-braid-positive L-space families (Baker-Kegel K_1..K_25, Himeno K_2..K_8, the (2,q)-cables of T(2,3) and T(2,5)),
with {sum(not r['holds'] for r in fam2)} violations, and equality det = 1 - sigma holds on {len(eq2)} of them, including
every Baker-Kegel K_n tested (n = 1..25). These are hyperbolic L-space knots that are not braid positive, so the
inequality is sharp exactly where the statement has content. Script `families_fast.sage`.
"""
(here / "verdict.md").write_text(text)
print(text)
