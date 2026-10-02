"""Topic 5.7: The Second Derivative Test. Narration comes from transcripts/5_7.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def flat(fn, label, color):
    a, _ = plot_axes([-1.5, 1.5, 1], [-2, 2, 1], w=4, h=3.2, coords=False)
    return VGroup(a, a.plot(fn, x_range=[-1.5, 1.5, 0.01], color=FUNC, stroke_width=5), Line(a.c2p(-0.6, fn(0)), a.c2p(0.6, fn(0)), color=SECANT, stroke_width=4),
                  Dot(a.c2p(0, fn(0)), color=INK), T(label, 34, color))


class Lesson(TranscriptScene):
    NUM = "5.7"

    def construct(self):
        cap = flat(lambda s: 1.2 - 0.9 * s * s, "concave down: max", TANGENT)
        cup = flat(lambda s: 0.9 * s * s - 1.2, "concave up: min", DERIV)
        for g in (cap, cup):
            g[4].next_to(g[0], DOWN, buff=0.3)
        VGroup(cap, cup).arrange(RIGHT, buff=1.6)
        with self.beat("Flat on top, flat on the bottom") as b:
            self.play(FadeIn(cap[:4]), FadeIn(cup[:4]), run_time=1)
            b.line(1)
            self.play(FadeIn(cap[4]), run_time=0.6)
            b.line(2)
            self.play(FadeIn(cup[4]), run_time=0.6)
        self.clear()
        self.title()

        with self.beat("The test") as b:
            head = M(r"\text{Suppose } f'(c) = 0.", 48, SECANT)
            rows = VGroup(M(r"f''(c) < 0:\ \text{relative maximum}", 46, TANGENT), M(r"f''(c) > 0:\ \text{relative minimum}", 46, DERIV),
                          M(r"f''(c) = 0:\ \text{no conclusion}", 46, DIM)).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            VGroup(head, rows).arrange(DOWN, buff=0.7)
            self.play(FadeIn(head), run_time=0.6)
            for k, r in enumerate(rows):
                b.line(k + 1)
                self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.7)
        self.clear()
        self.example("Using the test", r"Classify the critical points of $f(x) = 2x^3 - 6x$.",
                     [r"f'(x) = 6x^2 - 6 = 0 \text{ at } x = \pm 1", r"f''(x) = 12x", r"f''(-1) = -12 < 0: \ \text{relative max}; \quad f''(1) = 12 > 0: \ \text{relative min}"], at=[1, 2, 3])

        with self.beat("When the test is silent") as b:
            g = VGroup(flat(lambda s: 0.8 * s**4, r"$x^4$: min", DERIV), flat(lambda s: -0.8 * s**4, r"$-x^4$: max", TANGENT), flat(lambda s: 0.8 * s**3, r"$x^3$: neither", DIM))
            for p in g:
                p[4].next_to(p[0], DOWN, buff=0.3)
            g.arrange(RIGHT, buff=0.6).scale(0.9).shift(UP * 0.3)
            same = M(r"f'(0) = 0,\ \ f''(0) = 0", 40, SECANT).to_edge(UP, buff=0.5)
            self.play(FadeIn(same), *[FadeIn(p[:4]) for p in g], run_time=1)
            b.line(1)
            self.play(*[FadeIn(p[4]) for p in g], run_time=0.8)
        self.clear()

        ax, al = plot_axes([0, 6, 1], [0, 8, 2], w=7, h=5, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        h = lambda s: s + 4 / s
        with self.beat("One critical point") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(h, x_range=[0.55, 6], color=FUNC, stroke_width=5)), run_time=1.2)
            d = Dot(ax.c2p(2, 4), color=DERIV, radius=0.1)
            lab = VGroup(T("only critical point:", 32, DIM), T("relative min, so absolute min", 32, DERIV)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5).shift(UP * 1.2)
            self.play(FadeIn(d), FadeIn(lab[0]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(lab[1]), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"f'(c) = 0,\ f''(c) < 0:\ \text{max}", 44, TANGENT), M(r"f'(c) = 0,\ f''(c) > 0:\ \text{min}", 44, DERIV),
                          M(r"f''(c) = 0:\ \text{use the first derivative test}", 44, DIM)).arrange(DOWN, buff=0.5)
            self.play(FadeIn(card), run_time=1)
        self.clear()

        self.examples_card()
        self.example("Example 1: A cubic", r"Use the Second Derivative Test to classify the critical points of $f(x) = x^3 - 3x^2 + 4$.",
                     [r"f'(x) = 3x^2 - 6x = 3x(x - 2):\ \ x = 0,\ 2", r"f''(x) = 6x - 6", r"f''(0) = -6 < 0:\ \text{relative max at } x = 0",
                      r"f''(2) = 6 > 0:\ \text{relative min at } x = 2"], at=[1, 2, 3, 4])
        self.example("Example 2: When the test fails", r"Classify the critical point of $f(x) = x^4$.",
                     [r"f'(x) = 4x^3 = 0 \text{ at } x = 0", r"f''(x) = 12x^2,\ \ f''(0) = 0:\ \text{inconclusive}",
                      r"f' < 0 \text{ for } x < 0,\ \ f' > 0 \text{ for } x > 0:\ \text{relative min}"], at=[1, 2, 3])
        self.example("Example 3: The only critical point", r"Find the absolute minimum value of $f(x) = x + \dfrac{4}{x}$ on $(0, \infty)$. Justify.",
                     [r"f'(x) = 1 - \frac{4}{x^2} = 0 \text{ at } x = 2", r"f''(x) = \frac{8}{x^3},\ \ f''(2) = 1 > 0:\ \text{relative min}",
                      r"TEXT:It is the only critical point on $(0, \infty)$, so it is the absolute minimum.", r"f(2) = 2 + 2 = 4"], at=[1, 2, 3, 4])
        self.finish()
