"""Topic 6.3: Riemann sums, summation notation, definite integral notation. Narration comes from transcripts/6_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.3"

    def construct(self):
        sq = lambda s: s * s
        ax, al = plot_axes([0, 3.5, 1], [0, 10, 2], w=7, h=5)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        rsum = lambda n: sum(sq(1 + 2 * k / n) * 2 / n for k in range(1, n + 1))
        with self.beat("Infinitely many rectangles") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(sq, x_range=[0, 3.2], color=FUNC, stroke_width=5)), run_time=1.2)
            boxes = riemann_boxes(ax, sq, np.linspace(1, 3, 5), "right")
            read = M(rf"n = 4: \ {rsum(4):.2f}", 38, AREA).to_edge(RIGHT, buff=0.9).shift(UP * 1.6)
            self.play(FadeIn(boxes), FadeIn(read), run_time=0.8)
            for n in (8, 16, 64):
                self.play(Transform(boxes, riemann_boxes(ax, sq, np.linspace(1, 3, n + 1), "right")),
                          Transform(read, M(rf"n = {n}: \ {rsum(n):.2f}", 38, AREA).move_to(read)), run_time=1)
            b.line(1)
            self.play(Indicate(read, color=AREA), run_time=0.8)
            b.line(2)
            solid = ax.get_area(ax.plot(sq, x_range=[1, 3]), x_range=[1, 3], color=AREA, opacity=0.55)
            self.play(FadeOut(boxes), FadeIn(solid), FadeIn(M(r"\text{exact area} = \tfrac{26}{3} \approx 8.667", 38, FUNC).next_to(read, DOWN, buff=0.5)), run_time=1)
        self.clear()
        self.title()

        with self.beat("Sigma notation") as b:
            sig = M(r"\sum", 120, SECANT)
            greek = T("the Greek capital S: S for sum", 34, SECANT).next_to(sig, RIGHT, buff=0.6)
            self.play(Write(sig), run_time=0.8)
            self.play(FadeIn(greek), run_time=0.6)
            b.line(1)
            full = M(r"\sum_{k=1}^{4} (2k + 1)", 72).shift(UP * 1.4)
            self.play(ReplacementTransform(sig, full), FadeOut(greek), run_time=0.8)
            labs = VGroup(T("start: $k = 1$", 30, SECANT).next_to(full, DL, buff=0.2), T("stop: $4$", 30, SECANT).next_to(full, UL, buff=0.2))
            self.play(FadeIn(labs), run_time=0.6)
            b.line(2)
            what = T("what to add", 30, SECANT).next_to(full, RIGHT, buff=0.4)
            self.play(FadeIn(what), run_time=0.5)
            terms = VGroup(*[M(rf"k = {k}: \ {2 * k + 1}", 38) for k in range(1, 5)]).arrange(RIGHT, buff=0.7).shift(DOWN * 0.6)
            for tm in terms:
                self.play(FadeIn(tm), run_time=0.5)
            b.line(3)
            tot = M(r"3 + 5 + 7 + 9 = 24", 46, AREA).next_to(terms, DOWN, buff=0.7)
            self.play(Write(tot), run_time=1)
        self.clear()

        cube = lambda s: s**3
        ax, al = plot_axes([0, 2.2, 1], [0, 8, 2], w=5.2, h=4.6)
        VGroup(ax, al).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
        with self.beat("A Riemann sum in sigma notation") as b:
            n = 6
            boxes = riemann_boxes(ax, cube, np.linspace(0, 2, n + 1), "right", opacity=0.3)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(cube, x_range=[0, 2.05], color=FUNC, stroke_width=5)), FadeIn(boxes), run_time=1.2)
            rows = VGroup(M(r"\Delta x = \frac{2 - 0}{n} = \frac2n", 40), M(r"x_k = 0 + k \cdot \frac2n = \frac{2k}{n}", 40), M(r"f(x_k) = \left(\frac{2k}{n}\right)^3", 40),
                          M(r"\sum_{k=1}^{n} \left(\frac{2k}{n}\right)^3 \cdot \frac2n", 46, AREA)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(LEFT, buff=0.6)
            b.line(1)
            self.play(Write(rows[0]), run_time=1)
            b.line(2)
            k4 = boxes[3]
            self.play(k4.animate.set_fill(SECANT, 0.6), Write(rows[1]), FadeIn(M("x_k", 30, SECANT).next_to(ax.c2p(4 / 3, 0), DOWN, buff=0.15)), run_time=1)
            b.line(3)
            self.play(Write(rows[2]), FadeIn(Brace(k4, LEFT, color=SECANT)), run_time=1)
            b.line(4)
            self.play(Write(rows[3]), run_time=1.2)
        self.clear()

        with self.beat("The definite integral") as b:
            ax, al = plot_axes([0, 3.5, 1], [0, 10, 2], w=6.4, h=4.6)
            VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.5)
            lim = M(r"\lim_{n\to\infty} \sum_{k=1}^{n} f(x_k)\,\Delta x", 44).to_edge(UP, buff=0.4).shift(LEFT * 2.6)
            boxes = riemann_boxes(ax, sq, np.linspace(1, 3, 5), "right")
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(sq, x_range=[0, 3.2], color=FUNC, stroke_width=5)), FadeIn(boxes), Write(lim), run_time=1.4)
            for n in (8, 16, 64, 256):
                self.play(Transform(boxes, riemann_boxes(ax, sq, np.linspace(1, 3, n + 1), "right", opacity=0.45 if n < 64 else 0.55)), run_time=1)
            solid = ax.get_area(ax.plot(sq, x_range=[1, 3]), x_range=[1, 3], color=AREA, opacity=0.55)
            self.play(FadeOut(boxes), FadeIn(solid), run_time=1)
            b.line(1)
            big = M(r"\int_1^3 x^2\,dx", 120, ACCUM).move_to([3.6, 0.6, 0])
            name = T("the definite integral", 44, ACCUM).next_to(big, DOWN, buff=0.4)
            self.play(Write(big), run_time=1.6)
            self.play(FadeIn(name, shift=UP * 0.2), Circumscribe(VGroup(big, name), color=ACCUM), run_time=1.2)
            b.line(2)
            self.play(FadeOut(ax), FadeOut(al), FadeOut(solid), FadeOut(lim), run_time=0.6)
            self.play(VGroup(big, name).animate.scale(0.7).to_edge(UP, buff=0.6), run_time=0.8)
            halves = VGroup(VGroup(T("Derivatives", 44, DERIV), T("the first half of the course", 30, DIM)).arrange(DOWN, buff=0.2),
                            VGroup(T("Integrals", 44, ACCUM), T("the other core concept", 30, DIM)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=2.2).shift(DOWN * 1.2)
            self.play(FadeIn(halves[0]), run_time=0.8)
            self.wait(0.6)
            self.play(FadeIn(halves[1]), Indicate(halves[1][0], color=ACCUM), run_time=1.2)
        self.clear()

        with self.beat("From delta x to dx") as b:
            src = M(r"\lim_{n\to\infty}", r"\sum_{k=1}^{n}", r"f(x_k)", r"\,\Delta x", 60).move_to([-2.6, 2.4, 0])
            dst = M(r"\int_a^b", r"f(x)", r"\,dx", 60).move_to([2.9, 2.4, 0])
            arrow = Arrow(src.get_right(), dst.get_left(), buff=0.35, color=DIM, stroke_width=3)
            self.play(Write(src), run_time=1)
            self.play(GrowArrow(arrow), run_time=0.5)
            self.play(TransformFromCopy(VGroup(src[0], src[1]), dst[0]), run_time=1.2)
            s_lab = T("S for sum, stretched", 28, SECANT).next_to(dst[0], DOWN, buff=0.3)
            self.play(FadeIn(s_lab), run_time=0.5)
            b.line(1)
            self.play(Indicate(src[2], color=FUNC), run_time=0.6)
            self.play(TransformFromCopy(src[2], dst[1]), run_time=1)
            b.line(2)
            self.play(Indicate(src[3], color=SECANT), run_time=0.6)
            self.play(TransformFromCopy(src[3], dst[2]), run_time=1)
            # the familiar picture from Unit 2: a nudge drawn as a small labeled double arrow, here shrinking from Delta x to dx
            ma, _ = plot_axes([0, 3, 1], [0, 3, 1], w=5.2, h=3.2, coords=False)
            VGroup(ma).move_to([0, -1.6, 0])
            g = lambda s: 0.8 + 0.25 * s * s
            W = ValueTracker(0.9)
            sliver = always_redraw(lambda: Polygon(ma.c2p(1.4, 0), ma.c2p(1.4 + W.get_value(), 0), ma.c2p(1.4 + W.get_value(), g(1.4)), ma.c2p(1.4, g(1.4)),
                                                   stroke_color=AREA, stroke_width=2, fill_color=AREA, fill_opacity=0.5))
            lab = always_redraw(lambda: nudge_arrow(ma.c2p(1.4, 0), ma.c2p(1.4 + W.get_value(), 0), label=r"\Delta x" if W.get_value() > 0.3 else "dx", size=34).shift(DOWN * 0.1))
            words = always_redraw(lambda: T("$\\Delta x$: a finite width" if W.get_value() > 0.3 else "$dx$: a tiny nudge", 30, SECANT).next_to(ma, RIGHT, buff=0.5))
            self.play(FadeIn(ma), Create(ma.plot(g, x_range=[0, 3], color=FUNC, stroke_width=4)), FadeIn(sliver), FadeIn(lab), FadeIn(words), run_time=1)
            self.wait(1.2)
            self.play(W.animate.set_value(0.08), run_time=2.4, rate_func=smooth)
            self.wait(0.6)
            b.line(3)
            others = [m for m in self.mobjects if m is not dst and not isinstance(m, ValueTracker)]
            self.play(*[FadeOut(m) for m in others], run_time=0.6)
            big = M(r"\int_a^b", r"f(x)", r"\,dx", 110).shift(LEFT * 1.0 + DOWN * 0.6)
            self.play(ReplacementTransform(dst, big), run_time=0.8)
            lab_ab = T("limits: start $a$, stop $b$", 28, SECANT).next_to(big, UP, buff=0.3)
            lab_f = T("integrand: the height", 28, FUNC).next_to(big, DOWN, buff=0.3)
            lab_dx = T(r"$dx$: a tiny width", 28, AREA).next_to(big, RIGHT, buff=0.3)
            self.play(FadeIn(lab_ab), run_time=0.5)
            self.play(FadeIn(lab_f), FadeIn(lab_dx), run_time=0.8)
            b.line(4)
            pos = T("$f \\ge 0$: the exact area under the curve", 32, AREA).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(pos), run_time=0.6)
        self.clear()

        fa, fl = plot_axes([0, 3.5, 1], [0, 10, 2], w=4.4, h=3.8)
        ffig = VGroup(fa, fl, fa.plot(sq, x_range=[0, 3.2], color=FUNC, stroke_width=4))
        shade13 = fa.get_area(fa.plot(sq, x_range=[1, 3]), x_range=[1, 3], color=AREA, opacity=0.5)
        self.example("From sum to integral", r"Write $\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \left(1 + \frac{2k}{n}\right)^2 \frac2n$ as a definite integral.",
                     [r"\Delta x = \frac2n, \ \text{so} \ b - a = 2", r"x_k = 1 + \frac{2k}{n}, \ \text{so} \ a = 1", r"b = 1 + 2 = 3", r"f(x) = x^2", r"\int_1^3 x^2\,dx"],
                     at=[1, 2, 3, 4, 5], figure=ffig, cues={4: lambda sc: sc.play(FadeIn(shade13), run_time=0.6)},
                     notes_graph=dict(fns=[("x^2", 0, 3.2)], xr=(0, 3.5), yr=(0, 10), ystep=2), follow=True)

        with self.beat("Close") as b:
            card = VGroup(T(r"$\Sigma$: add up, $k$ from bottom to top.", 38), M(r"\text{Right sum: } \sum_{k=1}^{n} f(a + k\Delta x)\,\Delta x, \quad \Delta x = \frac{b - a}{n}", 40, AREA),
                          M(r"\int_a^b f(x)\,dx = \lim_{n\to\infty} \sum_{k=1}^{n} f(x_k)\,\Delta x", 44, FUNC)).arrange(DOWN, buff=0.6)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Evaluate a sum", r"Evaluate $\displaystyle\sum_{k=1}^{4} \left(\frac{2k}{4}\right)^3 \frac24$.",
                     [r"k = 1: \ \left(\tfrac12\right)^3 \cdot \tfrac12 = \tfrac{1}{16}", r"k = 2: \ (1)^3 \cdot \tfrac12 = \tfrac12", r"k = 3: \ \left(\tfrac32\right)^3 \cdot \tfrac12 = \tfrac{27}{16}",
                      r"k = 4: \ (2)^3 \cdot \tfrac12 = 4", r"\tfrac{1}{16} + \tfrac{8}{16} + \tfrac{27}{16} + \tfrac{64}{16} = \tfrac{100}{16} = 6.25"], at=[1, 2, 3, 4, 5])
        self.example("Example 2: Another limit", r"Write $\displaystyle\lim_{n\to\infty} \sum_{k=1}^{n} \sqrt{\frac{4k}{n}} \cdot \frac4n$ as a definite integral.",
                     [r"\Delta x = \frac4n, \ \text{so} \ b - a = 4", r"x_k = \frac{4k}{n} = 0 + k \cdot \frac4n, \ \text{so} \ a = 0,\ b = 4", r"f(x) = \sqrt x", r"\int_0^4 \sqrt x\,dx"],
                     at=[1, 2, 3, 4])
        ca, cl = plot_axes([-2.5, 2.5, 1], [-0.5, 2.5, 1], w=4.6, h=2.8)
        cfig = VGroup(ca, cl, ca.plot(lambda s: np.sqrt(max(4 - s * s, 0)), x_range=[-2, 2, 0.01], color=FUNC, stroke_width=4))
        semi = ca.get_area(ca.plot(lambda s: np.sqrt(max(4 - s * s, 0)), x_range=[-2, 2, 0.01]), x_range=[-2, 2], color=AREA, opacity=0.5)
        self.example("Example 3: An integral by geometry", r"Evaluate $\displaystyle\int_{-2}^{2} \sqrt{4 - x^2}\,dx$.",
                     [r"TEXT:$y = \sqrt{4 - x^2}$ is the upper half of $x^2 + y^2 = 4$: radius $2$.", r"\text{area} = \tfrac12 \pi (2)^2", r"= 2\pi"], at=[1, 3, 4], figure=cfig,
                     cues={1: lambda sc: sc.play(FadeIn(semi), run_time=0.6)},
                     notes_graph=dict(fns=[("sqrt(abs(4-x^2))", -2, 2)], xr=(-2.5, 2.5), yr=(-0.5, 2.5)))
        self.finish()
