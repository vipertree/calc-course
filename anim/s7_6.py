"""Topic 7.6: General solutions by separation of variables. Narration comes from transcripts/7_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.6"
    example_ref = r"\text{separate, integrate, solve}"

    def construct(self):
        with self.beat("Sorting the variables") as b:
            de = M(r"\frac{dy}{dx}", r"=", r"x", r"y", 64).shift(UP * 1.6)
            self.play(Write(de), run_time=1)
            b.line(1)
            sep = M(r"\frac{dy}{y}", r"=", r"x\,dx", 64).shift(UP * 0.1)
            self.play(TransformFromCopy(de, sep), run_time=1.4)
            labs = VGroup(T("all the $y$'s with $dy$", 30, ACCUM).next_to(sep[0], DOWN, buff=0.4), T("all the $x$'s with $dx$", 30, SECANT).next_to(sep[2], DOWN, buff=0.4))
            self.play(FadeIn(labs), run_time=0.6)
            b.line(2)
            integ = M(r"\int \frac{dy}{y} = \int x\,dx", 60, ACCUM).shift(DOWN * 2)
            self.play(Write(integ), run_time=1)
        self.clear()
        self.title()

        with self.beat("The method") as b:
            rows = VGroup(M(r"1.\ \ \frac{dy}{y} = x\,dx", 40), M(r"2.\ \ \ln|y| = \frac{x^2}{2} + C", 40), T("3. one constant, on the $x$ side", 34, DIM),
                          M(r"4.\ \ |y| = e^{x^2/2 + C} = e^C e^{x^2/2}", 40), M(r"y = Ae^{x^2/2}", 48, ACCUM)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(LEFT, buff=1.0)
            for k, m in enumerate(rows[:4]):
                if k:
                    b.line(k)
                self.play(FadeIn(m), run_time=0.8)
            b.line(4)
            self.play(Write(rows[4]), FadeIn(T(r"$A = \pm e^C$, any constant", 28, DIM).next_to(rows[4], RIGHT, buff=0.5)), run_time=1)
            ax, _ = plot_axes([-2, 2, 1], [-4, 4, 2], w=3.8, h=3.4, coords=False)
            fam = VGroup(ax, *[ax.plot(lambda s, a=a: a * np.exp(s * s / 2), x_range=[-1.6, 1.6] if abs(a) < 1 else [-1.25, 1.25], color=FUNC, stroke_width=3) for a in (-1.5, -0.5, 0.5, 1.5)])
            fam.to_edge(RIGHT, buff=0.5).shift(UP * 0.8)
            self.play(FadeIn(fam), run_time=0.8)
        self.clear()

        self.example("Another one", r"Find the general solution of $\dfrac{dy}{dx} = \dfrac{x^2}{y}$.",
                     [r"y\,dy = x^2\,dx", r"\frac{y^2}{2} = \frac{x^3}{3} + C", r"y^2 = \frac23x^3 + 2C = \frac23x^3 + K", r"y = \pm\sqrt{\tfrac23x^3 + K}"], at=[1, 2, 3, 4])

        with self.beat("Close") as b:
            card = VGroup(T("Separate: $y$'s with $dy$, $x$'s with $dx$.", 38), T("Integrate both sides; one $+\\,C$.", 38), T(r"Solve for $y$: constants combine ($A = \pm e^C$, $K = 2C$).", 34),
                          T("A general solution is a family.", 36, ACCUM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A trig factor", r"Find the general solution of $\dfrac{dy}{dx} = y\cos x$.",
                     [r"\frac{dy}{y} = \cos x\,dx", r"\ln|y| = \sin x + C", r"|y| = e^C e^{\sin x}", r"y = Ae^{\sin x}"], at=[1, 2, 3, 4])
        self.example("Example 2: Newton's law of cooling", r"Find the general solution of $\dfrac{dT}{dt} = k(T - 70)$.",
                     [r"\frac{dT}{T - 70} = k\,dt", r"\ln|T - 70| = kt + C", r"T - 70 = Ae^{kt}", r"T = 70 + Ae^{kt}"], at=[1, 2, 3, 4])
        self.example("Example 3: An exponential mix", r"Find the general solution of $\dfrac{dy}{dx} = e^{x - y}$.",
                     [r"e^{x - y} = e^x e^{-y}", r"e^y\,dy = e^x\,dx", r"e^y = e^x + C", r"y = \ln\left(e^x + C\right)"], at=[1, 2, 3, 4])
        self.finish()
