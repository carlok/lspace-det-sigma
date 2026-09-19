"""Draw the knots that matter for K33 and save each as SVG (PLink). Run with the scratch venv and Tcl/Tk paths set."""
import json
from pathlib import Path
import snappy

HERE = Path(__file__).parent
KNOTS = {
    "T(2,7)_equality": [1] * 7,                                  # det 7 = 1 + |sigma|, equality
    "T(3,4)_definite": [1, 2] * 4,                               # definite, det 3, not T(2,n)
    "T(3,5)_definite": [1, 2] * 5,                               # definite, det 1, the E_8 knot
    "BakerKegel_K1_o9_30634": [2, 1, 3, 2] * 3 + [-1, 2, 1, 1, 2],  # hyperbolic, equality, not braid positive
    "cable_2_3_of_trefoil": [2, 1, 3, 2] * 3 + [-1] * 3,          # L-space, not braid positive
}
out = []
for name, w in KNOTS.items():
    L = snappy.Link(braid_closure=w)
    L.simplify('global')
    h = L.knot_floer_homology()
    v = L.view()
    v.save_as_svg(str(HERE / f"{name}.svg"), "color")
    out.append(dict(name=name, braid=w, crossings=len(L.crossings), genus=int(h['seifert_genus']),
                    L_space=bool(h['L_space_knot'])))
    print(out[-1], flush=True)
json.dump(out, open(HERE / "pictures.json", "w"), indent=1)
