"""Topic 6.2: Approximating areas with Riemann sums. Narration comes from transcripts/6_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *

F = lambda s: 0.1 * s * s + 1               # the lesson's function: f(0), f(2), ... come out to clean decimals
EDGES = [0, 2, 4, 6, 8]
PICK = {"left": lambda a, b: a, "right": lambda a, b: b, "mid": lambda a, b: (a + b) / 2}


def num(v):
    return f"{v:g}"


def sums_axes():
    """f on [0, 8], numbers on the even ticks only, on the left half of the screen (the board takes the right half)."""
    ax, al = plot_axes([0, 9, 1], [0, 8, 1], w=6.4, h=4.9, coords=False, xlabel="x", ylabel="y")
    ax.x_axis.add_numbers([2, 4, 6, 8], font_size=26)
    ax.y_axis.add_numbers([2, 4, 6, 8], font_size=26)
    VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.35)
    curve = ax.plot(F, x_range=[0, 8.4], color=FUNC, stroke_width=5)
    return ax, al, curve


def rect(ax, a, b, h, color=AREA, opacity=0.45):
    return Polygon(ax.c2p(a, 0), ax.c2p(b, 0), ax.c2p(b, h), ax.c2p(a, h), stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity)


def area_tag(ax, a, b, s, color=INK):
    """width x height = area, written on the rectangle (or just above the curve, when the rectangle is too short to hold it)."""
    tag = VGroup(M(rf"2 \cdot f({num(s)})", 24, color), M(rf"= 2 \cdot {num(F(s))}", 24, color), M(rf"= {num(2 * F(s))}", 26, color)).arrange(DOWN, buff=0.08)
    h = F(s)
    tall = ax.c2p(0, h)[1] - ax.c2p(0, 0)[1]
    if tall > tag.height + 0.3:
        tag.move_to(ax.c2p((a + b) / 2, 0) + UP * (0.15 + tag.height / 2))
    else:
        tag.next_to(ax.c2p((a + b) / 2, max(F(a), F(b), h)), UP, buff=0.15)
    return tag


def height_marks(ax, s, color=SECANT):
    """Where a rectangle's height comes from: a dot on the axis at the sample point, a dashed line up, a dot on the curve."""
    return VGroup(Dot(ax.c2p(s, 0), color=color, radius=0.07), DashedLine(ax.c2p(s, 0), ax.c2p(s, F(s)), color=color, stroke_width=3),
                  Dot(ax.c2p(s, F(s)), color=color, radius=0.08))


def board_at(rows, top=2.9):
    """A column of lines on the right half, left-aligned."""
    g = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    for r in g:
        r.set_max_width(6.3)
    return g.move_to([3.75, 0, 0]).align_to([0, top, 0], UP)


