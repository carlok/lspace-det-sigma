"""Search for an unknotting of a knot by k crossing changes, over many diagrams.
A crossing change is PD [a,b,c,d] -> [b,c,d,a] (validated on the trefoil). Unknot test: knot Floer
homology of total rank 1 (HFK detects the unknot). Only positive crossings are changed: with tau(K) = k,
each change must lower tau by exactly 1, which only a positive-to-negative change can do."""
import itertools, json, sys, time, random
from multiprocessing import Pool
import snappy, spherogram

def is_unknot(pd):
    L = spherogram.Link(pd)
    L.simplify('global')
    if len(L.crossings) == 0:
        return True
    return L.knot_floer_homology()['total_rank'] == 1

def flip(pd, idx):
    out = [list(c) for c in pd]
    for i in idx:
        a, b, c, d = out[i]; out[i] = [b, c, d, a]
    return out

def search(args):
    braid, seed, k = args
    random.seed(seed)
    L = snappy.Link(braid_closure=braid)
    L.backtrack(random.randint(0, 12)); L.simplify(random.choice(['basic', 'level', 'global']))
    pd = [list(map(int, c)) for c in L.PD_code()]
    # signs aligned with the PD order
    Lp = spherogram.Link(pd)
    signs = [c.sign for c in Lp.crossings]
    labels = [sorted(map(int, c)) for c in Lp.PD_code()]
    order = {tuple(sorted(c)): i for i, c in enumerate(pd)}
    pos = [order[tuple(l)] for l, s in zip(labels, signs) if s == 1 and tuple(l) in order]
    tried = 0
    for idx in itertools.combinations(pos, k):
        tried += 1
        if is_unknot(flip(pd, idx)):
            return dict(seed=seed, crossings=len(pd), positive=len(pos), found=True, pd=pd, flip=list(idx), tried=tried)
    return dict(seed=seed, crossings=len(pd), positive=len(pos), found=False, tried=tried)

if __name__ == "__main__":
    # validation: trefoil, one change
    tre = [list(map(int, c)) for c in snappy.Link(braid_closure=[1, 1, 1]).PD_code()]
    assert not is_unknot(tre) and is_unknot(flip(tre, [0])), "crossing-change convention"
    assert search(([1, 1, 1, 1, 1], 0, 2))["found"], "T(2,5) in 2"
    assert not search(([1, 1, 1, 1, 1], 1, 1))["found"], "T(2,5) not in 1"
    braid = json.loads(sys.argv[1]); k = int(sys.argv[2]); n = int(sys.argv[3])
    t = time.time(); total = 0
    with Pool(10) as p:
        for r in p.imap_unordered(search, [(braid, s, k) for s in range(n)]):
            total += r["tried"]
            if r["found"]:
                print("FOUND", json.dumps(r), flush=True); p.terminate(); break
    print(f"diagrams {n} subsets tried {total} {time.time()-t:.0f}s", flush=True)
