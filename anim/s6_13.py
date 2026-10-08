"""Topic 6.13 (BC): Improper integrals. Narration comes from transcripts/6_13.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.13"

    def construct(self):
        a1, l1 = plot_axes([0, 10, 1], [0, 1.2, 0.5], w=8.6, h=2.6, coords=False, ylabel="1/x^2")
        a2, l2 = plot_axes([0, 10, 1], [0, 1.2, 0.5], w=8.6, h=2.6, coords=False, ylabel="1/x")
        VGroup(VGroup(a1, l1), VGroup(a2, l2)).arrange(DOWN, buff=0.6).to_edge(LEFT, buff=0.6)
        B = ValueTracker(1.05)
        with self.beat("An endless region") as b:
            self.play(FadeIn(T("BC only", 28, DIM).to_corner(UR, buff=0.4)), FadeIn(a1), FadeIn(l1), FadeIn(a2), FadeIn(l2),
                      Create(a1.plot(lambda s: 1 / s**2, x_range=[0.92, 10], color=FUNC, stroke_width=4)), Create(a2.plot(lambda s: 1 / s, x_range=[0.85, 10], color=FUNC, stroke_width=4)), run_time=1.2)
            sh1 = always_redraw(lambda: a1.get_area(a1.plot(lambda s: 1 / s**2, x_range=[1, B.get_value()]), x_range=[1, B.get_value()], color=DERIV, opacity=0.45))
            sh2 = always_redraw(lambda: a2.get_area(a2.plot(lambda s: 1 / s, x_range=[1, B.get_value()]), x_range=[1, B.get_value()], color=TANGENT, opacity=0.45))
            r1 = always_redraw(lambda: M(rf"1 - \tfrac1b = {1 - 1 / B.get_value():.3f}", 32, DERIV).next_to(a1, RIGHT, buff=0.3))
            r2 = always_redraw(lambda: M(rf"\ln b = {np.log(B.get_value()):.3f}", 32, TANGENT).next_to(a2, RIGHT, buff=0.3))
            self.add(sh1, sh2, r1, r2)
            b.line(1)
            self.play(B.animate.set_value(9.8), run_time=4, rate_func=rate_functions.ease_in_sine)
            b.line(2)
            self.play(FadeIn(T(r"$\to 1$", 30, DERIV).next_to(r1, DOWN, buff=0.15)), FadeIn(T(r"$\to \infty$", 30, TANGENT).next_to(r2, DOWN, buff=0.15)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Infinite limits of integration") as b:
            d = M(r"\int_a^\infty f(x)\,dx = \lim_{b\to\infty} \int_a^b f(x)\,dx", 50, ACCUM).to_edge(UP, buff=0.5)
            self.play(Write(d), run_time=1.2)
            b.line(1)
            tags = VGroup(T("a number: converges", 30, DERIV), T("infinite or no limit: diverges", 30, TANGENT)).arrange(RIGHT, buff=1.2).next_to(d, DOWN, buff=0.35)
            self.play(FadeIn(tags), run_time=0.6)
            b.line(2)
            w1 = M(r"\lim_{b\to\infty} \int_1^b x^{-2}\,dx = \lim_{b\to\infty} \left[-\frac1x\right]_1^b = \lim_{b\to\infty} \left(-\frac1b + 1\right) = 1", 38, DERIV).next_to(tags, DOWN, buff=0.6)
            w1.set_max_width(13)
            self.play(Write(w1), run_time=1.6)
            b.line(3)
            w2 = M(r"\lim_{b\to\infty} \int_1^b \frac1x\,dx = \lim_{b\to\infty} \ln b = \infty", 38, TANGENT).next_to(w1, DOWN, buff=0.5)
            self.play(Write(w2), run_time=1.2)
            b.line(4)
            self.play(FadeIn(T("Write the limit on every line.", 34, SECANT).to_edge(DOWN, buff=0.5)), run_time=0.6)
        self.clear()

        ax, al = plot_axes([0, 1.2, 0.5], [0, 6, 1], w=4.6, h=5, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        A = ValueTracker(0.6)
        with self.beat("A vertical asymptote") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda s: 1 / np.sqrt(s), x_range=[0.028, 1.15], color=FUNC, stroke_width=4)), run_time=1)
            self.add(always_redraw(lambda: ax.get_area(ax.plot(lambda s: 1 / np.sqrt(s), x_range=[A.get_value(), 1]), x_range=[A.get_value(), 1], color=AREA, opacity=0.45)))
            b.line(1)
            rows = VGroup(M(r"\int_0^1 x^{-1/2}\,dx = \lim_{a\to0^+} \int_a^1 x^{-1/2}\,dx", 38), M(r"= \lim_{a\to0^+} \left[2\sqrt x\right]_a^1", 38),
                          M(r"= \lim_{a\to0^+} \left(2 - 2\sqrt a\right) = 2", 38, AREA)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.5).shift(UP * 1)
            self.play(Write(rows[0]), A.animate.set_value(0.2), run_time=1.4)
            b.line(2)
            self.play(Write(rows[1]), run_time=1)
            b.line(3)
            self.play(Write(rows[2]), A.animate.set_value(0.03), run_time=1.6)
        self.clear()

        with self.beat("p-integrals") as b:
            rule = formula_box(M(r"\int_1^\infty \frac{1}{x^p}\,dx \ \text{ converges if } p > 1, \ \text{diverges if } p \le 1", 42, ACCUM), ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(rule), run_time=0.8)
            b.line(1)
            minis = VGroup()
            for p, col, word in ((2, DERIV, "converges (to 1)"), (1, TANGENT, "diverges"), (0.5, TANGENT, "diverges")):
                a, _ = plot_axes([0, 6, 1], [0, 1.4, 1], w=3.4, h=2, coords=False)
                g = VGroup(a, a.plot(lambda s, p=p: 1 / s**p, x_range=[0.8, 6], color=col, stroke_width=4))
                minis.add(VGroup(g, M(rf"p = {p}", 32, col), T(word, 28, col)).arrange(DOWN, buff=0.2))
            minis.arrange(RIGHT, buff=0.7).next_to(rule, DOWN, buff=0.6)
            self.play(LaggedStart(*[FadeIn(m) for m in minis], lag_ratio=0.4), run_time=1.6)
        self.clear()

        self.example("A hidden asymptote", r"Evaluate $\displaystyle\int_{-1}^{1} \frac{1}{x^2}\,dx$.",
                     [r"\text{tempting: } \left[-\tfrac1x\right]_{-1}^{1} = -2 \ \ \text{(but } \tfrac{1}{x^2} > 0\text{)}", r"TEXT:$\frac{1}{x^2} \to \infty$ at $x = 0$, inside $[-1, 1]$: split there.",
                      r"\int_0^1 x^{-2}\,dx = \lim_{a\to0^+} \left[-\frac1x\right]_a^1 = \lim_{a\to0^+} \left(-1 + \frac1a\right)", r"= \infty: \ \text{diverges, so the whole integral diverges}"],
                     at=[1, 2, 3, 4])

        with self.beat("Close") as b:
            card = VGroup(M(r"\int_a^\infty f\,dx = \lim_{b\to\infty} \int_a^b f\,dx", 44, ACCUM), T("Asymptote at $c$: replace $c$ by a limit.", 36),
                          T("A number: converges. Infinite or no limit: diverges.", 36), T("Write the limit on every line. Check inside the interval.", 34, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: An exponential tail", r"Evaluate $\displaystyle\int_0^\infty e^{-2x}\,dx$.",
                     [r"= \lim_{b\to\infty} \int_0^b e^{-2x}\,dx", r"= \lim_{b\to\infty} \left[-\tfrac12 e^{-2x}\right]_0^b = \lim_{b\to\infty} \left(-\tfrac12 e^{-2b} + \tfrac12\right)", r"= 0 + \tfrac12 = \tfrac12: \ \text{converges}"],
                     at=[1, 2, 4])
        self.example("Example 2: A slow tail", r"Evaluate $\displaystyle\int_1^\infty \frac{x}{x^2 + 1}\,dx$.",
                     [r"= \lim_{b\to\infty} \int_1^b \frac{x}{x^2 + 1}\,dx = \lim_{b\to\infty} \left[\tfrac12\ln\left(x^2 + 1\right)\right]_1^b", r"= \lim_{b\to\infty} \left(\tfrac12\ln\left(b^2 + 1\right) - \tfrac12\ln 2\right)",
                      r"= \infty: \ \text{diverges}"], at=[1, 2, 4])
        self.finish()
