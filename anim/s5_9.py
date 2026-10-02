"""Topic 5.9: Connecting f, f' and f''. Narration comes from transcripts/5_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.9"

    def three(self):
        f = lambda s: 0.25 * s**4 - s**3 + 2
        d1 = lambda s: s**3 - 3 * s**2
        d2 = lambda s: 3 * s**2 - 6 * s
        rows = []
        for fn, yr, lab, col in ((f, [-6, 3, 3], "f", FUNC), (d1, [-5, 10, 5], "f'", DERIV), (d2, [-5, 20, 5], "f''", TANGENT)):
            a, l = plot_axes([-1, 4, 1], yr, w=8, h=1.9, coords=False, ylabel=lab, font=22)
            rows.append(VGroup(a, l, a.plot(fn, x_range=[-0.6, 3.5], color=col, stroke_width=4)))
        g = VGroup(*rows).arrange(DOWN, buff=0.25).to_edge(LEFT, buff=0.6)
        return g, (f, d1, d2)

    def construct(self):
        g, fns = self.three()
        with self.beat("Three graphs, one function") as b:
            self.play(LaggedStart(*[FadeIn(r) for r in g], lag_ratio=0.3), run_time=1.6)
            b.line(1)
            S = ValueTracker(-0.55)
            axes = [r[0] for r in g]
            line = always_redraw(lambda: Line(axes[0].c2p(S.get_value(), 3), axes[2].c2p(S.get_value(), -5), color=SECANT, stroke_width=3))
            sg = lambda v: "+" if v > 1e-9 else "-" if v < -1e-9 else "0"
            read = always_redraw(lambda: VGroup(
                M(rf"f' \; {sg(fns[1](S.get_value()))}", 38, DERIV), M(rf"f'' \; {sg(fns[2](S.get_value()))}", 38, TANGENT)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=1.2))
            self.add(line, read)
            b.line(2)
            self.play(S.animate.set_value(3.45), run_time=6, rate_func=linear)
        self.clear()
        self.title()

        with self.beat("Which level decides") as b:
            tab = table([r"f", r"f'", r"f''"], [[r"\text{increasing}", r"f' > 0", r"\ "], [r"\text{extremum}", r"f' \text{ changes sign}", r"\ "],
                                               [r"\text{concave up}", r"f' \text{ increasing}", r"f'' > 0"], [r"\text{inflection}", r"f' \text{ has an extremum}", r"f'' \text{ changes sign}"]], size=36)
            self.play(FadeIn(tab[1]), FadeIn(VGroup(*tab.cells[0])), run_time=0.6)
            for k in range(1, 5):
                if k in (1, 3, 4):
                    b.line({1: 1, 3: 2, 4: 3}[k])
                self.play(FadeIn(VGroup(*tab.cells[k])), run_time=0.6)
        self.clear()

        with self.beat("Justify at the right level") as b:
            good = T(r"$f$ is concave up on $(3, \infty)$ \textbf{because} $f'' > 0$ there.", 42, DERIV).shift(UP * 1)
            bad = T(r"$f$ is concave up because it curves upward.", 42, DIM).shift(DOWN * 0.8)
            self.play(FadeIn(good), run_time=0.8)
            b.line(1)
            self.play(FadeIn(bad), run_time=0.6)
            self.play(Create(Cross(bad, stroke_color=TANGENT, scale_factor=0.9)), run_time=0.5)
        self.clear()

        with self.beat("Close") as b:
            g, _ = self.three()
            self.play(FadeIn(g), run_time=1)
            labs = VGroup(T(r"$f'$: direction and extrema", 32, DERIV).next_to(g[1], RIGHT, buff=0.3), T(r"$f''$: concavity and inflection", 32, TANGENT).next_to(g[2], RIGHT, buff=0.3))
            self.play(FadeIn(labs), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: All the features", r"$f'(x) = (x - 1)^2(x - 4)$. Find the relative extrema and inflection points of $f$.",
                     [r"\text{signs of } f' \text{: } -,\ -,\ + \ \Rightarrow\ \text{relative min at } x = 4 \text{ only}",
                      r"f''(x) = 2(x - 1)(x - 4) + (x - 1)^2 = 3(x - 1)(x - 3)", r"\text{signs of } f'' \text{: } +,\ -,\ + \ \Rightarrow\ \text{inflection at } x = 1,\ 3"], at=[1, 2, 3])
        self.example("Example 2: A sign table",
                     r"On $(-\infty, -1)$: $f' > 0$, $f'' < 0$. At $-1$: $f' = 0$. On $(-1, 2)$: $f' < 0$, $f'' < 0$. At $2$: $f'' = 0$. On $(2, \infty)$: $f' < 0$, $f'' > 0$. "
                     r"Find the relative extrema and inflection points of $f$.",
                     [r"x = -1:\ f' \text{ changes from } + \text{ to } -:\ \text{relative max}", r"x = 2:\ f'' \text{ changes from } - \text{ to } +:\ \text{inflection}",
                      r"\text{no relative min: } f' \text{ never goes from } - \text{ to } +"], at=[1, 2, 3])
        self.example("Example 3: When the second derivative is zero too", r"$f'(2) = 0$ and $f''(x) = (x - 2)e^{x}$. Does $f$ have a relative extremum at $x = 2$?",
                     [r"f''(2) = 0:\ \text{the Second Derivative Test is silent}", r"f'' < 0 \text{ for } x < 2,\ \ f'' > 0 \text{ for } x > 2",
                      r"f' \text{ has its minimum, } 0, \text{ at } x = 2:\ \ f' \ge 0 \text{ near } 2", r"\text{no extremum; an inflection point at } x = 2"], at=[1, 2, 3, 4])
        self.finish()
