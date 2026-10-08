"""Topic 5.4: The First Derivative Test. Narration comes from transcripts/5_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def mini(fn, signs, word):
    """A small graph with a horizontal tangent at its middle, the signs of f' on each side, and a word underneath."""
    a, _ = plot_axes([-1.2, 1.2, 1], [-1.5, 1.5, 1], w=3.4, h=2.8, coords=False)
    g = VGroup(a, a.plot(fn, x_range=[-1.2, 1.2, 0.01], color=FUNC, stroke_width=5),
               Line(a.c2p(-0.5, fn(0)), a.c2p(0.5, fn(0)), color=SECANT, stroke_width=4), Dot(a.c2p(0, fn(0)), color=INK))
    sg = VGroup(*[M(s, 40, DERIV if s == "+" else TANGENT) for s in signs]).arrange(RIGHT, buff=1.0).next_to(g, UP, buff=0.25)
    return VGroup(g, sg, T(word, 32, SECANT).next_to(g, DOWN, buff=0.25))


class Lesson(TranscriptScene):
    NUM = "5.4"

    def construct(self):
        cards = VGroup(mini(lambda s: 1 - s * s, "+-", "peak"), mini(lambda s: s * s - 1, "-+", "valley"), mini(lambda s: s**3, "++", "neither")).arrange(RIGHT, buff=0.7)
        with self.beat("Three flat spots") as b:
            self.play(*[FadeIn(c[0]) for c in cards], run_time=1.2)
            b.line(1)
            self.play(FadeIn(cards[0][2]), FadeIn(cards[1][2]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(cards[2][2]), run_time=0.6)
            b.line(3)
            self.play(*[FadeIn(c[1]) for c in cards], run_time=1)
        self.clear()
        self.title()

        def rule(signs, text, color):
            sc = sign_chart(["c"], list(signs), width=3.2, size=38)
            return VGroup(sc, T(text, 40, color).next_to(sc, RIGHT, buff=0.8))
        with self.beat("The test") as b:
            rows = VGroup(rule("+-", "relative maximum", DERIV), rule("-+", "relative minimum", DERIV), rule("++", "neither", DIM)).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
            head = T("The First Derivative Test", 46, SECANT).next_to(rows, UP, buff=0.6)
            self.play(FadeIn(head), run_time=0.6)
            for k, r in enumerate(rows):
                b.line(k + 1)
                self.play(FadeIn(r), run_time=0.8)
        self.clear()

        with self.beat("Write the reason") as b:
            good = T(r"$f$ has a relative maximum at $x = 2$ \textbf{because} $f'$ changes from positive to negative at $x = 2$.", 38, DERIV).set_max_width(12.5).shift(UP * 1.6)
            b.line(1)
            self.play(FadeIn(good), run_time=1)
            b.line(2)
            bad = VGroup(T(r"``because $f'(2) = 0$''", 36, DIM), T(r"``because the graph goes up then down''", 36, DIM)).arrange(DOWN, buff=0.5).shift(DOWN * 1)
            self.play(FadeIn(bad), run_time=0.8)
            self.play(*[Create(Cross(m, stroke_color=TANGENT, scale_factor=0.9)) for m in bad], run_time=0.8)
        self.clear()
        c0 = staged_chart([0, 4], ["-", "+", "+"], words=["dec", "inc", "inc"], width=7)
        self.example("From a sign chart", r"$f'(x) = x(x - 4)^2$. Find and classify the critical points of $f$.",
                     [r"x = 0 \text{ or } x - 4 = 0", r"x = 0 \text{ or } x = 4", r"TEXT:Test values: $-1$, $1$, $5$.",
                      r"f'(-1) = (-1)(25) = -25 < 0", r"f'(1) = (1)(9) = 9 > 0", r"f'(5) = (5)(1) = 5 > 0",
                      r"x = 0: \ - \text{ to } +, \text{ relative minimum}", r"x = 4: \ \text{no sign change, no extremum}"], at=[1, 1, 2, 3, 4, 5, 6, 7],
                     figure=c0, figure_at=2, cues={3: reveal_sign(c0, 0), 4: reveal_sign(c0, 1),
                                                   5: lambda sc: (reveal_sign(c0, 2)(sc), reveal_words(c0)(sc)),
                                                   6: mark_point(c0, 0, "min"), 7: mark_point(c0, 1, "neither", DIM)})

        with self.beat("Close") as b:
            charts = VGroup(*[VGroup(sign_chart(["c"], list(s), width=2.6, size=36), T(w, 32, SECANT)).arrange(DOWN, buff=0.5)
                              for s, w in (("+-", "max"), ("-+", "min"), ("++", "neither"))]).arrange(RIGHT, buff=1.0)
            self.play(LaggedStart(*[FadeIn(c) for c in charts], lag_ratio=0.4), run_time=1.6)
        self.clear()

        self.examples_card()
        c1 = staged_chart([0, 3], ["-", "-", "+"], words=["dec", "dec", "inc"], width=7)
        self.example("Example 1: A flat spot that isn't an extremum", r"Find and classify the critical points of $f(x) = x^4 - 4x^3$.",
                     [r"f'(x) = 4x^3 - 12x^2", r"= 4x^2(x - 3)", r"x = 0 \text{ or } x = 3",
                      r"f'(-1) = 4(1)(-4) = -16 < 0", r"f'(1) = 4(1)(-2) = -8 < 0", r"f'(4) = 4(16)(1) = 64 > 0",
                      r"x = 0:\ \text{no sign change, neither}", r"x = 3:\ - \text{ to } +, \text{ relative minimum}"], at=[1, 2, 3, 4, 5, 6, 7, 8],
                     figure=c1, figure_at=3, cues={3: reveal_sign(c1, 0), 4: reveal_sign(c1, 1),
                                                   5: lambda sc: (reveal_sign(c1, 2)(sc), reveal_words(c1)(sc)),
                                                   6: mark_point(c1, 0, "neither", DIM), 7: mark_point(c1, 1, "min")})
        c2 = staged_chart([r"\tfrac{2\pi}{3}", r"\tfrac{4\pi}{3}"], ["+", "-", "+"], words=["inc", "dec", "inc"], width=7)
        self.example("Example 2: A trig function", r"Find the relative extrema of $f(x) = x + 2\sin x$ on $(0, 2\pi)$.",
                     [r"f'(x) = 1 + 2\cos x", r"1 + 2\cos x = 0", r"\cos x = -\tfrac12", r"x = \tfrac{2\pi}{3} \text{ or } x = \tfrac{4\pi}{3}",
                      r"f'\left(\tfrac\pi2\right) = 1 + 2(0) = 1 > 0", r"f'(\pi) = 1 + 2(-1) = -1 < 0", r"f'\left(\tfrac{3\pi}{2}\right) = 1 + 2(0) = 1 > 0",
                      r"\text{relative max at } \tfrac{2\pi}{3} \ (+ \text{ to } -)", r"\text{relative min at } \tfrac{4\pi}{3} \ (- \text{ to } +)"],
                     at=[1, 2, 2, 3, 4, 5, 6, 7, 8],
                     figure=c2, figure_at=3, cues={4: reveal_sign(c2, 0), 5: reveal_sign(c2, 1),
                                                   6: lambda sc: (reveal_sign(c2, 2)(sc), reveal_words(c2)(sc)),
                                                   7: mark_point(c2, 0, "max"), 8: mark_point(c2, 1, "min")})
        c3 = staged_chart([-2, 1], ["+", "-", "+"], words=["inc", "dec", "inc"], width=7)
        self.example("Example 3: Given the derivative", r"$f'(x) = (x - 1)(x + 2)e^{x}$. Find the relative extrema of $f$ and justify.",
                     [r"TEXT:$e^x > 0$, so $f'$ has the sign of $(x - 1)(x + 2)$.", r"x = 1 \text{ or } x = -2",
                      r"f'(-3) = (-4)(-1)e^{-3} > 0", r"f'(0) = (-1)(2)(1) = -2 < 0", r"f'(2) = (1)(4)e^{2} > 0",
                      r"\text{relative max at } x = -2 \text{: } f' \text{ changes from } + \text{ to } -",
                      r"\text{relative min at } x = 1 \text{: } f' \text{ changes from } - \text{ to } +"], at=[1, 2, 3, 4, 5, 6, 7],
                     figure=c3, figure_at=2, cues={2: reveal_sign(c3, 0), 3: reveal_sign(c3, 1),
                                                   4: lambda sc: (reveal_sign(c3, 2)(sc), reveal_words(c3)(sc)),
                                                   5: mark_point(c3, 0, "max"), 6: mark_point(c3, 1, "min")})
        self.finish()
