"""Topic 8.1: Average value of a function. Narration comes from transcripts/8_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.1"

    def construct(self):
        with self.beat("Averaging infinitely many numbers") as b:
            ax, al = plot_axes([0, 24, 6], [40, 80, 10], w=6.4, h=3.6, xlabel="t", ylabel="T")
            VGroup(ax, al).to_edge(RIGHT, buff=0.6).shift(UP * 0.5)
            curve = ax.plot(lambda s: 60 + 12 * np.sin(np.pi * (s - 9) / 12), x_range=[0, 24], color=FUNC, stroke_width=4)
            bulb = VGroup(RoundedRectangle(width=0.36, height=3.0, corner_radius=0.18, stroke_color=INK, stroke_width=3),
                          Circle(radius=0.36, stroke_color=INK, stroke_width=3, fill_color=TANGENT, fill_opacity=1).shift(DOWN * 1.6),
                          Rectangle(width=0.16, height=1.9, stroke_width=0, fill_color=TANGENT, fill_opacity=1).shift(DOWN * 0.55)).to_edge(LEFT, buff=1.4)
            self.play(FadeIn(bulb), FadeIn(ax), FadeIn(al), Create(curve), run_time=1.4)
            pts = [3, 8, 13, 18, 22]
            dots = VGroup(*[Dot(ax.c2p(s, 60 + 12 * np.sin(np.pi * (s - 9) / 12)), color=SECANT, radius=0.08) for s in pts])
            avg5 = M(r"\text{average} = \frac{\text{sum}}{5}", 40, SECANT).next_to(ax, DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(d, scale=1.6) for d in dots], lag_ratio=0.2), Write(avg5), run_time=1.4)
            b.line(1)
            q = T("What about every instant of the day?", 38, INK).next_to(avg5, DOWN, buff=0.35)
            self.play(FadeIn(q), FadeOut(dots), run_time=0.8)
            b.line(2)
        self.clear()
        self.title()

        f = lambda s: 1.2 + 0.5 * np.sin(1.3 * s) + 0.25 * s
        with self.beat("From a list to an integral") as b:
            ax, al = plot_axes([0, 5, 1], [0, 3, 1], w=5.6, h=3.4, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.5).shift(UP * 0.6)
            a_, b_ = 0.5, 4.5
            curve = ax.plot(f, x_range=[0.2, 4.8], color=FUNC, stroke_width=4)
            labs = VGroup(M("a", 30, DIM).next_to(ax.c2p(a_, 0), DOWN, buff=0.15), M("b", 30, DIM).next_to(ax.c2p(b_, 0), DOWN, buff=0.15))
            edges = np.linspace(a_, b_, 7)
            mids = (edges[:-1] + edges[1:]) / 2
            ticks = VGroup(*[DashedLine(ax.c2p(e, 0), ax.c2p(e, f(e)), color=DIM, stroke_width=2) for e in edges])
            samples = VGroup(*[Dot(ax.c2p(m, f(m)), color=SECANT, radius=0.07) for m in mids])
            self.play(FadeIn(ax), FadeIn(labs), Create(curve), run_time=1)
            self.play(Create(ticks), FadeIn(samples), FadeIn(nudge_arrow(ax.c2p(edges[0], 0), ax.c2p(edges[1], 0), label=r"\Delta x").shift(DOWN * 0.45)), run_time=1)
            rows = [r"\text{average} \approx \frac{f(x_1) + \cdots + f(x_n)}{n}", r"n = \frac{b - a}{\Delta x}",
                    r"\text{average} \approx \frac{1}{b - a}\sum f(x_k)\,\Delta x", r"f_{\text{avg}} = \frac{1}{b - a}\int_a^b f(x)\,dx"]
            board = VGroup(*[M(r, 38) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
            self.play(Write(board[0]), run_time=1)
            b.line(1)
            self.play(Write(board[1]), run_time=0.8)
            b.line(2)
            self.play(Write(board[2]), run_time=1)
            b.line(3)
            self.play(Transform(samples, riemann_boxes(ax, f, list(edges), kind="mid")), run_time=1)
            self.play(Write(board[3]), run_time=1)
            box = formula_box(VGroup(M(r"f_{\text{avg}} = \frac{1}{b - a}\int_a^b f(x)\,dx", 42, ACCUM),
                                     T("total accumulated, divided by the length of the interval", 28)).arrange(DOWN, buff=0.2), ACCUM).to_edge(DOWN, buff=0.5)
            b.line(4)
            self.play(FadeIn(box), run_time=1)
        self.clear()

        with self.beat("Leveling the area") as b:
            ax, al = plot_axes([0, 5, 1], [0, 3, 1], w=7, h=4, coords=False)
            VGroup(ax, al).shift(UP * 0.4)
            a_, b_ = 0.5, 4.5
            avg = float(np.mean([f(s) for s in np.linspace(a_, b_, 2001)]))
            curve = ax.plot(f, x_range=[0.2, 4.8], color=FUNC, stroke_width=4)
            shade = region(ax, f, lambda s: 0, a_, b_)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(shade), run_time=1.2)
            b.line(1)
            rect = Polygon(ax.c2p(a_, 0), ax.c2p(b_, 0), ax.c2p(b_, avg), ax.c2p(a_, avg), stroke_width=0, fill_color=WATER, fill_opacity=0.55)
            line = DashedLine(ax.c2p(0, avg), ax.c2p(5, avg), color=SECANT, stroke_width=3)
            self.play(Transform(shade, rect), Create(line), run_time=2)
            tags = VGroup(M(r"\text{height } f_{\text{avg}}", 30, SECANT).next_to(ax.c2p(5, avg), RIGHT, buff=0.1),
                          M(r"\text{width } b - a", 30, DIM).next_to(ax.c2p((a_ + b_) / 2, 0), DOWN, buff=0.25),
                          T("same area", 30, INK).move_to(ax.c2p((a_ + b_) / 2, avg / 2)))
            self.play(FadeIn(tags), run_time=0.8)
            b.line(2)
            xs = np.linspace(a_, b_, 4001)
            c = float(xs[np.argmin([abs(f(s) - avg) for s in xs])])
            dot = Dot(ax.c2p(a_, f(a_)), color=TANGENT, radius=0.1)
            self.play(FadeIn(dot), run_time=0.4)
            self.play(MoveAlongPath(dot, ax.plot(f, x_range=[a_, c], color=FUNC)), run_time=1.4)
            self.play(FadeIn(M(r"f(c) = f_{\text{avg}}", 32, TANGENT).next_to(dot, UL, buff=0.1)), run_time=0.6)
        self.clear()

        g = lambda s: s**2
        ax, _ = plot_axes([0, 4.5, 1], [0, 17, 4], w=4.4, h=3.8)
        fig = VGroup(ax, ax.plot(g, x_range=[0, 4.1], color=FUNC, stroke_width=4), region(ax, g, lambda s: 0, 1, 4, opacity=0.3),
                     DashedLine(ax.c2p(0, 7), ax.c2p(4.4, 7), color=SECANT, stroke_width=3), Dot(ax.c2p(np.sqrt(7), 7), color=TANGENT, radius=0.09),
                     M(r"(\sqrt7,\ 7)", 26, TANGENT).next_to(ax.c2p(np.sqrt(7), 7), UL, buff=0.08))
        self.example("Average value of x squared", r"Find the average value of $f(x) = x^2$ on $[1, 4]$. Then find where $f$ equals its average value.",
                     [r"f_{\text{avg}} = \frac{1}{4 - 1}\int_1^4 x^2\,dx", r"= \frac13\left[\frac{x^3}{3}\right]_1^4", r"= \frac13\left(\frac{64}{3} - \frac13\right)", r"= \frac13 \cdot 21",
                      r"= 7", r"x^2 = 7", r"x = \pm\sqrt7", r"TEXT:$\sqrt7 \approx 2.65$ is in $[1, 4]$; $-\sqrt7$ is not."],
                     at=[1, 2, 2, 2, 3, 4, 4, 5], figure=fig, figure_at=4,
                     notes_graph=dict(fns=[("x^2", 0, 4.1)], xr=(0, 4.5), yr=(0, 17), ystep=4), follow=True)

        with self.beat("Average value is not average rate of change") as b:
            def panel(kind):
                ax, _ = plot_axes([0, 4.5, 1], [0, 17, 4], w=4.6, h=3.4)
                grp = VGroup(ax, ax.plot(g, x_range=[0, 4.1], color=FUNC, stroke_width=4))
                if kind == "rate":
                    grp.add(Line(ax.c2p(1, 1), ax.c2p(4, 16), color=SECANT, stroke_width=4), Dot(ax.c2p(1, 1), color=SECANT), Dot(ax.c2p(4, 16), color=SECANT))
                    cap = VGroup(T("average rate of change", 32, SECANT), M(r"\text{a slope: } \frac{16 - 1}{4 - 1} = 5", 34))
                else:
                    grp.add(region(ax, g, lambda s: 0, 1, 4, opacity=0.3), DashedLine(ax.c2p(1, 7), ax.c2p(4, 7), color=ACCUM, stroke_width=4))
                    cap = VGroup(T("average value", 32, ACCUM), M(r"\text{a height: } \frac13\int_1^4 x^2\,dx = 7", 34))
                return VGroup(grp, cap.arrange(DOWN, buff=0.15).next_to(grp, DOWN, buff=0.3))
            left, right = panel("rate"), panel("value")
            VGroup(left, right).arrange(RIGHT, buff=0.9).move_to(UP * 0.2)
            self.play(FadeIn(left), run_time=1)
            b.line(1)
            self.play(FadeIn(right), run_time=1)
            b.line(2)
            note = M(r"\frac{1}{b - a}\int_a^b f'(x)\,dx = \frac{f(b) - f(a)}{b - a}", 36, DERIV).to_edge(DOWN, buff=0.3)
            self.play(FadeOut(VGroup(left[1], right[1])), Write(note), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"f_{\text{avg}} = \frac{1}{b - a}\int_a^b f(x)\,dx", 48, ACCUM), ACCUM),
                          T("the height of the rectangle with the same area", 36),
                          T("continuous $f$ reaches its average at some $c$", 36, TANGENT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([0, 6.5, 1], [0, 3, 1], w=5, h=2.8)
        fig1 = VGroup(ax, Line(ax.c2p(0, 2), ax.c2p(2, 2), color=FUNC, stroke_width=4),
                      ax.plot(lambda s: np.sqrt(max(4 - (s - 4)**2, 0)), x_range=[2, 6, 0.01], color=FUNC, stroke_width=4))
        self.example("Example 1: From a graph", r"The graph of $f$ on $[0, 6]$ is a segment at height $2$, then a semicircle of radius $2$. Find the average value of $f$ on $[0, 6]$.",
                     [r"\int_0^6 f(x)\,dx = 2 \cdot 2 + \tfrac12\pi(2)^2", r"= 4 + 2\pi", r"f_{\text{avg}} = \frac{4 + 2\pi}{6}", r"= \frac{2 + \pi}{3} \approx 1.71"],
                     at=[1, 1, 2, 3], figure=fig1,
                     notes_graph=dict(fns=[("2+0*x", 0, 2), ("sqrt(abs(4-(x-4)^2))", 2, 6)], xr=(0, 6.5), yr=(0, 3)))
        ax, _ = plot_axes([0, 3.5, 1], [0, 1.2, 0.5], w=4.6, h=2.6, coords=False)
        fig2 = VGroup(ax, ax.plot(np.sin, x_range=[0, np.pi], color=FUNC, stroke_width=4), region(ax, np.sin, lambda s: 0, 0, np.pi, opacity=0.25),
                      DashedLine(ax.c2p(0, 2 / np.pi), ax.c2p(np.pi, 2 / np.pi), color=SECANT, stroke_width=3), M(r"\tfrac{2}{\pi}", 28, SECANT).next_to(ax.c2p(0, 2 / np.pi), LEFT, buff=0.1))
        self.example("Example 2: Average of sine", r"Find the average value of $\sin x$ on $[0, \pi]$.",
                     [r"f_{\text{avg}} = \frac1\pi\int_0^\pi \sin x\,dx", r"= \frac1\pi\left[-\cos x\right]_0^\pi", r"= \frac1\pi(1 + 1)", r"= \frac2\pi \approx 0.637"],
                     at=[1, 2, 2, 3], figure=fig2, figure_at=3)
        tab = table(["t", "0", "2", "4", "6", "8"], [["T(t)", "60", "64", "70", "68", "62"]], size=34)
        self.example("Example 3: Average temperature from a table", VGroup(T(r"Use a trapezoidal sum with four subintervals to approximate the average temperature over $0 \le t \le 8$.", 38), tab).arrange(DOWN, buff=0.3),
                     [r"\int_0^8 T\,dt \approx 2\cdot\tfrac{60 + 64}{2} + 2\cdot\tfrac{64 + 70}{2} + 2\cdot\tfrac{70 + 68}{2} + 2\cdot\tfrac{68 + 62}{2}", r"= 124 + 134 + 138 + 130", r"= 526",
                      r"\text{average} \approx \frac{526}{8} = 65.75\ ^\circ\text{F}"], at=[1, 2, 2, 3],
                     text=r"A table gives $T(t)$ in $^\circ$F at $t = 0, 2, 4, 6, 8$ hours: $60, 64, 70, 68, 62$. Use a trapezoidal sum with four subintervals to approximate the average temperature over $0 \le t \le 8$.")
        self.finish()
