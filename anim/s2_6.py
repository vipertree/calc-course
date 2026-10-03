"""Topic 2.6: Constant, sum, difference and constant multiple rules. Narration comes from transcripts/2_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "2.6"

    def construct(self):
        ax, al = plot_axes([-2, 2, 1], [0, 8, 2], w=6.4, h=5)
        VGroup(ax, al).shift(DOWN * 0.3 + LEFT * 2)
        c = ValueTracker(0)
        curve = always_redraw(lambda: ax.plot(lambda x: x * x + c.get_value(), x_range=[-2, 2], color=FUNC, stroke_width=5))
        tan = always_redraw(lambda: ax.plot(lambda x: 1 + c.get_value() + 2 * (x - 1), x_range=[0.2, 1.9], color=TANGENT, stroke_width=4))
        lab = always_redraw(lambda: M(r"y = x^2" + (r" + 3" if c.get_value() > 1.5 else ""), 44, FUNC).to_edge(RIGHT, buff=1).shift(UP * 2))
        with self.beat("Lifting a graph") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(curve), run_time=1)
            self.play(Create(tan), FadeIn(lab), FadeIn(M(r"\text{slope } 2", 40, TANGENT).to_edge(RIGHT, buff=1).shift(UP * 1)), run_time=0.8)
            self.play(c.animate.set_value(3), run_time=2)
            b.line(1)
            self.play(Indicate(tan, color=TANGENT), run_time=1)
        self.clear()
        self.title()

        a2, l2 = plot_axes([0, 4, 1], [0, 7, 1], w=6.4, h=4.4)
        VGroup(a2, l2).shift(DOWN * 0.5 + LEFT * 2)
        with self.beat("The constant rule") as b:
            self.play(FadeIn(a2), FadeIn(l2), Create(a2.plot(lambda x: 5, x_range=[0, 4], color=FUNC, stroke_width=5)), run_time=1)
            self.play(FadeIn(M(r"y = 5,\ \ \text{slope } 0", 40, FUNC).to_edge(RIGHT, buff=0.8).shift(UP * 1.4)), run_time=0.6)
            b.line(1)
            self.play(FadeIn(formula_box(M(r"\frac{d}{dx}\, c = 0", 54), DERIV).to_edge(RIGHT, buff=0.8).shift(DOWN * 0.4)), run_time=0.8)
        self.clear()

        ax, al = plot_axes([0, 2, 1], [0, 9, 3], w=6.4, h=5.2)
        VGroup(ax, al).shift(DOWN * 0.3 + LEFT * 2.4)
        k = ValueTracker(1)
        with self.beat("Stretching a graph") as b:
            curve = always_redraw(lambda: ax.plot(lambda x: k.get_value() * x * x, x_range=[0, min(2, (9 / k.get_value()) ** 0.5)], color=FUNC, stroke_width=5))
            tri = always_redraw(lambda: VGroup(DashedLine(ax.c2p(1, k.get_value()), ax.c2p(1.4, k.get_value()), color=DIM),
                                               Line(ax.c2p(1.4, k.get_value()), ax.c2p(1.4, k.get_value() * 1.96), color=SECANT, stroke_width=5)))
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(tri), run_time=1.2)
            self.play(k.animate.set_value(3), run_time=2)
            b.line(1)
            box = formula_box(M(r"\frac{d}{dx}\big[k\,f(x)\big] = k\,f'(x)", 46), DERIV).to_edge(RIGHT, buff=0.5).shift(UP * 1)
            self.play(FadeIn(M(r"\text{slope } 2 \to 6", 40, TANGENT).next_to(box, DOWN, buff=0.5)), FadeIn(box), run_time=1)
        self.clear()

        ax, al = plot_axes([0, 3, 1], [0, 14, 2], w=6.4, h=5.6, coords=False)
        VGroup(ax, al).shift(DOWN * 0.3 + LEFT * 2.4)
        # f low and g well above it, so each rise sits clearly on its own curve
        f = lambda x: 1.5 + 0.4 * x + 0.3 * x * x
        g = lambda x: 3.0 + 0.8 * x + 0.35 * x * x
        with self.beat("Adding functions") as b:
            self.play(FadeIn(ax), Create(ax.plot(f, x_range=[0, 3], color=SECANT, stroke_width=4)), Create(ax.plot(g, x_range=[0, 3], color=DERIV, stroke_width=4)), run_time=1.2)
            s = ax.plot(lambda x: f(x) + g(x), x_range=[0, 2.6], color=FUNC, stroke_width=5)
            self.play(Create(s), FadeIn(VGroup(M("f", 34, SECANT).next_to(ax.c2p(3, f(3)), RIGHT), M("g", 34, DERIV).next_to(ax.c2p(3, g(3)), RIGHT),
                                                M("f + g", 34, FUNC).next_to(ax.c2p(2.6, f(2.6) + g(2.6)), RIGHT))), run_time=1)
            # Adder: show each rise on its own curve first, then stack the same two pieces on f + g
            x0, x1 = 1, 1.8
            df, dg = f(x1) - f(x0), g(x1) - g(x0)
            runs = VGroup(*[DashedLine(ax.c2p(x0, h(x0)), ax.c2p(x1, h(x0)), color=DIM) for h in (f, g, lambda t: f(t) + g(t))])
            on_f = Line(ax.c2p(x1, f(x0)), ax.c2p(x1, f(x1)), color=SECANT, stroke_width=8)
            on_g = Line(ax.c2p(x1, g(x0)), ax.c2p(x1, g(x1)), color=DERIV, stroke_width=8)
            nud = nudge_arrow(ax.c2p(x0, 0), ax.c2p(x1, 0), "dx", DOWN, INK, 30, 0.12)
            self.play(FadeIn(nud), Create(runs[0]), Create(runs[1]), run_time=0.8)
            self.play(Create(on_f), FadeIn(M("df", 30, SECANT).next_to(on_f, RIGHT, buff=0.1)), run_time=0.7)
            self.play(Create(on_g), FadeIn(M("dg", 30, DERIV).next_to(on_g, RIGHT, buff=0.1)), run_time=0.7)
            # carry copies up to the sum: f's rise first, g's rise on top of it
            base = f(x0) + g(x0)
            up_f = on_f.copy(); up_g = on_g.copy()
            self.play(Create(runs[2]), run_time=0.4)
            self.play(up_f.animate.move_to(ax.c2p(x1, base + df / 2)), run_time=1)
            self.play(up_g.animate.move_to(ax.c2p(x1, base + df + dg / 2)), run_time=1)
            br = BraceBetweenPoints(ax.c2p(x1, base + df + dg), ax.c2p(x1, base), RIGHT, color=FUNC).shift(RIGHT * 0.08)
            self.play(GrowFromCenter(br), FadeIn(M("d(f + g)", 30, FUNC).next_to(br, RIGHT, buff=0.1)), run_time=0.8)
            b.line(1)
            e = M(r"\frac{d(f + g)}{dx} = \frac{df}{dx} + \frac{dg}{dx}", 40).to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
            self.play(Write(e), run_time=1.2)
            b.line(2)
            box = formula_box(M(r"\frac{d}{dx}\big[f \pm g\big] = f' \pm g'", 46), DERIV).next_to(e, DOWN, buff=0.6)
            self.play(FadeIn(box), run_time=0.8)
        self.clear()

        self.example("A polynomial", r"Find $f'(x)$ for $f(x) = 4x^3 - 5x^2 + 7x - 2$.",
                     [r"f(x) = 4x^3 - 5x^2 + 7x - 2", r"4x^3 \to 4 \cdot 3x^2 = 12x^2", r"-5x^2 \to -10x, \quad 7x \to 7, \quad -2 \to 0",
                      r"f'(x) = 12x^2 - 10x + 7"], at=[1, 2, 3, 4])
        warn = VGroup(M(r"\frac{x^3 - 2x + 5}{x} = \frac{x^3}{x} - \frac{2x}{x} + \frac{5}{x} \ \checkmark", 34, DERIV),
                      VGroup(M(r"\frac{5}{x + 2} \ne \frac{5}{x} + \frac{5}{2}", 34, TANGENT), T("(several terms below: no split)", 26, DIM)).arrange(DOWN, buff=0.15)
                      ).arrange(DOWN, buff=0.5)
        self.example("Rewrite, then differentiate", r"Find $\dfrac{dy}{dx}$ for $y = \dfrac{x^3 - 2x + 5}{x}$.",
                     [r"y = \frac{x^3}{x} - \frac{2x}{x} + \frac{5}{x}", r"y = x^2 - 2 + 5x^{-1}", r"\frac{dy}{dx} = 2x - 5x^{-2}",
                      r"TEXT:Split a fraction only when the denominator is a single term.", r"TEXT:Several terms below: wait for the quotient rule."], figure=warn, at=[1, 2, 2, 3, 4],
                     figure_at=3)
        a2, _ = plot_axes([-3.5, 3.5, 1], [-16, 18, 8], w=5.2, h=4.2)
        cub2 = lambda x: x ** 3 - 12 * x + 1
        fig2 = VGroup(a2, a2.plot(cub2, x_range=[-3.5, 3.5], color=FUNC, stroke_width=4),
                      Line(a2.c2p(-3, 17), a2.c2p(-1, 17), color=TANGENT, stroke_width=4), Line(a2.c2p(1, -15), a2.c2p(3, -15), color=TANGENT, stroke_width=4),
                      closed_dot(a2, -2, 17, INK), closed_dot(a2, 2, -15, INK))
        self.example("Horizontal tangents", r"Where does $g(x) = x^3 - 12x + 1$ have horizontal tangent lines?",
                     [r"\text{slope of a horizontal line?}", r"0:\ \text{when is } g'(x) = 0\,?", r"g'(x) = 3x^2 - 12 = 0", r"3(x^2 - 4) = 0",
                      r"3(x - 2)(x + 2) = 0", r"TEXT:Zero product property: one of the factors must be $0$.", r"x - 2 = 0 \ \text{ or } \ x + 2 = 0",
                      r"x = 2 \ \text{ or } \ x = -2"],
                     figure=fig2, at=[1, 2, 3, 4, 5, 6, 6, 7], follow=True)
        self.example("In context", r"A company's cost to make $n$ phone cases is $C(n) = 500 + 20n - 0.01n^2$ dollars. Find $C'(100)$ and interpret it.",
                     [r"C'(n) = 0 + 20 - 0.02n", r"C'(100) = 20 - 2 = 18", r"TEXT:At $n = 100$, cost is increasing at $18$ dollars per case. The fixed $500$ has no effect on the rate."],
                     at=[1, 2, 3])

        with self.beat("Close") as b:
            rows = VGroup(M(r"\frac{d}{dx}\, c = 0", 46), M(r"\frac{d}{dx}\, x^n = n x^{n - 1}", 46), M(r"\frac{d}{dx}\big[k\,f\big] = k\,f'", 46),
                          M(r"\frac{d}{dx}\big[f \pm g\big] = f' \pm g'", 46)).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            self.play(FadeIn(formula_box(rows, DERIV)), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A polynomial, term by term", r"Find $f'(x)$ for $f(x) = 6x^5 - 4x^3 + x - 9$.",
                     [r"f(x) = 6x^5 - 4x^3 + x - 9", r"6x^5 \to 6 \cdot 5x^4 = 30x^4", r"-4x^3 \to -12x^2", r"x \to 1, \quad -9 \to 0", r"f'(x) = 30x^4 - 12x^2 + 1"], at=[1, 1, 2, 3, 4])
        self.example("Example 2: Rewrite before differentiating", r"Find $\dfrac{dy}{dx}$ for $y = \dfrac{x^2 + 3}{\sqrt{x}}$.",
                     [r"y = \frac{x^2}{x^{1/2}} + \frac{3}{x^{1/2}}", r"= x^{3/2} + 3x^{-1/2}", r"\frac{dy}{dx} = \frac32 x^{1/2} - \frac32 x^{-3/2}"], at=[1, 2, 3])
        a3, _ = plot_axes([0, 4.5, 1], [0, 6, 1], w=5.4, h=4.2)
        cub = lambda x: x ** 3 - 6 * x * x + 9 * x + 1
        fig = VGroup(a3, a3.plot(cub, x_range=[0, 4.3], color=FUNC, stroke_width=4),
                     Line(a3.c2p(0.4, 5), a3.c2p(1.6, 5), color=TANGENT, stroke_width=4), Line(a3.c2p(2.4, 1), a3.c2p(3.6, 1), color=TANGENT, stroke_width=4),
                     closed_dot(a3, 1, 5, INK), closed_dot(a3, 3, 1, INK))
        self.example("Example 3: Horizontal tangents", r"Where does $y = x^3 - 6x^2 + 9x + 1$ have horizontal tangent lines?",
                     [r"\text{horizontal: slope } 0 \ \Rightarrow\ y' = 0", r"y' = 3x^2 - 12x + 9 = 3(x - 1)(x - 3) = 0", r"x = 1 \text{ and } x = 3"], figure=fig, at=[1, 2, 3])
        self.finish()
