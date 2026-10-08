"""Topic 9.5 (BC): Integrating vector-valued functions. Narration comes from transcripts/9_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.5"

    def construct(self):
        px = lambda s: -2.5 + 1.6 * s
        py = lambda s: 0.5 + 1.8 * np.sin(1.4 * s)
        with self.beat("Running the film backward") as b:
            ax, _ = plot_axes([-3, 3, 1], [-2, 3, 1], w=7, h=4.6, coords=False)
            tt = ValueTracker(0.0)
            vel = always_redraw(lambda: Arrow(ax.c2p(px(tt.get_value()), py(tt.get_value())), ax.c2p(px(tt.get_value()) + 0.5 * 1.6, py(tt.get_value()) + 0.5 * 1.8 * 1.4 * np.cos(1.4 * tt.get_value())), buff=0, color=DERIV, stroke_width=5))
            q = M("?", 60, TANGENT).move_to(ax.c2p(1, 2.4))
            self.play(FadeIn(ax), FadeIn(q), run_time=0.6)
            self.add(vel)
            self.play(tt.animate.set_value(3.2), run_time=2.4, rate_func=linear)
            b.line(1)
            start = VGroup(Dot(ax.c2p(px(0), py(0)), color=INK), T("start", 26, INK).next_to(ax.c2p(px(0), py(0)), DOWN, buff=0.15))
            self.play(FadeOut(q), FadeIn(start), Create(param_curve(ax, px, py, 0, 3.2)), run_time=1.6)
        self.clear()
        self.title()

        with self.beat("Integrate each component") as b:
            rows = VGroup(M(r"\int \langle x(t),\ y(t)\rangle\,dt = \left\langle \int x(t)\,dt,\ \int y(t)\,dt\right\rangle", 40), M(r"+\ \langle C_1,\ C_2\rangle", 40, SECANT),
                          M(r"\int_a^b \vec v(t)\,dt = \vec r(b) - \vec r(a): \ \text{displacement}", 40, ACCUM), M(r"\vec r(t) = \vec r(0) + \int_0^t \vec v(u)\,du", 44, FUNC)).arrange(DOWN, buff=0.5)
            self.play(Write(rows[0]), run_time=1.2)
            b.line(1)
            self.play(FadeIn(rows[1]), run_time=0.8)
            b.line(2)
            self.play(Write(rows[2]), run_time=1)
            b.line(3)
            self.play(Write(rows[3]), run_time=1)
        self.clear()

        self.example("Position from velocity", r"A particle has velocity $\vec v(t) = \langle 2t,\ 3t^2\rangle$ and $\vec r(0) = \langle 1, -2\rangle$. Find $\vec r(t)$ and $\vec r(2)$.",
                     [r"\vec r(t) = \left\langle \int 2t\,dt,\ \int 3t^2\,dt\right\rangle = \langle t^2 + C_1,\ t^3 + C_2\rangle", r"\vec r(0) = \langle C_1,\ C_2\rangle = \langle 1, -2\rangle", r"\vec r(t) = \langle t^2 + 1,\ t^3 - 2\rangle",
                      r"\vec r(2) = \langle 4 + 1,\ 8 - 2\rangle = \langle 5, 6\rangle", r"\text{or: } \langle 1, -2\rangle + \int_0^2 \langle 2t, 3t^2\rangle\,dt = \langle 1, -2\rangle + \langle 4, 8\rangle = \langle 5, 6\rangle"], at=[1, 2, 3, 3, 4])

        with self.beat("Close") as b:
            card = VGroup(M(r"\int \langle x, y\rangle\,dt = \left\langle \int x\,dt, \int y\,dt\right\rangle + \langle C_1, C_2\rangle", 40), M(r"\int_a^b \vec v\,dt = \text{displacement}", 40, ACCUM),
                          M(r"\vec r(t) = \vec r(0) + \int_0^t \vec v", 44, FUNC)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A definite integral", r"Evaluate $\displaystyle\int_0^\pi \langle \sin t,\ \cos t\rangle\,dt$.",
                     [r"= \left\langle \int_0^\pi \sin t\,dt,\ \int_0^\pi \cos t\,dt\right\rangle", r"= \left\langle [-\cos t]_0^\pi,\ [\sin t]_0^\pi\right\rangle", r"= \langle 2,\ 0\rangle"], at=[1, 1, 1])
        ax, _ = plot_axes([0, 80, 20], [0, 16, 4], w=5, h=2.4)
        fig2 = VGroup(ax, param_curve(ax, lambda s: 40 * s, lambda s: 30 * s - 16 * s * s, 0, 15 / 8), Dot(ax.c2p(75, 0), color=TANGENT))
        self.example("Example 2: A thrown ball", r"A ball has $\vec a(t) = \langle 0, -32\rangle$ ft/s$^2$, initial velocity $\langle 40, 30\rangle$, and starts at the origin. When and where does it land ($y = 0$)?",
                     [r"\vec v(t) = \langle 40,\ 30 - 32t\rangle", r"\vec r(t) = \langle 40t,\ 30t - 16t^2\rangle", r"30t - 16t^2 = 0", r"t(30 - 16t) = 0: \ t = \tfrac{15}{8} \text{ s}", r"x = 40 \cdot \tfrac{15}{8} = 75 \text{ ft}"],
                     at=[1, 2, 3, 3, 3], figure=fig2)
        self.example("Example 3: Exponential and log components", r"$\vec v(t) = \left\langle e^t,\ \frac{1}{t + 1}\right\rangle$ and $\vec r(0) = \langle 2, 0\rangle$. Find $\vec r(1)$.",
                     [r"\vec r(t) = \langle e^t + C_1,\ \ln(t + 1) + C_2\rangle", r"\vec r(0) = \langle 1 + C_1,\ C_2\rangle = \langle 2, 0\rangle: \ C_1 = 1, \ C_2 = 0", r"\vec r(t) = \langle e^t + 1,\ \ln(t + 1)\rangle",
                      r"\vec r(1) = \langle e + 1,\ \ln 2\rangle \approx \langle 3.72,\ 0.69\rangle"], at=[1, 2, 2, 3])
        self.finish()
