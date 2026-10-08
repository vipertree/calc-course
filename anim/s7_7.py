"""Topic 7.7: Particular solutions with initial conditions. Narration comes from transcripts/7_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.7"
    example_ref = r"\text{integrate, then find } C"

    def construct(self):
        ax, al = plot_axes([-3, 3, 1], [-4, 4, 1], w=6, h=6, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8)
        with self.beat("One curve from a family") as b:
            fam = VGroup()
            for K in (-4, -1, 1, 3, 6):
                lo = np.sqrt(max(-K, 0)) + 0.01
                for sgn in (1, -1):
                    if K < 0:
                        for side in (1, -1):
                            fam.add(ax.plot(lambda s, K=K, sgn=sgn: sgn * np.sqrt(max(s * s + K, 0)), x_range=sorted([side * lo, side * 3]), color=DIM, stroke_width=2))
                    else:
                        fam.add(ax.plot(lambda s, K=K, sgn=sgn: sgn * np.sqrt(s * s + K), x_range=[-3, 3], color=DIM, stroke_width=2))
            self.play(FadeIn(ax), FadeIn(al), Create(fam), run_time=1.6)
            b.line(1)
            dot = Dot(ax.c2p(1, 2), color=SECANT, radius=0.1)
            self.play(FadeIn(dot), FadeIn(M("(1, 2)", 32, SECANT).next_to(dot, LEFT, buff=0.15)), run_time=0.6)
            b.line(2)
            part = ax.plot(lambda s: np.sqrt(s * s + 3), x_range=[-3, 3], color=ACCUM, stroke_width=6)
            self.play(fam.animate.set_opacity(0.25), Create(part), FadeIn(M(r"y = \sqrt{x^2 + 3}", 40, ACCUM).to_edge(RIGHT, buff=1.0)), run_time=1.2)
        self.clear()
        self.title()

        self.example("Find C right away", r"Find the particular solution of $\dfrac{dy}{dx} = \dfrac xy$ with $y(1) = 2$.",
                     [r"y\,dy = x\,dx, \ \ \frac{y^2}{2} = \frac{x^2}{2} + C", r"(1, 2): \ \frac42 = \frac12 + C, \ \ C = \frac32", r"y^2 = x^2 + 3",
                      r"y = +\sqrt{x^2 + 3} \ \ (y(1) = 2 > 0)", r"TEXT:Substitute the point as soon as you've integrated."], at=[1, 2, 3, 4, 5], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T("Separate, integrate, then substitute the initial condition to find $C$.", 34, ACCUM), T("Then solve for $y$, choosing the sign that fits the point.", 34),
                          T("Watch the domain: defined at and around the starting point.", 34, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=1.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: Exponential growth", r"Find the particular solution of $\dfrac{dy}{dx} = 2xy$ with $y(0) = 3$.",
                     [r"\frac{dy}{y} = 2x\,dx, \ \ \ln|y| = x^2 + C", r"(0, 3): \ \ln 3 = 0 + C, \ \ C = \ln 3", r"|y| = e^{x^2} \cdot e^{\ln 3} = 3e^{x^2}", r"y = 3e^{x^2}"], at=[1, 2, 3, 4])
        self.example("Example 2: A cooling cup", r"Coffee cools by $\dfrac{dT}{dt} = -0.1(T - 70)$, with $T(0) = 190$. Find $T(t)$, then $T(10)$.",
                     [r"\ln|T - 70| = -0.1t + C", r"(0, 190): \ \ln 120 = C", r"T = 70 + 120e^{-0.1t}", r"T(10) = 70 + 120e^{-1} \approx 114.1^\circ\text{F}"], at=[1, 2, 3, 4])
        da, dl = plot_axes([-2, 2, 1], [0, 6, 1], w=4.4, h=4)
        dfig = VGroup(da, dl, da.plot(lambda s: 2 / (2 - s * s), x_range=[-1.29, 1.29], color=ACCUM, stroke_width=4),
                      DashedLine(da.c2p(-np.sqrt(2), 0), da.c2p(-np.sqrt(2), 6), color=DIM), DashedLine(da.c2p(np.sqrt(2), 0), da.c2p(np.sqrt(2), 6), color=DIM),
                      Dot(da.c2p(0, 1), color=SECANT))
        self.example("Example 3: A domain", r"Find the particular solution of $\dfrac{dy}{dx} = xy^2$ with $y(0) = 1$, and give its domain.",
                     [r"\frac{dy}{y^2} = x\,dx, \ \ -\frac1y = \frac{x^2}{2} + C", r"(0, 1): \ C = -1; \ \ -\frac1y = \frac{x^2 - 2}{2}", r"y = \frac{2}{2 - x^2}",
                      r"\text{undefined at } x = \pm\sqrt2: \ \ -\sqrt2 < x < \sqrt2"], at=[1, 2, 3, 4], figure=dfig,
                     notes_graph=dict(fns=[("2/(2-x^2)", -1.29, 1.29)], xr=(-2, 2), yr=(0, 6), vlines=[-1.4142, 1.4142], closed=[(0, 1)]))
        self.finish()
