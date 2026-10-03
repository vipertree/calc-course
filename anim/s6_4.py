"""Topic 6.4: The Fundamental Theorem of Calculus and accumulation functions. Narration comes from transcripts/6_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.4"

    def construct(self):
        f = lambda s: 1 + 0.5 * np.sin(1.3 * s) + 0.15 * s
        A = lambda s: s + 0.5 * (1 - np.cos(1.3 * s)) / 1.3 + 0.075 * s * s     # the exact running total of f from 0
        top, tl = plot_axes([0, 6, 1], [0, 3, 1], w=9, h=2.6, xlabel="t", ylabel="f")
        bot, bl = plot_axes([0, 6, 1], [0, 12, 4], w=9, h=2.8, xlabel="x", ylabel="A")
        VGroup(top, tl).to_edge(UP, buff=0.4)
        VGroup(bot, bl).next_to(VGroup(top, tl), DOWN, buff=0.5)
        X = ValueTracker(0.01)
        with self.beat("A running total") as b:
            self.play(FadeIn(top), FadeIn(tl), Create(top.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)), run_time=1.2)
            region = always_redraw(lambda: top.get_area(top.plot(f, x_range=[0, X.get_value()]), x_range=[0, X.get_value()], color=AREA, opacity=0.5))
            mark = always_redraw(lambda: DashedLine(top.c2p(X.get_value(), 0), top.c2p(X.get_value(), f(X.get_value())), color=SECANT))
            xl = always_redraw(lambda: M("x", 30, SECANT).next_to(top.c2p(X.get_value(), 0), DOWN, buff=0.12))
            self.add(region, mark, xl)
            self.play(X.animate.set_value(1.5), run_time=1.2)
            b.line(1)
            self.play(FadeIn(bot), FadeIn(bl), run_time=0.5)
            trace = always_redraw(lambda: bot.plot(A, x_range=[0, max(X.get_value(), 0.02)], color=ACCUM, stroke_width=5))
            pen = always_redraw(lambda: Dot(bot.c2p(X.get_value(), A(X.get_value())), color=ACCUM))
            self.add(trace, pen)
            self.play(X.animate.set_value(5.8), run_time=5, rate_func=linear)
            b.line(2)
            self.play(FadeIn(M(r"A(x)", 36, ACCUM).next_to(bot.c2p(5.8, A(5.8)), UL, buff=0.1)), run_time=0.6)
        self.clear()
        self.title()

        with self.beat("Accumulation functions") as b:
            eq = M(r"A(x)", r"=", r"\int_a^x", r"f(t)\,dt", 72).to_edge(UP, buff=0.8)
            self.play(Write(eq), run_time=1.2)
            b.line(1)
            la = T("$a$: a fixed start", 30, SECANT).next_to(eq[2], DL, buff=0.25)
            lx = T("$x$: the moving end, the input", 30, SECANT).next_to(eq[2], UR, buff=0.15).shift(RIGHT * 0.6)
            self.play(FadeIn(la), FadeIn(lx), run_time=0.8)
            b.line(2)
            lt = T("$t$: runs from $a$ to $x$", 30, FUNC).next_to(eq[3], DOWN, buff=0.35)
            self.play(FadeIn(lt), run_time=0.6)
            mini, _ = plot_axes([0, 5, 1], [0, 3, 1], w=4.6, h=2.4, coords=False)
            g = lambda s: 1.2 + 0.3 * np.sin(s)
            pic = VGroup(mini, mini.plot(g, x_range=[0, 5], color=FUNC, stroke_width=4),
                         mini.get_area(mini.plot(g, x_range=[1, 3.5]), x_range=[1, 3.5], color=AREA, opacity=0.5),
                         M("a", 28).next_to(mini.c2p(1, 0), DOWN, buff=0.1), M("x", 28, SECANT).next_to(mini.c2p(3.5, 0), DOWN, buff=0.1)).shift(DOWN * 1.3 + LEFT * 2.5)
            self.play(FadeIn(pic), run_time=0.8)
            b.line(3)
            zero = M(r"A(a) = \int_a^a f(t)\,dt = 0", 40, ACCUM).next_to(pic, RIGHT, buff=1)
            self.play(Write(zero), run_time=1)
        self.clear()

        ax, al = plot_axes([0, 5, 1], [0, 3, 1], w=6, h=4, coords=False, xlabel="t", ylabel="f")
        VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        g = lambda s: 1 + 0.25 * s + 0.2 * np.sin(2 * s)
        xx, h = 2.8, 0.45
        with self.beat("How fast the area grows") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(g, x_range=[0, 4.8], color=FUNC, stroke_width=5)),
                      FadeIn(ax.get_area(ax.plot(g, x_range=[0.5, xx]), x_range=[0.5, xx], color=AREA, opacity=0.4)), run_time=1.2)
            sliver = ax.get_area(ax.plot(g, x_range=[xx, xx + h]), x_range=[xx, xx + h], color=SECANT, opacity=0.7)
            labs = VGroup(M("x", 28).next_to(ax.c2p(xx, 0), DOWN, buff=0.1), M("x + h", 28).next_to(ax.c2p(xx + h, 0), DOWN, buff=0.1).shift(RIGHT * 0.25))
            self.play(FadeIn(sliver), FadeIn(labs), run_time=0.8)
            b.line(1)
            hb = Brace(Line(ax.c2p(xx, 0), ax.c2p(xx, g(xx))), LEFT, color=SECANT)
            self.play(FadeIn(hb), FadeIn(M("f(x)", 28, SECANT).next_to(hb, LEFT, buff=0.1)), run_time=0.6)
            rows = VGroup(M(r"A(x + h) - A(x) \approx f(x) \cdot h", 38), M(r"\frac{A(x + h) - A(x)}{h} \approx f(x)", 38),
                          M(r"h \to 0: \ \ A'(x) = f(x)", 40, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
            self.play(Write(rows[0]), run_time=1)
            b.line(2)
            self.play(Write(rows[1]), run_time=1)
            b.line(3)
            self.play(Write(rows[2]), run_time=1)
            b.line(4)
            thm = formula_box(VGroup(T("If $f$ is continuous, then", 32), M(r"\frac{d}{dx}\int_a^x f(t)\,dt = f(x)", 44, ACCUM)).arrange(DOWN, buff=0.2), ACCUM)
            thm.next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
            self.play(FadeIn(thm), run_time=0.8)
        self.clear()

        with self.beat("With the chain rule") as b:
            q = M(r"\frac{d}{dx}\int_1^{", r"x^2", r"} \cos t\,dt", 60).to_edge(UP, buff=0.8)
            self.play(Write(q), run_time=1)
            b.line(1)
            box = SurroundingRectangle(q[1], color=SECANT, buff=0.06)
            self.play(Create(box), FadeIn(T("inside function $u = x^2$", 30, SECANT).next_to(box, RIGHT, buff=0.4)), run_time=0.8)
            b.line(2)
            r1 = M(r"= \cos\left(x^2\right) \cdot \frac{d}{dx}\left(x^2\right)", 46).next_to(q, DOWN, buff=0.6)
            r2 = M(r"= \cos\left(x^2\right) \cdot 2x = 2x\cos\left(x^2\right)", 46).next_to(r1, DOWN, buff=0.4).align_to(r1, LEFT)
            self.play(Write(r1), run_time=1)
            self.play(Write(r2), run_time=1)
            b.line(3)
            gen = formula_box(M(r"\frac{d}{dx}\int_a^{u(x)} f(t)\,dt = f\left(u(x)\right) \cdot u'(x)", 44, ACCUM), ACCUM).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(gen), run_time=0.8)
        self.clear()

        self.example("Using the theorem", r"Let $g(x) = \displaystyle\int_2^x \left(t^2 - 3t\right) dt$. Find $g'(4)$ and $g(2)$.",
                     [r"g'(x) = x^2 - 3x \ \ \text{(FTC)}", r"g'(4) = 16 - 12 = 4", r"g(2) = \int_2^2 \left(t^2 - 3t\right) dt = 0"], at=[1, 2, 3])

        with self.beat("Close") as b:
            card = VGroup(M(r"A(x) = \int_a^x f(t)\,dt: \ \text{a running total}", 44, ACCUM), M(r"A'(x) = f(x)", 48), M(r"\text{top limit } u(x): \ f\left(u(x)\right) \cdot u'(x)", 42),
                          M(r"A(a) = 0", 42, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Straight from the theorem", r"Find $\dfrac{d}{dx}\displaystyle\int_0^x \sqrt{1 + t^3}\,dt$.",
                     [r"\text{top limit: } x \ \text{(no chain rule)}", r"\sqrt{1 + x^3}"], at=[1, 2])
        self.example("Example 2: A function on top", r"Find $\dfrac{d}{dx}\displaystyle\int_3^{\sin x} e^{t^2}\,dt$.",
                     [r"u = \sin x, \ \ u' = \cos x", r"\text{integrand at } u: \ e^{(\sin x)^2}", r"e^{\sin^2 x}\cos x"], at=[1, 2, 3])
        self.example("Example 3: x on the bottom", r"Find $\dfrac{d}{dx}\displaystyle\int_x^5 \left(t^4 + 1\right) dt$.",
                     [r"\int_x^5 \left(t^4 + 1\right) dt = -\int_5^x \left(t^4 + 1\right) dt", r"\frac{d}{dx}: \ -\left(x^4 + 1\right)"], at=[1, 2])
        self.finish()
