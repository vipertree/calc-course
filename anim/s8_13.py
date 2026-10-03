"""Topic 8.13 (BC): Arc length. Narration comes from transcripts/8_13.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.13"

    def construct(self):
        road = lambda s: 1.5 + 0.9 * np.sin(1.1 * s) + 0.15 * s
        with self.beat("How long is a curve?") as b:
            ax, _ = plot_axes([0, 6, 1], [0, 3.5, 1], w=8, h=4.4, coords=False)
            ax.shift(DOWN * 0.3)
            curve = ax.plot(road, x_range=[0.3, 5.7], color=FUNC, stroke_width=6)
            A, B = Dot(ax.c2p(0.3, road(0.3)), color=INK), Dot(ax.c2p(5.7, road(5.7)), color=INK)
            self.play(Create(curve), FadeIn(A), FadeIn(B), FadeIn(M("A", 32).next_to(A, LEFT)), FadeIn(M("B", 32).next_to(B, RIGHT)), run_time=1.4)
            chord = DashedLine(A.get_center(), B.get_center(), color=DIM)
            self.play(Create(chord), FadeIn(T("too short", 28, DIM).next_to(chord, DOWN, buff=0.1)), run_time=0.8)
            b.line(1)
            lab = None
            for n in (4, 8, 16):
                xs = np.linspace(0.3, 5.7, n + 1)
                segs = VGroup(*[Line(ax.c2p(p, road(p)), ax.c2p(q, road(q)), color=SECANT, stroke_width=4) for p, q in zip(xs, xs[1:])])
                length = sum(np.hypot(q - p, road(q) - road(p)) for p, q in zip(xs, xs[1:]))
                new = M(rf"{n} \text{{ segments: }} {length:.3f}", 34, SECANT).to_edge(UP, buff=0.4)
                self.play(FadeIn(segs), Transform(lab, new) if lab else FadeIn(new), run_time=1)
                lab = lab or new
                self.wait(0.3)
                self.play(FadeOut(segs), run_time=0.3)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Pythagoras on a tiny piece") as b:
            ax, _ = plot_axes([0, 6, 1], [0, 3.5, 1], w=5.4, h=3.6, coords=False)
            ax.to_edge(LEFT, buff=0.4).shift(UP * 0.4)
            self.play(Create(ax.plot(road, x_range=[0.3, 5.7], color=FUNC, stroke_width=5)), run_time=0.8)
            x0, dx = 2.2, 0.9
            p, q = ax.c2p(x0, road(x0)), ax.c2p(x0 + dx, road(x0 + dx))
            corner = np.array([q[0], p[1], 0])
            tri = VGroup(Line(p, corner, color=DIM, stroke_width=4), Line(corner, q, color=DIM, stroke_width=4), Line(p, q, color=SECANT, stroke_width=5))
            labs = VGroup(M("dx", 30).next_to(tri[0], DOWN, buff=0.1), M("dy", 30).next_to(tri[1], RIGHT, buff=0.1), M("ds", 30, SECANT).next_to(tri[2].get_center(), UL, buff=0.1))
            self.play(Create(tri), FadeIn(labs), run_time=1)
            b.line(1)
            rows = [r"ds^2 = dx^2 + dy^2", r"ds = \sqrt{dx^2 + dy^2}", r"ds = \sqrt{1 + \left(\tfrac{dy}{dx}\right)^2}\,dx"]
            board = VGroup(*[M(r, 38) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
            self.play(Write(board[0]), run_time=0.8)
            b.line(2)
            self.play(Write(board[1]), run_time=0.8)
            self.play(Write(board[2]), run_time=1)
            b.line(3)
            box = formula_box(VGroup(M(r"L = \int_a^b \sqrt{1 + [f'(x)]^2}\,dx", 42, ACCUM), T("add up the tiny hypotenuses", 28, DIM)).arrange(DOWN, buff=0.15), ACCUM).next_to(board, DOWN, buff=0.5)
            self.play(FadeIn(box), run_time=0.8)
            b.line(4)
            self.play(FadeIn(T("$f'$ continuous: a smooth curve", 28, DIM).next_to(box, DOWN, buff=0.3)), run_time=0.6)
        self.clear()

        with self.beat("A check with a line") as b:
            ax, al = plot_axes([0, 3.5, 1], [0, 6.5, 1], w=3.8, h=5)
            VGroup(ax, al).to_edge(LEFT, buff=1)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda s: 2 * s, x_range=[0, 3], color=FUNC, stroke_width=5)), run_time=1)
            r1 = M(r"f' = 2: \ \ L = \int_0^3 \sqrt{1 + 4}\,dx = 3\sqrt5", 40).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)
            self.play(Write(r1), run_time=1)
            b.line(1)
            b.line(2)
            r2 = M(r"\sqrt{3^2 + 6^2} = \sqrt{45} = 3\sqrt5", 40, ACCUM).next_to(r1, DOWN, buff=0.6)
            self.play(Write(r2), FadeIn(M(r"\checkmark", 60, GRASS).next_to(r2, RIGHT, buff=0.3)), run_time=1)
        self.clear()

        ax, _ = plot_axes([0, 3.4, 1], [0, 3.8, 1], w=3.8, h=3.8)
        fig = VGroup(ax, ax.plot(lambda s: 2 / 3 * s**1.5, x_range=[0, 3], color=FUNC, stroke_width=5), M(r"L = \tfrac{14}{3}", 30, ACCUM).next_to(ax.c2p(1.5, 1.6), UL, buff=0.1))
        self.example("A curve with an exact length", r"Find the length of $y = \frac23x^{3/2}$ from $x = 0$ to $x = 3$.",
                     [r"f'(x) = \tfrac23 \cdot \tfrac32 x^{1/2} = \sqrt x", r"1 + [f'(x)]^2 = 1 + x", r"L = \int_0^3 \sqrt{1 + x}\,dx", r"= \left[\tfrac23(1 + x)^{3/2}\right]_0^3",
                      r"= \tfrac23\left(4^{3/2} - 1^{3/2}\right)", r"= \tfrac23(8 - 1)", r"= \tfrac{14}{3} \approx 4.67"], at=[1, 2, 3, 4, 4, 5, 5], figure=fig,
                     notes_graph=dict(fns=[("2/3*x^(1.5)", 0, 3)], xr=(0, 3.4), yr=(0, 3.8)))

        with self.beat("Most arc lengths need a calculator") as b:
            r1 = M(r"y = x^2 \text{ on } [0, 1]: \ \int_0^1 \sqrt{1 + 4x^2}\,dx \approx 1.479", 40).to_edge(UP, buff=0.8)
            self.play(Write(r1), FadeIn(T("(calculator)", 28, DIM).next_to(r1, DOWN, buff=0.15)), run_time=1.2)
            b.line(1)
            b.line(2)
            r2 = M(r"x = g(y): \ L = \int_c^d \sqrt{1 + [g'(y)]^2}\,dy", 40, ACCUM).shift(UP * 0.2)
            self.play(Write(r2), run_time=1)
            b.line(3)
            r3 = VGroup(M(r"\text{speed} = |v|, \quad \text{distance traveled} = \int |v|\,dt", 36, DERIV), T("parametric motion: Unit 9", 28, DIM)).arrange(DOWN, buff=0.2).shift(DOWN * 1.6)
            self.play(FadeIn(r3), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"L = \int_a^b \sqrt{1 + [f'(x)]^2}\,dx", 48, ACCUM), ACCUM), M(r"ds^2 = dx^2 + dy^2", 40), T("check: a line gives the distance formula", 34),
                          T("usually: set up, then calculator", 34, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A designed perfect square", r"Find the length of $y = \frac{x^2}{2} - \frac{\ln x}{4}$ from $x = 1$ to $x = 2$.",
                     [r"f' = x - \tfrac{1}{4x}", r"[f']^2 = x^2 - \tfrac12 + \tfrac{1}{16x^2}", r"1 + [f']^2 = x^2 + \tfrac12 + \tfrac{1}{16x^2} = \left(x + \tfrac{1}{4x}\right)^2", r"L = \int_1^2 \left(x + \tfrac{1}{4x}\right) dx",
                      r"= \left[\tfrac{x^2}{2} + \tfrac{\ln x}{4}\right]_1^2", r"= \left(2 + \tfrac{\ln 2}{4}\right) - \tfrac12", r"= \tfrac32 + \tfrac{\ln 2}{4} \approx 1.67"], at=[1, 1, 2, 2, 3, 3, 3])
        ax, _ = plot_axes([0, 1.3, 0.5], [0, 1.3, 0.5], w=3.4, h=3.4)
        fig2 = VGroup(ax, ax.plot(lambda s: s * s, x_range=[0, 1], color=FUNC, stroke_width=5), DashedLine(ax.c2p(0, 0), ax.c2p(1, 1), color=DIM))
        self.example("Example 2: The parabola, by calculator", r"Set up and evaluate the length of $y = x^2$ from $x = 0$ to $x = 1$.",
                     [r"f' = 2x", r"L = \int_0^1 \sqrt{1 + 4x^2}\,dx", r"\approx 1.479 \ \ (\text{calculator})", r"\text{straight line: } \sqrt2 \approx 1.414"], at=[1, 1, 2, 2], figure=fig2)
        self.example("Example 3: A log of cosine", r"Find the length of $y = \ln(\cos x)$ from $x = 0$ to $x = \frac\pi4$.",
                     [r"f' = \tfrac{-\sin x}{\cos x} = -\tan x", r"1 + \tan^2 x = \sec^2 x", r"L = \int_0^{\pi/4} \sec x\,dx", r"= \left[\ln|\sec x + \tan x|\right]_0^{\pi/4}", r"= \ln\left(\sqrt2 + 1\right) - \ln 1",
                      r"= \ln\left(1 + \sqrt2\right) \approx 0.881"], at=[1, 1, 2, 2, 3, 3])
        self.finish()
