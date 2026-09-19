"""Unknot a braid closure by changing k positive letters (all k-subsets). Unknot certificate: SnapPy
simplifies the diagram to 0 crossings, else knot Floer homology of total rank 1."""
import itertools, json, sys, time
from multiprocessing import Pool
import snappy
W = json.loads(sys.argv[1]); K = int(sys.argv[2])
def test(idx):
    v = list(W)
    for i in idx: v[i] = -v[i]
    L = snappy.Link(braid_closure=v); L.simplify('global')
    if len(L.crossings) == 0: return idx, "0 crossings"
    if L.knot_floer_homology()['total_rank'] == 1: return idx, "HFK rank 1"
    return None
if __name__ == "__main__":
    pos = [i for i, x in enumerate(W) if x > 0]
    subsets = list(itertools.combinations(pos, K))
    t = time.time(); print(f"{len(pos)} positive letters, {len(subsets)} subsets", flush=True)
    with Pool(10) as p:
        for i, r in enumerate(p.imap_unordered(test, subsets, chunksize=50)):
            if r:
                print("FOUND", r, flush=True); p.terminate(); break
        else:
            print("none", flush=True)
    print(f"{time.time()-t:.0f}s", flush=True)
