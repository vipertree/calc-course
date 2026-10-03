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


def _pi_name(k):
    """k * pi as LaTeX, k a multiple of 1/4 (e.g. 1.5 -> 3pi/2)."""
    from fractions import Fraction
    q = Fraction(k).limit_denominator(12)
    if q == 0:
        return "0"
    sign = "-" if q < 0 else ""
    n, d = abs(q.numerator), q.denominator
    top = r"\pi" if n == 1 else rf"{n}\pi"
    return f"${sign}{top}$" if d == 1 else rf"${sign}\frac{{{top}}}{{{d}}}$"


def _pi_ticks(lo, hi, step):
    import math
    ks, k = [], math.ceil(lo / (step * math.pi) - 1e-9) * step
    while k * math.pi <= hi + 1e-9:
        if abs(k) > 1e-9:
            ks.append(k)
        k += step
    return ("xtick={" + ",".join(f"{k * math.pi:.5f}" for k in ks) + "}, xticklabels={" + ",".join("{" + _pi_name(k) + "}" for k in ks) + "}")


def unit_circle(name, angles=(), triangle=None, caption="", size="6cm", labels=True):
    """A unit circle figure. angles: (theta in radians, label) points marked on the circle, label placed outside;
    triangle: an angle whose reference triangle (and ray) is drawn."""
    import math
    r = 2.0
    body = [r"\draw[->, gray] (-2.9,0) -- (3.0,0) node[right] {$x$};", r"\draw[->, gray] (0,-2.9) -- (0,3.0) node[above] {$y$};",
            rf"\draw[thick] (0,0) circle ({r});"]
    if labels:
        body += [r"\node[below right, font=\footnotesize] at (2,0) {$1$};", r"\node[below left, font=\footnotesize] at (-2,0) {$-1$};",
                 r"\node[above left, font=\footnotesize] at (0,2) {$1$};", r"\node[below left, font=\footnotesize] at (0,-2) {$-1$};"]
    if triangle is not None:
        c, s_ = r * math.cos(triangle), r * math.sin(triangle)
        body += [rf"\fill[blue!12] (0,0) -- ({c:.3f},0) -- ({c:.3f},{s_:.3f}) -- cycle;",
                 rf"\draw[very thick] (0,0) -- ({c:.3f},{s_:.3f});", rf"\draw[dashed] ({c:.3f},0) -- ({c:.3f},{s_:.3f});",
                 rf"\draw[->] (0.5,0) arc (0:{math.degrees(triangle):.1f}:0.5);"]
    for t, lab in angles:
        c, s_ = r * math.cos(t), r * math.sin(t)
        body.append(rf"\fill ({c:.3f},{s_:.3f}) circle (2pt);")
        if lab:
            # anchored on the far side of the point, so a long label grows away from the circle; points on an axis
            # put their label just beside the axis line, not on it
            on_axis = abs(math.sin(t)) < 0.05 or abs(math.cos(t)) < 0.05
            a = t + (0.35 if on_axis else 0)
            # the compass anchor opposite the direction of the point (angle anchors sit mid-edge on a wide label)
            anchor = ["west", "south west", "south", "south east", "east", "north east", "north", "north west"][round(math.degrees(a) / 45) % 8]
            body.append(rf"\node[font=\footnotesize, anchor={anchor}, inner sep=2pt] at ({(r + 0.12) * math.cos(a):.3f},{(r + 0.12) * math.sin(a):.3f}) {{{lab}}};")
    return Figure(name=name, caption=caption, tikz=rf"\begin{{tikzpicture}}[scale={float(size.rstrip('cm')) / 5.4:.3f}]" + "".join(body) + r"\end{tikzpicture}")


def triangle(name, a, b, opp="", adj="", hyp="", angle=r"$\theta$", caption="", size="4cm"):
    """A right triangle, legs a (across) and b (up), angle at the left corner; labels are LaTeX ($...$)."""
    k = float(size.rstrip("cm")) / max(a, b) * 0.8
    A, B, C = (0, 0), (a * k, 0), (a * k, b * k)
    body = [rf"\draw[thick] (0,0) -- ({B[0]:.3f},0) -- ({C[0]:.3f},{C[1]:.3f}) -- cycle;",
            rf"\draw ({B[0] - 0.25:.3f},0) -- ({B[0] - 0.25:.3f},0.25) -- ({B[0]:.3f},0.25);",
            r"\draw (0.6,0) arc (0:%.1f:0.6);" % __import__("math").degrees(__import__("math").atan2(b, a)),
            rf"\node at (0.95,{0.32 * b / max(a, b) + 0.05:.3f}) {{{angle}}};" if angle else ""]
    if adj:
        body.append(rf"\node[below] at ({B[0] / 2:.3f},0) {{{adj}}};")
    if opp:
        body.append(rf"\node[right] at ({B[0]:.3f},{C[1] / 2:.3f}) {{{opp}}};")
    if hyp:
        body.append(rf"\node[above left] at ({B[0] / 2:.3f},{C[1] / 2:.3f}) {{{hyp}}};")
    return Figure(name=name, caption=caption, tikz=r"\begin{tikzpicture}" + "".join(body) + r"\end{tikzpicture}")


def graph(name, fns, xr, yr, open=(), closed=(), vlines=(), hlines=(), labels=(), caption="",
          w="6.4cm", h="4.6cm", xstep=1, ystep=1, xlabel="x", ylabel="y", extra="", grid=True, samples=120, under="", xpi=0):
    """xpi: label the x ticks as multiples of pi, every xpi*pi (xr is still in plain numbers, e.g. (-0.3, 6.6))."""
    body = [under]  # drawn first, beneath the curves (shading)
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
        pos = "anchor=center" if pos == "center" else pos      # TikZ has no bare "center" key
        body.append(rf"\node[{pos}, font=\footnotesize] at (axis cs:{x},{y}) {{{text}}};")
    body.append(extra)
    g = "" if grid else ", grid=none"
    xt = f"xtick={{{_ticks(xr[0], xr[1], xstep)}}}"
    if xpi:
        xt = _pi_ticks(xr[0], xr[1], xpi)
    axis = (rf"\begin{{axis}}[calcaxes{g}, width={w}, height={h}, xmin={xr[0]}, xmax={xr[1]}, ymin={yr[0]}, ymax={yr[1]},"
            rf" {xt}, ytick={{{_ticks(yr[0], yr[1], ystep)}}},"
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


def region(name, fns, xr, yr, pieces, caption="", var="x", **kw):
    """A graph() with shaded regions. pieces: [(top, bottom, a, b), ...] with top/bottom Python callables of one
    variable. var="x" shades between y = bottom(x) and y = top(x) for a <= x <= b; var="y" shades between
    x = bottom(y) (left) and x = top(y) (right) for a <= y <= b. Curves themselves still come from fns."""
    fills = []
    for top, bottom, a, b in pieces:
        n = 60
        s = [a + (b - a) * i / n for i in range(n + 1)]
        up = [(v, top(v)) for v in s]
        down = [(v, bottom(v)) for v in reversed(s)]
        pts = up + down
        if var == "y":
            pts = [(q, p) for p, q in pts]
        fills.append(r"\fill[ink!14] " + " -- ".join(f"(axis cs:{p:.4f},{q:.4f})" for p, q in pts) + " -- cycle;")
    return graph(name, fns, xr, yr, caption=caption, under="".join(fills), **kw)
