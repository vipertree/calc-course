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

        with self.beat("Inputs and outputs") as bt:
            self.play(FadeOut(p1), FadeOut(p3[1]), run_time=0.5)
            bt.line(1)
            across = DashedLine(ax.c2p(3, 18), ax.c2p(0, 18), color=TANGENT, stroke_width=3)
            out = VGroup(T(r"the maximum: $18$", 36, TANGENT), T(r"an output, a value of $f$", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            out.move_to(UP * 2.4).shift(RIGHT * (1.0 - out.get_left()[0]))     # the right column starts just past the graph
            self.play(Create(across), FadeIn(out), Indicate(al[1], color=TANGENT), run_time=1)
            bt.line(2)
            down = DashedLine(ax.c2p(3, 18), ax.c2p(3, 0), color=SECANT, stroke_width=3)
            inp = VGroup(T(r"where: $x = 3$", 36, SECANT), T("an input", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            inp.next_to(out, DOWN, buff=0.6).align_to(out, LEFT)
            self.play(Create(down), FadeIn(inp), Indicate(al[0], color=SECANT), run_time=1)
            bt.line(3)
            say = T(r"absolute max $18$, at $x = 3$", 38, INK).next_to(inp, DOWN, buff=0.7).align_to(out, LEFT)
            self.play(FadeIn(say), run_time=0.8)
            bt.line(4)
            qs = VGroup(VGroup(T("What is the absolute maximum?", 30), M("18", 36, TANGENT)).arrange(RIGHT, buff=0.4),
                        VGroup(T("At what $x$ does it occur?", 30), M("x = 3", 36, SECANT)).arrange(RIGHT, buff=0.4)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            qs.set_max_width(5.9).next_to(say, DOWN, buff=0.6).align_to(out, LEFT)
            self.play(FadeIn(qs[0]), run_time=0.6)
            self.play(FadeIn(qs[1]), run_time=0.6)
        self.clear()
        self.example("A parabola on an interval", r"Find the absolute extrema of $f(x) = x^2 - 4x$ on $[0, 5]$. Give each value and where it happens.",
                     [r"f'(x) = 2x - 4", r"2x - 4 = 0, \ \text{so}\ x = 2", r"f(0) = 0", r"f(2) = 4 - 8 = -4", r"f(5) = 25 - 20 = 5",
                      r"\text{absolute max: } 5 \text{ (output), at } x = 5 \text{ (input)}", r"\text{absolute min: } -4 \text{ (output), at } x = 2 \text{ (input)}"],
                     at=[1, 2, 3, 4, 5, 6, 7])

        with self.beat("Close") as bt:
            tab = table(["x", "f(x)"], [["0", "0"], ["1", "-2"], ["3", "18"]], size=40)
            self.play(FadeIn(tab), run_time=1)
            note = T(r"endpoints and critical points; the table is the justification", 34, DIM).next_to(tab, DOWN, buff=0.6)
            self.play(FadeIn(note), run_time=0.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: Just the value", r"Find the absolute maximum value of $f(x) = x^3 - 3x + 1$ on $[0, 3]$.",
                     [r"f'(x) = 3x^2 - 3", r"3x^2 - 3 = 0, \ \ x^2 = 1, \ \ x = \pm 1", r"\text{only } x = 1 \text{ is in } [0, 3]",
                      r"f(0) = 1, \ \ f(1) = 1 - 3 + 1 = -1, \ \ f(3) = 27 - 9 + 1 = 19", r"\text{absolute maximum value: } 19"], at=[1, 2, 3, 4, 5])
        self.example("Example 2: Just the location", r"At what value of $x$ does $f(x) = x - 2\ln x$ attain its absolute minimum on $\left[1, e^2\right]$?",
                     [r"f'(x) = 1 - \frac2x", r"1 - \frac2x = 0, \ \ \frac2x = 1, \ \ x = 2", r"f(1) = 1, \ \ f(2) = 2 - 2\ln 2 \approx 0.614",
                      r"f\left(e^2\right) = e^2 - 4 \approx 3.389", r"\text{smallest output at } x = 2: \ \text{answer } x = 2"], at=[1, 2, 3, 4, 5])
        self.example("Example 3: Both", r"Find the absolute maximum and minimum values of $f(x) = \sin x + \cos x$ on $[0, \pi]$, and where each occurs.",
                     [r"f'(x) = \cos x - \sin x", r"\cos x = \sin x, \ \text{so}\ x = \frac\pi4",
                      r"f(0) = 0 + 1 = 1, \ \ f\left(\frac\pi4\right) = \frac{\sqrt2}{2} + \frac{\sqrt2}{2} = \sqrt2, \ \ f(\pi) = 0 + (-1) = -1",
                      r"\text{absolute max } \sqrt2 \text{ at } x = \frac\pi4", r"\text{absolute min } -1 \text{ at } x = \pi"], at=[1, 2, 3, 4, 4])
        self.finish()
