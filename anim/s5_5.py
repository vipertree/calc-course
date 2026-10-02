"""Topic 5.5: The Candidates Test. Narration comes from transcripts/5_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.5"

    def construct(self):
        ax, al = plot_axes([0, 6, 1], [0, 5, 1], w=9, h=5.2, coords=False)
        VGroup(ax, al).shift(DOWN * 0.3)
        f = lambda s: 0.25 * (s - 0.6) * (s - 3) * (s - 5.2) + 2.4
        a, b = 0.4, 5.8
        crit = [r.real for r in np.roots(np.polyder(np.poly1d(0.25 * np.poly([0.6, 3, 5.2])))) if a < r.real < b]
        with self.beat("A short list") as bt:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[a, b], color=FUNC, stroke_width=5)), run_time=1.2)
            ends = VGroup(*[DashedLine(ax.c2p(s, 0), ax.c2p(s, f(s)), color=DIM) for s in (a, b)])
            self.play(Create(ends), FadeIn(VGroup(M("a", 32).next_to(ax.c2p(a, 0), DOWN, buff=0.15), M("b", 32).next_to(ax.c2p(b, 0), DOWN, buff=0.15))), run_time=0.8)
            bt.line(1)
            cd = VGroup(*[Dot(ax.c2p(s, f(s)), color=SECANT, radius=0.1) for s in crit])
            self.play(FadeIn(cd), run_time=0.8)
            bt.line(2)
            ed = VGroup(*[Dot(ax.c2p(s, f(s)), color=DERIV, radius=0.1) for s in (a, b)])
            self.play(FadeIn(ed), run_time=0.8)
            bt.line(3)
            pts = [(s, f(s)) for s in [a, b] + crit]
            hi, lo = max(pts, key=lambda p: p[1]), min(pts, key=lambda p: p[1])
            self.play(Create(Circle(radius=0.28, color=TANGENT).move_to(ax.c2p(*hi))), Create(Circle(radius=0.28, color=TANGENT).move_to(ax.c2p(*lo))), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("The test") as bt:
            steps = VGroup(T(r"1. Find the critical points in $(a, b)$.", 42), T("2. Evaluate $f$ at each one and at both endpoints.", 42),
                           T("3. Largest: absolute max. Smallest: absolute min.", 42)).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            head = T("The Candidates Test", 48, SECANT).next_to(steps, UP, buff=0.6)
            self.play(FadeIn(head), FadeIn(steps[0], shift=RIGHT * 0.2), run_time=0.8)
            bt.line(1)
            self.play(FadeIn(steps[1], shift=RIGHT * 0.2), run_time=0.6)
            bt.line(2)
            self.play(FadeIn(steps[2], shift=RIGHT * 0.2), run_time=0.6)
        self.clear()

        ax, al = plot_axes([0, 3, 1], [-3, 18, 3], w=6.4, h=5.4, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        g = lambda s: s**3 - 3 * s
        with self.beat("Don't skip the endpoints") as bt:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(g, x_range=[0, 3], color=FUNC, stroke_width=5)), run_time=1.2)
            p1 = VGroup(Dot(ax.c2p(1, -2), color=SECANT), M("f(1) = -2", 36, SECANT))
            p1[1].to_edge(RIGHT, buff=1.4).shift(UP * 0.2)
            self.play(FadeIn(p1), run_time=0.6)
            bt.line(1)
            self.play(Indicate(p1[1], color=SECANT), run_time=0.8)
            bt.line(2)
            p3 = VGroup(Dot(ax.c2p(3, 18), color=TANGENT), M("f(3) = 18", 40, TANGENT).next_to(p1[1], UP, buff=0.8).align_to(p1[1], LEFT))
            self.play(FadeIn(p3), run_time=0.6)
        self.clear()
        self.example("A parabola on an interval", r"Find the absolute extrema of $f(x) = x^2 - 4x$ on $[0, 5]$.",
                     [r"f'(x) = 2x - 4 = 0 \text{ at } x = 2", r"f(0) = 0, \quad f(2) = -4, \quad f(5) = 5", r"\text{absolute max } 5 \text{ at } x = 5; \ \ \text{absolute min } -4 \text{ at } x = 2"], at=[1, 2, 3])

        with self.beat("Close") as bt:
            tab = table(["x", "f(x)"], [["0", "0"], ["1", "-2"], ["3", "18"]], size=40)
            self.play(FadeIn(tab), run_time=1)
            note = T(r"endpoints and critical points; the table is the justification", 34, DIM).next_to(tab, DOWN, buff=0.6)
            self.play(FadeIn(note), run_time=0.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: A cubic", r"Find the absolute extrema of $f(x) = x^3 - 3x + 1$ on $[0, 3]$.",
                     [r"f'(x) = 3x^2 - 3 = 0 \text{ at } x = \pm 1;\ \text{only } x = 1 \text{ is in } [0, 3]", r"f(0) = 1,\ \ f(1) = -1,\ \ f(3) = 19",
                      r"\text{absolute max } 19 \text{ at } x = 3;\ \ \text{absolute min } -1 \text{ at } x = 1"], at=[1, 2, 3])
        self.example("Example 2: A logarithm", r"Find the absolute extrema of $f(x) = x - 2\ln x$ on $\left[1, e^2\right]$.",
                     [r"f'(x) = 1 - \frac2x = 0 \text{ at } x = 2", r"f(1) = 1,\ \ f(2) = 2 - 2\ln 2 \approx 0.614", r"f\left(e^2\right) = e^2 - 4 \approx 3.389",
                      r"\text{absolute max } e^2 - 4 \text{ at } x = e^2;\ \ \text{absolute min } 2 - 2\ln 2 \text{ at } x = 2"], at=[1, 2, 3, 4])
        self.example("Example 3: A trig function", r"Find the absolute extrema of $f(x) = \sin x + \cos x$ on $[0, \pi]$.",
                     [r"f'(x) = \cos x - \sin x = 0 \text{ at } x = \frac\pi4", r"f(0) = 1,\ \ f\left(\frac\pi4\right) = \sqrt2,\ \ f(\pi) = -1",
                      r"\text{absolute max } \sqrt2 \text{ at } \frac\pi4;\ \ \text{absolute min } -1 \text{ at } \pi"], at=[1, 2, 3])
        self.finish()
