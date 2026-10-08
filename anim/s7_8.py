"""Topic 7.8: Exponential models. Narration comes from transcripts/7_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.8"

    def construct(self):
        with self.beat("Growth proportional to size") as b:
            dish = Circle(radius=1.5, stroke_color=INK, stroke_width=3, fill_color="#F3EEDD", fill_opacity=0.6).to_edge(LEFT, buff=1.2)
            rng = np.random.default_rng(3)
            pts = [dish.get_center() + 1.3 * np.sqrt(rng.random()) * np.array([np.cos(a), np.sin(a), 0]) for a in rng.random(64) * TAU]
            count = M(r"100", 40, FUNC).next_to(dish, DOWN, buff=0.4)
            self.play(FadeIn(dish), FadeIn(count), FadeIn(VGroup(*[Dot(p, radius=0.06, color=DERIV) for p in pts[:8]])), run_time=0.8)
            for n, lab in ((16, "200"), (32, "400"), (64, "800")):
                self.play(FadeIn(VGroup(*[Dot(p, radius=0.06, color=DERIV) for p in pts[n // 2:n]])), Transform(count, M(lab, 40, FUNC).move_to(count)), run_time=0.8)
            ax, al = plot_axes([0, 3, 1], [0, 900, 200], w=5.4, h=3.6, xlabel="t", ylabel="P")
            VGroup(ax, al).to_edge(RIGHT, buff=0.6).shift(UP * 0.4)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda s: 100 * 2**s, x_range=[0, 3], color=FUNC, stroke_width=4)), run_time=1)
            b.line(1)
            de = M(r"\frac{dP}{dt} = kP", 50, ACCUM).next_to(ax, DOWN, buff=0.6)
            self.play(Write(de), run_time=1)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The solution") as b:
            rows = VGroup(M(r"\frac{dy}{dt} = ky", 44), M(r"\frac{dy}{y} = k\,dt", 44), M(r"\ln|y| = kt + C", 44), M(r"y = Ae^{kt}", 44)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(LEFT, buff=1.0).shift(UP * 0.6)
            self.play(Write(rows[0]), Write(rows[1]), run_time=1)
            self.play(Write(rows[2]), run_time=0.8)
            b.line(1)
            self.play(Write(rows[3]), run_time=0.8)
            box = formula_box(M(r"\frac{dy}{dt} = ky: \quad y = y_0e^{kt}", 46, ACCUM), ACCUM).next_to(rows, DOWN, buff=0.6).align_to(rows, LEFT)
            self.play(FadeIn(box), run_time=0.8)
            b.line(2)
            g1, _ = plot_axes([0, 3, 1], [0, 4, 1], w=3, h=2.4, coords=False)
            g2, _ = plot_axes([0, 3, 1], [0, 4, 1], w=3, h=2.4, coords=False)
            p1 = VGroup(g1, g1.plot(lambda s: np.exp(0.45 * s), x_range=[0, 3], color=DERIV, stroke_width=4), T("$k > 0$: growth", 26, DERIV).next_to(g1, DOWN, buff=0.15))
            p2 = VGroup(g2, g2.plot(lambda s: 3.5 * np.exp(-0.9 * s), x_range=[0, 3], color=TANGENT, stroke_width=4), T("$k < 0$: decay", 26, TANGENT).next_to(g2, DOWN, buff=0.15))
            VGroup(p1, p2).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=0.8)
            self.play(FadeIn(p1), FadeIn(p2), run_time=1)
        self.clear()

        self.example("Finding k from data", r"A population grows at a rate proportional to its size. $P(0) = 500$ and $P(3) = 800$. Find $P(6)$.",
                     [r"P = 500e^{kt}", r"800 = 500e^{3k}", r"e^{3k} = \frac85, \ \ k = \tfrac13\ln\tfrac85 \approx 0.157", r"P(6) = 500e^{6k} = 500\left(e^{3k}\right)^2", r"= 500\left(\tfrac85\right)^2 = 1280"],
                     at=[1, 1, 2, 3, 4])

        with self.beat("Half-life and doubling time") as b:
            r1 = M(r"\text{decay: } e^{kT} = \tfrac12, \ \ T = \frac{\ln 2}{|k|}", 44, TANGENT).to_edge(UP, buff=0.6)
            self.play(Write(r1), run_time=1)
            b.line(1)
            r2 = M(r"\text{growth: } e^{kT} = 2, \ \ T = \frac{\ln 2}{k}", 44, DERIV).next_to(r1, DOWN, buff=0.5)
            self.play(Write(r2), run_time=1)
            b.line(2)
            ax, _ = plot_axes([0, 4, 1], [0, 1.1, 0.5], w=7, h=3, coords=False)
            ax.next_to(r2, DOWN, buff=0.6)
            marks = VGroup(*[DashedLine(ax.c2p(n, 0), ax.c2p(n, 0.5**n), color=DIM) for n in (1, 2, 3)])
            self.play(FadeIn(ax), Create(ax.plot(lambda s: 0.5**s, x_range=[0, 4], color=TANGENT, stroke_width=4)), Create(marks),
                      FadeIn(VGroup(*[M(lab, 26, TANGENT).next_to(ax.c2p(n, 0.5**n), UR, buff=0.08) for n, lab in ((1, r"\tfrac12"), (2, r"\tfrac14"), (3, r"\tfrac18"))])), run_time=1.4)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"\frac{dy}{dt} = ky", 44), M(r"y = y_0e^{kt}", 48, ACCUM), T("Find $k$ from a second data point.", 36), M(r"\text{half-life or doubling time: } \frac{\ln 2}{|k|}", 40, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Half-life", r"A substance has a half-life of $10$ years. There are $80$ g now. How much remains after $25$ years?",
                     [r"y = 80e^{kt}; \ \ e^{10k} = \tfrac12, \ \ k = -\frac{\ln 2}{10}", r"y(25) = 80e^{25k} = 80\left(e^{10k}\right)^{2.5} = 80\left(\tfrac12\right)^{2.5}", r"\approx 14.14 \text{ g}"], at=[1, 2, 3])
        self.example("Example 2: When will it reach a target?", r"A bacteria count triples every $4$ hours. When is it $10$ times its starting size?",
                     [r"e^{4k} = 3, \ \ k = \frac{\ln 3}{4}", r"e^{kt} = 10, \ \ t = \frac{\ln 10}{k}", r"t = \frac{4\ln 10}{\ln 3} \approx 8.38 \text{ hours}"], at=[1, 2, 3])
        self.finish()
