"""Topic 8.4: Area between curves (functions of x). Narration comes from transcripts/8_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "8.4"

    def construct(self):
        top = lambda s: 3.2 - 0.35 * (s - 2.5)**2
        bot = lambda s: 0.6 + 0.25 * np.sin(1.4 * s) + 0.1 * s
        xs = np.linspace(0, 5, 4001)
        diff = np.array([top(s) - bot(s) for s in xs])
        cross = [float(xs[i]) for i in range(len(xs) - 1) if diff[i] * diff[i + 1] < 0]
        a_, b_ = cross[0], cross[-1]

        with self.beat("Between two curves") as b:
            ax, al = plot_axes([0, 5, 1], [0, 4, 1], w=7, h=4.4, coords=False)
            VGroup(ax, al).shift(DOWN * 0.2)
            gt = ax.plot(top, x_range=[0, 5], color=FUNC, stroke_width=4)
            gb = ax.plot(bot, x_range=[0, 5], color=DERIV, stroke_width=4)
            self.play(FadeIn(ax), FadeIn(al), Create(gt), Create(gb), run_time=1.2)
            b.line(1)
            under_t = region(ax, top, lambda s: 0, a_, b_, color=AREA, opacity=0.4)
            under_b = region(ax, bot, lambda s: 0, a_, b_, color=BG, opacity=1)
            self.play(FadeIn(under_t), run_time=0.8)
            self.play(FadeIn(under_b), run_time=0.8)
            self.add(gt, gb)
            b.line(2)
            self.play(FadeIn(M(r"\int (\text{top} - \text{bottom})\,dx", 40, ACCUM).to_edge(UP, buff=0.4)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Top minus bottom") as b:
            ax, al = plot_axes([0, 5, 1], [0, 4, 1], w=6.2, h=4.2, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.4)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(top, x_range=[0, 5], color=FUNC, stroke_width=4)), Create(ax.plot(bot, x_range=[0, 5], color=DERIV, stroke_width=4)),
                      FadeIn(M("f", 32, FUNC).next_to(ax.c2p(2.5, top(2.5)), UP, buff=0.1)), FadeIn(M("g", 32, DERIV).next_to(ax.c2p(4.6, bot(4.6)), DOWN, buff=0.1)), run_time=1)
            sl = slice_rect(ax, top, bot, 2.0, 0.22, label="dx")
            h = M(r"f(x) - g(x)", 30, SECANT).next_to(sl[0], RIGHT, buff=0.1)
            self.play(FadeIn(sl), FadeIn(h), run_time=1)
            b.line(1)
            edges = np.linspace(a_, b_, 13)
            many = VGroup(*[slice_rect(ax, top, bot, (p + q) / 2, q - p) for p, q in zip(edges, edges[1:])])
            board = VGroup(M(r"\text{area} \approx \sum \big(f(x) - g(x)\big)\,\Delta x", 38), M(r"\text{area} = \int_a^b \big(f(x) - g(x)\big)\,dx", 40)).arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=0.3).shift(UP * 0.8)
            self.play(FadeOut(VGroup(sl, h)), FadeIn(many), Write(board[0]), run_time=1.2)
            self.play(Write(board[1]), run_time=1)
            b.line(2)
            self.play(FadeIn(formula_box(M(r"\int (\text{top} - \text{bottom})\,dx", 42, ACCUM), ACCUM).next_to(board, DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("Even below the axis") as b:
            t2 = lambda s: 1.0 + 0.3 * np.sin(s)
            b2 = lambda s: -2.0 + 0.4 * np.cos(1.2 * s)
            ax, al = plot_axes([0, 5, 1], [-3, 5, 1], w=6, h=4.8)
            VGroup(ax, al).to_edge(LEFT, buff=0.6)
            shift = ValueTracker(0)
            gt = always_redraw(lambda: ax.plot(lambda s: t2(s) + shift.get_value(), x_range=[0, 5], color=FUNC, stroke_width=4))
            gb = always_redraw(lambda: ax.plot(lambda s: b2(s) + shift.get_value(), x_range=[0, 5], color=DERIV, stroke_width=4))
            reg = always_redraw(lambda: region(ax, lambda s: t2(s) + shift.get_value(), lambda s: b2(s) + shift.get_value(), 0.5, 4.5, opacity=0.35))
            self.play(FadeIn(ax), FadeIn(al), FadeIn(reg), Create(gt), Create(gb), run_time=1.2)
            self.add(gt, gb)
            b.line(1)
            nums = VGroup(M(r"\text{top} = 1", 36, FUNC), M(r"\text{bottom} = -2", 36, DERIV), M(r"\text{height} = 1 - (-2) = 3", 38, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6)
            self.play(LaggedStart(*[FadeIn(n) for n in nums], lag_ratio=0.4), run_time=1.6)
            b.line(2)
            self.play(shift.animate.set_value(3), run_time=2)
            self.play(Indicate(nums[2]), run_time=0.8)
        self.clear()

        with self.beat("Finding the limits") as b:
            ax, al = plot_axes([0, 5, 1], [0, 4, 1], w=7, h=4.2, coords=False)
            VGroup(ax, al).shift(DOWN * 0.4)
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(top, x_range=[0, 5], color=FUNC, stroke_width=4)), Create(ax.plot(bot, x_range=[0, 5], color=DERIV, stroke_width=4)), run_time=1)
            marks = VGroup(*[VGroup(Dot(ax.c2p(c, top(c)), color=SECANT), DashedLine(ax.c2p(c, top(c)), ax.c2p(c, 0), color=DIM), M(n, 32, DIM).next_to(ax.c2p(c, 0), DOWN, buff=0.15))
                             for c, n in ((a_, "a"), (b_, "b"))])
            self.play(FadeIn(marks), FadeIn(M(r"\text{set } f(x) = g(x) \text{ and solve}", 38).to_edge(UP, buff=0.4)), run_time=1)
            b.line(1)
            mid = (a_ + b_) / 2
            self.play(FadeIn(Dot(ax.c2p(mid, top(mid)), color=FUNC)), FadeIn(Dot(ax.c2p(mid, bot(mid)), color=DERIV)),
                      FadeIn(T("which is on top? plug in a number", 30, SECANT).next_to(ax.c2p(mid, top(mid)), UP, buff=0.3)), run_time=1)
        self.clear()

        ax, _ = plot_axes([-1.8, 2.8, 1], [-2.5, 3, 1], w=4.6, h=4.4)
        f1, g1 = (lambda s: s), (lambda s: s**2 - 2)
        fig = VGroup(ax, region(ax, f1, g1, -1, 2, opacity=0.35), ax.plot(f1, x_range=[-1.8, 2.8], color=FUNC, stroke_width=4),
                     ax.plot(g1, x_range=[-1.8, 2.25], color=DERIV, stroke_width=4), slice_rect(ax, f1, g1, 0.6, 0.18, label="dx"),
                     M("y = x", 26, FUNC).next_to(ax.c2p(2.6, 2.6), LEFT, buff=0.15), M("y = x^2 - 2", 26, DERIV).next_to(ax.c2p(2.2, 2.84), RIGHT, buff=0.05))
        self.example("Area between a line and a parabola", r"Find the area of the region bounded by $y = x$ and $y = x^2 - 2$.",
                     [r"x^2 - 2 = x", r"x^2 - x - 2 = 0", r"(x - 2)(x + 1) = 0", r"x = -1, \ \ x = 2", r"TEXT:Test $x = 0$: line $0$, parabola $-2$, so the line is on top.",
                      r"A = \int_{-1}^{2} \big(x - (x^2 - 2)\big)\,dx", r"= \int_{-1}^{2} \left(x - x^2 + 2\right) dx", r"= \left[\tfrac{x^2}{2} - \tfrac{x^3}{3} + 2x\right]_{-1}^{2}",
                      r"= \left(2 - \tfrac83 + 4\right) - \left(\tfrac12 + \tfrac13 - 2\right)", r"= \tfrac{10}{3} - \left(-\tfrac76\right)", r"= \tfrac{27}{6} = \tfrac92"],
                     at=[1, 2, 2, 2, 3, 4, 4, 5, 6, 6, 7], figure=fig, figure_at=3,
                     notes_graph=dict(fns=[("x", -1.8, 2.8), ("x^2-2", -1.8, 2.25)], xr=(-2, 3), yr=(-2.5, 3)))

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"\text{Area} = \int_a^b (\text{top} - \text{bottom})\,dx", 46, ACCUM), ACCUM), T("limits: where the curves meet", 36), T("top: test a point", 36, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([0, 4.5, 1], [0, 2.5, 1], w=4.6, h=2.8)
        fig1 = VGroup(ax, region(ax, np.sqrt, lambda s: s / 2, 0, 4, opacity=0.35), ax.plot(np.sqrt, x_range=[0, 4.5], color=FUNC, stroke_width=4), ax.plot(lambda s: s / 2, x_range=[0, 4.5], color=DERIV, stroke_width=4))
        self.example("Example 1: Root and line", r"Find the area between $y = \sqrt x$ and $y = \frac x2$.",
                     [r"\sqrt x = \tfrac x2", r"x = \tfrac{x^2}{4}", r"x^2 - 4x = 0", r"x(x - 4) = 0: \ x = 0, \ x = 4", r"TEXT:Test $x = 1$: $\sqrt1 = 1 > \tfrac12$, so the root is on top.",
                      r"A = \int_0^4 \left(\sqrt x - \tfrac x2\right) dx", r"= \left[\tfrac23x^{3/2} - \tfrac{x^2}{4}\right]_0^4", r"= \tfrac{16}{3} - 4 = \tfrac43"], at=[1, 1, 1, 1, 2, 3, 3, 3], figure=fig1, figure_at=2)
        ax, _ = plot_axes([0, 1.6, 0.5], [0, 1.2, 0.5], w=4, h=3, coords=False)
        fig2 = VGroup(ax, region(ax, np.cos, np.sin, 0, np.pi / 4, opacity=0.35), ax.plot(np.cos, x_range=[0, 1.57], color=FUNC, stroke_width=4), ax.plot(np.sin, x_range=[0, 1.57], color=DERIV, stroke_width=4),
                      M(r"\tfrac\pi4", 26, DIM).next_to(ax.c2p(np.pi / 4, 0), DOWN, buff=0.12))
        self.example("Example 2: Sine and cosine", r"Find the area between $y = \cos x$ and $y = \sin x$ for $0 \le x \le \frac\pi4$.",
                     [r"TEXT:On $\left[0, \tfrac\pi4\right]$, $\cos x \ge \sin x$.", r"A = \int_0^{\pi/4} (\cos x - \sin x)\,dx", r"= \left[\sin x + \cos x\right]_0^{\pi/4}",
                      r"= \left(\tfrac{\sqrt2}{2} + \tfrac{\sqrt2}{2}\right) - (0 + 1)", r"= \sqrt2 - 1 \approx 0.414"], at=[1, 2, 2, 3, 3], figure=fig2)
        ax, _ = plot_axes([0, 2.5, 1], [0, 8, 2], w=3.6, h=3.6)
        fig3 = VGroup(ax, region(ax, np.exp, lambda s: 1, 0, 2, opacity=0.35), ax.plot(np.exp, x_range=[0, 2.1], color=FUNC, stroke_width=4), Line(ax.c2p(0, 1), ax.c2p(2.5, 1), color=DERIV, stroke_width=4),
                      DashedLine(ax.c2p(2, 0), ax.c2p(2, 8), color=DIM))
        self.example("Example 3: Three boundaries", r"Find the area of the region bounded by $y = e^x$, $y = 1$, and $x = 2$.",
                     [r"TEXT:$e^x = 1$ at $x = 0$; the region runs from $0$ to $2$, $e^x$ on top.", r"A = \int_0^2 \left(e^x - 1\right) dx", r"= \left[e^x - x\right]_0^2",
                      r"= \left(e^2 - 2\right) - (1 - 0)", r"= e^2 - 3 \approx 4.39"], at=[1, 2, 2, 3, 3], figure=fig3)
        self.finish()
