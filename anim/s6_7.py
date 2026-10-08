"""Topic 6.7: The Fundamental Theorem of Calculus and definite integrals. Narration comes from transcripts/6_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.7"

    def construct(self):
        sq = lambda s: s * s
        ax, al = plot_axes([0, 3.5, 1], [0, 10, 2], w=6.4, h=4.8)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        with self.beat("A shortcut for area") as b:
            boxes = riemann_boxes(ax, sq, np.linspace(0, 3, 25), "right", opacity=0.35)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(sq, x_range=[0, 3.2], color=FUNC, stroke_width=5)), FadeIn(boxes), run_time=1.2)
            hard = T("limit of Riemann sums: hard", 34, DIM).to_edge(RIGHT, buff=0.6).shift(UP * 2)
            self.play(FadeIn(hard), run_time=0.6)
            b.line(1)
            region = ax.get_area(ax.plot(sq, x_range=[0, 3]), x_range=[0, 3], color=AREA, opacity=0.5)
            F = M(r"F(x) = \frac{x^3}{3}", 44, ACCUM).next_to(hard, DOWN, buff=0.6)
            chk = T(r"($F'(x) = x^2$)", 30, DIM).next_to(F, DOWN, buff=0.2)
            self.play(FadeOut(boxes), FadeIn(region), FadeOut(hard), FadeIn(F), FadeIn(chk), run_time=1)
            b.line(2)
            ev = M(r"F(3) - F(0) = \frac{27}{3} - 0 = 9", 42, AREA).next_to(chk, DOWN, buff=0.6)
            self.play(Write(ev), FadeIn(M(r"9", 40, INK).move_to(ax.c2p(2.3, 1.6))), run_time=1.2)
        self.clear()
        self.title()

        with self.beat("Why it works") as b:
            rows = VGroup(M(r"A(x) = \int_a^x f(t)\,dt \ \text{ has } \ A' = f", 40), M(r"F' = f: \ F \text{ is an antiderivative of } f", 40),
                          M(r"F(x) = A(x) + C", 40), M(r"F(b) - F(a) = \left(A(b) + C\right) - \left(A(a) + C\right)", 40),
                          M(r"= A(b) - A(a) = A(b) - 0 = \int_a^b f(x)\,dx", 40)).arrange(DOWN, aligned_edge=LEFT, buff=0.38).to_edge(UP, buff=0.5)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(Write(rows[1]), run_time=1)
            self.play(Write(rows[2]), run_time=0.8)
            b.line(2)
            self.play(Write(rows[3]), run_time=1)
            b.line(3)
            self.play(Write(rows[4]), run_time=1)
            thm = formula_box(M(r"F' = f \text{ on } [a, b]: \quad \int_a^b f(x)\,dx = F(b) - F(a)", 44, ACCUM), ACCUM).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(thm), run_time=0.8)
        self.clear()

        with self.beat("Reversing derivatives") as b:
            tab = table([r"f(x)", r"\text{an antiderivative } F(x)"], [[r"x^n \ (n \ne -1)", r"\frac{x^{n+1}}{n + 1}"], [r"\cos x", r"\sin x"], [r"\sin x", r"-\cos x"],
                                                                   [r"e^x", r"e^x"], [r"\frac1x", r"\ln|x|"], [r"\sec^2 x", r"\tan x"]], size=36).shift(UP * 0.4)
            rows = [VGroup(*tab.cells[r]) for r in range(1, 7)]
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab[1]), run_time=0.6)
            b.line(1)
            self.play(FadeIn(rows[0]), run_time=0.6)
            b.line(2)
            for r in rows[1:]:
                self.play(FadeIn(r), run_time=0.5)
            b.line(3)
            bar = M(r"F(x)\Big|_a^b = F(b) - F(a)", 44, ACCUM).to_edge(DOWN, buff=0.4)
            self.play(Write(bar), run_time=1)
        self.clear()

        with self.beat("Net change") as b:
            r1 = VGroup(M(r"\int_a^b f'(x)\,dx = f(b) - f(a)", 50, ACCUM), T("the integral of a rate of change is the net change", 32, DIM)).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.6)
            self.play(Write(r1[0]), run_time=1.2)
            b.line(1)
            self.play(FadeIn(r1[1]), run_time=0.6)
            b.line(2)
            r2 = VGroup(M(r"f(b) = f(a) + \int_a^b f'(x)\,dx", 50, FUNC), T("where it ends = where it starts + how much it changed", 32, DIM)).arrange(DOWN, buff=0.25).next_to(r1, DOWN, buff=0.8)
            self.play(Write(r2[0]), FadeIn(r2[1]), run_time=1.2)
            start = Rectangle(width=1.2, height=1.2, stroke_width=0, fill_color=FUNC, fill_opacity=0.4)
            add = Rectangle(width=1.2, height=0.8, stroke_width=0, fill_color=AREA, fill_opacity=0.6).next_to(start, UP, buff=0)
            pic = VGroup(start, add, T("$f(a)$", 26).move_to(start), T(r"$\int f'$", 26).move_to(add)).next_to(r2, DOWN, buff=0.5)
            self.play(FadeIn(pic), run_time=0.8)
        self.clear()

        self.example("Evaluating an integral", r"Evaluate $\displaystyle\int_1^4 \left(3x^2 - 2x\right) dx$.",
                     [r"\text{antiderivative: } x^3 - x^2", r"\left[x^3 - x^2\right]_1^4 = \left(4^3 - 4^2\right) - \left(1^3 - 1^2\right)", r"= (64 - 16) - (1 - 1)", r"= 48 - 0 = 48"],
                     at=[1, 2, 3, 4])

        with self.beat("Close") as b:
            card = VGroup(M(r"\int_a^b f(x)\,dx = F(b) - F(a), \ \ F' = f", 44, ACCUM), T("Antiderivatives: run derivative rules backward.", 36),
                          M(r"\int_a^b f'(x)\,dx = f(b) - f(a): \ \text{net change}", 42), M(r"f(b) = f(a) + \int_a^b f'(x)\,dx", 42, FUNC)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A trig integral", r"Evaluate $\displaystyle\int_0^\pi \sin x\,dx$.",
                     [r"\text{antiderivative: } -\cos x", r"\left[-\cos x\right]_0^\pi = -\cos\pi - (-\cos 0)", r"= -(-1) - (-1)", r"= 1 + 1 = 2"], at=[1, 2, 3, 4])
        self.example("Example 2: A root", r"Evaluate $\displaystyle\int_1^9 \sqrt x\,dx$.",
                     [r"\sqrt x = x^{1/2}, \ \ \text{antiderivative: } \frac{x^{3/2}}{3/2} = \frac23 x^{3/2}", r"\left[\tfrac23 x^{3/2}\right]_1^9 = \tfrac23\left(9^{3/2}\right) - \tfrac23\left(1^{3/2}\right)",
                      r"= \tfrac23(27) - \tfrac23 = 18 - \tfrac23 = \tfrac{52}{3}"], at=[1, 2, 4])
        self.example("Example 3: Net change", r"A plant is $10$ cm tall at $t = 1$ week and grows at $h'(t) = 6t - 2$ cm per week. How tall is it at $t = 3$?",
                     [r"h(3) = h(1) + \int_1^3 h'(t)\,dt", r"\int_1^3 (6t - 2)\,dt = \left[3t^2 - 2t\right]_1^3", r"= (27 - 6) - (3 - 2) = 21 - 1 = 20", r"h(3) = 10 + 20 = 30 \text{ cm}"],
                     at=[1, 2, 3, 4])
        self.finish()
