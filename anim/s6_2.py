"""Topic 6.2: Approximating areas with Riemann sums. Narration comes from transcripts/6_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.2"

    def construct(self):
        f = lambda s: 0.25 * s * s + 1
        ax, al = plot_axes([0, 4.5, 1], [0, 6, 1], w=7.4, h=4.8)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        curve = ax.plot(f, x_range=[0, 4.3], color=FUNC, stroke_width=5)
        with self.beat("Rectangles under a curve") as b:
            region = ax.get_area(ax.plot(f, x_range=[0, 4]), x_range=[0, 4], color=AREA, opacity=0.3)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(region), run_time=1.2)
            b.line(1)
            boxes = riemann_boxes(ax, f, np.linspace(0, 4, 5), "left")
            val = lambda n: sum(f(a) for a in np.linspace(0, 4, n + 1)[:-1]) * 4 / n
            read = M(rf"\text{{total}} = {val(4):.2f}", 38, AREA).to_edge(RIGHT, buff=0.8).shift(UP * 1.5)
            self.play(FadeOut(region), FadeIn(boxes), FadeIn(read), run_time=1)
            b.line(2)
            for n in (8, 16, 32):
                nb = riemann_boxes(ax, f, np.linspace(0, 4, n + 1), "left")
                self.play(Transform(boxes, nb), Transform(read, M(rf"\text{{total}} = {val(n):.2f}", 38, AREA).move_to(read)), run_time=1.2)
            self.play(FadeIn(M(r"\text{true area} \approx 9.33", 36, FUNC).next_to(read, DOWN, buff=0.4)), run_time=0.6)
        self.clear()
        self.title()

        ax, al = plot_axes([0, 4.5, 1], [0, 6, 1], w=6.2, h=4.6)
        VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        curve = ax.plot(f, x_range=[0, 4.3], color=FUNC, stroke_width=5)
        edges = [0, 1, 2, 3, 4]
        with self.beat("Left and right sums") as b:
            ticks = VGroup(*[DashedLine(ax.c2p(e, 0), ax.c2p(e, f(e)), color=DIM, stroke_width=2) for e in edges])
            dx = M(r"\Delta x = 1", 34, SECANT).next_to(ax.c2p(0.5, 0), DOWN, buff=0.45)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), Create(ticks), FadeIn(dx), run_time=1.2)
            b.line(1)
            left = riemann_boxes(ax, f, edges, "left")
            hs = [r"f(0) = 1", r"f(1) = 1.25", r"f(2) = 2", r"f(3) = 3.25"]
            for k in range(4):
                self.play(FadeIn(left[k]), run_time=0.4)
            rows = VGroup(*[M(h, 32) for h in hs]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.9).shift(UP * 2)
            self.play(FadeIn(rows), run_time=0.8)
            b.line(2)
            L = M(r"L = 1(1 + 1.25 + 2 + 3.25) = 7.5", 34, AREA).next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
            self.play(Write(L), run_time=1)
            b.line(3)
            right = riemann_boxes(ax, f, edges, "right", color=SECANT, opacity=0.3)
            self.play(FadeOut(left), FadeIn(right), FadeOut(rows), run_time=0.8)
            rows2 = VGroup(*[M(h, 32) for h in (r"f(1) = 1.25", r"f(2) = 2", r"f(3) = 3.25", r"f(4) = 5")]).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(rows, aligned_edge=UL)
            self.play(FadeIn(rows2), run_time=0.6)
            b.line(4)
            R = M(r"R = 1(1.25 + 2 + 3.25 + 5) = 11.5", 34, SECANT).next_to(L, DOWN, buff=0.3).align_to(rows, LEFT)
            self.play(Write(R), run_time=1)
            b.line(5)
            self.play(FadeIn(left), run_time=0.6)
            note = VGroup(T("increasing: left too small,", 30, DIM), T("right too big", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(R, DOWN, buff=0.4).align_to(rows, LEFT)
            self.play(FadeIn(note), run_time=0.6)
        self.clear()

        ax, al = plot_axes([0, 4.5, 1], [0, 6, 1], w=6.2, h=4.6)
        VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        curve = ax.plot(f, x_range=[0, 4.3], color=FUNC, stroke_width=5)
        with self.beat("Midpoints and trapezoids") as b:
            mid = riemann_boxes(ax, f, edges, "mid")
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(mid), run_time=1.2)
            dots = VGroup(*[Dot(ax.c2p(m, f(m)), color=SECANT, radius=0.06) for m in (0.5, 1.5, 2.5, 3.5)])
            self.play(FadeIn(dots), run_time=0.5)
            b.line(1)
            Mm = M(r"M = 1(1.0625 + 1.5625 + 2.5625 + 4.0625) = 9.25", 30, AREA).to_edge(RIGHT, buff=0.4).shift(UP * 2.4)
            Mm.set_max_width(6.6)
            self.play(Write(Mm), run_time=1)
            b.line(2)
            trap = riemann_boxes(ax, f, edges, "trap", color=ACCUM, opacity=0.35)
            self.play(FadeOut(mid), FadeOut(dots), FadeIn(trap), run_time=0.8)
            b.line(3)
            Tt = M(r"T = \tfrac12(1)\left(1 + 2(1.25) + 2(2) + 2(3.25) + 5\right) = 9.5", 30, ACCUM).next_to(Mm, DOWN, buff=0.4).align_to(Mm, LEFT)
            Tt.set_max_width(6.6)
            avg = M(r"T = \tfrac{L + R}{2} = \tfrac{7.5 + 11.5}{2} = 9.5", 30, ACCUM).next_to(Tt, DOWN, buff=0.3).align_to(Mm, LEFT)
            self.play(Write(Tt), run_time=1.2)
            self.play(FadeIn(avg), run_time=0.6)
            b.line(4)
            true = M(r"\text{true area} \approx 9.33", 34, FUNC).next_to(avg, DOWN, buff=0.5).align_to(Mm, LEFT)
            self.play(FadeIn(true), run_time=0.6)
        self.clear()

        with self.beat("Over or under") as b:
            def panel(fn, kind, label, color):
                a, _ = plot_axes([0, 2, 1], [0, 2.4, 1], w=2.9, h=2.2, coords=False)
                g = VGroup(a, riemann_boxes(a, fn, [0, 1, 2], kind, color=color, opacity=0.35), a.plot(fn, x_range=[0, 2], color=FUNC, stroke_width=4))
                return VGroup(g, T(label, 26).next_to(g, DOWN, buff=0.2))
            inc = lambda s: 0.3 + 0.45 * s * s
            dec = lambda s: 2.1 - 0.45 * s * s
            up_ = lambda s: 0.3 + 0.45 * s * s
            dn_ = lambda s: 0.4 + 1.6 * s - 0.4 * s * s
            ps = VGroup(VGroup(panel(inc, "left", "increasing: left under", AREA), panel(inc, "right", "increasing: right over", SECANT)),
                        VGroup(panel(dec, "left", "decreasing: left over", SECANT), panel(dec, "right", "decreasing: right under", AREA)),
                        VGroup(panel(up_, "trap", "concave up: trapezoid over", ACCUM)), VGroup(panel(dn_, "trap", "concave down: trapezoid under", ACCUM)))
            for g in ps[:2]:
                g.arrange(RIGHT, buff=0.3)
            top = VGroup(ps[0], ps[1]).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.4)
            bot = VGroup(ps[2], ps[3]).arrange(RIGHT, buff=1.4).next_to(top, DOWN, buff=0.5)
            VGroup(top, bot).set_max_width(13)
            b.line(1)
            self.play(FadeIn(ps[0]), run_time=0.8)
            self.play(FadeIn(ps[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(ps[2]), run_time=0.8)
            b.line(3)
            self.play(FadeIn(ps[3]), run_time=0.8)
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
                     [r"\text{widths: } 2,\ 3,\ 4,\ 1", r"2(4) + 3(6) + 4(7) + 1(5)", r"= 8 + 18 + 28 + 5", r"= 59 \text{ gallons}"], at=[1, 2, 3, 4], figure=ufig,
                     cues={1: lambda sc: sc.play(LaggedStart(*[FadeIn(bx) for bx in boxes], lag_ratio=0.3), run_time=1.4)},
                     text=r"Water flows into a tank at $r(t)$ gallons per minute, with selected values in the table. "
                          r"\[ \begin{array}{c|ccccc} t \text{ (min)} & 0 & 2 & 5 & 9 & 10 \\ \hline r(t) & 4 & 6 & 7 & 5 & 3 \end{array} \] "
                          r"Use a left Riemann sum with the four subintervals indicated by the table to approximate the water that flows in from $t = 0$ to $t = 10$.")

        with self.beat("Close") as b:
            card = VGroup(T(r"Riemann sum: add (height) $\times$ (width).", 38, AREA), T("Left, right, midpoint: where the height comes from.", 34),
                          T("Trapezoid: average the two sides.", 34, ACCUM), T("Increasing: left under, right over. Concave up: trapezoid over.", 32, DIM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ea, el = plot_axes([0, 3.5, 1], [0, 1.2, 0.5], w=4.6, h=3.2)
        efig = VGroup(ea, el, ea.plot(lambda s: 1 / s, x_range=[0.85, 3.4], color=FUNC, stroke_width=4))
        rb = riemann_boxes(ea, lambda s: 1 / s, [1, 1.5, 2, 2.5, 3], "right")
        self.example("Example 1: A right sum",
                     r"Use a right Riemann sum with $4$ equal subintervals to approximate the area under $f(x) = \dfrac1x$ on $[1, 3]$. Is it an overestimate or an underestimate?",
                     [r"\Delta x = \frac{3 - 1}{4} = 0.5", r"\text{right ends: } 1.5,\ 2,\ 2.5,\ 3", r"f: \ \tfrac23,\ \tfrac12,\ \tfrac25,\ \tfrac13",
                      r"R = 0.5\left(\tfrac23 + \tfrac12 + \tfrac25 + \tfrac13\right) = 0.5\left(\tfrac{19}{10}\right) = 0.95",
                      r"TEXT:$f$ is decreasing, so the right sum is an underestimate."], at=[1, 2, 2, 3, 4], figure=efig,
                     cues={1: lambda sc: sc.play(FadeIn(rb), run_time=0.8)},
                     notes_graph=dict(fns=[("1/x", 0.85, 3.4)], xr=(0, 3.5), yr=(0, 1.2), ystep=0.5))
        tab2 = table(["x", "0", "1", "3", "4"], [["f(x)", "2", "5", "7", "4"]], size=36)
        self.example("Example 2: Trapezoids from a table",
                     VGroup(T(r"Use a trapezoidal sum with the subintervals in the table to approximate the area under $f$ from $x = 0$ to $x = 4$.", 34), tab2).arrange(DOWN, buff=0.3),
                     [r"\text{widths: } 1,\ 2,\ 1", r"(1)\frac{2 + 5}{2} = 3.5", r"(2)\frac{5 + 7}{2} = 12", r"(1)\frac{7 + 4}{2} = 5.5", r"T = 3.5 + 12 + 5.5 = 21"],
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