class Lesson(TranscriptScene):
    NUM = "6.2"

    def build_sum(self, ax, kind, color, lines):
        """Rectangles one at a time, each with its height point marked and its area written on it. lines: narration line
        index for each rectangle (None: same line as the one before)."""
        rects, tags = VGroup(), VGroup()
        for k, (a, b) in enumerate(zip(EDGES, EDGES[1:])):
            if lines[k] is not None:
                self._b.line(lines[k])
            s = PICK[kind](a, b)
            mk = height_marks(ax, s)
            r = rect(ax, a, b, F(s), color)
            tg = area_tag(ax, a, b, s)
            self.play(FadeIn(mk[0], scale=1.6), Create(mk[1]), FadeIn(mk[2], scale=1.6), run_time=0.7)
            self.play(GrowFromEdge(r, DOWN), run_time=0.7)
            self.play(FadeIn(tg), run_time=0.6)
            self.wait(0.4)
            self.play(FadeOut(mk[0]), FadeOut(mk[1]), mk[2].animate.scale(0.75), run_time=0.4)
            rects.add(r)
            tags.add(VGroup(tg, mk[2]))
        return rects, tags

    def construct(self):
        ax, al, curve = sums_axes()
        with self.beat("Rectangles under a curve") as b:
            reg = ax.get_area(ax.plot(F, x_range=[0, 8]), x_range=[0, 8], color=AREA, opacity=0.3)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(reg), run_time=1.2)
            b.line(1)
            boxes = riemann_boxes(ax, F, np.linspace(0, 8, 5), "left")
            val = lambda n: sum(F(a) for a in np.linspace(0, 8, n + 1)[:-1]) * 8 / n
            read = M(rf"\text{{total}} = {val(4):.2f}", 38, AREA).move_to([3.6, 1.5, 0])
            self.play(FadeOut(reg), FadeIn(boxes), FadeIn(read), run_time=1)
            b.line(2)
            for n in (8, 16, 32):
                nb = riemann_boxes(ax, F, np.linspace(0, 8, n + 1), "left")
                self.play(Transform(boxes, nb), Transform(read, M(rf"\text{{total}} = {val(n):.2f}", 38, AREA).move_to(read)), run_time=1.2)
            self.play(FadeIn(M(r"\text{true area} \approx 25.07", 36, FUNC).next_to(read, DOWN, buff=0.4)), run_time=0.6)
        self.clear()
        self.title()

        ax, al, curve = sums_axes()
        cuts = VGroup(*[DashedLine(ax.c2p(e, 0), ax.c2p(e, F(e)), color=DIM, stroke_width=2) for e in EDGES])
        with self.beat("Left Riemann sum") as b:
            self._b = b
            fl = M(r"f(x) = 0.1x^2 + 1", 36, FUNC).move_to([3.75, 2.6, 0])
            dx = nudge_arrow(ax.c2p(0, 0), ax.c2p(2, 0), label=r"\Delta x = 2", size=28).shift(DOWN * 0.55)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(fl), run_time=1.2)
            self.play(Create(cuts), FadeIn(dx), run_time=1)
            left, ltags = self.build_sum(ax, "left", AREA, [1, 3, 4, 5])
            b.line(6)
            tot = M(r"2 + 2.8 + 5.2 + 9.2 = 19.2", 40, AREA).move_to([3.75, 0.6, 0])
            self.play(Write(tot), run_time=1.2)
            b.line(7)
            name = callout("left Riemann sum", AREA, 36).next_to(tot, DOWN, buff=0.6)
            self.play(FadeIn(name), run_time=0.6)

        with self.beat("Factoring out the width") as b:
            self.play(FadeOut(tot), FadeOut(name), FadeOut(fl), run_time=0.5)
            rows = [M(r"L = 2 \cdot f(0) + 2 \cdot f(2) + 2 \cdot f(4) + 2 \cdot f(6)", 34), M(r"= 2\left[f(0) + f(2) + f(4) + f(6)\right]", 34),
                    M(r"= 2\left[1 + 1.4 + 2.6 + 4.6\right]", 34), M(r"= 2(9.6) = 19.2", 34, AREA),
                    T(r"Or add the rectangles one at a time: width $\times$ height.", 30, DIM)]
            bd = board_at(rows)
            for r in bd[1:4]:
                r.shift(RIGHT * 0.45)
            self.play(Write(bd[0]), run_time=1.2)
            self.play(Write(bd[1]), run_time=1.2)
            b.line(1)
            self.play(Write(bd[2]), run_time=1)
            self.play(Write(bd[3]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(bd[4]), Indicate(ltags, color=SECANT), run_time=1.2)
        self.play(FadeOut(bd), FadeOut(left), FadeOut(ltags), run_time=0.6)

        with self.beat("Right Riemann sum") as b:
            self._b = b
            q = T("Use the right side of each piece?", 34, SECANT).move_to([3.75, 2.6, 0])
            self.play(FadeIn(q), run_time=0.6)
            right, rtags = self.build_sum(ax, "right", SECANT, [1, 2, None, 3])
            b.line(4)
            self.play(FadeOut(q), run_time=0.3)
            name = callout("right Riemann sum", SECANT, 34)
            rows = [name, M(r"R = 2\left[f(2) + f(4) + f(6) + f(8)\right]", 34), M(r"= 2\left[1.4 + 2.6 + 4.6 + 7.4\right]", 34), M(r"= 2(16) = 32", 34, SECANT)]
            bd = board_at(rows)
            for r in bd[2:]:
                r.shift(RIGHT * 0.45)
            self.play(FadeIn(bd[0]), run_time=0.6)
            self.play(Write(bd[1]), run_time=1.2)
            b.line(5)
            self.play(Write(bd[2]), run_time=1)
            self.play(Write(bd[3]), run_time=0.8)
        self.play(FadeOut(bd), FadeOut(right), FadeOut(rtags), run_time=0.6)

        with self.beat("Midpoint Riemann sum") as b:
            self._b = b
            mids = VGroup(*[VGroup(Line(ax.c2p(m, 0) + DOWN * 0.12, ax.c2p(m, 0) + UP * 0.12, color=SECANT, stroke_width=4),
                                   M(num(m), 26, SECANT).next_to(ax.c2p(m, 0), UP, buff=0.18)) for m in (1, 3, 5, 7)])
            self.play(FadeIn(mids), run_time=0.8)
            self.play(FadeOut(mids), run_time=0.4)
            mid, mtags = self.build_sum(ax, "mid", AREA, [1, 2, None, None])
            b.line(3)
            name = callout("midpoint Riemann sum", AREA, 34)
            rows = [name, M(r"M = 2\left[f(1) + f(3) + f(5) + f(7)\right]", 34), M(r"= 2\left[1.1 + 1.9 + 3.5 + 5.9\right]", 34), M(r"= 2(12.4) = 24.8", 34, AREA)]
            bd = board_at(rows)
            for r in bd[2:]:
                r.shift(RIGHT * 0.45)
            self.play(FadeIn(bd[0]), run_time=0.6)
            self.play(Write(bd[1]), run_time=1.2)
            b.line(4)
            self.play(Write(bd[2]), run_time=1)
            self.play(Write(bd[3]), run_time=0.8)
        self.play(FadeOut(bd), FadeOut(mid), FadeOut(mtags), run_time=0.6)

        with self.beat("Trapezoids") as b:
            trap = riemann_boxes(ax, F, EDGES, "trap", color=ACCUM, opacity=0.35)
            self.play(FadeIn(trap), run_time=0.8)
            rows = [M(r"T = 2 \cdot \frac{f(0) + f(2)}{2} + 2 \cdot \frac{f(2) + f(4)}{2} + \cdots", 32),
                    M(r"= \frac22\left[f(0) + 2f(2) + 2f(4) + 2f(6) + f(8)\right]", 32), M(r"= 1\left[1 + 2.8 + 5.2 + 9.2 + 7.4\right] = 25.6", 32, ACCUM),
                    M(r"T = \frac{L + R}{2} = \frac{19.2 + 32}{2} = 25.6", 32, ACCUM), M(r"\text{true area} \approx 25.07", 34, FUNC)]
            bd = board_at(rows)
            for r in bd[1:3]:
                r.shift(RIGHT * 0.45)
            self.play(Write(bd[0]), run_time=1.2)
            b.line(1)
            self.play(Write(bd[1]), run_time=1.2)
            b.line(2)
            self.play(Write(bd[2]), run_time=1)
            self.play(FadeIn(bd[3]), run_time=0.6)
            b.line(3)
            self.play(FadeIn(bd[4]), run_time=0.6)
        self.clear()

        with self.beat("Over or under") as b:
            ax, al, curve = sums_axes()
            left = VGroup(*[rect(ax, a, a + 2, F(a)) for a in (0, 2, 4, 6)])
            q = VGroup(T("$f$ increasing, left Riemann sum:", 32), T("what can we expect?", 32, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.75, 2.4, 0])
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(left), FadeIn(q), run_time=1.2)
            b.line(1)
            gaps = VGroup(*[region(ax, F, (lambda h: lambda s: h)(F(a)), a, a + 2, color=TANGENT, opacity=0.75) for a in (0, 2, 4, 6)])
            ans = VGroup(T("underestimate", 36, AREA), T("every rectangle is under the graph", 28, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(q, DOWN, buff=0.5).align_to(q, LEFT)
            self.play(FadeIn(gaps), run_time=0.8)
            self.play(Indicate(gaps, color=TANGENT), FadeIn(ans), run_time=1.2)
            b.line(2)
            right = VGroup(*[rect(ax, a, a + 2, F(a + 2), SECANT, 0.35) for a in (0, 2, 4, 6)])
            q2 = T("Right Riemann sum?", 32, SECANT).next_to(ans, DOWN, buff=0.5).align_to(q, LEFT)
            self.play(FadeOut(left), FadeOut(gaps), FadeIn(right), FadeIn(q2), run_time=1)
            b.line(3)
            pokes = VGroup(*[region(ax, (lambda h: lambda s: h)(F(a + 2)), F, a, a + 2, color=TANGENT, opacity=0.75) for a in (0, 2, 4, 6)])
            ans2 = VGroup(T("overestimate", 36, SECANT), T("the rectangles poke above the graph", 28, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(q2, DOWN, buff=0.3).align_to(q, LEFT)
            self.play(FadeIn(pokes), run_time=0.8)
            self.play(Indicate(pokes, color=TANGENT), FadeIn(ans2), run_time=1.2)
            self.wait(0.6)
            self.clear()

            # decreasing: the same picture flipped, and the answers flip with it
            G = lambda s: 0.1 * (8 - s) ** 2 + 1
            da, dl = plot_axes([0, 9, 1], [0, 8, 1], w=5.6, h=4.3, coords=False, xlabel="x", ylabel="y")
            da.x_axis.add_numbers([2, 4, 6, 8], font_size=26)
            VGroup(da, dl).to_edge(LEFT, buff=0.6).shift(DOWN * 0.35)
            gc = da.plot(G, x_range=[0, 8.2], color=FUNC, stroke_width=5)
            tag = T("$f$ decreasing", 32, FUNC).next_to(da.c2p(5, 6.5), RIGHT, buff=0)
            b.line(4)
            dl_r = VGroup(*[Polygon(da.c2p(a, 0), da.c2p(a + 2, 0), da.c2p(a + 2, G(a)), da.c2p(a, G(a)), stroke_color=AREA, stroke_width=2, fill_color=AREA, fill_opacity=0.35)
                            for a in (0, 2, 4, 6)])
            dr_r = VGroup(*[Polygon(da.c2p(a, 0), da.c2p(a + 2, 0), da.c2p(a + 2, G(a + 2)), da.c2p(a, G(a + 2)), stroke_color=SECANT, stroke_width=2, fill_color=SECANT, fill_opacity=0.45)
                            for a in (0, 2, 4, 6)])
            a1 = VGroup(T("left sum: overestimate", 32, AREA), T("right sum: underestimate", 32, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.9, 1.8, 0])
            self.play(FadeIn(da), FadeIn(dl), Create(gc), FadeIn(tag), run_time=1)
            self.play(FadeIn(dl_r), FadeIn(a1[0]), run_time=1)
            self.play(FadeIn(dr_r), FadeIn(a1[1]), run_time=1)
            b.line(5)
            rule = callout(r"increasing: left under, right over\\ decreasing: left over, right under", ACCUM, 30).next_to(a1, DOWN, buff=0.6).align_to(a1, LEFT)
            self.play(FadeIn(rule), run_time=0.8)
            b.line(6)
            self.clear()

            def panel(fn, label):
                a, _ = plot_axes([0, 2, 1], [0, 2.4, 1], w=3.4, h=2.6, coords=False)
                g = VGroup(a, riemann_boxes(a, fn, [0, 1, 2], "trap", color=ACCUM, opacity=0.35), a.plot(fn, x_range=[0, 2], color=FUNC, stroke_width=4))
                return VGroup(g, T(label, 30).next_to(g, DOWN, buff=0.25))
            ps = VGroup(panel(lambda s: 0.3 + 0.45 * s * s, "concave up: trapezoid over"), panel(lambda s: 0.4 + 1.6 * s - 0.4 * s * s, "concave down: trapezoid under"))
            ps.arrange(RIGHT, buff=1.4).move_to(DOWN * 0.2)
            self.play(FadeIn(ps[0]), run_time=0.8)
            self.play(FadeIn(ps[1]), run_time=0.8)
        self.clear()

        ua, ul = plot_axes([0, 10, 1], [0, 8, 2], w=5.6, h=3.4, xlabel="t", ylabel="r")
        tt, rr = [0, 2, 5, 9, 10], [4, 6, 7, 5, 3]
        boxes = VGroup(*[Polygon(ua.c2p(a, 0), ua.c2p(b, 0), ua.c2p(b, h), ua.c2p(a, h), stroke_color=AREA, stroke_width=2, fill_color=AREA, fill_opacity=0.45)
                         for a, b, h in zip(tt, tt[1:], rr)])
        ufig = VGroup(ua, ul, VGroup(*[Dot(ua.c2p(a, h), color=FUNC, radius=0.06) for a, h in zip(tt, rr)]))
        tab = table(["t"] + [str(v) for v in tt], [["r(t)"] + [str(v) for v in rr]], size=34)
        widths = VGroup(*[M(str(b - a), 26, SECANT).move_to((tab.cells[0][k + 1].get_center() + tab.cells[0][k + 2].get_center()) / 2 + UP * 0.45) for k, (a, b) in enumerate(zip(tt, tt[1:]))])
        self.example("Uneven widths",
                     VGroup(T(r"Water flows into a tank at $r(t)$ gallons per minute. Use a left Riemann sum with the four subintervals in the table to approximate the water "
                              r"that flows in from $t = 0$ to $t = 10$.", 32), VGroup(tab, widths)).arrange(DOWN, buff=0.3),
                     [r"\text{widths: } 2,\ 3,\ 4,\ 1", r"2 \cdot r(0) + 3 \cdot r(2) + 4 \cdot r(5) + 1 \cdot r(9)", r"= 2(4) + 3(6) + 4(7) + 1(5)",
                      r"= 8 + 18 + 28 + 5", r"= 59 \text{ gallons}"], at=[1, 2, 3, 4, 5], figure=ufig,
                     cues={1: lambda sc: sc.play(LaggedStart(*[FadeIn(bx) for bx in boxes], lag_ratio=0.3), run_time=1.4)},
                     text=r"Water flows into a tank at $r(t)$ gallons per minute, with selected values in the table. "
                          r"\[ \begin{array}{c|ccccc} t \text{ (min)} & 0 & 2 & 5 & 9 & 10 \\ \hline r(t) & 4 & 6 & 7 & 5 & 3 \end{array} \] "
                          r"Use a left Riemann sum with the four subintervals indicated by the table to approximate the water that flows in from $t = 0$ to $t = 10$.", follow=True)

        with self.beat("Close") as b:
            card = VGroup(T(r"Riemann sum: add up (width) $\times$ (height).", 38, AREA), T("Left, right, midpoint: where the height comes from.", 34),
                          T(r"Write $\Delta x\left[f(x_1) + f(x_2) + \cdots\right]$, then the numbers.", 34),
                          T("Trapezoid: average the two sides.", 34, ACCUM), T("Increasing: left under, right over. Concave up: trapezoid over.", 32, DIM)).arrange(DOWN, buff=0.42)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ea, el = plot_axes([0, 3.5, 1], [0, 1.2, 0.5], w=4.6, h=3.2)
        efig = VGroup(ea, el, ea.plot(lambda s: 1 / s, x_range=[0.85, 3.4], color=FUNC, stroke_width=4))
        rb = riemann_boxes(ea, lambda s: 1 / s, [1, 1.5, 2, 2.5, 3], "right")
        self.example("Example 1: A right sum",
                     r"Use a right Riemann sum with $4$ equal subintervals to approximate the area under $f(x) = \dfrac1x$ on $[1, 3]$. Is it an overestimate or an underestimate?",
                     [r"\Delta x = \frac{3 - 1}{4} = 0.5", r"\text{right ends: } 1.5,\ 2,\ 2.5,\ 3", r"R = 0.5\left[f(1.5) + f(2) + f(2.5) + f(3)\right]",
                      r"= 0.5\left[\tfrac23 + \tfrac12 + \tfrac25 + \tfrac13\right]", r"= 0.5\left(\tfrac{19}{10}\right) = \tfrac{19}{20} = 0.95",
                      r"TEXT:$f$ is decreasing, so the right sum is an underestimate."], at=[1, 2, 2, 3, 4, 5], figure=efig,
                     cues={1: lambda sc: sc.play(FadeIn(rb), run_time=0.8)},
                     notes_graph=dict(fns=[("1/x", 0.85, 3.4)], xr=(0, 3.5), yr=(0, 1.2), ystep=0.5))
        tab2 = table(["x", "0", "1", "3", "4"], [["f(x)", "2", "5", "7", "4"]], size=36)
        self.example("Example 2: Trapezoids from a table",
                     VGroup(T(r"Use a trapezoidal sum with the subintervals in the table to approximate the area under $f$ from $x = 0$ to $x = 4$.", 34), tab2).arrange(DOWN, buff=0.3),
                     [r"\text{widths: } 1,\ 2,\ 1", r"(1)\frac{f(0) + f(1)}{2} = (1)\frac{2 + 5}{2} = 3.5", r"(2)\frac{f(1) + f(3)}{2} = (2)\frac{5 + 7}{2} = 12",
                      r"(1)\frac{f(3) + f(4)}{2} = (1)\frac{7 + 4}{2} = 5.5", r"T = 3.5 + 12 + 5.5 = 21"],
                     at=[1, 2, 3, 4, 5],
                     text=r"\[ \begin{array}{c|cccc} x & 0 & 1 & 3 & 4 \\ \hline f(x) & 2 & 5 & 7 & 4 \end{array} \] "
                          r"Use a trapezoidal sum with the subintervals indicated by the table to approximate the area under the graph of $f$ from $x = 0$ to $x = 4$.")
        oa, ol = plot_axes([0, 2.2, 1], [0, 3, 1], w=4.4, h=3.4, coords=False)
        hill = lambda s: 0.5 + 2 * s - 0.5 * s * s
        ofig = VGroup(oa, ol, riemann_boxes(oa, hill, [0.2, 2], "left", AREA, 0.3), riemann_boxes(oa, hill, [0.2, 2], "right", SECANT, 0.2),
                      riemann_boxes(oa, hill, [0.2, 2], "trap", ACCUM, 0.3), oa.plot(hill, x_range=[0, 2.1], color=FUNC, stroke_width=4))
        self.example("Example 3: Putting them in order",
                     r"$f$ is positive, increasing and concave down on $[a, b]$. Put the left sum $L$, the right sum $R$, the trapezoidal sum $T$, and the exact area $A$ in order.",
                     [r"\text{increasing: } L < A < R", r"\text{concave down: } T < A", r"T = \frac{L + R}{2} > L", r"L < T < A < R"], at=[1, 2, 3, 4], figure=ofig)
        self.finish()
