"""Topic 1.14: Connecting infinite limits and vertical asymptotes. Narration comes from transcripts/1_14.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def branch_plot(ax, f, c, xr, gap=0.12, **kw):
    return VGroup(ax.plot(f, x_range=[xr[0], c - gap], **kw), ax.plot(f, x_range=[c + gap, xr[1]], **kw))


class Lesson(TranscriptScene):
    NUM = "1.14"

    def division_bars(self):
        rows = VGroup(*[M(rf"1 \div {d} = {q}", 44) for d, q in [("0.1", "10"), ("0.01", "100"), ("0.001", "1000")]]).arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(LEFT * 3.5)
        bars = VGroup(*[Rectangle(width=0.8, height=h_, fill_color=TANGENT, fill_opacity=0.8, stroke_width=0) for h_ in (0.5, 1.8, 5.2)]).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        bars.shift(RIGHT * 3 + DOWN * 0.2)
        return rows, bars

    def construct(self):
        rows, bars = self.division_bars()
        with self.beat("Dividing by almost nothing") as b:
            for r, bar in zip(rows, bars):
                self.play(Write(r), GrowFromEdge(bar, DOWN), run_time=1)
            b.line(1)
            self.play(Indicate(bars[-1], color=SECANT), run_time=1)
        self.clear()
        self.title()

        # Adder (2026-10-30): before any sign rules, see what a number over zero does, with numbers plugged in
        with self.beat("A number over zero") as b:
            fx = M(r"f(x) = \frac{1}{x - 2}", 46, FUNC).to_corner(UL, buff=0.6)
            sub = M(r"x = 2:\ \ \frac{1}{2 - 2} = \frac{1}{0}", 40, SECANT).next_to(fx, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(fx), run_time=0.8)
            self.play(Write(sub), run_time=0.8)
            vals = [("1.9", "-0.1", "-10"), ("1.99", "-0.01", "-100"), ("1.999", "-0.001", "-1000"),
                    ("2.1", "0.1", "10"), ("2.01", "0.01", "100"), ("2.001", "0.001", "1000")]
            head = VGroup(M("x", 34, DIM), M("x - 2", 34, DIM), M("f(x)", 34, DIM))
            cells = [VGroup(*[M(v, 34, INK if j == 0 else (TANGENT if i < 3 else DERIV)) for j, v in enumerate(row)]) for i, row in enumerate(vals)]
            grid = VGroup(head, *cells)
            for r in grid:
                for j, cell in enumerate(r):
                    cell.move_to(RIGHT * 1.75 * j, aligned_edge=LEFT)
            grid.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(sub, DOWN, buff=0.45, aligned_edge=LEFT)
            rule = Line(head.get_corner(DL) + DOWN * 0.08, head.get_corner(DR) + DOWN * 0.08 + RIGHT * 0.4, color=DIM, stroke_width=2)
            gx, gl = plot_axes([1, 3, 0.5], [-12, 12, 4], w=5.0, h=5.6, coords=False)
            VGroup(gx, gl).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
            self.play(FadeIn(head), Create(rule), FadeIn(gx), FadeIn(gl), FadeIn(asymptote(gx, 2, [-12, 12])), run_time=0.8)
            b.line(1)
            dl = Dot(gx.c2p(1.9, -10), color=TANGENT)
            self.play(FadeIn(cells[0]), FadeIn(dl), run_time=0.8)
            b.line(2)
            down = Arrow(gx.c2p(1.95, -9), gx.c2p(1.95, -12.6), buff=0, color=TANGENT, stroke_width=5)
            self.play(FadeIn(cells[1]), run_time=0.6)
            self.play(FadeIn(cells[2]), GrowArrow(down), run_time=0.8)
            b.line(3)
            dr = Dot(gx.c2p(2.1, 10), color=DERIV)
            up = Arrow(gx.c2p(2.05, 9), gx.c2p(2.05, 12.6), buff=0, color=DERIV, stroke_width=5)
            self.play(FadeIn(cells[3]), FadeIn(dr), run_time=0.7)
            self.play(FadeIn(cells[4]), FadeIn(cells[5]), GrowArrow(up), run_time=0.9)
            b.line(4)
            self.play(Create(branch_plot(gx, lambda x: 1 / (x - 2), 2, [1, 3], gap=0.085, color=FUNC, stroke_width=4)), run_time=1.4)
            b.line(5)
            col = VGroup(*[c[1] for c in cells])
            neg = SurroundingRectangle(VGroup(*[c[1] for c in cells[:3]]), color=TANGENT, buff=0.08)
            pos = SurroundingRectangle(VGroup(*[c[1] for c in cells[3:]]), color=DERIV, buff=0.08)
            self.play(Create(neg), run_time=0.6)
            self.play(Create(pos), run_time=0.6)
        self.clear()

        ax, al = plot_axes([0, 4, 1], [0, 8, 2], w=7, h=5.2)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        f = lambda x: 1 / (x - 2) ** 2
        with self.beat("Infinite limits") as b:
            self.play(FadeIn(ax), FadeIn(al), FadeIn(asymptote(ax, 2, [0, 8])), Create(branch_plot(ax, f, 2, [0, 4], gap=0.36, color=FUNC, stroke_width=5)), run_time=1.8)
            st = M(r"\lim_{x\to2}\frac{1}{(x - 2)^2} = \infty", 48, FUNC).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
            self.play(Write(st), run_time=1.2)
            b.line(1)
            note = T(r"still does not exist: \\ $\infty$ says \emph{how} it fails", 38, SECANT).next_to(st, DOWN, buff=0.6)
            self.play(FadeIn(note), run_time=0.8)
        with self.beat("Vertical asymptotes") as b:
            va = T(r"vertical asymptote $x = 2$", 34, DIM).next_to(ax.c2p(2, 8), UP, buff=0.1)
            self.play(FadeIn(va), run_time=0.8)
            b.line(1)
            self.play(FadeOut(note), FadeOut(st), run_time=0.4)
            a2, _ = plot_axes([0, 4, 1], [-6, 6, 2], w=5.2, h=4.4)
            a2.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.3)
            self.play(FadeIn(a2), FadeIn(asymptote(a2, 2, [-6, 6])), Create(branch_plot(a2, lambda x: 1 / (x - 2), 2, [0, 4], gap=0.17, color=FUNC, stroke_width=4)), run_time=1.4)
        self.clear()

        # one worked example (the old lesson did it twice): a test number on each side, the sign fraction every time
        ch = staged_chart([1], ["-", "+"], name=r"\text{sign of } f", width=6)
        self.example("Finding the sign", r"Let $f(x) = \dfrac{x + 3}{(x - 1)(x + 2)}$. Find $\displaystyle\lim_{x\to1^-} f(x)$ and $\displaystyle\lim_{x\to1^+} f(x)$.",
                     [r"\text{plug in: } \frac{4}{(0)(3)} = \frac{4}{0}", r"\text{left, } x = 0.9:\ \ \frac{3.9}{(-0.1)(2.9)}", r"\frac{(+)}{(-)(+)} = -",
                      r"\lim_{x\to1^-} f(x) = -\infty", r"\text{right, } x = 1.1:\ \ \frac{4.1}{(0.1)(3.1)}", r"\frac{(+)}{(+)(+)} = +, \ \text{so}\ \lim_{x\to1^+} f(x) = \infty",
                      r"TEXT:Only the signs matter: near $1$, every factor but $x - 1$ keeps its sign."],
                     at=[1, 2, 2, 3, 4, 4, 5], follow=True, figure=ch, figure_at=2, cues={2: reveal_sign(ch, 0), 5: reveal_sign(ch, 1)})
        with self.beat("Not every zero of the denominator") as b:
            e = M(r"\frac{x^2 - 1}{x - 1} = \frac{(x - 1)(x + 1)}{x - 1}", 56).shift(UP * 1.6)
            self.play(Write(e), run_time=1.4)
            a3, _ = plot_axes([-1, 3, 1], [-1, 4, 1], w=5.4, h=3.4)
            a3.shift(DOWN * 1.6)
            self.play(FadeIn(a3), Create(a3.plot(lambda x: x + 1, x_range=[-1, 3], color=FUNC, stroke_width=4)), FadeIn(open_dot(a3, 1, 2)), run_time=1.2)
            self.play(FadeIn(T("a hole, not an asymptote", 36, SECANT).next_to(a3, RIGHT, buff=0.3)), run_time=0.8)
        self.clear()

        with self.beat("Beyond rational functions") as b:
            panels = VGroup()
            a4, _ = plot_axes([0, 4, 1], [-3, 2, 1], w=3.8, h=3, coords=False)
            panels.add(VGroup(a4, a4.plot(np.log, x_range=[0.05, 4], color=FUNC), asymptote(a4, 0, [-3, 2]), M(r"\ln x", 34).next_to(a4, DOWN)))
            a5, _ = plot_axes([-3, 3, 1], [-4, 4, 1], w=3.8, h=3, coords=False)
            tp = VGroup(*[a5.plot(np.tan, x_range=[lo, hi], color=FUNC) for lo, hi in [(-3, -1.82), (-1.32, 1.32), (1.82, 3)]])
            panels.add(VGroup(a5, tp, asymptote(a5, -np.pi / 2, [-4, 4]), asymptote(a5, np.pi / 2, [-4, 4]), M(r"\tan x", 34).next_to(a5, DOWN)))
            a6, _ = plot_axes([-2, 2, 1], [0, 6, 1], w=3.8, h=3, coords=False)
            ep = VGroup(a6.plot(lambda x: np.exp(1 / x), x_range=[0.56, 2], color=FUNC), a6.plot(lambda x: np.exp(1 / x), x_range=[-2, -0.05], color=FUNC))
            panels.add(VGroup(a6, ep, asymptote(a6, 0, [0, 6]), M(r"e^{1/x}", 34).next_to(a6, DOWN)))
            panels.arrange(RIGHT, buff=0.5)
            self.play(FadeIn(panels[0]), run_time=1)
            b.line(1)
            self.play(FadeIn(panels[1]), FadeIn(panels[2]), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            rows, bars = self.division_bars()
            self.play(FadeIn(rows), FadeIn(bars), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: One side at a time", r"Find $\displaystyle\lim_{x\to4^-}\frac{2x + 1}{x - 4}$ and $\displaystyle\lim_{x\to4^+}\frac{2x + 1}{x - 4}$.",
                     [r"\frac{9}{0}:\ \text{heads off toward infinity}", r"2x + 1 \approx 9 > 0", r"x \to 4^-:\ \frac{(+)}{(-)} = -,\ \text{so}\ \lim_{x\to4^-}\frac{2x + 1}{x - 4} = -\infty", r"x \to 4^+:\ \frac{(+)}{(+)} = +,\ \text{so}\ \lim_{x\to4^+}\frac{2x + 1}{x - 4} = \infty"],
                     at=[1, 2, 3, 4])
        self.example("Example 2: Which zeros make asymptotes?", r"Find the vertical asymptotes of $f(x) = \dfrac{x^2 - 9}{x^2 - 2x - 3}$.",
                     [r"\text{denominator } 0 \text{ at } x = 3,\ x = -1", r"\frac{(x - 3)(x + 3)}{(x - 3)(x + 1)}", r"x = 3:\ \text{hole}; \quad x = -1:\ \text{vertical asymptote}"],
                     at=[1, 2, 3])
        self.example("Example 3: Same sign on both sides", r"Find $\displaystyle\lim_{x\to0}\frac{x - 2}{x^2}$.",
                     [r"\frac{-2}{0}", r"\text{top} < 0, \quad x^2 > 0 \text{ on both sides:}\ \ \frac{(-)}{(+)} = -", r"\lim_{x\to0}\frac{x - 2}{x^2} = -\infty"], at=[1, 2, 3])
        self.finish()
