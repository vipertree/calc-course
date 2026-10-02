"""Topic 1.9: Connecting multiple representations of limits. Narration comes from transcripts/1_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def g(x):
    return 3 + (x - 2) ** 2


def panel(title, content, w=4.4, h=2.8):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.15, color=DIM, fill_color=PANEL, fill_opacity=1)
    content.set_max_width(w - 0.5).set_max_height(h - 0.8).move_to(r).shift(DOWN * 0.15)
    t = T(title, 30, DIM).next_to(r.get_top(), DOWN, buff=0.15)
    return VGroup(r, t, content)


class Lesson(TranscriptScene):
    NUM = "1.9"

    def four(self):
        a, _ = plot_axes([0, 4, 1], [0, 6, 1], w=3.6, h=2.2, coords=False)
        gp = VGroup(a, a.plot(lambda x: x + 1, x_range=[0, 4], color=FUNC), open_dot(a, 2, 3))
        ps = VGroup(panel("formula", M(r"f(x) = \frac{x^2 - x - 2}{x - 2}", 40)), panel("graph", gp),
                    panel("table", table(["x", "1.99", "2.01"], [["f(x)", "2.99", "3.01"]], size=36)),
                    panel("words", T(r"``as $x$ nears $2$,\\ $f(x)$ nears $3$''", 36)))
        ps.arrange_in_grid(2, 2, buff=(1.6, 0.5))
        return ps

    def construct(self):
        ps = self.four()
        q = M("?", 90, SECANT)
        with self.beat("One limit, four views") as b:
            self.play(LaggedStart(*[FadeIn(p) for p in ps], lag_ratio=0.25), FadeIn(q), run_time=2.2)
            b.line(1)
            self.play(Transform(q, M("3", 90, SECANT)), run_time=1)
        self.clear()
        self.title()

        ps = self.four()
        with self.beat("Each view has a strength") as b:
            self.play(FadeIn(ps), run_time=0.8)
            tags = ["exact answers", "the big picture", "evidence near a point", "meaning and units"]
            labs = VGroup(*[T(t_, 30, SECANT).next_to(p, DOWN, buff=0.12) for t_, p in zip(tags, ps)])
            for m in labs:
                self.play(FadeIn(m), run_time=0.6)
        self.clear()

        ax, al = plot_axes([0, 4, 1], [0, 6, 1], w=6.2, h=4.6, xlabel="x", ylabel="g(x)")
        VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        gc = ax.plot(g, x_range=[0.3, 3.7], color=DERIV, stroke_width=5)
        fdef = M(r"f(u) = \begin{cases} u + 1, & u < 3 \\ 10 - u, & u \ge 3 \end{cases}", 44, FUNC).to_edge(RIGHT, buff=0.6).shift(UP * 2)
        with self.beat("Two functions, two views") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(gc), FadeIn(open_dot(ax, 2, 3, DERIV)), Write(fdef), run_time=1.8)
            qq = M(r"\lim_{x\to2} f\big(g(x)\big) = \ ?", 48).next_to(fdef, DOWN, buff=0.6)
            self.play(Write(qq), run_time=1.2)

        xv = ValueTracker(3)
        mk = always_redraw(lambda: Dot(ax.c2p(xv.get_value(), g(xv.get_value())), color=SECANT, radius=0.1))
        rd = always_redraw(lambda: M(f"g = {g(xv.get_value()):.2f}", 40, SECANT).next_to(qq, DOWN, buff=0.5))
        with self.beat("Inside out, with direction") as b:
            self.add(mk, rd)
            self.play(xv.animate.set_value(2.5), run_time=0.9)
            self.play(xv.animate.set_value(2.3), run_time=0.8)
            self.play(xv.animate.set_value(2.1), run_time=0.8)
            b.line(1)
            above = T("always above 3", 34, SECANT).next_to(rd, DOWN, buff=0.3)
            self.play(FadeIn(above), run_time=0.6)
            b.line(2)
            r7 = M(r"\lim_{u\to3^+}(10 - u) = 7", 44, FUNC).next_to(above, DOWN, buff=0.4)
            self.play(Write(r7), run_time=1.2)
            b.line(3)
            self.play(Indicate(fdef, color=DIM), run_time=1)
        self.clear()

        with self.beat("Why the direction matters") as b:
            l = VGroup(T(r"$g \to 3$ from above", 40, SECANT), M(r"f \to 10 - 3 = 7", 48, FUNC)).arrange(DOWN, buff=0.4)
            r = VGroup(T(r"$g \to 3$ from below", 40, TANGENT), M(r"f \to 3 + 1 = 4", 48, FUNC)).arrange(DOWN, buff=0.4)
            VGroup(l, r).arrange(RIGHT, buff=2.4)
            self.play(FadeIn(l), run_time=0.9)
            self.play(FadeIn(r), run_time=0.9)
        self.clear()

        with self.beat("Checking with a table") as b:
            tb = table(["x", "g(x)", r"f(g(x))"], [["2.5", "3.25", "6.75"], ["2.3", "3.09", "6.91"], ["2.1", "3.01", "6.99"]], size=44)
            self.play(FadeIn(tb), run_time=1.2)
            self.play(*[Indicate(tb.cells[r][2], color=SECANT) for r in (1, 2, 3)], run_time=1)
        self.clear()
        ktab = table(["x", "0.9", "0.99", "1.01", "1.1"], [["k(x)", "1.8", "1.98", "2.02", "2.2"]], size=38)
        self.example("Table meets formula", r"Values of $k$ near $x = 1$ are in the table. Assuming the pattern continues, find $\displaystyle\lim_{x\to1}\left[3k(x) - x^2\right]$.",
                     [r"\lim_{x\to1} k(x) = 2 \ \ (\text{from the table})", r"\lim_{x\to1}\left[3k(x) - x^2\right] = 3(2) - 1^2 = 5"], at=[1, 2], figure=ktab, text=r"Values of $k$ near $x = 1$ are shown. \par\smallskip\centerline{\begin{tabular}{c|cccc} $x$ & 0.9 & 0.99 & 1.01 & 1.1 \\ \hline $k(x)$ & 1.8 & 1.98 & 2.02 & 2.2\end{tabular}} \par Assuming the pattern continues, find \[ \lim_{x\to1}\left[3k(x) - x^2\right]. \]")

        with self.beat("Close") as b:
            ps = self.four()
            seven = M("7", 90, SECANT)
            self.play(FadeIn(ps), FadeIn(seven), run_time=1.2)
            self.play(*[Create(Line(p.get_center(), seven.get_center(), color=DIM, buff=1.2)) for p in ps], run_time=1)
        self.clear()

        self.examples_card()
        a1, _ = plot_axes([0, 2, 1], [0, 3, 1], w=4.2, h=3.4)
        fig1 = VGroup(a1, a1.plot(lambda x: 2 + 0.6 * (x - 1), x_range=[0, 2], color=FUNC), open_dot(a1, 1, 2))
        tg = table(["x", "0.9", "0.99", "1.01", "1.1"], [["g(x)", "-2.8", "-2.98", "-3.02", "-3.2"]], size=30)
        head = VGroup(T(r"$f$ is graphed; $g$ is a table. Find $\displaystyle\lim_{x\to1}(f + g)$ and $\displaystyle\lim_{x\to1} fg$.", 36), tg).arrange(DOWN, buff=0.3)
        self.example("Example 1: A graph and a table together", head,
                     [r"\lim_{x\to1} f(x) = 2", r"\lim_{x\to1} g(x) = -3", r"\lim_{x\to1}(f + g) = 2 + (-3) = -1", r"\lim_{x\to1} fg = 2(-3) = -6"],
                     figure=fig1, at=[1, 2, 3, 4],
                     text=r"$f$ is graphed and $g$ is given by the table. Find $\displaystyle\lim_{x\to1}(f + g)$ and $\displaystyle\lim_{x\to1} f(x)g(x)$. \[ \begin{array}{c|cccc} x & 0.9 & 0.99 & 1.01 & 1.1 \\ \hline g(x) & -2.8 & -2.98 & -3.02 & -3.2 \end{array} \]",
                     notes_graph=dict(fns=[("2+0.6*(x-1)", 0, 2)], xr=(0, 2), yr=(0, 3), open=[(1, 2)], ylabel="f(x)"))
        a2, _ = plot_axes([1, 5, 1], [0, 7, 1], w=4.6, h=3.8)
        fig2 = VGroup(a2, a2.plot(lambda u: 5 + 0.8 * np.sin(u - 3), x_range=[1, 5], color=FUNC), closed_dot(a2, 3, 5))
        self.example("Example 2: A composite with no direction trap", r"$g(x) = x^2 - 1$ and $f$ is graphed. Find $\displaystyle\lim_{x\to2} f\big(g(x)\big)$.",
                     [r"\lim_{x\to2} g(x) = 4 - 1 = 3", r"f \text{ is unbroken at } 3:\ f \to 5", r"\lim_{x\to2} f\big(g(x)\big) = 5"], figure=fig2, at=[1, 2, 3],
                     notes_graph=dict(fns=[("5+0.8*sin(deg(x-3))", 1, 5)], xr=(1, 5), yr=(0, 7), closed=[(3, 5)], ylabel="f(x)"))
        self.example("Example 3: From words to a limit", r"``As $n$ approaches $500$, the cost per item $C(n)$ approaches 12 dollars.'' Write this as a limit, then find $\displaystyle\lim_{n\to500}\big(3C(n) + 2\big)$.",
                     [r"\lim_{n\to500} C(n) = 12", r"\lim_{n\to500}\big(3C(n) + 2\big) = 3(12) + 2", r"= 38\ \text{dollars}"], at=[1, 2, 3])
        self.finish()
