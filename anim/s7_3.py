"""Topic 7.3: Sketching slope fields. Narration comes from transcripts/7_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.3"

    def construct(self):
        f = lambda x, y: x - y
        ax, al = plot_axes([-3, 3, 1], [-3, 3, 1], w=6, h=6, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.9)
        grid = np.arange(-2.5, 2.6, 0.5)
        with self.beat("A picture of a differential equation") as b:
            de = M(r"\frac{dy}{dx} = x - y", 48, ACCUM).to_edge(RIGHT, buff=1.2).shift(UP * 2)
            self.play(FadeIn(ax), FadeIn(al), Write(de), run_time=1)
            one = slope_field(ax, f, [1], [-1], length=0.6, color=SECANT, width=5)
            self.play(FadeIn(Dot(ax.c2p(1, -1), color=SECANT, radius=0.05)), Create(one), FadeIn(M(r"(1, -1): \ 1 - (-1) = 2", 34, SECANT).next_to(de, DOWN, buff=0.5)), run_time=1)
            b.line(1)
            field = slope_field(ax, f, grid, grid)
            self.play(LaggedStart(*[Create(s) for s in field], lag_ratio=0.01), run_time=3)
            b.line(2)
            for c, col in ((-1.0, FUNC), (2.0, DERIV)):
                sol = ax.plot(lambda x, c=c: x - 1 + c * np.exp(-x), x_range=[-1.4 if c > 0 else -1.6, 3], color=col, stroke_width=5)
                self.play(Create(sol), run_time=1.6)
        self.clear()
        self.title()

        with self.beat("Patterns to look for") as b:
            panels = VGroup()
            for fn, lab in ((lambda x, y: x, r"\frac{dy}{dx} = x"), (lambda x, y: y, r"\frac{dy}{dx} = y"), (lambda x, y: x - y, r"\frac{dy}{dx} = x - y")):
                a, _ = plot_axes([-2, 2, 1], [-2, 2, 1], w=3.6, h=3.6, coords=False)
                panels.add(VGroup(a, slope_field(a, fn, [-1.5, -1, -0.5, 0, 0.5, 1, 1.5], [-1.5, -1, -0.5, 0, 0.5, 1, 1.5], length=0.3), M(lab, 34).next_to(a, UP, buff=0.2)))
            panels.arrange(RIGHT, buff=0.6).shift(UP * 0.3)
            notes = VGroup(T("same slope down columns", 26, SECANT), T("same slope along rows", 26, SECANT), T("flat along $y = x$", 26, SECANT))
            for n, p in zip(notes, panels):
                n.next_to(p, DOWN, buff=0.25)
            self.play(FadeIn(panels[0]), FadeIn(notes[0]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(panels[1]), FadeIn(notes[1]), run_time=0.8)
            b.line(2)
            a3 = panels[2][0]
            self.play(FadeIn(panels[2]), FadeIn(notes[2]), Create(DashedLine(a3.c2p(-2, -2), a3.c2p(2, 2), color=TANGENT)), run_time=1)
        self.clear()

        ga, gl = plot_axes([-2, 2, 1], [-2, 2, 1], w=4.4, h=4.4)
        dots = VGroup(*[Dot(ga.c2p(x, y), radius=0.05, color=INK) for x in (-1, 0, 1) for y in (-1, 0, 1)])
        gfig = VGroup(ga, gl, dots)
        col = lambda xv: (lambda sc: sc.play(Create(slope_field(ga, f, [xv], [-1, 0, 1], length=0.55, color=ACCUM, width=4)), run_time=0.8))
        self.example("Sketching nine segments", r"Sketch the slope field for $\dfrac{dy}{dx} = x - y$ at the nine points with $x, y \in \{-1, 0, 1\}$.",
                     [r"x = -1: \ y = -1, 0, 1 \ \to \ 0, \ -1, \ -2", r"x = 0: \ \to \ 1, \ 0, \ -1", r"x = 1: \ \to \ 2, \ 1, \ 0", r"\text{flat segments line up along } y = x"],
                     at=[1, 2, 3, 4], figure=gfig, cues={0: col(-1), 1: col(0), 2: col(1)}, follow=True)

        with self.beat("Close") as b:
            card = VGroup(T(r"Slope field: a short segment of slope $\frac{dy}{dx}$ at each point.", 34, ACCUM), T("Only $x$: same slope down columns. Only $y$: same slope along rows.", 32),
                          T("Right side zero: flat segments.", 32), T("Solution curves follow the segments.", 32, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ea, el = plot_axes([-2, 2, 1], [-3, 3, 1], w=4.4, h=4.6)
        efig = VGroup(ea, el, VGroup(*[Dot(ea.c2p(x, y), radius=0.05, color=INK) for x in (-1, 0, 1) for y in (-2, 0, 2)]))
        row = lambda yv: (lambda sc: sc.play(Create(slope_field(ea, lambda x, y: y / 2, [-1, 0, 1], [yv], length=0.55, color=ACCUM, width=4)), run_time=0.8))
        self.example("Example 1: Slopes from y alone", r"Sketch the slope field for $\dfrac{dy}{dx} = \dfrac y2$ at the points with $x \in \{-1, 0, 1\}$ and $y \in \{-2, 0, 2\}$.",
                     [r"\text{depends only on } y: \ \text{one slope per row}", r"y = -2: \ -1; \ \ y = 0: \ 0; \ \ y = 2: \ 1", r"\text{bottom row down, middle flat, top row up}"],
                     at=[1, 2, 3], figure=efig, cues={1: lambda sc: (row(-2)(sc), row(0)(sc), row(2)(sc))})
        ca, cl = plot_axes([-2.5, 2.5, 1], [-2.5, 2.5, 1], w=4.4, h=4.4, coords=False)
        pts = [v for v in np.arange(-2, 2.1, 0.5)]
        circ = lambda x, y: -x / y if abs(y) > 1e-9 else 1e6
        cfig = VGroup(ca, cl, slope_field(ca, circ, pts, pts, length=0.3))
        self.example("Example 2: Which equation?", r"Which differential equation has this slope field: $\dfrac{dy}{dx} = x$, $\dfrac{dy}{dx} = y$, or $\dfrac{dy}{dx} = -\dfrac xy$?",
                     [r"\text{on the } y\text{-axis } (x = 0): \text{ flat, so not } \frac{dy}{dx} = y", r"\text{slopes change along rows: not } \frac{dy}{dx} = x",
                      r"-\frac xy: \ 0 \text{ at } x = 0, \text{ vertical at } y = 0", r"\frac{dy}{dx} = -\frac xy"], at=[1, 2, 3, 3], figure=cfig,
                     text=r"A slope field is shown: its segments are flat along the $y$-axis, vertical along the $x$-axis, and circle the origin. Which differential equation has this slope field: "
                          r"$\frac{dy}{dx} = x$, $\frac{dy}{dx} = y$, or $\frac{dy}{dx} = -\frac xy$?")
        self.finish()
