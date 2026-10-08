"""Topic 0.6: Solving trigonometric equations. Narration comes from transcripts/0_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def circle_cut(level, vertical=False, sols=(), labels=(), r=2.0):
    """A unit circle cut by the line y = level (or x = level), with the solution points marked and labeled."""
    uc = TrigCircle(r=r)
    if vertical:
        cut = DashedLine(uc.c + np.array([level * r, -(r + 0.3), 0]), uc.c + np.array([level * r, r + 0.3, 0]), color=SECANT)
    else:
        cut = DashedLine(uc.c + np.array([-(r + 0.3), level * r, 0]), uc.c + np.array([r + 0.3, level * r, 0]), color=SECANT)
    g = VGroup(uc, cut, *[uc.ray(t, DIM) for t in sols], *[uc.dot(t, FUNC) for t in sols])
    g.add(*[uc.coord(t, lab, FUNC, 28, out=0.45) for t, lab in zip(sols, labels)])
    return g


class Lesson(TranscriptScene):
    NUM = "0.6"

    def construct(self):
        with self.beat("When is the rider up high") as b:
            W = ferris_wheel(1.5).move_to(LEFT * 5 + DOWN * 0.4)
            ax, al = plot_axes([0, 8, 1], [0, 50, 10], w=7.2, h=4.4, xlabel="t", ylabel="h")
            VGroup(ax, al).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.2)
            hf = lambda s: 25 - 20 * np.cos(PI * s / 2)
            self.play(FadeIn(W), FadeIn(ax), FadeIn(al), run_time=0.8)
            self.play(Create(ax.plot(hf, x_range=[0, 8], color=FUNC, stroke_width=4)), run_time=2)
            b.line(1)
            self.play(Create(DashedLine(ax.c2p(0, 35), ax.c2p(8, 35), color=SECANT)), FadeIn(M("35", 26, SECANT).next_to(ax.c2p(0, 35), LEFT, buff=0.1)), run_time=0.8)
            for k, tv in enumerate((4 / 3, 8 / 3, 16 / 3, 20 / 3)):
                self.play(FadeIn(Dot(ax.c2p(tv, 35), color=SECANT, radius=0.1)), FadeIn(T("up" if k % 2 == 0 else "down", 24, SECANT).next_to(ax.c2p(tv, 35), UP, buff=0.12)), run_time=0.5)
            b.line(2)
            self.play(FadeIn(T("many solutions: find all of them in the interval", 32).to_edge(UP, buff=0.5)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Two angles for every value") as b:
            uc = TrigCircle(r=2.0, center=LEFT * 4.4 + DOWN * 0.3)
            self.play(Create(uc), run_time=0.6)
            self.play(Create(DashedLine(uc.c + np.array([-2.3, 1.0, 0]), uc.c + np.array([2.3, 1.0, 0]), color=SECANT)), FadeIn(M(r"y = \tfrac12", 28, SECANT).next_to(uc.c + np.array([2.3, 1.0, 0]), RIGHT, buff=0.1)), run_time=0.8)
            b.line(1)
            self.play(FadeIn(uc.dot(PI / 6)), FadeIn(uc.dot(5 * PI / 6)), Create(uc.ray(PI / 6, DIM)), Create(uc.ray(5 * PI / 6, DIM)),
                      FadeIn(uc.coord(PI / 6, r"\tfrac{\pi}{6}", FUNC, 30, 0.4)), FadeIn(uc.coord(5 * PI / 6, r"\tfrac{5\pi}{6}", FUNC, 30, 0.4)), run_time=1)
            ax, labs = pi_axes(0, 4, [-1.3, 1.3, 1], w=6.6, h=2.6, step=1)
            VGroup(ax, labs).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)
            self.play(FadeIn(ax), FadeIn(labs), Create(ax.plot(np.sin, x_range=[0, 4 * PI], color=FUNC, stroke_width=4)), Create(DashedLine(ax.c2p(0, 0.5), ax.c2p(4 * PI, 0.5), color=SECANT)), run_time=1.2)
            b.line(2)
            self.play(*[FadeIn(Dot(ax.c2p(v, 0.5), color=SECANT)) for v in (PI / 6, 5 * PI / 6, 13 * PI / 6, 17 * PI / 6)], run_time=0.6)
            self.play(FadeIn(M(r"x = \tfrac{\pi}{6} + 2k\pi \ \text{ or } \ x = \tfrac{5\pi}{6} + 2k\pi", 36).next_to(ax, DOWN, buff=0.6)), run_time=0.8)
            b.line(3)
            self.play(FadeIn(formula_box(M(r"0 \le x < 2\pi: \quad x = \tfrac{\pi}{6}, \ \tfrac{5\pi}{6}", 38, ACCUM), ACCUM).to_edge(RIGHT, buff=0.8).to_edge(DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        self.example("Solving 2cos x + 1 = 0", r"Solve $2\cos x + 1 = 0$ for $0 \le x < 2\pi$.",
                     [r"2\cos x = -1", r"\cos x = -\frac12", r"\text{reference angle } \tfrac{\pi}{3}; \ \cos < 0 \text{ in II and III}", r"x = \pi - \frac{\pi}{3} = \frac{2\pi}{3}", r"x = \pi + \frac{\pi}{3} = \frac{4\pi}{3}"],
                     at=[1, 2, 3, 4, 5], figure=circle_cut(-0.5, True, (2 * PI / 3, 4 * PI / 3), (r"\tfrac{2\pi}{3}", r"\tfrac{4\pi}{3}")), figure_at=3)

        with self.beat("Factoring") as b:
            head = M(r"\text{Solve } 2\sin^2 x = \sin x, \quad 0 \le x < 2\pi", 44).to_edge(UP, buff=0.5)
            self.play(Write(head), run_time=0.8)
            b.line(1)
            warn = callout(r"Don't divide by $\sin x$: it loses the solutions where $\sin x = 0$.", TANGENT, 32).next_to(head, DOWN, buff=0.4)
            self.play(FadeIn(warn), run_time=0.8)
            bd = Board()
            bd.anchor = warn.get_bottom() + DOWN * 0.4
            bd.write(self, r"2\sin^2 x - \sin x = 0")
            b.line(2)
            bd.write(self, r"\sin x\,(2\sin x - 1) = 0")
            b.line(3)
            bd.write(self, r"\sin x = 0: \quad x = 0, \ \pi", FUNC)
            bd.write(self, r"2\sin x - 1 = 0: \quad \sin x = \tfrac12, \quad x = \tfrac{\pi}{6}, \ \tfrac{5\pi}{6}", FUNC)
        self.clear()

        with self.beat("Using an identity first") as b:
            bd = Board()
            bd.anchor = UP * 3.1
            bd.write(self, r"\text{Solve } \sin 2x = \cos x, \quad 0 \le x < 2\pi")
            bd.write(self, r"2\sin x\cos x = \cos x", ACCUM)
            b.line(1)
            bd.write(self, r"2\sin x\cos x - \cos x = 0")
            bd.write(self, r"\cos x\,(2\sin x - 1) = 0")
            b.line(2)
            bd.write(self, r"\cos x = 0: \quad x = \tfrac{\pi}{2}, \ \tfrac{3\pi}{2}", FUNC)
            bd.write(self, r"\sin x = \tfrac12: \quad x = \tfrac{\pi}{6}, \ \tfrac{5\pi}{6}", FUNC)
        self.clear()

        with self.beat("Multiple angles") as b:
            head = M(r"\text{Solve } \sin 2x = 1, \quad 0 \le x < 2\pi", 44).to_edge(UP, buff=0.5)
            self.play(Write(head), run_time=0.8)
            ax, labs = pi_axes(0, 2, [-1.3, 1.3, 1], w=7, h=2.6, step=0.25)
            VGroup(ax, labs).to_edge(DOWN, buff=0.6).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(ax), FadeIn(labs), Create(ax.plot(lambda v: np.sin(2 * v), x_range=[0, 2 * PI], color=FUNC, stroke_width=4)), run_time=1.2)
            b.line(1)
            steps = VGroup(M(r"0 \le x < 2\pi \ \text{ so } \ 0 \le 2x < 4\pi", 36), M(r"\sin u = 1 \text{ at } u = \tfrac{\pi}{2}, \ \tfrac{5\pi}{2}", 36)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.6)
            self.play(Write(steps[0]), run_time=0.8)
            self.play(Write(steps[1]), run_time=0.8)
            b.line(2)
            fin = VGroup(M(r"2x = \tfrac{\pi}{2}, \ \tfrac{5\pi}{2}", 36), M(r"x = \tfrac{\pi}{4}, \ \tfrac{5\pi}{4}", 40, FUNC)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(steps, DOWN, buff=0.3).align_to(steps, LEFT)
            self.play(Write(fin), *[FadeIn(Dot(ax.c2p(v, 1), color=SECANT)) for v in (PI / 4, 5 * PI / 4)], run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(T("Isolate the trig function, or move everything to one side and factor.", 34), T("Never divide by a trig function.", 34, TANGENT),
                          T("Reference angle, then every quadrant where the sign is right.", 34), T(r"For $kx$: solve on $k$ turns, then divide by $k$.", 34, ACCUM)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A tangent equation", r"Solve $\tan x = -1$ for $0 \le x < 2\pi$.",
                     [r"\tan\tfrac{\pi}{4} = 1: \ \text{reference angle } \tfrac{\pi}{4}", r"\tan < 0 \text{ in quadrants II and IV}", r"x = \pi - \frac{\pi}{4} = \frac{3\pi}{4}", r"x = 2\pi - \frac{\pi}{4} = \frac{7\pi}{4}"],
                     at=[1, 2, 3, 4])
        self.example("Example 2: A quadratic in sine", r"Solve $2\sin^2 x - \sin x - 1 = 0$ for $0 \le x < 2\pi$.",
                     [r"u = \sin x: \quad 2u^2 - u - 1 = 0", r"(2u + 1)(u - 1) = 0", r"u = -\tfrac12 \ \text{ or } \ u = 1", r"\sin x = -\tfrac12: \quad x = \frac{7\pi}{6}, \ \frac{11\pi}{6}", r"\sin x = 1: \quad x = \frac{\pi}{2}"],
                     at=[1, 2, 2, 3, 4])
        self.example("Example 3: An identity and a quadratic", r"Solve $\cos 2x = \cos x$ for $0 \le x < 2\pi$.",
                     [r"2\cos^2 x - 1 = \cos x", r"2\cos^2 x - \cos x - 1 = 0", r"(2\cos x + 1)(\cos x - 1) = 0", r"\cos x = -\tfrac12: \quad x = \frac{2\pi}{3}, \ \frac{4\pi}{3}", r"\cos x = 1: \quad x = 0"],
                     at=[1, 2, 2, 3, 4])
        self.example("Example 4: A double angle", r"Solve $\sin 2x = \frac{\sqrt3}{2}$ for $0 \le x < 2\pi$.",
                     [r"0 \le 2x < 4\pi", r"\text{first turn: } 2x = \tfrac{\pi}{3}, \ \tfrac{2\pi}{3}", r"\text{second turn: } 2x = \tfrac{7\pi}{3}, \ \tfrac{8\pi}{3}", r"x = \frac{\pi}{6}, \ \frac{\pi}{3}, \ \frac{7\pi}{6}, \ \frac{4\pi}{3}"],
                     at=[1, 2, 2, 4])
        self.finish()
