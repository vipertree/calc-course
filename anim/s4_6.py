"""Topic 4.6: Local linearity and linearization. Narration comes from transcripts/4_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "4.6"

    def zoom_view(self):
        """A window onto y = sqrt(x) around (4, 2) whose half-width W shrinks; the curve and the tangent are redrawn in window units."""
        W = ValueTracker(3.5)
        frame = Rectangle(width=8, height=5, color=DIM, stroke_width=3).shift(LEFT * 1.6 + DOWN * 0.2)
        ax = Axes(x_range=[-1, 1], y_range=[-1, 1], x_length=8, y_length=5, tips=False, axis_config={"stroke_opacity": 0}).move_to(frame)
        ys = lambda: W.get_value() * 0.625

        def curve():
            w = W.get_value()
            lo = max(-1, (0.02 - 4) / w)
            return ax.plot(lambda u: np.clip((np.sqrt(4 + w * u) - 2) / ys(), -1.2, 1.2), x_range=[lo, 1, 0.01], color=FUNC, stroke_width=6)

        tan = ax.plot(lambda u: u * 0.4, x_range=[-1, 1], color=TANGENT, stroke_width=4)
        cur = always_redraw(curve)
        dot = Dot(ax.c2p(0, 0), color=INK, radius=0.09)
        read = always_redraw(lambda: M(rf"\text{{window width}} = {2 * W.get_value():.3g}", 34, DIM).next_to(frame, RIGHT, buff=0.3).align_to(frame, UP))
        return W, VGroup(frame, tan, dot), cur, read

    def construct(self):
        W, still, cur, read = self.zoom_view()
        lab = VGroup(M(r"y = \sqrt{x}", 38, FUNC), M(r"\text{tangent at } x = 4", 34, TANGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        with self.beat("Zoom in") as b:
            self.add(still[0])
            self.play(Create(cur), run_time=1)
            self.play(Create(still[1]), FadeIn(still[2]), run_time=0.8)
            lab.next_to(still[0], RIGHT, buff=0.3).shift(DOWN * 1.2)
            self.play(FadeIn(lab), FadeIn(read), run_time=0.6)
            b.line(1)
            for w in (1.0, 0.25, 0.05):
                self.play(W.animate.set_value(w), run_time=1.6)
            b.line(2)
            self.play(Indicate(still[1], color=TANGENT), run_time=1)
        self.clear()
        self.title()

        ax, al = plot_axes([0, 6, 1], [0, 5, 1], w=7, h=5, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        f = lambda s: 0.12 * (s - 1) ** 2 + 1
        a, xb = 2.0, 4.6
        fa, sl = f(a), 0.24 * (a - 1)
        with self.beat("The tangent line as an estimate") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)), run_time=1.2)
            P = Dot(ax.c2p(a, fa), color=INK)
            hgt = DashedLine(ax.c2p(a, 0), ax.c2p(a, fa), color=DIM)
            self.play(FadeIn(P), Create(hgt), FadeIn(M("f(a)", 32).next_to(hgt, LEFT, buff=0.1)), run_time=0.8)
            self.play(Create(tangent_line(ax, f, a, sl, [0.3, 5.6])), run_time=0.8)
            b.line(1)
            run = Line(ax.c2p(a, fa), ax.c2p(xb, fa), color=SECANT, stroke_width=4)
            rise = Line(ax.c2p(xb, fa), ax.c2p(xb, fa + sl * (xb - a)), color=DERIV, stroke_width=5)
            self.play(Create(run), FadeIn(M("x - a", 30, SECANT).next_to(run, DOWN, buff=0.1)), run_time=0.8)
            self.play(Create(rise), FadeIn(M(r"f'(a)(x - a)", 30, DERIV).next_to(rise, RIGHT, buff=0.1)), run_time=0.8)
            b.line(2)
            form = M(r"L(x) = f(a) + f'(a)(x - a)", 46).to_edge(RIGHT, buff=0.4).shift(UP * 2.6)
            self.play(Write(form), run_time=1.2)
            b.line(3)
            approx = M(r"f(x) \approx L(x)", 46, TANGENT).next_to(form, DOWN, buff=0.5)
            self.play(Write(approx), run_time=0.8)
        self.clear()
        self.example("Using given values", r"$f(4) = 10$ and $f'(4) = 2.5$. Estimate $f(4.2)$.",
                     [r"L(x) = 10 + 2.5(x - 4)", r"f(4.2) \approx L(4.2) = 10 + 2.5(0.2) = 10.5"], at=[1, 2])

        with self.beat("Choosing a") as b:
            q = M(r"\text{Estimate } \sqrt{26}", 56).shift(UP * 2)
            self.play(Write(q), run_time=0.8)
            nl = NumberLine(x_range=[23, 28, 1], length=9, include_numbers=True, font_size=36, color=DIM).shift(DOWN * 0.3)
            self.play(Create(nl), run_time=0.8)
            mark = Dot(nl.n2p(26), color=TANGENT)
            self.play(FadeIn(mark), run_time=0.4)
            b.line(1)
            ring = Circle(radius=0.35, color=DERIV).move_to(nl.n2p(25))
            self.play(Create(ring), FadeIn(M(r"\sqrt{25} = 5", 44, DERIV).next_to(nl.n2p(25), DOWN, buff=0.9)), run_time=1)
        self.clear()

        def panel(sign):
            ax, al = plot_axes([0, 4, 1], [0, 4, 1], w=4.6, h=3.6, coords=False)
            g = (lambda s: 3.4 - 0.3 * (s - 3.6) ** 2) if sign < 0 else (lambda s: 0.3 * (s - 0.4) ** 2 + 0.6)
            dg = (lambda s: -0.6 * (s - 3.6)) if sign < 0 else (lambda s: 0.6 * (s - 0.4))
            a0, x1 = 1.4, 2.6
            curve = ax.plot(g, x_range=[0, 4], color=FUNC, stroke_width=5)
            tl = tangent_line(ax, g, a0, dg(a0), [0.4, 2.9])
            est = g(a0) + dg(a0) * (x1 - a0)
            gap = Line(ax.c2p(x1, g(x1)), ax.c2p(x1, est), color=SECANT, stroke_width=5)
            dots = VGroup(Dot(ax.c2p(x1, est), color=TANGENT), Dot(ax.c2p(x1, g(x1)), color=FUNC))
            word = T("overestimate" if sign < 0 else "underestimate", 34, SECANT)
            return VGroup(VGroup(ax, al, curve, tl), VGroup(gap, dots), word)

        with self.beat("Too big or too small") as b:
            left, right = self.place(panel(-1), LEFT * 3.3), self.place(panel(1), RIGHT * 3.3)
            b.line(1)
            self.play(FadeIn(left[0]), run_time=0.8)
            self.play(Create(left[1]), FadeIn(left[2]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(right[0]), run_time=0.8)
            self.play(Create(right[1]), FadeIn(right[2]), run_time=0.8)
            b.line(3)
            names = VGroup(T("concave down", 30, DIM).next_to(left[2], DOWN, buff=0.2), T("concave up", 30, DIM).next_to(right[2], DOWN, buff=0.2))
            self.play(FadeIn(names), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            box = VGroup(M(r"L(x) = f(a) + f'(a)(x - a)", 56))
            box.add(SurroundingRectangle(box[0], color=TANGENT, buff=0.3))
            self.play(FadeIn(box), run_time=1)
        self.clear()

        self.examples_card()
        self.example("Example 1: The square root of 26",
                     r"Use a linearization to estimate $\sqrt{26}$. Is the estimate too big or too small?",
                     [r"f(x) = \sqrt x,\ \ a = 25:\ \ f(25) = 5", r"f'(x) = \frac{1}{2\sqrt x},\ \ f'(25) = \frac{1}{10}",
                      r"L(x) = 5 + \frac{1}{10}(x - 25)", r"\sqrt{26} \approx L(26) = 5.1",
                      r"TEXT:The graph of $\sqrt x$ bends down, below its tangent lines, so $5.1$ is an overestimate."], at=[1, 2, 3, 4, 5])
        self.example("Example 2: From given values", r"$f(2) = 7$ and $f'(2) = -3$. Estimate $f(2.1)$.",
                     [r"L(x) = 7 - 3(x - 2)", r"f(2.1) \approx 7 - 3(0.1) = 6.7"], at=[1, 2])
        self.example("Example 3: A cube root", r"Use a linearization to estimate $\sqrt[3]{8.12}$.",
                     [r"f(x) = x^{1/3},\ \ a = 8:\ \ f(8) = 2", r"f'(x) = \frac13 x^{-2/3},\ \ f'(8) = \frac13\cdot\frac14 = \frac{1}{12}",
                      r"L(8.12) = 2 + \frac{1}{12}(0.12) = 2.01"], at=[1, 2, 3])
        self.finish()

    @staticmethod
    def place(p, where):
        """Move a too-big/too-small panel (axes, marks, word) as one piece, word under the axes."""
        p[2].next_to(p[0], DOWN, buff=0.2)
        VGroup(*p).move_to(where + DOWN * 0.1)
        return p
