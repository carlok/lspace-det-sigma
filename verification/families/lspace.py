"""Which H(n,m) are L-space knots, by knot Floer homology (with a time limit), and are they outside the SnapPy census
(hyperbolic volume above 9.14, more than any census manifold with at most 9 tetrahedra can have, or not identified)?

    python lspace.py     # writes lspace.jsonl
"""
import json, signal, time
import snappy
from hnm import H


class Slow(Exception):
    pass


def alarm(*a):
    raise Slow()


signal.signal(signal.SIGALRM, alarm)
jobs = [(n, 1) for n in range(2, 9)] + [(n, 3) for n in range(2, 6)] + [(3, 5), (3, 7), (3, 9), (3, 11), (4, 5), (4, 7), (4, 9)]
with open("lspace.jsonl", "w") as f:
    for n, m in jobs:
        t0 = time.time()
        L = snappy.Link(braid_closure=H(n, m)); L.simplify('global')
        out = dict(n=n, m=m, crossings=len(L.crossings))
        signal.alarm(1200)
        try:
            h = L.knot_floer_homology()
            out.update(genus=h['seifert_genus'], tau=h['tau'], L_space=h['L_space_knot'], hfk_rank=h['total_rank'])
        except Slow:
            out['hfk'] = 'timeout'
        finally:
            signal.alarm(0)
        M = L.exterior(); ids = []
        for _ in range(4):
            try:
                ids = [str(x) for x in M.identify()]; break
            except Exception:
                M.randomize()
        for _ in range(40):                       # a geometric solution, so that the volume is that of a hyperbolic structure
            if M.solution_type() == 'all tetrahedra positively oriented':
                break
            M.randomize()
        out.update(census=ids, solution_type=M.solution_type(), volume=round(float(M.volume()), 4),
                   outside_census=(not ids and float(M.volume()) > 9.14), seconds=round(time.time() - t0, 1))
        f.write(json.dumps(out) + "\n"); f.flush()
        print(json.dumps(out), flush=True)
