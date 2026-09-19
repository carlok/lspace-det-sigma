import itertools, sys, time, ast
from multiprocessing import Pool
import spherogram
from unknot3 import is_unknot, flip
PD = ast.literal_eval(open(sys.argv[1]).read()); K = int(sys.argv[2]); SIGN = int(sys.argv[3])
def test(idx):
    return idx if is_unknot(flip(PD, idx)) else None
if __name__ == "__main__":
    Lp = spherogram.Link(PD)
    signs = {tuple(sorted(map(int, c))): x.sign for c, x in zip(Lp.PD_code(), Lp.crossings)}
    cand = [i for i, c in enumerate(PD) if signs[tuple(sorted(c))] == SIGN]
    subsets = list(itertools.combinations(cand, K)); t = time.time()
    print(len(PD), "crossings,", len(cand), "with sign", SIGN, ",", len(subsets), "subsets", flush=True)
    with Pool(10) as p:
        for r in p.imap_unordered(test, subsets, chunksize=20):
            if r is not None:
                print("FOUND", r, flush=True); p.terminate(); break
        else:
            print("none", flush=True)
    print(f"{time.time()-t:.0f}s")
