"""Topic 10.2 (BC): Geometric series. Narration comes from transcripts/10_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "10.2"

    def construct(self):
        with self.beat("A bouncing ball") as b:
            ground = Line(LEFT * 6.5, RIGHT * 6.5, color=DIM, stroke_width=4).shift(DOWN * 2.6)
            scale = 0.45
            heights = [10 * 0.6**k for k in range(6)]
            x = -6.0
            path = VMobject(color=FUNC, stroke_width=3)
            segs = [np.array([x, ground.get_y() + heights[0] * scale, 0])]
            for k in range(1, 6):
                x0 = x
                x += 1.5 * (0.6 ** (k / 2)) + 0.6
                arc = [np.array([x0 + (x - x0) * u, ground.get_y() + heights[k] * scale * 4 * u * (1 - u), 0]) for u in np.linspace(0, 1, 30)]
                segs += arc
            path.set_points_smoothly(segs)
            ball = Circle(radius=0.18, stroke_width=0, fill_color=TANGENT, fill_opacity=1).move_to(segs[0])
            self.play(Create(ground), FadeIn(ball), run_time=0.6)
            self.play(MoveAlongPath(ball, path), Create(path), run_time=3, rate_func=linear)
            labels = M(r"10,\ 6,\ 3.6,\ 2.16,\ \ldots", 40).to_edge(UP, buff=0.5)
            self.play(FadeIn(labels), run_time=0.6)
            b.line(1)
            self.play(FadeIn(T(r"each term $= 0.6 \times$ the one before", 32, SECANT).next_to(labels, DOWN, buff=0.3)), run_time=0.8)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The partial sum formula") as b:
            r1 = M(r"S_n = a + ar + ar^2 + \cdots + ar^{n-1}", 42).shift(UP * 1.8)
            r2 = M(r"rS_n = \phantom{a + } ar + ar^2 + \cdots + ar^{n-1} + ar^n", 42).next_to(r1, DOWN, buff=0.35).align_to(r1, LEFT)
            self.play(Write(r1), run_time=1)
            b.line(1)
            self.play(Write(r2), run_time=1)
            b.line(2)
            r3 = M(r"S_n - rS_n = a - ar^n", 42, SECANT).next_to(r2, DOWN, buff=0.5)
            self.play(Write(r3), run_time=1)
            b.line(3)
            box = formula_box(M(r"S_n = \frac{a\left(1 - r^n\right)}{1 - r}", 46, ACCUM), ACCUM).next_to(r3, DOWN, buff=0.5)
            self.play(FadeIn(box), run_time=0.8)
        self.clear()

        with self.beat("When it converges") as b:
            r1 = M(r"|r| < 1: \ r^n \to 0, \ \ S_n \to \frac{a}{1 - r}", 44).to_edge(UP, buff=0.6)
            self.play(Write(r1), run_time=1)
            b.line(1)
            box = formula_box(VGroup(M(r"\sum_{n=0}^{\infty} ar^n = \frac{a}{1 - r} \ \ \text{when } |r| < 1", 42, ACCUM), T("diverges when $|r| \\ge 1$", 30, TANGENT),
                                     T("first term over one minus the ratio", 28, DIM)).arrange(DOWN, buff=0.2), ACCUM).next_to(r1, DOWN, buff=0.5)
            self.play(FadeIn(box), run_time=1)
            b.line(2)
            def spark(rr, col, lab):
                ax, _ = plot_axes([0, 6, 2], [0, 2.2, 1], w=2.8, h=1.6, coords=False)
                return VGroup(ax, VGroup(*[Dot(ax.c2p(k, min(rr**k, 2.2)), color=col, radius=0.05) for k in range(7)]), M(lab, 28, col).next_to(ax, DOWN, buff=0.1))
            sp3 = VGroup(spark(0.5, DERIV, r"r = \tfrac12"), spark(1, DIM, "r = 1"), spark(1.15, TANGENT, "r > 1")).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.3)
            self.play(FadeIn(sp3), run_time=1)
        self.clear()

        self.example("Summing a geometric series", r"Find $\displaystyle\sum_{n=0}^{\infty} 3\left(\frac25\right)^n$.",
                     [r"a = 3\left(\tfrac25\right)^0 = 3", r"r = \tfrac25", r"|r| < 1: \ \text{converges}", r"\text{sum} = \frac{3}{1 - \frac25}", r"= \frac{3}{3/5} = 5"], at=[1, 2, 2, 3, 3], follow=True)

        with self.beat("Watch the starting index") as b:
            rows = VGroup(M(r"\sum_{n=1}^{\infty} \left(\tfrac12\right)^n: \ a = \tfrac12, \ \text{sum} = \frac{1/2}{1 - 1/2} = 1", 40), M(r"\sum_{n=0}^{\infty} \left(\tfrac12\right)^n: \ a = 1, \ \text{sum} = \frac{1}{1 - 1/2} = 2", 40),
                          T("same ratio, different first term", 32, SECANT), T("find $a$ by plugging in the first value of $n$", 32, TANGENT)).arrange(DOWN, buff=0.5)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(Write(rows[1]), FadeIn(rows[2]), run_time=1)
            b.line(2)
            self.play(FadeIn(rows[3]), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"a + ar + ar^2 + \cdots \ \text{converges iff } |r| < 1", 42), formula_box(M(r"\text{sum} = \frac{a}{1 - r}", 48, ACCUM), ACCUM), T("find $a$ from the first index", 34, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A negative ratio", r"Find $\displaystyle\sum_{n=1}^{\infty} \left(-\frac13\right)^n$.", [r"a = -\tfrac13, \ \ r = -\tfrac13, \ \ |r| < 1", r"\text{sum} = \frac{-1/3}{1 + 1/3} = \frac{-1/3}{4/3} = -\tfrac14"], at=[1, 2])
        self.example("Example 2: A ratio too big", r"Does $\displaystyle\sum_{n=0}^{\infty} 2\left(\frac32\right)^n$ converge?", [r"r = \tfrac32, \ \ |r| \ge 1: \ \text{diverges}"], at=[1])
        self.example("Example 3: A repeating decimal", r"Write $0.777\ldots$ as a fraction.", [r"0.777\ldots = \tfrac{7}{10} + \tfrac{7}{100} + \tfrac{7}{1000} + \cdots", r"a = \tfrac{7}{10}, \ \ r = \tfrac{1}{10}", r"\text{sum} = \frac{7/10}{9/10} = \frac79"], at=[1, 1, 2])
        self.finish()
