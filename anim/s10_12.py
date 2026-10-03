"""Topic 10.12 (BC): Lagrange error bound. Narration comes from transcripts/10_12.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.12"

    def construct(self):
        with self.beat("How good is the approximation?") as b:
            ax, al = plot_axes([-1, 2, 1], [0, 6, 1], w=6, h=4.4)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            P3 = lambda s: 1 + s + s * s / 2 + s**3 / 6
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(np.exp, x_range=[-1, 1.75], color=FUNC, stroke_width=5)), Create(ax.plot(P3, x_range=[-1, 1.8], color=SECANT, stroke_width=3)), run_time=1.2)
            glass = VGroup(Circle(radius=0.6, color=INK, stroke_width=4), Line(ORIGIN, DR * 0.6, color=INK, stroke_width=8).shift(DR * 0.55)).move_to(ax.c2p(0.1, np.exp(0.1)))
            self.play(FadeIn(glass), run_time=0.6)
            b.line(1)
            self.play(FadeIn(M(r"\text{error} = |f(x) - P_3(x)|", 38).to_edge(RIGHT, buff=0.6).shift(UP * 1)), run_time=0.8)
            b.line(2)
            self.play(FadeIn(T("how big, without knowing $f(0.1)$?", 32, SECANT).to_edge(RIGHT, buff=0.6)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("The bound") as b:
            box = formula_box(M(r"|f(x) - P_n(x)| \le \frac{M}{(n + 1)!}\,|x - a|^{n+1}", 48, ACCUM), ACCUM).to_edge(UP, buff=0.7)
            self.play(FadeIn(box), run_time=1)
            b.line(1)
            notes = VGroup(T("$M$: an upper bound for $|f^{(n+1)}(z)|$ for all $z$ between $a$ and $x$", 30, SECANT), T("$(n + 1)!$: the next factorial", 30), T("$|x - a|^{n+1}$: the next power of the distance", 30)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(box, DOWN, buff=0.5)
            self.play(FadeIn(notes), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("the next Taylor term, with the next derivative at its worst case", 32, DIM).to_edge(DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        self.example("Bounding the error for e to the 0.1", r"$P_3(x) = 1 + x + \frac{x^2}{2} + \frac{x^3}{6}$ approximates $e^x$. Use the Lagrange error bound to bound the error in approximating $e^{0.1}$.",
                     [r"n = 3, \ a = 0, \ x = 0.1", r"f^{(4)}(z) = e^z", r"0 \le z \le 0.1: \ e^z \le e^{0.1} < 1.2, \ \ M = 1.2", r"\text{error} \le \frac{1.2}{4!}(0.1)^4", r"= \frac{1.2 \cdot 0.0001}{24}", r"= 0.000005"],
                     at=[1, 1, 2, 3, 4, 4])

        with self.beat("Close") as b:
            card = VGroup(M(r"|f(x) - P_n(x)| \le \frac{M}{(n + 1)!}|x - a|^{n+1}", 44, ACCUM), T("$M$: an upper bound for $|f^{(n+1)}|$ between $a$ and $x$", 34), T("same shape as the next Taylor term", 34, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Sine", r"Bound the error in approximating $\sin(0.5)$ with $P_3(x) = x - \frac{x^3}{6}$.", [r"f^{(4)}(x) = \sin x, \ |\sin z| \le 1: \ M = 1", r"\text{error} \le \frac{1}{4!}(0.5)^4 = \frac{0.0625}{24} \approx 0.0026"], at=[1, 2])
        self.example("Example 2: ln x near 1", r"$P_3(x) = (x - 1) - \frac12(x - 1)^2 + \frac13(x - 1)^3$ approximates $\ln x$ near $1$. Bound the error at $x = 1.2$.",
                     [r"f^{(4)}(x) = -\frac{6}{x^4}", r"\text{on } [1, 1.2]: \ \left|-\tfrac{6}{z^4}\right| \le \tfrac{6}{1^4} = 6", r"\text{error} \le \frac{6}{4!}(0.2)^4 = \frac{6 \cdot 0.0016}{24} = 0.0004"], at=[1, 1, 2])
        self.example("Example 3: A given derivative bound", r"$|f^{(4)}(x)| \le 12$ for $1 \le x \le 3$, and $P_3$ is the third-degree Taylor polynomial for $f$ about $x = 2$. Bound $|f(2.5) - P_3(2.5)|$.",
                     [r"M = 12, \ n = 3, \ |x - a| = 0.5", r"\text{error} \le \frac{12}{4!}(0.5)^4 = \frac{12 \cdot 0.0625}{24} = 0.03125"], at=[1, 2])
        self.finish()
