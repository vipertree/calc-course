"""Topic 1.4: Estimating limit values from tables. Narration comes from transcripts/1_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def reveal_cols(scene, tb, cols, run_time=0.6):
    scene.play(*[FadeIn(tb.cells[r][c]) for c in cols for r in range(len(tb.cells))], run_time=run_time)


def blank_table(headers, rows, size=36):
    tb = table(headers, rows, size=size)
    for row in tb.cells:
        for m in row[1:]:
            m.set_opacity(0)
    return tb


def show(tb, cols):
    return [tb.cells[r][c].animate.set_opacity(1) for c in cols for r in range(len(tb.cells))]


class Lesson(TranscriptScene):
    NUM = "1.4"

    def construct(self):
        with self.beat("A limit with no graph handy") as b:
            e = M(r"\lim_{x\to0}\frac{\sin x}{x}", 80, FUNC)
            self.play(Write(e), run_time=1.4)
            b.line(1)
            z = M(r"\frac{\sin 0}{0} = \frac{0}{0}", 64, TANGENT).next_to(e, DOWN, buff=0.6)
            self.play(Write(z), run_time=1)
            self.play(FadeOut(z), run_time=1)
        self.clear()
        self.title()

        xs = ["-0.1", "-0.01", "-0.001", "0.001", "0.01", "0.1"]
        ys = ["0.998334", "0.999983", "0.9999998", "0.9999998", "0.999983", "0.998334"]
        tb = blank_table(["x"] + xs, [[r"\frac{\sin x}{x}"] + ys], size=34)
        tb.set_max_width(13).shift(UP * 0.5)
        with self.beat("Building the table") as b:
            self.play(FadeIn(tb), run_time=0.8)
            b.line(1)
            for pair in [(1, 6), (2, 5), (3, 4)]:
                self.play(*show(tb, pair), run_time=0.8)
            b.line(2)
            self.play(*[Indicate(tb.cells[1][c], color=SECANT) for c in (3, 4)], run_time=1)
            b.line(3)
            res = M(r"\lim_{x\to0}\frac{\sin x}{x} = 1", 60, SECANT).next_to(tb, DOWN, buff=0.8)
            self.play(Write(res), run_time=1.2)
        self.clear()

        with self.beat("What makes a good table") as b:
            items = VGroup(*[T(rf"$\checkmark$\ \ {s_}", 44) for s_ in ["inputs from both sides", "inputs that keep getting closer (factors of ten)",
                                                                          "watch for digits that stop changing"]]).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            for m in items:
                self.play(FadeIn(m, shift=RIGHT * 0.3), run_time=0.9)
        self.clear()
        own = table(["x", "0.9", "0.99", "0.999", "1.001", "1.01", "1.1"], [["f(x)", "2.71", "2.9701", "2.997", "3.003", "3.0301", "3.31"]], size=30)
        self.example("Your own table", r"Use a table to estimate $\displaystyle\lim_{x\to1}\frac{x^3 - 1}{x - 1}$.",
                     [r"\text{left: } 2.71,\ 2.9701,\ 2.997", r"\text{right: } 3.31,\ 3.0301,\ 3.003", r"\lim_{x\to1}\frac{x^3 - 1}{x - 1} \approx 3"], at=[1, 2, 3], figure=own)

        with self.beat("Trap one: unlucky inputs") as b:
            t2 = blank_table(["x", "0.1", "0.01", "0.001"], [[r"\sin\frac{\pi}{x}", "0", "0", "0"]], size=40)
            t2.to_edge(UP, buff=0.7)
            self.play(FadeIn(t2), *show(t2, [1, 2, 3]), run_time=1.4)
            b.line(1)
            a, _ = plot_axes([0, 0.6, 0.1], [-1.3, 1.3, 1], w=10, h=3.6, coords=False)
            a.next_to(t2, DOWN, buff=0.5)
            wave = a.plot(lambda x: np.sin(np.pi / x), x_range=[0.012, 0.6], color=FUNC, use_smoothing=False)
            pts = VGroup(*[Dot(a.c2p(v, 0), color=SECANT, radius=0.09) for v in (0.1,)])
            self.play(FadeIn(a), Create(wave), run_time=2)
            b.line(2)
            self.play(FadeIn(pts), run_time=0.6)
            dne = M(r"\lim_{x\to0}\sin\frac{\pi}{x}\ \text{does not exist}", 44, TANGENT).to_edge(DOWN, buff=0.4)
            self.play(Write(dne), run_time=1.2)
        self.clear()

        with self.beat("Trap two: too close for the calculator") as b:
            calc = RoundedRectangle(width=7.6, height=4, corner_radius=0.3, color=DIM, stroke_width=6, fill_color="#20302A", fill_opacity=1)
            l0 = M(r"\frac{1 - \cos x}{x^2}", 54, DERIV).move_to(calc).shift(UP * 1.1)
            self.play(FadeIn(calc), Write(l0), run_time=1.2)
            r1 = M(r"x = 0.001:\ \ 0.49999996", 44, DERIV).next_to(l0, DOWN, buff=0.4)
            self.play(Write(r1), run_time=1)
            b.line(1)
            r2 = M(r"x = 10^{-9}:\ \ 0", 44, TANGENT).next_to(r1, DOWN, buff=0.3)
            self.play(Write(r2), run_time=1)
            b.line(2)
            warn = T("suspect the calculator, not the math", 40, SECANT).next_to(calc, DOWN, buff=0.4)
            self.play(FadeIn(warn), run_time=0.8)
        self.clear()

        with self.beat("Reading a given table") as b:
            t3 = table(["x", "1.9", "1.99", "1.999", "2.001", "2.01", "2.1"], [["f(x)", "3.9", "3.99", "3.999", "5.001", "5.01", "5.1"]], size=38)
            t3.set_max_width(13).shift(UP * 0.6)
            self.play(FadeIn(t3), run_time=1)
            b.line(1)
            lb = Brace(VGroup(*[t3.cells[1][c] for c in (1, 2, 3)]), DOWN, color=SECANT)
            rb = Brace(VGroup(*[t3.cells[1][c] for c in (4, 5, 6)]), DOWN, color=TANGENT)
            self.play(GrowFromCenter(lb), FadeIn(T(r"heading to 4", 36, SECANT).next_to(lb, DOWN)), run_time=0.9)
            self.play(GrowFromCenter(rb), FadeIn(T(r"heading to 5", 36, TANGENT).next_to(rb, DOWN)), run_time=0.9)
            b.line(2)
            dn = M(r"\lim_{x\to2} f(x)\ \text{does not exist}", 46).to_edge(DOWN, buff=0.6)
            self.play(Write(dn), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            a, al = plot_axes([-4, 4, 2], [-0.5, 1.5, 0.5], w=6.4, h=3.6)
            VGroup(a, al).to_edge(RIGHT, buff=0.6)
            sinc = VGroup(a.plot(lambda x: np.sin(x) / x, x_range=[-4, -0.01], color=FUNC, stroke_width=4),
                          a.plot(lambda x: np.sin(x) / x, x_range=[0.01, 4], color=FUNC, stroke_width=4), open_dot(a, 0, 1))
            ev = VGroup(T("a table gives", 40), T("evidence, not proof", 48, SECANT)).arrange(DOWN).to_edge(LEFT, buff=0.8)
            self.play(FadeIn(a), FadeIn(al), Create(sinc), FadeIn(ev), run_time=1.8)
        self.clear()

        # ---------------------------------------------------------------- worked examples
        self.examples_card()
        te = table(["x", "-0.1", "-0.01", "-0.001", "0.001", "0.01", "0.1"],
                   [["(1+x)^{1/x}", "2.8680", "2.7320", "2.7196", "2.7169", "2.7048", "2.5937"]], size=34)
        self.example("Example 1: A famous number", r"Estimate $\displaystyle\lim_{x\to0}(1 + x)^{1/x}$.",
                     [te, r"\text{right: } 2.59,\ 2.70,\ 2.717 \qquad \text{left: } 2.87,\ 2.73,\ 2.7196",
                      r"\lim_{x\to0}(1 + x)^{1/x} \approx 2.718 = e"], at=[1, 3, 5],
                     text=r"Estimate $\displaystyle\lim_{x\to0}(1 + x)^{1/x}$ from the table. \[ \begin{array}{c|cccccc} x & -0.1 & -0.01 & -0.001 & 0.001 & 0.01 & 0.1 \\ \hline (1+x)^{1/x} & 2.8680 & 2.7320 & 2.7196 & 2.7169 & 2.7048 & 2.5937 \end{array} \]")
        tf = table(["x", "4.9", "4.99", "4.999", "5", "5.001", "5.01", "5.1"], [["f(x)", "7.2", "7.02", "7.002", "2", "6.998", "6.98", "6.8"]], size=34)
        tf.cells[0][4].set_opacity(0.35)
        tf.cells[1][4].set_opacity(0.35)
        self.example("Example 2: The value in the middle doesn't count", r"Find $\displaystyle\lim_{x\to5} f(x)$.",
                     [tf, r"\text{left} \to 7 \qquad \text{right} \to 7", r"\lim_{x\to5} f(x) = 7", r"f(5) = 2\ \text{(ignored by the limit)}"], at=[1, 2, 3, 4],
                     text=r"Find $\displaystyle\lim_{x\to5} f(x)$ from the table. \[ \begin{array}{c|ccccccc} x & 4.9 & 4.99 & 4.999 & 5 & 5.001 & 5.01 & 5.1 \\ \hline f(x) & 7.2 & 7.02 & 7.002 & 2 & 6.998 & 6.98 & 6.8 \end{array} \]")
        tg = table(["x", "1.9", "1.99", "1.999", "2.001", "2.01", "2.1"],
                   [[r"\tfrac{1}{(x-2)^2}", "100", "10^4", "10^6", "10^6", "10^4", "100"]], size=34)
        self.example("Example 3: Outputs that run away", r"Estimate $\displaystyle\lim_{x\to2}\frac{1}{(x - 2)^2}$.",
                     [tg, r"\text{grows without bound on both sides}", r"\lim_{x\to2}\frac{1}{(x-2)^2} = \infty \quad (\text{does not exist})"], at=[1, 3, 4],
                     text=r"Estimate $\displaystyle\lim_{x\to2}\frac{1}{(x - 2)^2}$ from the table. \[ \begin{array}{c|cccccc} x & 1.9 & 1.99 & 1.999 & 2.001 & 2.01 & 2.1 \\ \hline \frac{1}{(x-2)^2} & 100 & 10^4 & 10^6 & 10^6 & 10^4 & 100 \end{array} \]")
        self.finish()
