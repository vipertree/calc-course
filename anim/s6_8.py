"""Topic 6.8: Antiderivatives and indefinite integrals. Narration comes from transcripts/6_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.8"

    def construct(self):
        ax, al = plot_axes([-2.5, 2.5, 1], [-3, 8, 1], w=6.4, h=5.4, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        shifts = [(-2, TANGENT), (0, FUNC), (1, DERIV), (3, ACCUM)]
        with self.beat("A whole family") as b:
            self.play(FadeIn(ax), FadeIn(al), run_time=0.6)
            curves = VGroup(*[ax.plot(lambda s, c=c: s * s + c, x_range=[-2.3, 2.3], color=col, stroke_width=4) for c, col in shifts])
            labs = VGroup(*[M(rf"x^2 {'+' if c >= 0 else '-'} {abs(c)}" if c else "x^2", 28, col).next_to(ax.c2p(2.3, 2.3 ** 2 + c), RIGHT, buff=0.1) for c, col in shifts])
            for c, l in zip(curves, labs):
                self.play(Create(c), FadeIn(l), run_time=0.6)
            b.line(1)
            tans = VGroup(*[tangent_line(ax, lambda s, c=c: s * s + c, 1, 2, [0.4, 1.6], color=SECANT).set_stroke(width=4) for c, _ in shifts])
            self.play(Create(tans), FadeIn(T("slope $2$ at $x = 1$ on every one", 30, SECANT).to_edge(RIGHT, buff=0.6).shift(UP * 1.5)), run_time=1)
            b.line(2)
            fam = M(r"\text{derivative } 2x: \quad x^2 + C", 46, ACCUM).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
            self.play(Write(fam), run_time=1)
        self.clear()
        self.title()

        with self.beat("Indefinite integrals") as b:
            eq = M(r"\int f(x)\,dx = F(x) + C, \quad F'(x) = f(x)", 54, ACCUM).to_edge(UP, buff=0.8)
            self.play(Write(eq), run_time=1.2)
            tags = VGroup(T("no limits: indefinite", 30, DIM).next_to(eq, DOWN, buff=0.3).align_to(eq, LEFT), T("$+\\,C$: the constant of integration", 30, DIM).next_to(eq, DOWN, buff=0.3).align_to(eq, RIGHT))
            self.play(FadeIn(tags[0]), run_time=0.5)
            b.line(1)
            self.play(FadeIn(tags[1]), run_time=0.5)
            b.line(2)
            cmp = VGroup(VGroup(M(r"\int_1^3 2x\,dx = 8", 44, AREA), T("a number", 30, DIM)).arrange(DOWN, buff=0.2),
                         VGroup(M(r"\int 2x\,dx = x^2 + C", 44, ACCUM), T("a family of functions", 30, DIM)).arrange(DOWN, buff=0.2)).arrange(RIGHT, buff=1.6).shift(DOWN * 1.4)
            self.play(FadeIn(cmp[0]), run_time=0.6)
            self.play(FadeIn(cmp[1]), run_time=0.6)
        self.clear()

        with self.beat("The basic rules") as b:
            g1 = VGroup(M(r"\int x^n\,dx = \frac{x^{n+1}}{n + 1} + C \ \ (n \ne -1)", 32), M(r"\int k\,f(x)\,dx = k\int f(x)\,dx", 32),
                        M(r"\int \left[f \pm g\right] dx = \int f\,dx \pm \int g\,dx", 32)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            g2 = VGroup(M(r"\int e^x\,dx = e^x + C", 32), M(r"\int \frac1x\,dx = \ln|x| + C", 32)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            g3 = VGroup(M(r"\int \cos x\,dx = \sin x + C", 32), M(r"\int \sin x\,dx = -\cos x + C", 32, TANGENT), M(r"\int \sec^2 x\,dx = \tan x + C", 32),
                        M(r"\int \csc^2 x\,dx = -\cot x + C", 32, TANGENT), M(r"\int \sec x\tan x\,dx = \sec x + C", 32), M(r"\int \csc x\cot x\,dx = -\csc x + C", 32, TANGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            g4 = VGroup(M(r"\int \frac{1}{1 + x^2}\,dx = \arctan x + C", 32), M(r"\int \frac{1}{\sqrt{1 - x^2}}\,dx = \arcsin x + C", 32)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
            left = VGroup(g1, g2, g4).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=0.5)
            g3.to_edge(RIGHT, buff=0.5).align_to(left, UP)
            VGroup(left, g3).set_max_height(7.2)
            self.play(FadeIn(T("each line: a derivative rule read backward", 28, DIM).to_edge(DOWN, buff=0.2)), run_time=0.5)
            b.line(1)
            self.play(FadeIn(g1), run_time=1)
            b.line(2)
            self.play(FadeIn(g2), run_time=0.8)
            b.line(3)
            self.play(FadeIn(g3), run_time=1.2)
            b.line(4)
            self.play(FadeIn(g4), run_time=0.8)
        self.clear()

        with self.beat("Rewrite first") as b:
            rows = VGroup(*[VGroup(M(a, 42), T(c, 30, DIM), M(r, 42, ACCUM)).arrange(RIGHT, buff=0.5) for a, c, r in (
                (r"\int \frac{1}{\sqrt x}\,dx", "write as a power:", r"x^{-1/2}"), (r"\int \frac{x^3 - 2x}{x}\,dx", "split:", r"x^2 - 2"),
                (r"\int (x + 1)^2\,dx", "expand:", r"x^2 + 2x + 1"))]).arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(UP * 0.6)
            b.line(1)
            for r in rows:
                self.play(FadeIn(r), run_time=0.8)
            b.line(2)
            no = T("No product rule or quotient rule for integrals: rewrite into sums of powers.", 32, SECANT).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(no), run_time=0.8)
        self.clear()

        self.example("Term by term", r"Find $\displaystyle\int \left(3\sqrt x - \frac{4}{x^2} + 2\cos x\right) dx$.",
                     [r"= \int \left(3x^{1/2} - 4x^{-2} + 2\cos x\right) dx", r"3 \cdot \frac{x^{3/2}}{3/2} = 2x^{3/2}", r"-4 \cdot \frac{x^{-1}}{-1} = 4x^{-1} = \frac4x", r"2\sin x",
                      r"2x^{3/2} + \frac4x + 2\sin x + C"], at=[1, 2, 3, 4, 5], follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"\int f(x)\,dx = F(x) + C", 48, ACCUM), T("Read derivative rules backward.", 38), T("Rewrite into powers before integrating.", 38), T("Always $+\\,C$.", 40, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Expand first", r"Find $\displaystyle\int \left(x^2 + 1\right)^2 dx$.",
                     [r"\left(x^2 + 1\right)^2 = x^4 + 2x^2 + 1", r"\int \left(x^4 + 2x^2 + 1\right) dx", r"= \frac{x^5}{5} + \frac{2x^3}{3} + x + C"], at=[1, 2, 3])
        self.example("Example 2: Split the fraction", r"Find $\displaystyle\int \frac{x^3 - 2x + 5}{x}\,dx$.",
                     [r"\frac{x^3 - 2x + 5}{x} = x^2 - 2 + \frac5x", r"\int \left(x^2 - 2 + \frac5x\right) dx", r"= \frac{x^3}{3} - 2x + 5\ln|x| + C"], at=[1, 2, 3])
        self.example("Example 3: Finding C", r"$f'(x) = 6x^2 - 4$ and $f(1) = 3$. Find $f(x)$.",
                     [r"f(x) = 2x^3 - 4x + C", r"f(1) = 2 - 4 + C = 3", r"-2 + C = 3, \ \ C = 5", r"f(x) = 2x^3 - 4x + 5"], at=[1, 2, 3, 4])
        self.finish()
