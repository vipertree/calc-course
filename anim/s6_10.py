"""Topic 6.10: Long division and completing the square. Narration comes from transcripts/6_10.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.10"

    def construct(self):
        with self.beat("Two rewrites") as b:
            L = VGroup(M(r"\int \frac{x^2 + 3x + 5}{x + 1}\,dx", 48), T("top degree $\\ge$ bottom degree: divide", 30, SECANT)).arrange(DOWN, buff=0.4)
            R = VGroup(M(r"\int \frac{1}{x^2 + 4x + 13}\,dx", 48), T("quadratic bottom, no real roots: complete the square", 30, ACCUM)).arrange(DOWN, buff=0.4)
            VGroup(L, R).arrange(RIGHT, buff=1.0).shift(UP * 0.6)
            VGroup(L, R).set_max_width(13)
            self.play(FadeIn(L[0]), FadeIn(R[0]), run_time=1)
            b.line(1)
            self.play(FadeIn(L[1]), run_time=0.6)
            b.line(2)
            self.play(FadeIn(R[1]), run_time=0.6)
            self.play(FadeIn(T("rewrite into a form you know", 34, DIM).to_edge(DOWN, buff=0.8)), run_time=0.6)
        self.clear()
        self.title()

        with self.beat("Divide first") as b:
            q = M(r"x + 2", 44, SECANT)
            dvs = M(r"x + 1", 44)
            dvd = M(r"x^2 + 3x + 5", 44)
            bar = Line(LEFT * 1.4, RIGHT * 1.6, color=INK, stroke_width=3)
            dvd.move_to(ORIGIN)
            bar.next_to(dvd, UP, buff=0.12).align_to(dvd, LEFT).shift(LEFT * 0.15)
            hook = Line(bar.get_start(), bar.get_start() + DOWN * 0.7, color=INK, stroke_width=3)
            dvs.next_to(hook, LEFT, buff=0.15)
            q.next_to(bar, UP, buff=0.12).align_to(dvd, RIGHT)
            r1 = M(r"-(x^2 + x)", 44, DIM).next_to(dvd, DOWN, buff=0.2).align_to(dvd, LEFT)
            s1 = M(r"2x + 5", 44).next_to(r1, DOWN, buff=0.2).align_to(dvd, RIGHT)
            r2 = M(r"-(2x + 2)", 44, DIM).next_to(s1, DOWN, buff=0.2).align_to(dvd, RIGHT)
            s2 = M(r"3", 44, TANGENT).next_to(r2, DOWN, buff=0.2).align_to(dvd, RIGHT)
            div = VGroup(q, dvs, dvd, bar, hook, r1, s1, r2, s2).to_edge(LEFT, buff=1.0).shift(UP * 0.8)
            self.play(FadeIn(dvs), FadeIn(dvd), Create(bar), Create(hook), run_time=1)
            b.line(1)
            self.play(FadeIn(q[0][0]), Write(r1), run_time=1)
            self.play(Write(s1), run_time=0.8)
            b.line(2)
            self.play(FadeIn(q[0][1:]), Write(r2), run_time=1)
            self.play(Write(s2), run_time=0.8)
            b.line(3)
            res = M(r"\frac{x^2 + 3x + 5}{x + 1} = x + 2 + \frac{3}{x + 1}", 42).to_edge(RIGHT, buff=0.5).shift(UP * 1.6)
            self.play(Write(res), run_time=1.2)
            b.line(4)
            ans = M(r"\int = \frac{x^2}{2} + 2x + 3\ln|x + 1| + C", 42, ACCUM).next_to(res, DOWN, buff=0.6).align_to(res, LEFT)
            self.play(Write(ans), run_time=1.2)
        self.clear()

        with self.beat("Two more forms") as b:
            r1 = formula_box(M(r"\int \frac{du}{a^2 + u^2} = \frac1a\arctan\frac ua + C", 46, ACCUM), ACCUM)
            r2 = formula_box(M(r"\int \frac{du}{\sqrt{a^2 - u^2}} = \arcsin\frac ua + C", 46, ACCUM), ACCUM)
            VGroup(r1, r2).arrange(DOWN, buff=0.7).shift(UP * 0.5)
            src = T("from the inverse trig derivatives, with $a^2$ in place of $1$", 30, DIM).to_edge(UP, buff=0.5)
            self.play(FadeIn(src), run_time=0.6)
            b.line(1)
            self.play(FadeIn(r1), run_time=0.8)
            b.line(2)
            self.play(FadeIn(r2), run_time=0.8)
            b.line(3)
            tip = T("Complete the square to make $a^2 + u^2$ or $a^2 - u^2$.", 34, SECANT).to_edge(DOWN, buff=0.7)
            self.play(FadeIn(tip), run_time=0.6)
        self.clear()

        self.example("Complete the square", r"Find $\displaystyle\int \frac{1}{x^2 + 4x + 13}\,dx$.",
                     [r"x^2 + 4x + 13 = \left(x^2 + 4x + 4\right) + 9 = (x + 2)^2 + 9", r"u = x + 2, \ \ du = dx, \ \ a = 3", r"\int \frac{du}{u^2 + 3^2} = \frac13\arctan\frac u3",
                      r"= \frac13\arctan\frac{x + 2}{3} + C"], at=[1, 2, 3, 4], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T(r"Top degree $\ge$ bottom degree: divide first.", 36, SECANT), T("Quadratic bottom that won't factor: complete the square.", 36),
                          M(r"\int \frac{du}{a^2 + u^2} = \frac1a\arctan\frac ua + C", 40, ACCUM), M(r"\int \frac{du}{\sqrt{a^2 - u^2}} = \arcsin\frac ua + C", 40, ACCUM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A cubic over a line", r"Find $\displaystyle\int \frac{x^3 + 1}{x - 1}\,dx$.",
                     [r"x^3 + 1 = (x - 1)\left(x^2 + x + 1\right) + 2", r"\frac{x^3 + 1}{x - 1} = x^2 + x + 1 + \frac{2}{x - 1}", r"\int = \frac{x^3}{3} + \frac{x^2}{2} + x + 2\ln|x - 1| + C"],
                     at=[1, 2, 3])
        self.example("Example 2: An arcsine", r"Find $\displaystyle\int \frac{1}{\sqrt{-x^2 + 6x - 5}}\,dx$.",
                     [r"-x^2 + 6x - 5 = -\left(x^2 - 6x\right) - 5", r"= -\left(x^2 - 6x + 9\right) + 9 - 5 = 4 - (x - 3)^2", r"u = x - 3, \ \ a = 2",
                      r"\int \frac{du}{\sqrt{2^2 - u^2}} = \arcsin\frac u2 = \arcsin\frac{x - 3}{2} + C"], at=[1, 2, 3, 4])
        self.example("Example 3: A definite integral", r"Evaluate $\displaystyle\int_0^1 \frac{x}{x + 1}\,dx$.",
                     [r"\frac{x}{x + 1} = 1 - \frac{1}{x + 1}", r"\int_0^1 \left(1 - \frac{1}{x + 1}\right) dx = \left[x - \ln|x + 1|\right]_0^1", r"= (1 - \ln 2) - (0 - \ln 1)", r"= 1 - \ln 2"],
                     at=[1, 2, 3, 4])
        self.finish()
