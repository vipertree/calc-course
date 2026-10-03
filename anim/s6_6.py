"""Topic 6.6: Applying properties of definite integrals. Narration comes from transcripts/6_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.6"

    def construct(self):
        f = lambda s: 1.5 + 0.6 * np.sin(1.2 * s) + 0.15 * s
        ax, al = plot_axes([0, 6, 1], [0, 3.5, 1], w=8.6, h=4.4, coords=False)
        VGroup(ax, al).shift(DOWN * 0.6)
        with self.beat("Pieces of area") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)), run_time=1.2)
            left = ax.get_area(ax.plot(f, x_range=[0.6, 3]), x_range=[0.6, 3], color=AREA, opacity=0.5)
            right = ax.get_area(ax.plot(f, x_range=[3, 5.4]), x_range=[3, 5.4], color=ACCUM, opacity=0.5)
            labs = VGroup(*[M(s, 32).next_to(ax.c2p(v, 0), DOWN, buff=0.15) for s, v in (("a", 0.6), ("b", 3), ("c", 5.4))])
            self.play(FadeIn(labs), run_time=0.5)
            b.line(1)
            self.play(FadeIn(left), run_time=0.8)
            self.play(FadeIn(right), run_time=0.8)
            eq = M(r"\int_a^b f\,dx", r"+", r"\int_b^c f\,dx", r"=", r"\int_a^c f\,dx", 46).to_edge(UP, buff=0.5)
            eq[0].set_color(AREA)
            eq[2].set_color(ACCUM)
            self.play(Write(eq), run_time=1.2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The properties") as b:
            props = VGroup(M(r"\int_a^a f(x)\,dx = 0", 40), M(r"\int_b^a f(x)\,dx = -\int_a^b f(x)\,dx", 40), M(r"\int_a^b k\,f(x)\,dx = k\int_a^b f(x)\,dx", 40),
                           M(r"\int_a^b \left[f(x) \pm g(x)\right] dx = \int_a^b f(x)\,dx \pm \int_a^b g(x)\,dx", 40),
                           M(r"\int_a^b f\,dx + \int_b^c f\,dx = \int_a^c f\,dx", 40)).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(LEFT, buff=0.7)
            notes = ["no width", "backward: flip the sign", "stretch by $k$: area times $k$", "sums split", "neighbors add"]
            tags = VGroup(*[T(n, 28, DIM).next_to(p, RIGHT, buff=0.5) for n, p in zip(notes, props)])
            for k in range(5):
                if k:
                    b.line(k)
                self.play(FadeIn(props[k]), FadeIn(tags[k]), run_time=0.8)
            VGroup(props, tags).set_max_width(13)
        self.clear()

        with self.beat("Using given values") as b:
            given = VGroup(M(r"\int_1^4 f(x)\,dx = 6", 42, FUNC), M(r"\int_1^4 g(x)\,dx = -2", 42, ACCUM)).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.6)
            self.play(FadeIn(given), run_time=0.8)
            rows = VGroup(M(r"\int_1^4 \left[3f(x) - 2g(x)\right] dx = 3\int_1^4 f(x)\,dx - 2\int_1^4 g(x)\,dx", 38), M(r"= 3(6) - 2(-2)", 40), M(r"= 18 + 4 = 22", 42, AREA),
                          M(r"\int_4^1 f(x)\,dx = -6", 42, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(given, DOWN, buff=0.6)
            rows.set_max_width(12.8)
            for k, m in zip((1, 2, 3, 4), rows):
                b.line(k)
                self.play(Write(m), run_time=1)
        self.clear()

        nl = NumberLine(x_range=[0, 5, 1], length=5, include_numbers=True, font_size=26, color=DIM)
        brA = BraceBetweenPoints(nl.n2p(0), nl.n2p(3), UP, color=AREA)
        brB = BraceBetweenPoints(nl.n2p(3), nl.n2p(5), UP, color=ACCUM)
        nfig = VGroup(nl, brA, brB, M("?", 30, AREA).next_to(brA, UP, buff=0.1), M("4", 30, ACCUM).next_to(brB, UP, buff=0.1),
                      BraceBetweenPoints(nl.n2p(0), nl.n2p(5), DOWN, color=FUNC).shift(DOWN * 0.45), M("10", 30, FUNC).next_to(nl, DOWN, buff=1.0))
        self.example("Splitting an interval",
                     r"$\int_0^5 f(x)\,dx = 10$ and $\int_3^5 f(x)\,dx = 4$. Find (a) $\int_0^3 f(x)\,dx$, (b) $\int_3^0 2f(x)\,dx$, (c) $\int_0^3 \left[f(x) + 1\right] dx$.",
                     [r"\text{(a) } \int_0^3 f\,dx + \int_3^5 f\,dx = \int_0^5 f\,dx: \ \ \int_0^3 f\,dx + 4 = 10", r"\int_0^3 f(x)\,dx = 6",
                      r"\text{(b) } \int_3^0 2f(x)\,dx = -2\int_0^3 f(x)\,dx = -2(6) = -12", r"\text{(c) } \int_0^3 f(x)\,dx + \int_0^3 1\,dx = 6 + 3", r"= 9"],
                     at=[1, 2, 3, 4, 5], figure=nfig)

        with self.beat("Close") as b:
            card = VGroup(M(r"\int_a^a = 0", 42), T("Backward limits flip the sign.", 38), T("Constants come out. Sums split.", 38), T("Neighboring intervals add.", 38, AREA)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        aa, alab = plot_axes([-3, 5, 1], [0, 5, 1], w=4.8, h=3.2)
        afig = VGroup(aa, alab, aa.plot(abs, x_range=[-2.8, 4.6], color=FUNC, stroke_width=4))
        t1 = Polygon(aa.c2p(-2, 0), aa.c2p(0, 0), aa.c2p(-2, 2), stroke_width=0, fill_color=AREA, fill_opacity=0.5)
        t2 = Polygon(aa.c2p(0, 0), aa.c2p(4, 0), aa.c2p(4, 4), stroke_width=0, fill_color=ACCUM, fill_opacity=0.5)
        self.example("Example 1: An absolute value", r"Evaluate $\displaystyle\int_{-2}^{4} |x|\,dx$.",
                     [r"\int_{-2}^{0} |x|\,dx + \int_0^4 |x|\,dx", r"\tfrac12(2)(2) = 2", r"\tfrac12(4)(4) = 8", r"2 + 8 = 10"], at=[1, 2, 3, 4], figure=afig,
                     cues={1: lambda sc: sc.play(FadeIn(t1), run_time=0.5), 2: lambda sc: sc.play(FadeIn(t2), run_time=0.5)},
                     notes_graph=dict(fns=[("abs(x)", -2.8, 4.6)], xr=(-3, 5), yr=(0, 5)))
        pa, pl = plot_axes([-2, 4, 1], [0, 5, 1], w=4.8, h=3.2)
        pfig = VGroup(pa, pl, Line(pa.c2p(-1, 2), pa.c2p(1, 2), color=FUNC, stroke_width=4), Line(pa.c2p(1, 2), pa.c2p(3, 4), color=FUNC, stroke_width=4))
        rect = Polygon(pa.c2p(-1, 0), pa.c2p(1, 0), pa.c2p(1, 2), pa.c2p(-1, 2), stroke_width=0, fill_color=AREA, fill_opacity=0.5)
        trap = Polygon(pa.c2p(1, 0), pa.c2p(3, 0), pa.c2p(3, 4), pa.c2p(1, 2), stroke_width=0, fill_color=ACCUM, fill_opacity=0.5)
        self.example("Example 2: A piecewise function", r"$f(x) = 2$ for $x < 1$ and $f(x) = x + 1$ for $x \ge 1$. Evaluate $\displaystyle\int_{-1}^{3} f(x)\,dx$.",
                     [r"\text{split at } 1", r"\int_{-1}^{1} 2\,dx = 2(2) = 4", r"\int_1^3 (x + 1)\,dx = \tfrac{2 + 4}{2}(2) = 6", r"4 + 6 = 10"], at=[1, 2, 3, 4], figure=pfig,
                     cues={1: lambda sc: sc.play(FadeIn(rect), run_time=0.5), 2: lambda sc: sc.play(FadeIn(trap), run_time=0.5)})
        self.example("Example 3: Find the constant", r"$\int_2^5 f(x)\,dx = 7$ and $\int_2^5 \left[f(x) + k\right] dx = 16$. Find $k$.",
                     [r"\int_2^5 f(x)\,dx + \int_2^5 k\,dx = 16", r"7 + k(5 - 2) = 16", r"3k = 9", r"k = 3"], at=[1, 2, 3, 4])
        self.finish()
