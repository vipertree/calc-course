"""Topic 1.12: Confirming continuity over an interval. Narration comes from transcripts/1_12.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def family(name, fn, xr, yr):
    a, _ = plot_axes([xr[0], xr[1], 1], [yr[0], yr[1], 1], w=2.4, h=1.6, coords=False)
    return VGroup(VGroup(a, a.plot(fn, x_range=[xr[0] + 0.01, xr[1]], color=FUNC, use_smoothing=False)), T(name, 26, DIM)).arrange(DOWN, buff=0.15)


def shelf():
    fams = [("polynomials", lambda x: 0.3 * x ** 3 - x, (-2, 2), (-2, 2)), ("rational", lambda x: 1 / x if abs(x) > 0.3 else np.nan, (-2, 2), (-3, 3)),
            ("roots, powers", np.sqrt, (0, 4), (0, 2)), ("exponentials", np.exp, (-2, 1), (0, 3)),
            ("logarithms", np.log, (0.05, 4), (-3, 2)), ("trig", np.sin, (-3, 3), (-1.2, 1.2))]
    return VGroup(*[family(n, f, xr, yr) for n, f, xr, yr in fams]).arrange_in_grid(2, 3, buff=(0.8, 0.5))


class Lesson(TranscriptScene):
    NUM = "1.12"

    def construct(self):
        ax, al = plot_axes([0, 6, 1], [0, 4, 1], w=9, h=4.4, coords=False)
        f = lambda x: 2 + 0.8 * np.sin(x)
        curve = ax.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)
        with self.beat("From one point to many") as b:
            self.play(FadeIn(ax), Create(curve), run_time=1.4)
            xv = ValueTracker(0.5)
            glass = always_redraw(lambda: Circle(radius=0.35, color=SECANT, stroke_width=4).move_to(ax.c2p(xv.get_value(), f(xv.get_value()))))
            self.add(glass)
            ticks = VGroup()
            for v in [1.2, 1.9, 2.6, 3.3]:
                self.play(xv.animate.set_value(v), run_time=0.5)
                tk = Text("✓", color=DERIV, font_size=26).move_to(ax.c2p(v, f(v) - 0.6))
                ticks.add(tk)
                self.add(tk)
            b.line(1)
            self.play(xv.animate.set_value(5.5), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("The definition") as b:
            a, _ = plot_axes([0, 6, 1], [0, 4, 1], w=9, h=4, coords=False)
            band = Rectangle(width=abs(a.c2p(4.5, 0)[0] - a.c2p(1.5, 0)[0]), height=0.25, fill_color=SECANT, fill_opacity=0.5, stroke_width=0).move_to(a.c2p(3, 0))
            ab = VGroup(M("a", 36, SECANT).next_to(a.c2p(1.5, 0), DOWN), M("b", 36, SECANT).next_to(a.c2p(4.5, 0), DOWN))
            self.play(FadeIn(a), Create(a.plot(lambda x: 2 + 0.5 * np.cos(x), x_range=[0, 6], color=FUNC, stroke_width=5)), FadeIn(band), FadeIn(ab), run_time=1.6)
            t = T("continuous at every point of the interval", 40, SECANT).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(t), run_time=0.8)
        self.clear()

        sh = shelf()
        with self.beat("The library of continuous functions") as b:
            self.play(LaggedStart(*[FadeIn(m) for m in sh], lag_ratio=0.2), run_time=2.4)
            ban = T("continuous on their domains", 44, SECANT).to_edge(UP, buff=0.5)
            self.play(FadeIn(ban), run_time=0.8)
            b.line(1)
            q = T(r"``where is it continuous?'' $\to$ ``where is it defined?''", 38).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(q), run_time=0.8)
        self.clear()

        with self.beat("Reading a domain") as b:
            e = M(r"\frac{\sqrt{x - 1}}{x - 4}", 72, FUNC).to_edge(UP, buff=0.6)
            self.play(Write(e), run_time=1)
            c1 = M(r"x - 1 \ge 0 \Rightarrow x \ge 1", 44, SECANT).next_to(e, DOWN, buff=0.5).shift(LEFT * 3)
            c2 = M(r"x - 4 \ne 0 \Rightarrow x \ne 4", 44, TANGENT).next_to(e, DOWN, buff=0.5).shift(RIGHT * 3)
            self.play(Write(c1), Write(c2), run_time=1.4)
            nl = NumberLine(x_range=[-1, 8, 1], length=11, color=DIM, include_numbers=True, font_size=28).shift(DOWN * 1.2)
            shade = Line(nl.n2p(1), nl.n2p(8), color=FUNC, stroke_width=10)
            self.play(Create(nl), run_time=0.6)
            b.line(1)
            self.play(Create(shade), FadeIn(Dot(nl.n2p(1), color=FUNC, radius=0.12)),
                      FadeIn(Circle(radius=0.12, color=TANGENT, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(nl.n2p(4))), run_time=1.2)
            ans = M(r"[1, 4) \cup (4, \infty)", 50, FUNC).to_edge(DOWN, buff=0.5)
            self.play(Write(ans), run_time=1)
        self.clear()
        self.example("Read the domain", r"Where is $f(x) = \dfrac{\sqrt{x - 1}}{x - 4}$ continuous?",
                     [r"\sqrt{x - 1}: \ x \ge 1", r"x - 4 \ne 0: \ x \ne 4", r"\text{continuous on } [1, 4) \cup (4, \infty)"], at=[1, 2, 3])
        self.example("Logs and trig", r"Where are (a) $g(x) = \ln(9 - x^2)$ and (b) $h(x) = \tan x$ continuous?",
                     [r"\text{(a) } 9 - x^2 > 0 \ \Rightarrow\ -3 < x < 3", r"\text{(b) } \tan x = \frac{\sin x}{\cos x}: \ \cos x \ne 0", r"x \ne \frac{\pi}{2} + k\pi"], at=[1, 2, 3])

        with self.beat("Building bigger functions") as b:
            ops = VGroup(M(r"f + g", 50), M(r"f - g", 50), M(r"f\,g", 50), M(r"f\big(g(x)\big)", 50), M(r"\frac{f}{g}\ (g \ne 0)", 50, SECANT)).arrange(RIGHT, buff=0.8)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.2) for m in ops], lag_ratio=0.3), run_time=2.2)
            ok = T("all continuous", 40, DERIV).next_to(ops, DOWN, buff=0.6)
            self.play(FadeIn(ok), run_time=0.6)
        self.clear()

        a2, al2 = plot_axes([-1, 3, 1], [-1, 3, 1], w=7, h=5)
        VGroup(a2, al2).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        with self.beat("Piecewise functions need one extra check") as b:
            pw = M(r"f(x) = \begin{cases} x^2, & x < 1 \\ 2 - x, & x \ge 1 \end{cases}", 44).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            self.play(FadeIn(a2), FadeIn(al2), Write(pw), run_time=1.2)
            self.play(Create(a2.plot(lambda x: x * x, x_range=[-1, 1], color=FUNC, stroke_width=5)), Create(a2.plot(lambda x: 2 - x, x_range=[1, 3], color=FUNC, stroke_width=5)), run_time=1.4)
            gl = Circle(radius=0.4, color=SECANT, stroke_width=4).move_to(a2.c2p(1, 1))
            self.play(Create(gl), run_time=0.6)
            b.line(1)
            ch = VGroup(M(r"\lim_{x\to1^-} = 1", 40), M(r"\lim_{x\to1^+} = 1", 40), M(r"f(1) = 1", 40), T("continuous everywhere", 36, DERIV)).arrange(DOWN, aligned_edge=LEFT).next_to(pw, DOWN, buff=0.4)
            self.play(FadeIn(ch), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            sh = shelf().scale(0.8).shift(UP * 0.5)
            note = T("check the domain; check the seams", 44, SECANT).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(sh), FadeIn(note), run_time=1.4)
        self.clear()

        self.examples_card()
        self.example("Example 1: A log over a line", r"Where is $f(x) = \dfrac{\ln(x + 2)}{x - 1}$ continuous?",
                     [r"\text{built from continuous pieces: find the domain}", r"x + 2 > 0 \Rightarrow x > -2, \qquad x \ne 1", r"(-2, 1) \cup (1, \infty)"], at=[1, 2, 3])
        self.example("Example 2: Factor the denominator", r"Where is $g(x) = \dfrac{x + 3}{x^2 - x - 6}$ discontinuous?",
                     [r"\text{rational: only where the denominator is } 0", r"x^2 - x - 6 = (x - 3)(x + 2)", r"x = 3 \text{ and } x = -2"], at=[1, 2, 3])
        self.example("Example 3: Two seams", r"Is $h$ continuous everywhere? \[ h(x) = \begin{cases} x + 2, & x < 0 \\ 2\cos x, & 0 \le x \le \pi \\ x - \pi - 2, & x > \pi \end{cases} \]",
                     [r"x = 0:\ \ \lim_{x\to0^-}(x + 2) = 2, \quad h(0) = 2\cos 0 = 2\ \checkmark",
                      r"x = \pi:\ \ h(\pi) = 2\cos\pi = -2, \quad \lim_{x\to\pi^+}(x - \pi - 2) = -2\ \checkmark",
                      r"\text{continuous everywhere}"], at=[1, 2, 3])
        self.finish()
