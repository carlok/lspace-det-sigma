"""Figures for the unknotting in k32: the knot H(2,3) (Baker-Kegel K_1, census o9_30634) with the crossings the proof
changes circled, and one bundle crossing X_3 with the triangle j > i circled. The words come from
verification/families/hnm.py, so the pictures show the verified unknotting. Writes fig_*.tex, .pdf and .png here
(with captions, standalone) and fig_*_note.tex/.pdf (without, for k32.tex).

Convention: the braid runs left to right, position 1 at the bottom, and in a positive letter s_i the strand coming from
position i+1 passes over, which is a right-handed crossing. check_figures.py confirms this against SnapPy."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "verification" / "families"))
from hnm import H, X, slice_bennequin, unknotting_flips  # noqa: E402

DX, DY = 0.9, 0.75          # width of one letter, spacing of the strands
R_MARK = 0.40               # radius of the circle around a changed crossing


def y(p):
    return (p - 1) * DY


def changed_letters(word, flipped):
    """Indices where the flipped word inverts a letter; nothing else may differ."""
    assert len(word) == len(flipped)
    assert all(a == b or a == -b for a, b in zip(word, flipped))
    return {k for k, (a, b) in enumerate(zip(word, flipped)) if a != b}


def follow(word, strands):
    """For each letter, (lower strand, upper strand, over strand) by starting position, read left to right."""
    at = list(range(1, strands + 1))          # at[p-1] = starting position of the strand now at position p
    rows = []
    for g in word:
        i = abs(g)
        lo, hi = at[i - 1], at[i]
        rows.append((lo, hi, hi if g > 0 else lo))
        at[i - 1], at[i] = hi, lo
    return rows


def braid_tikz(word, strands, marked=(), color=None, close=False):
    color = color or {}
    now = {p: color.get(p, "black") for p in range(1, strands + 1)}   # colour of the strand now at position p
    out = []
    for k, g in enumerate(word):
        i = abs(g)
        x0, x1 = k * DX, (k + 1) * DX
        xm, ym = (x0 + x1) / 2, (y(i) + y(i + 1)) / 2
        for p in range(1, strands + 1):
            if p not in (i, i + 1):
                out.append(f"\\draw[{now[p]}] ({x0:.3f},{y(p):.3f}) -- ({x1:.3f},{y(p):.3f});")
        halo = "white"
        if k in marked:
            out.append(f"\\fill[red!15] ({xm:.3f},{ym:.3f}) circle ({R_MARK});")
            out.append(f"\\draw[red, thick] ({xm:.3f},{ym:.3f}) circle ({R_MARK});")
            halo = "red!15"
        rise = f"({x0:.3f},{y(i):.3f}) .. controls ({xm:.3f},{y(i):.3f}) and ({xm:.3f},{y(i + 1):.3f}) .. ({x1:.3f},{y(i + 1):.3f})"
        fall = f"({x0:.3f},{y(i + 1):.3f}) .. controls ({xm:.3f},{y(i + 1):.3f}) and ({xm:.3f},{y(i):.3f}) .. ({x1:.3f},{y(i):.3f})"
        c_rise, c_fall = now[i], now[i + 1]
        (under, cu), (over, co) = ((rise, c_rise), (fall, c_fall)) if g > 0 else ((fall, c_fall), (rise, c_rise))
        out.append(f"\\draw[{cu}] {under};")
        out.append(f"\\begin{{scope}}\\clip ({xm:.3f},{ym:.3f}) circle (0.3);"
                   f"\\draw[{halo}, line width=5pt] {over};\\end{{scope}}")
        out.append(f"\\draw[{co}] {over};")
        now[i], now[i + 1] = c_fall, c_rise
    if close:
        w, gap = len(word) * DX, 0.45
        for p in range(1, strands + 1):
            d = p * gap
            out.append(f"\\draw[{now[p]}, rounded corners=0.18cm] ({w:.3f},{y(p):.3f}) -- ({w + d:.3f},{y(p):.3f}) -- "
                       f"({w + d:.3f},{-d:.3f}) -- ({-d:.3f},{-d:.3f}) -- ({-d:.3f},{y(p):.3f}) -- (0,{y(p):.3f});")
    return out


def brace(k0, k1, top, label):
    return (f"\\draw[decorate, decoration={{brace, amplitude=4pt}}] ({k0 * DX + 0.06:.3f},{top:.3f}) -- "
            f"({k1 * DX - 0.06:.3f},{top:.3f}) node[midway, above=5pt] {{{label}}};")


def document(lines):
    return "\n".join([
        r"\documentclass[border=8pt]{standalone}",
        r"\usepackage{tikz}",
        r"\usetikzlibrary{decorations.pathreplacing}",
        r"\begin{document}",
        r"\begin{tikzpicture}[line width=0.9pt, line cap=round]",
        *lines,
        r"\end{tikzpicture}",
        r"\end{document}",
        "",
    ])


def fig_h23():
    n, m = 2, 3
    word = H(n, m)
    flipped, count = unknotting_flips(n, m)
    marked = changed_letters(word, flipped)
    assert len(word) == 17 and len(marked) == count == slice_bennequin(word, 2 * n) == 6
    lx = len(X(n))
    lines = braid_tikz(word, 2 * n, marked, close=True)
    top = y(2 * n) + 0.3
    for c in range(m):
        lines.append(brace(c * lx, (c + 1) * lx, top, f"$X_2$, copy {c + 1}"))
    lines.append(brace(m * lx, len(word), top, "$T_2$"))
    w = len(word) * DX
    caption = (f"\\node[anchor=north west, text width={w + 1.5:.2f}cm, font=\\small] at ({-0.7:.2f},{-2 * n * 0.45 - 0.3:.2f}) "
               r"{$H(2,3)$, the Baker--Kegel knot $K_1$ (census o9\_30634), as the closure of the 4-braid "
               r"$X_2^3 T_2$ with $X_2 = \sigma_2\sigma_1\sigma_3\sigma_2$ and "
               r"$T_2 = \sigma_1^{-1}\sigma_2\sigma_1\sigma_1\sigma_2$. Changing the 6 circled crossings gives the "
               r"unknot: all of copy 2, which then cancels copy 1; the last crossing of copy 3; and the "
               r"$\sigma_2$ of $T_2$. Since $g = g_4 = 6$ (slice--Bennequin), $u = 6$.};")
    return "fig_h23", lines, caption


def fig_grid():
    n = 3
    x = X(n)
    flipped, _ = unknotting_flips(n, 1)
    marked = changed_letters(x, flipped[:len(x)])
    assert len(x) == 9 and marked == set(range(n * (n + 1) // 2, len(x)))
    rows = follow(x, 2 * n)
    pairs = []
    for lo, hi, over in rows:
        a, b = (lo, hi) if lo <= n else (hi, lo)
        assert a <= n < b and over == b                     # every crossing is A under B in this convention
        pairs.append((a, b - n))
    assert {k for k, (i, j) in enumerate(pairs) if j > i} == marked
    blue, orange = "blue!70!black", "orange!90!black"
    color = {p: blue if p <= n else orange for p in range(1, 2 * n + 1)}
    lines = braid_tikz(x, 2 * n, marked, color=color)
    for p in range(1, 2 * n + 1):
        name = f"A_{p}" if p <= n else f"B_{p - n}"
        lines.append(f"\\node[left, {color[p]}] at (0,{y(p):.3f}) {{${name}$}};")
    for k, (i, j) in enumerate(pairs):
        style = "red" if k in marked else "black"
        lines.append(f"\\node[{style}, font=\\scriptsize] at ({(k + 0.5) * DX:.3f},{-0.5:.3f}) {{$({i},{j})$}};")
    # the n x n grid of pairs, rows A_i and columns B_j
    gx, gy, s = len(x) * DX + 1.4, y(2 * n) - 0.2, 0.6
    for i in range(1, n + 1):
        lines.append(f"\\node[{blue}, left] at ({gx:.2f},{gy - (i - 0.5) * s:.2f}) {{$A_{i}$}};")
        for j in range(1, n + 1):
            x0, y0 = gx + (j - 1) * s, gy - i * s
            fill = "red!15" if j > i else "white"
            mark = "C" if j < i else ("L" if j == i else "")
            lines.append(f"\\draw[fill={fill}, line width=0.5pt] ({x0:.2f},{y0:.2f}) rectangle ({x0 + s:.2f},{y0 + s:.2f});")
            if mark:
                lines.append(f"\\node[font=\\scriptsize] at ({x0 + s / 2:.2f},{y0 + s / 2:.2f}) {{${mark}$}};")
    for j in range(1, n + 1):
        lines.append(f"\\node[{orange}, above] at ({gx + (j - 0.5) * s:.2f},{gy:.2f}) {{$B_{j}$}};")
    w = gx + n * s
    caption = (f"\\node[anchor=north west, text width={w + 0.8:.2f}cm, font=\\small] at ({-0.8:.2f},{-0.9:.2f}) "
               r"{One bundle crossing $X_3$: the $n$-cable of a crossing, for $n = 3$. Each strand $A_i$ crosses "
               r"each $B_j$ once, $B$ on top every time; under each crossing, its pair $(i,j)$. In the grid, $C$ "
               r"marks the pairs crossed before the middle layer $L$ ($j < i$). Step 2 of the note changes the "
               r"pairs with $j > i$ (circled, shaded), the second half of the word, so that it becomes "
               r"$C\,L\,C^{-1}$.};")
    return "fig_grid", lines, caption


def pdflatex(name, lines):
    (HERE / f"{name}.tex").write_text(document(lines))
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{name}.tex"], cwd=HERE, check=True,
                   stdout=subprocess.DEVNULL)
    for ext in ("aux", "log"):
        (HERE / f"{name}.{ext}").unlink(missing_ok=True)


def build(name, lines, caption):
    """name.pdf/.png carry their caption and stand alone (for email); name_note.pdf has none and goes into k32.tex."""
    pdflatex(name, lines + [caption])
    subprocess.run(["pdftoppm", "-png", "-r", "300", "-singlefile", f"{name}.pdf", name], cwd=HERE, check=True)
    pdflatex(f"{name}_note", lines)
    print(f"wrote {name}.tex/.pdf/.png and {name}_note.tex/.pdf")


if __name__ == "__main__":
    for make in (fig_h23, fig_grid):
        build(*make())
