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
            # Adder (2026-10-14): the old slider was unclear. Now: pick a value of x, watch the partial sums S_n settle or
            # run off, and mark the result on a number line of x values; the marks fill in the interval and its radius
            head = M(r"1 + x + x^2 + x^3 + \cdots", 46).to_edge(UP, buff=0.4)
            self.play(Write(head), run_time=1)
            ax, al = plot_axes([0, 12, 2], [-3, 5, 1], w=5.6, h=5.0, xlabel="n", ylabel="S_n", font=24)
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(DOWN * 0.6)
            line = NumberLine(x_range=[-2, 2, 1], length=5.3, include_numbers=True, font_size=32, color=DIM).to_edge(RIGHT, buff=0.8).shift(UP * 0.2)
            xlab = M("x", 34, DIM).next_to(line, RIGHT, buff=0.2)
            self.play(FadeIn(ax), FadeIn(al), Create(line), FadeIn(xlab), run_time=1)
            b.line(1)
            cur = VGroup()

            def case(xv, xtex, result, good):
                """the partial sums for this x on the graph, and a mark on the number line"""
                sums, t = [], 0.0
                for k in range(13):
                    t += xv**k
                    sums.append(t)
                col = DERIV if good else TANGENT
                dots = VGroup(*[Dot(ax.c2p(k, v), radius=0.07, color=col) for k, v in enumerate(sums) if -3 <= v <= 5])
                tag = M("x = " + xtex, 38, col).next_to(ax, UP, buff=0.2).align_to(ax, RIGHT)
                extra = VGroup()
                if good:
                    lim = 1 / (1 - xv)
                    extra.add(DashedLine(ax.c2p(0, lim), ax.c2p(12, lim), color=DIM, stroke_width=2, dash_length=0.1))
                mark = (Dot(line.n2p(xv), radius=0.1, color=DERIV) if good else M(r"\times", 44, TANGENT)).next_to(line.n2p(xv), UP, buff=0.18)
                res = T(result, 32, col).next_to(line, DOWN, buff=0.8)
                old = list(cur)
                self.play(*[FadeOut(m) for m in old], FadeIn(tag), FadeIn(res), FadeIn(extra), run_time=0.6)
                cur.remove(*old)
                self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.25), run_time=2.2)
                self.play(FadeIn(mark, scale=0.6), run_time=0.5)
                cur.add(tag, res, extra, dots)
                return mark

            marks = VGroup()
            marks.add(case(0.5, r"\tfrac12", r"$S_n \to 2$: converges", True))
            b.line(2)
            marks.add(case(-0.5, r"-\tfrac12", r"$S_n \to \frac23$: converges", True))
            b.line(3)
            marks.add(case(1.5, r"\tfrac32", r"$S_n$ grows past any bound: diverges", False))
            b.line(4)
            marks.add(case(-1.5, r"-\tfrac32", r"$S_n$ swings wider and wider: diverges", False))
            b.line(5)
            marks.add(case(1, "1", r"$S_n = n + 1$: diverges", False))
            marks.add(case(-1, "-1", r"$S_n = 1, 0, 1, 0, \ldots$: diverges", False))
            b.line(6)
            self.play(*[FadeOut(m) for m in cur], run_time=0.5)
            seg = Line(line.n2p(-1), line.n2p(1), color=DERIV, stroke_width=10)
            ends = VGroup(*[Circle(radius=0.11, color=DERIV, stroke_width=4, fill_color=BG, fill_opacity=1).move_to(line.n2p(v)) for v in (-1, 1)])
            self.play(Create(seg), FadeIn(ends), run_time=1)
            cen = T("center", 28, INK).next_to(line.n2p(0), DOWN, buff=0.7)
            rad = DoubleArrow(line.n2p(0) + UP * 1.0, line.n2p(1) + UP * 1.0, buff=0, color=ACCUM, stroke_width=4, tip_length=0.2)
            rlab = M("R = 1", 32, ACCUM).next_to(rad, UP, buff=0.12)
            self.play(FadeIn(cen), GrowFromCenter(rad), FadeIn(rlab), run_time=1)
            b.line(7)
            geo = M(r"\text{converges when } |x| < 1", 34, DERIV).next_to(cen, DOWN, buff=0.45)
            self.play(Write(geo), run_time=1)
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

        # the ratio test stays boxed in the top right corner through the worked examples (Adder: formulas stay on screen)
        self.example_ref = r"\begin{aligned}&L = \lim_{n\to\infty} \left|\tfrac{a_{n+1}}{a_n}\right|\\ &L < 1\text{: converges}\\ &L > 1\text{: diverges}\end{aligned}"
        fig = interval_line(-1, 5, True, False, [-2, 6, 1], [(-1, "-1"), (2, "2"), (5, "5")])
        self.example("Finding the interval", r"Find the interval of convergence of $\displaystyle\sum_{n=1}^{\infty} \frac{(x - 2)^n}{n \cdot 3^n}$.",
                     [r"\left|\frac{a_{n+1}}{a_n}\right| = \frac{|x - 2|^{n+1}}{(n + 1)3^{n+1}} \cdot \frac{n \cdot 3^n}{|x - 2|^n}", r"= \frac{|x - 2|}{3} \cdot \frac{n}{n + 1}", r"L = \frac{|x - 2|}{3}",
                      r"L < 1: \ |x - 2| < 3, \ R = 3, \ -1 < x < 5", r"x = 5: \ \sum \frac{3^n}{n3^n} = \sum \frac1n \ \text{diverges}", r"x = -1: \ \sum \frac{(-3)^n}{n3^n} = \sum \frac{(-1)^n}{n} \ \text{converges (AST)}", r"[-1, 5)"],
                     at=[1, 1, 2, 3, 4, 5, 6], figure=fig, figure_at=6, follow=True)

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
