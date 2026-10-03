"""Shorthand for the pgfplots graphs that fill Unit 1 and later units.

    graph("t1_3_a", [("x+1", -3, 1), ("3-x", 1, 4)], xr=(-3, 4), yr=(-1, 5),
          open=[(1, 2)], closed=[(1, 4)], vlines=[2], caption="...")

Function strings are pgfplots math (x^2, sin(deg(x)), exp(x), ...). A third and
fourth tuple entry give the domain; a fifth entry "dashed" draws with fn2.
"""
from . import Figure


def _ticks(lo, hi, step):
    import math
    out, v = [], math.ceil(lo / step - 1e-9) * step
    while v <= hi + 1e-9:
        if abs(v) > 1e-9:
            out.append(f"{v:g}")
        v += step
    return ",".join(out)


def graph(name, fns, xr, yr, open=(), closed=(), vlines=(), hlines=(), labels=(), caption="",
          w="6.4cm", h="4.6cm", xstep=1, ystep=1, xlabel="x", ylabel="y", extra="", grid=True, samples=120):
    body = []
    for f in fns:
        expr, a, b = f[0], f[1], f[2]
        style = "fn2" if len(f) > 3 and f[3] == "dashed" else "fn"
        body.append(rf"\addplot[{style}, domain={a}:{b}, samples={samples}]{{{expr}}};")
    for v in vlines:
        body.append(rf"\draw[asym] (axis cs:{v},{yr[0]}) -- (axis cs:{v},{yr[1]});")
    for v in hlines:
        body.append(rf"\draw[asym] (axis cs:{xr[0]},{v}) -- (axis cs:{xr[1]},{v});")
    if closed:
        body.append(r"\addplot[closed] coordinates {" + " ".join(f"({x},{y})" for x, y in closed) + "};")
    if open:
        body.append(r"\addplot[open] coordinates {" + " ".join(f"({x},{y})" for x, y in open) + "};")
    for x, y, pos, text in labels:
        body.append(rf"\node[{pos}, font=\footnotesize] at (axis cs:{x},{y}) {{{text}}};")
    body.append(extra)
    g = "" if grid else ", grid=none"
    axis = (rf"\begin{{axis}}[calcaxes{g}, width={w}, height={h}, xmin={xr[0]}, xmax={xr[1]}, ymin={yr[0]}, ymax={yr[1]},"
            rf" xtick={{{_ticks(xr[0], xr[1], xstep)}}}, ytick={{{_ticks(yr[0], yr[1], ystep)}}},"
            rf" xlabel={{${xlabel}$}}, ylabel={{${ylabel}$}}]")
    return Figure(name=name, caption=caption, tikz=r"\begin{tikzpicture}" + axis + "".join(body) + r"\end{axis}\end{tikzpicture}")


def slope_field(name, f, xs, ys, xr, yr, caption="", curves=(), w="6cm", h="6cm", length=0.32, closed=(), xlabel="x", ylabel="y"):
    """A slope field figure: a short segment of slope f(x, y) at each (x, y) in xs x ys, optionally with solution curves
    (pgfplots expressions as in graph()). Segment length is in axis units, corrected for the axis aspect ratio."""
    import math
    W, H = float(w.rstrip("cm")), float(h.rstrip("cm"))
    ux, uy = W / (xr[1] - xr[0]), H / (yr[1] - yr[0])          # cm per unit
    segs = []
    for x in xs:
        for y in ys:
            m = f(x, y)
            dx, dy = ux, m * uy                                   # direction in cm
            n = math.hypot(dx, dy)
            hx, hy = dx / n * (length / 2) / ux, dy / n * (length / 2) / uy
            segs.append(rf"\draw[thick] (axis cs:{x - hx:.4f},{y - hy:.4f}) -- (axis cs:{x + hx:.4f},{y + hy:.4f});")
    return graph(name, list(curves), xr, yr, closed=closed, caption=caption, w=w, h=h, extra="".join(segs), xlabel=xlabel, ylabel=ylabel)
