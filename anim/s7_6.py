"""Topic 7.6: General solutions by separation of variables. Narration comes from transcripts/7_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.6"
    example_ref = r"\text{separate, integrate, solve}"

    def construct(self):
        with self.beat("Stop and ponder") as b:
            de = M(r"\frac{dy}{dx} = xy", 64, ACCUM).shift(UP * 2.4)
            self.play(Write(de), run_time=1)
            b.line(1)
            q = M(r"\int xy\,dx \ \ ?", 52).shift(UP * 0.6 + LEFT * 2.6)
            why = T(r"$xy$ is a function of $x$ \emph{and} $y$", 32, DIM).next_to(q, RIGHT, buff=0.8)
            self.play(FadeIn(q), run_time=0.7)
            self.play(FadeIn(why), run_time=0.7)
            self.play(Create(Cross(q, stroke_color=TANGENT, stroke_width=5)), run_time=0.6)
            b.line(2)
            plan = M(r"(\text{a function of } y)", r"\,dy", r"\ =\ ", r"(\text{a function of } x)", r"\,dx", 44).shift(DOWN * 1.2)
            plan[0:2].set_color(ACCUM)
            plan[3:5].set_color(SECANT)
            then = T("then integrate both sides", 34).next_to(plan, DOWN, buff=0.5)
            self.play(FadeIn(plan), run_time=1)
            self.play(FadeIn(then), run_time=0.6)
        self.clear()

        with self.beat("Sorting the variables") as b:
            de = M(r"\frac{dy}{dx} = xy", 56).shift(UP * 2.75)
            self.play(FadeIn(de), run_time=0.6)
            ops = T(r"divide both sides by $y$, multiply both sides by $dx$", 30, DIM).shift(UP * 1.75)
            sep = M(r"\frac{dy}{y}", r"\ =\ ", r"x\,dx", 60).shift(UP * 0.55)
            sep[0].set_color(ACCUM)
            sep[2].set_color(SECANT)
            self.play(FadeIn(ops), run_time=0.6)
            self.play(FadeIn(sep, shift=DOWN * 0.2), run_time=1)
            labs = VGroup(T("all the $y$'s with $dy$", 30, ACCUM).next_to(sep[0], DOWN, buff=0.3).shift(LEFT * 1.4),
                          T("all the $x$'s with $dx$", 30, SECANT).next_to(sep[2], DOWN, buff=0.3).shift(RIGHT * 1.4))
            self.play(FadeIn(labs), run_time=0.6)
            b.line(1)
            integ = M(r"\int \frac{dy}{y} = \int x\,dx", 60).shift(DOWN * 1.55)
            self.play(Write(integ), run_time=1)
            b.line(2)
            real = M(r"\int", r"\frac1y", r"\,", r"dy", r" = \int x\,dx", 60).move_to(integ)
            self.play(ReplacementTransform(integ, real), run_time=1)
            br1, br2 = Brace(real[1], DOWN, color=ACCUM, buff=0.1), Brace(real[3], DOWN, color=DERIV, buff=0.1)
            l1 = T("integrand", 30, ACCUM).next_to(br1, DOWN, buff=0.12).shift(LEFT * 0.7)
            l2 = T("with respect to $y$", 30, DERIV).next_to(br2, DOWN, buff=0.12).shift(RIGHT * 1.3)
            self.play(real[1].animate.set_color(ACCUM), real[3].animate.set_color(DERIV), FadeIn(br1), FadeIn(br2), FadeIn(l1), FadeIn(l2), run_time=1)
        self.clear()
        self.title()

        def problem():
            return formula_box(M(r"\frac{dy}{dx} = xy", 40), ACCUM).to_corner(UL, buff=0.4)

        with self.beat("The method") as b:
            box = problem()
            self.play(FadeIn(box), run_time=0.6)
            r1 = M(r"1.\ \ \text{Separate: } \ \frac{dy}{y} = x\,dx", 42)
            r2 = M(r"2.\ \ \text{Integrate: } \ \int \frac1y\,dy = \int x\,dx", 42)
            r3 = M(r"\ln|y| = \frac{x^2}{2} + C", 42)
            rows = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(box, DOWN, buff=0.7).to_edge(LEFT, buff=1.0)
            r3.shift(RIGHT * 2.9)
            self.play(Indicate(box, color=ACCUM), run_time=0.6)
            self.play(FadeIn(r1), run_time=0.8)
            b.line(1)
            self.play(FadeIn(r2), run_time=0.8)
            self.play(FadeIn(r3), run_time=0.8)
        self.clear()

        with self.beat("Only one constant") as b:
            box = problem()
            head = T("3. One constant", 40).next_to(box, DOWN, buff=0.5).to_edge(LEFT, buff=1.0)
            self.play(FadeIn(box), FadeIn(head), run_time=0.7)
            b.line(1)
            e1 = M(r"\ln|y|", r" + D", r" = \frac{x^2}{2}", r" + C", 48).next_to(head, DOWN, buff=0.5).align_to(head, LEFT).shift(RIGHT * 0.6)
            e1[1].set_color(SECANT)
            e1[3].set_color(ACCUM)
            n1 = T("each side gets a constant", 30, DIM).next_to(e1, RIGHT, buff=0.8)
            self.play(Write(e1), run_time=1)
            self.play(FadeIn(n1), Indicate(e1[1], color=SECANT), Indicate(e1[3], color=ACCUM), run_time=0.9)
            b.line(2)
            sub = T("subtract $D$ from both sides", 28, DIM).next_to(e1, DOWN, buff=0.45).align_to(e1, LEFT)
            e2 = M(r"\ln|y| = \frac{x^2}{2} + ", r"C - D", 48).next_to(sub, DOWN, buff=0.35).align_to(e1, LEFT)
            self.play(FadeIn(sub), run_time=0.5)
            self.play(Write(e2), run_time=1)
            b.line(3)
            bx = SurroundingRectangle(e2[1], color=SECANT, buff=0.1)
            n2 = T("just a new constant", 30, SECANT).next_to(e2, RIGHT, buff=0.8)
            self.play(Create(bx), FadeIn(n2), run_time=0.8)
            e3 = M(r"\ln|y| = \frac{x^2}{2} + ", r"C", 48).next_to(e2, DOWN, buff=0.6).align_to(e1, LEFT)
            e3[1].set_color(ACCUM)
            n3 = T("one constant, on one side", 30, ACCUM).next_to(e3, RIGHT, buff=0.8)
            self.play(Write(e3), FadeIn(n3), run_time=1)
        self.clear()

        with self.beat("Solve for y") as b:
            box = problem()
            self.play(FadeIn(box), run_time=0.6)
            r4 = M(r"4.\ \ |y| = e^{x^2/2 + C} = e^C e^{x^2/2}", 42).next_to(box, DOWN, buff=0.7).to_edge(LEFT, buff=1.0)
            self.play(FadeIn(r4), run_time=0.9)
            b.line(1)
            r5 = M(r"y = Ae^{x^2/2}", 52, ACCUM).next_to(r4, DOWN, buff=0.6).align_to(r4, LEFT).shift(RIGHT * 0.9)
            note = T(r"$A = \pm e^C$, any constant", 30, DIM).next_to(r5, DOWN, buff=0.3).align_to(r5, LEFT)
            ax, _ = plot_axes([-2, 2, 1], [-4, 4, 2], w=3.6, h=3.2, coords=False)
            fam = VGroup(ax, *[ax.plot(lambda s, a=a: a * np.exp(s * s / 2), x_range=[-1.6, 1.6] if abs(a) < 1 else [-1.25, 1.25], color=FUNC, stroke_width=3) for a in (-1.5, -0.5, 0.5, 1.5)])
            fam.to_edge(RIGHT, buff=0.7).to_edge(DOWN, buff=0.9)
            self.play(Write(r5), FadeIn(note), run_time=1)
            self.play(FadeIn(fam), run_time=0.8)
        self.clear()

        self.example("Another one", r"Find the general solution of $\dfrac{dy}{dx} = \dfrac{x^2}{y}$.",
                     [r"y\,dy = x^2\,dx", r"\int y\,dy = \int x^2\,dx", r"\frac{y^2}{2} = \frac{x^3}{3} + C", r"y^2 = \frac23x^3 + 2C = \frac23x^3 + K", r"y = \pm\sqrt{\tfrac23x^3 + K}"], at=[1, 2, 2, 3, 4])

        with self.beat("Close") as b:
            card = VGroup(T("Separate: $y$'s with $dy$, $x$'s with $dx$.", 38), T("Integrate both sides; one $+\\,C$.", 38), T(r"Solve for $y$: constants combine ($A = \pm e^C$, $K = 2C$).", 34),
                          T("A general solution is a family.", 36, ACCUM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A trig factor", r"Find the general solution of $\dfrac{dy}{dx} = y\cos x$.",
                     [r"\frac{dy}{y} = \cos x\,dx", r"\int \frac1y\,dy = \int \cos x\,dx", r"\ln|y| = \sin x + C", r"|y| = e^C e^{\sin x}", r"y = Ae^{\sin x}"], at=[1, 2, 2, 3, 4])
        self.example("Example 2: Newton's law of cooling", r"Find the general solution of $\dfrac{dT}{dt} = k(T - 70)$.",
                     [r"\frac{dT}{T - 70} = k\,dt", r"\int \frac{1}{T - 70}\,dT = \int k\,dt", r"\ln|T - 70| = kt + C", r"|T - 70| = e^C e^{kt}", r"T - 70 = Ae^{kt}", r"T = 70 + Ae^{kt}"], at=[1, 2, 2, 3, 3, 4], size=44)
        self.example("Example 3: An exponential mix", r"Find the general solution of $\dfrac{dy}{dx} = e^{x - y}$.",
                     [r"e^{x - y} = e^x e^{-y}", r"e^y\,dy = e^x\,dx", r"\int e^y\,dy = \int e^x\,dx", r"e^y = e^x + C", r"y = \ln\left(e^x + C\right)"], at=[1, 2, 3, 3, 4])
        self.finish()
