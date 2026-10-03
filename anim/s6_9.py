"""Topic 6.9: Integrating using substitution. Narration comes from transcripts/6_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.9"
    example_ref = r"u = \text{inside},\ \ du = u'\,dx"      # the substitution recipe stays in the corner during examples (Adder: keep the rule on screen)

    def construct(self):
        with self.beat("The chain rule, backward") as b:
            d = M(r"\frac{d}{dx}\sin\left(", r"x^2", r"\right) = \cos\left(x^2\right) \cdot ", r"2x", 56).shift(UP * 1.5)
            br = Brace(d[1], DOWN, color=SECANT)
            self.play(Write(d), run_time=1.2)
            self.play(FadeIn(br), FadeIn(T("inside", 28, SECANT).next_to(br, DOWN, buff=0.1)), d[3].animate.set_color(DERIV), run_time=0.8)
            b.line(1)
            i = M(r"\int ", r"2x", r"\cos\left(x^2\right)dx = \sin\left(x^2\right) + C", 56).shift(DOWN * 0.8)
            i[1].set_color(DERIV)
            self.play(Write(i), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("the derivative of the inside is a factor", 32, DERIV).next_to(i, DOWN, buff=0.6)), Indicate(i[1], color=DERIV), run_time=1)
        self.clear()
        self.title()

        with self.beat("The method") as b:
            top = M(r"\int ", r"2x\,dx", r"\cdot\cos\left(", r"x^2", r"\right)", 56).to_edge(UP, buff=0.6)
            self.play(Write(top), run_time=1)
            steps = VGroup(M(r"1.\ \ u = x^2", 44), M(r"2.\ \ du = 2x\,dx", 44), M(r"3.\ \ \int \cos u\,du", 44, SECANT), M(r"4.\ \ \sin u + C = \sin\left(x^2\right) + C", 44, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(top, DOWN, buff=0.7)
            br = Brace(top[3], DOWN, color=SECANT)
            self.play(FadeIn(br), Write(steps[0]), run_time=1)
            b.line(1)
            box = SurroundingRectangle(top[1], color=DERIV, buff=0.06)
            self.play(Create(box), Write(steps[1]), run_time=1)
            b.line(2)
            self.play(Write(steps[2]), run_time=1)
            b.line(3)
            self.play(Write(steps[3]), run_time=1.2)
        self.clear()

        self.example("Fixing a constant", r"Find $\displaystyle\int x\sqrt{x^2 + 4}\,dx$.",
                     [r"u = x^2 + 4", r"du = 2x\,dx, \ \ x\,dx = \tfrac12\,du", r"\int \sqrt u \cdot \tfrac12\,du = \tfrac12\int u^{1/2}\,du", r"= \tfrac12 \cdot \frac{u^{3/2}}{3/2} = \tfrac13 u^{3/2}",
                      r"= \tfrac13\left(x^2 + 4\right)^{3/2} + C"], at=[1, 2, 3, 4, 5])
        self.example("Definite integrals: change the limits", r"Evaluate $\displaystyle\int_0^2 x\left(x^2 + 1\right)^3 dx$.",
                     [r"u = x^2 + 1, \ \ du = 2x\,dx, \ \ x\,dx = \tfrac12\,du", r"x = 0: \ u = 1; \ \ x = 2: \ u = 5", r"\tfrac12\int_1^5 u^3\,du", r"= \tfrac12\left[\frac{u^4}{4}\right]_1^5 = \tfrac18(625 - 1)",
                      r"= \frac{624}{8} = 78"], at=[1, 2, 3, 4, 5], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T("$u$: an inside function whose derivative is a factor.", 36), M(r"du = u'\,dx; \ \text{fix constants by dividing}", 40),
                          T("Rewrite everything in $u$, integrate, put $x$ back.", 36), T("Definite: change the limits to $u$ values.", 36, ACCUM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A linear inside", r"Find $\displaystyle\int e^{3x}\,dx$.",
                     [r"u = 3x, \ \ du = 3\,dx, \ \ dx = \tfrac13\,du", r"\int e^u \cdot \tfrac13\,du = \tfrac13 e^u", r"= \tfrac13 e^{3x} + C"], at=[1, 2, 3])
        self.example("Example 2: A logarithm inside", r"Find $\displaystyle\int \frac{\ln x}{x}\,dx$.",
                     [r"u = \ln x, \ \ du = \frac1x\,dx", r"\int u\,du = \frac{u^2}{2}", r"= \frac{(\ln x)^2}{2} + C"], at=[1, 2, 3])
        self.example("Example 3: Trig with new limits", r"Evaluate $\displaystyle\int_0^{\pi/2} \cos^2 x\,\sin x\,dx$.",
                     [r"u = \cos x, \ \ du = -\sin x\,dx, \ \ \sin x\,dx = -du", r"x = 0: \ u = 1; \ \ x = \tfrac\pi2: \ u = 0", r"-\int_1^0 u^2\,du = \int_0^1 u^2\,du",
                      r"= \left[\frac{u^3}{3}\right]_0^1 = \frac13"], at=[1, 2, 3, 4])
        self.finish()
