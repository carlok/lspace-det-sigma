"""K33 on SnapPy census knots, one shard: sage census_shard.sage <snappy site-packages> <shard> <nshards> <out> <done-names file>"""
import sys, json
sys.path.append(sys.argv[1])
import snappy
shard, nshards, outp, donep = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
done = set(json.load(open(donep)))
out = open(outp, "a")
names = [M.name() for M in snappy.CensusKnots()]
for idx, name in enumerate(names):
    if idx % nshards != shard or name in done:
        continue
    try:
        M = snappy.Manifold(name)
        cs = [c for c in M.alexander_polynomial().coefficients(sparse=False) if c != 0]
        if not (all(abs(c) == 1 for c in cs) and all(cs[i] == -cs[i + 1] for i in range(len(cs) - 1))):
            out.write(json.dumps(dict(source="census", name=name, L_space=False, reason="Alexander polynomial not of L-space form")) + "\n"); out.flush(); continue
        L = M.exterior_to_link(); L.simplify('global')
        h = L.knot_floer_homology()
        if not h['L_space_knot']:
            out.write(json.dumps(dict(source="census", name=name, L_space=False)) + "\n"); out.flush(); continue
        sig, det = int(L.signature()), int(L.determinant())
        sign = int(1) if int(h['tau']) > int(0) else int(-1)
        bound = int(1) - sign * sig
        out.write(json.dumps(dict(source="census", name=name, crossings=len(L.crossings), genus=int(h['seifert_genus']),
                                  tau=int(h['tau']), signature=sig, det=det, bound=bound, holds=bool(det <= bound))) + "\n")
    except Exception as e:
        out.write(json.dumps(dict(source="census", name=name, error=repr(e)[:200])) + "\n")
    out.flush()
    print('progress', shard, name, flush=True)
print("shard", shard, "done", flush=True)
