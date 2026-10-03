"""Topic 10.13 (BC): Radius and interval of convergence. Narration comes from transcripts/10_13.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def interval_line(lo, hi, lo_closed, hi_closed, xr, labels):
    line = NumberLine(x_range=xr, length=8, include_numbers=False, color=DIM)
    seg = Line(line.n2p(lo), line.n2p(hi), color=DERIV, stroke_width=10)
    def end(v, closed):
        return Dot(line.n2p(v), radius=0.12, color=DERIV) if closed else Circle(radius=0.12, color=DERIV, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(line.n2p(v))
    labs = VGroup(*[M(t, 30).next_to(line.n2p(v), DOWN, buff=0.25) for v, t in labels])
    return VGroup(line, seg, end(lo, lo_closed), end(hi, hi_closed), labs)


class Lesson(TranscriptScene):
    NUM = "10.13"

    def construct(self):
        with self.beat("A series with an x in it") as b:
            title = M(r"1 + x + x^2 + x^3 + \cdots", 48).to_edge(UP, buff=0.6)
            self.play(Write(title), run_time=1)
            line = NumberLine(x_range=[-2, 2, 1], length=9, include_numbers=True, font_size=28, color=DIM).shift(DOWN * 0.5)
            xt = ValueTracker(-1.6)
            ptr = always_redraw(lambda: Triangle(color=SECANT, fill_opacity=1).scale(0.15).rotate(PI).next_to(line.n2p(xt.get_value()), UP, buff=0.05))
            mark = always_redraw(lambda: (M(r"\checkmark", 40, DERIV) if abs(xt.get_value()) < 1 else M(r"\times", 40, TANGENT)).next_to(line.n2p(xt.get_value()), UP, buff=0.5))
            self.play(Create(line), run_time=0.6)
            self.add(ptr, mark)
            self.play(xt.animate.set_value(1.6), run_time=3, rate_func=linear)
            b.line(1)
            self.play(Create(Line(line.n2p(-1), line.n2p(1), color=DERIV, stroke_width=10)), run_time=0.8)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Radius and interval") as b:
            r0 = M(r"\sum c_n (x - a)^n", 46).to_edge(UP, buff=0.6)
            self.play(Write(r0), run_time=0.8)
            b.line(1)
            line = NumberLine(x_range=[-4, 4, 1], length=9, color=DIM).shift(UP * 0.2)
            seg = Line(line.n2p(-2.5), line.n2p(2.5), color=DERIV, stroke_width=10)
            labs = VGroup(M("a - R", 30).next_to(line.n2p(-2.5), DOWN, buff=0.25), M("a", 30).next_to(line.n2p(0), DOWN, buff=0.25), M("a + R", 30).next_to(line.n2p(2.5), DOWN, buff=0.25))
            self.play(Create(line), Create(seg), FadeIn(labs), FadeIn(T("converges absolutely", 28, DERIV).next_to(seg, UP, buff=0.2)),
                      FadeIn(T("diverges", 28, TANGENT).next_to(line.n2p(-3.5), UP, buff=0.2)), FadeIn(T("diverges", 28, TANGENT).next_to(line.n2p(3.5), UP, buff=0.2)), run_time=1.2)
            b.line(2)
            q = VGroup(M("?", 40, SECANT).next_to(line.n2p(-2.5), UP, buff=0.6), M("?", 40, SECANT).next_to(line.n2p(2.5), UP, buff=0.6))
            self.play(FadeIn(q), FadeIn(T("check each endpoint separately", 30, SECANT).shift(DOWN * 1.6)), run_time=0.8)
            b.line(3)
            self.play(FadeIn(T("$R = 0$: only $x = a$; \\ $R = \\infty$: all $x$", 30, DIM).to_edge(DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        fig = interval_line(-1, 5, True, False, [-2, 6, 1], [(-1, "-1"), (2, "2"), (5, "5")])
        self.example("Finding the interval", r"Find the interval of convergence of $\displaystyle\sum_{n=1}^{\infty} \frac{(x - 2)^n}{n \cdot 3^n}$.",
                     [r"\left|\frac{a_{n+1}}{a_n}\right| = \frac{|x - 2|^{n+1}}{(n + 1)3^{n+1}} \cdot \frac{n \cdot 3^n}{|x - 2|^n}", r"= \frac{|x - 2|}{3} \cdot \frac{n}{n + 1}", r"L = \frac{|x - 2|}{3}",
                      r"L < 1: \ |x - 2| < 3, \ R = 3, \ -1 < x < 5", r"x = 5: \ \sum \frac{3^n}{n3^n} = \sum \frac1n \ \text{diverges}", r"x = -1: \ \sum \frac{(-3)^n}{n3^n} = \sum \frac{(-1)^n}{n} \ \text{converges (AST)}", r"[-1, 5)"],
                     at=[1, 1, 2, 3, 4, 5, 6], figure=fig, figure_at=6)

        with self.beat("Close") as b:
            card = VGroup(T("ratio test on $|a_{n+1}/a_n|$: $L < 1$ gives $|x - a| < R$", 34), T("check both endpoints separately (often $p$-series or AST)", 34, SECANT),
                          T("interval: $(a - R, a + R)$ plus any endpoints that converge", 34, ACCUM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Converges everywhere", r"Find the radius of convergence of $\sum \frac{x^n}{n!}$.", [r"\left|\frac{a_{n+1}}{a_n}\right| = \frac{|x|}{n + 1} \to 0 < 1 \text{ for every } x", r"R = \infty: \ (-\infty, \infty)"], at=[1, 2])
        self.example("Example 2: Converges only at the center", r"Find the radius of convergence of $\sum n!\,x^n$.", [r"\left|\frac{a_{n+1}}{a_n}\right| = (n + 1)|x| \to \infty \text{ unless } x = 0", r"R = 0: \ \text{converges only at } x = 0"], at=[1, 2])
        fig3 = interval_line(-1, 1, True, True, [-2, 2, 1], [(-1, "-1"), (0, "0"), (1, "1")])
        self.example("Example 3: Both endpoints included", r"Find the interval of convergence of $\displaystyle\sum_{n=1}^{\infty} \frac{x^n}{n^2}$.",
                     [r"L = |x| \cdot \frac{n^2}{(n + 1)^2} \to |x|: \ R = 1", r"x = 1: \ \sum \tfrac{1}{n^2} \ \text{converges}", r"x = -1: \ \sum \tfrac{(-1)^n}{n^2} \ \text{converges}", r"[-1, 1]"], at=[1, 2, 2, 3], figure=fig3, figure_at=3)
        self.finish()
