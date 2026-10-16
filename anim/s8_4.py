"""Topic 8.4: Area between curves (functions of x). Narration comes from transcripts/8_4.md.

Adder's notes (2026-10-14): the cold open shows the areas (the whole area under the top, then the smaller area under the
bottom cut out) and, in the same scene, the other view: slivers whose height is top minus bottom. Below the axis, little
lines at x = 2 show top = 1 and bottom = -2. Every bounded-region example starts with a sketch, thought through aloud
(y = x is a line; y = x^2 - 2 is the parabola shifted down 2), then which is on top, then the intersections, labeled on
the sketch once found. Slivers are lines, not rectangles with dx.
"""
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
            ax, al = plot_axes([0, 5, 1], [0, 4, 1], w=7, h=4.2, coords=False)
            VGroup(ax, al).shift(DOWN * 0.7)
            gt = ax.plot(top, x_range=[0, 5], color=FUNC, stroke_width=4)
            gb = ax.plot(bot, x_range=[0, 5], color=DERIV, stroke_width=4)
            labs = VGroup(M("f", 34, FUNC).next_to(ax.c2p(0.35, top(0.35)), UL, buff=0.08), M("g", 34, DERIV).next_to(ax.c2p(4.85, bot(4.85)), DOWN, buff=0.12))
            self.play(FadeIn(ax), FadeIn(al), Create(gt), Create(gb), FadeIn(labs), run_time=1.2)
            b.line(1)
            under_t = region(ax, top, lambda s: 0, a_, b_, color=AREA, opacity=0.45)
            e1 = M(r"\int_a^b f(x)\,dx", 40, AREA).to_edge(UP, buff=0.4).shift(LEFT * 2.6)
            self.play(FadeIn(under_t), Write(e1), run_time=1)
            self.add(gt, gb)
            b.line(2)
            under_b = region(ax, bot, lambda s: 0, a_, b_, color=TANGENT, opacity=0.75)
            e2 = M(r"-\int_a^b g(x)\,dx", 40, TANGENT).next_to(e1, RIGHT, buff=0.3)
            self.play(FadeIn(under_b), Write(e2), run_time=1)
            self.add(gt, gb)
            # cut it out: the region under g slides away, and what stays behind is the region between the curves
            between = region(ax, top, bot, a_, b_, color=AREA, opacity=0.45)
            self.remove(under_t)
            self.add(between, under_b, gt, gb)
            self.play(under_b.animate.shift(DOWN * 1.2).set_opacity(0), run_time=1.6)
            self.remove(under_b)
            b.line(3)
            self.play(between.animate.set_fill(opacity=0.15), run_time=0.5)
            lines = VGroup(*[sliver(ax, top, bot, x0, width=3) for x0 in np.linspace(a_ + 0.08, b_ - 0.08, 26)])
            self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.08), run_time=2)
            one = sliver(ax, top, bot, 2.0, width=7, color=TANGENT)
            hl = T("height: top $-$ bottom", 30, TANGENT).move_to(ax.c2p(2.0, 3.75))
            self.play(Create(one), FadeIn(hl), run_time=0.8)
            b.line(4)
            e3 = formula_box(M(r"\int_a^b (\text{top} - \text{bottom})\,dx", 40, ACCUM), ACCUM).to_edge(UP, buff=0.3).shift(RIGHT * 3.4)
            self.play(FadeIn(e3), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Top minus bottom") as b:
            ax, al = plot_axes([0, 5, 1], [0, 4, 1], w=6.2, h=4.2, coords=False)
            VGroup(ax, al).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
            labs = VGroup(M("a", 30, DIM).next_to(ax.c2p(a_, 0), DOWN, buff=0.12), M("b", 30, DIM).next_to(ax.c2p(b_, 0), DOWN, buff=0.12))
            self.play(FadeIn(ax), FadeIn(al), FadeIn(labs), Create(ax.plot(top, x_range=[0, 5], color=FUNC, stroke_width=4)), Create(ax.plot(bot, x_range=[0, 5], color=DERIV, stroke_width=4)),
                      FadeIn(M("f", 32, FUNC).next_to(ax.c2p(0.35, top(0.35)), UL, buff=0.08)), FadeIn(M("g", 32, DERIV).next_to(ax.c2p(4.85, bot(4.85)), DOWN, buff=0.12)), run_time=1)
            one = sliver(ax, top, bot, 2.0, width=7)
            h = M(r"\text{height: } f(x) - g(x)", 30, SECANT).move_to(ax.c2p(2.0, 3.72))
            xl = M("x", 28, SECANT).next_to(ax.c2p(2.0, 0), DOWN, buff=0.12)
            self.play(Create(one), FadeIn(h), FadeIn(xl), run_time=1)
            b.line(1)
            many = VGroup(*[sliver(ax, top, bot, x0, width=3) for x0 in np.linspace(a_ + 0.08, b_ - 0.08, 22)])
            board = M(r"\text{area} = \int_a^b \big(f(x) - g(x)\big)\,dx", 40).to_edge(RIGHT, buff=0.3).shift(UP * 0.8)
            self.play(LaggedStart(*[Create(l) for l in many], lag_ratio=0.08), run_time=1.6)
            self.play(FadeIn(region(ax, top, bot, a_, b_, opacity=0.3)), Write(board), run_time=1)
            b.line(2)
            self.play(FadeIn(formula_box(M(r"\int (\text{top} - \text{bottom})\,dx", 42, ACCUM), ACCUM).next_to(board, DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("Even below the axis") as b:
            t2 = lambda s: 1.0 + 0.35 * np.sin(1.3 * (s - 2))
            b2 = lambda s: -2.0 + 0.45 * (1 - np.cos(1.1 * (s - 2)))
            ax, al = plot_axes([0, 5, 1], [-3, 5, 1], w=5.6, h=4.8)
            VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
            shift = ValueTracker(0)
            up_ = lambda: shift.get_value()
            gt = always_redraw(lambda: ax.plot(lambda s: t2(s) + up_(), x_range=[0, 5], color=FUNC, stroke_width=4))
            gb = always_redraw(lambda: ax.plot(lambda s: b2(s) + up_(), x_range=[0, 5], color=DERIV, stroke_width=4))
            reg = always_redraw(lambda: region(ax, lambda s: t2(s) + up_(), lambda s: b2(s) + up_(), 0.5, 4.5, opacity=0.3))
            self.play(FadeIn(ax), FadeIn(al), FadeIn(reg), Create(gt), Create(gb), run_time=1.2)
            self.add(gt, gb)
            b.line(1)
            col = 2.0
            at = M(r"\text{at } x = 2:", 36, DIM).move_to([col, 2.4, 0], aligned_edge=LEFT)
            l_top = Line(ax.c2p(2, 0), ax.c2p(2, 1), color=FUNC, stroke_width=7)
            l_bot = Line(ax.c2p(2, 0), ax.c2p(2, -2), color=DERIV, stroke_width=7)
            d_top, d_bot = Dot(ax.c2p(2, 1), color=FUNC, radius=0.07), Dot(ax.c2p(2, -2), color=DERIV, radius=0.07)
            n1 = M(r"\text{top} = 1", 36, FUNC).next_to(at, DOWN, buff=0.4, aligned_edge=LEFT)
            n2 = M(r"\text{bottom} = -2", 36, DERIV).next_to(n1, DOWN, buff=0.35, aligned_edge=LEFT)
            self.play(FadeIn(at), run_time=0.4)
            self.play(Create(l_top), FadeIn(d_top), FadeIn(n1), run_time=0.9)
            self.play(Create(l_bot), FadeIn(d_bot), FadeIn(n2), run_time=0.9)
            b.line(2)
            sl = always_redraw(lambda: Line(ax.c2p(2, -2 + up_()), ax.c2p(2, 1 + up_()), color=SECANT, stroke_width=7))
            n3 = M(r"\text{height} = 1 - (-2) = 3", 38, SECANT).next_to(n2, DOWN, buff=0.45, aligned_edge=LEFT)
            self.play(FadeIn(sl), FadeOut(l_top), FadeOut(l_bot), FadeOut(d_top), FadeOut(d_bot), FadeIn(n3), run_time=1)
            b.line(3)
            self.play(FadeOut(VGroup(at, n1, n2)), n3.animate.become(M(r"\text{height} = 3", 38, SECANT).move_to(n3, aligned_edge=LEFT)), run_time=0.6)
            self.play(shift.animate.set_value(3), run_time=2)
            self.play(Indicate(n3), run_time=0.8)
        self.clear()

        with self.beat("Sketch first") as b:
            ax, al = plot_axes([0, 5, 1], [0, 4, 1], w=6.2, h=4, coords=False)
            VGroup(ax, al).to_edge(RIGHT, buff=0.5).shift(DOWN * 0.3)
            self.play(FadeIn(ax), FadeIn(al), run_time=0.6)
            pen1, pen2 = ax.plot(top, x_range=[0, 5], color=FUNC, stroke_width=4), ax.plot(bot, x_range=[0, 5], color=DERIV, stroke_width=4)
            self.play(Create(pen1), run_time=1.2)
            self.play(Create(pen2), run_time=1.2)
            steps = VGroup(T("1. sketch: which is on top?", 34), T("2. set $f(x) = g(x)$ and solve", 34), T("3. label the intersection points", 34)).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            steps.to_edge(LEFT, buff=0.6).shift(UP * 0.6)
            self.play(FadeIn(steps[0]), FadeIn(region(ax, top, bot, a_, b_, opacity=0.3)), run_time=0.8)
            b.line(1)
            self.play(FadeIn(steps[1]), run_time=0.8)
            b.line(2)
            marks = VGroup(*[VGroup(Dot(ax.c2p(c, top(c)), color=SECANT), DashedLine(ax.c2p(c, top(c)), ax.c2p(c, 0), color=DIM), M(n, 32, DIM).next_to(ax.c2p(c, 0), DOWN, buff=0.15))
                             for c, n in ((a_, "a"), (b_, "b"))])
            self.play(FadeIn(steps[2]), FadeIn(marks), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- the lesson example: sketch, then solve
        ax, _ = plot_axes([-2, 3, 1], [-2.5, 3, 1], w=4.6, h=4.6)
        f1, g1 = (lambda s: s), (lambda s: s**2 - 2)
        line = VGroup(ax.plot(f1, x_range=[-2, 2.8], color=FUNC, stroke_width=4), M("y = x", 26, FUNC).move_to(ax.c2p(1.0, 2.55)))
        ghost = ax.plot(lambda s: s**2, x_range=[-1.7, 1.7], color=DIM, stroke_width=3)
        para = VGroup(ax.plot(g1, x_range=[-2, 2.2], color=DERIV, stroke_width=4), M("y = x^2 - 2", 26, DERIV).move_to(ax.c2p(-1.25, 2.1)))
        shade = region(ax, f1, g1, -1, 2, opacity=0.3)
        pts = VGroup(point_label(ax, -1, -1, "(-1, -1)", (-1.0, -2.25)), point_label(ax, 2, 2, "(2, 2)", (2.55, 1.55)))
        sl = sliver(ax, f1, g1, 0.6)

        def sketch_parabola(sc):
            sc.play(Create(ghost), run_time=0.8)
            sc.play(ghost.animate.shift(ax.c2p(0, -2) - ax.c2p(0, 0)), run_time=1.2)
            sc.play(FadeIn(para), FadeOut(ghost), run_time=0.6)

        self.example("Area between a line and a parabola", r"Find the area of the region bounded by $y = x$ and $y = x^2 - 2$.",
                     [r"TEXT:$y = x$: a line through the origin, slope $1$", r"TEXT:$y = x^2 - 2$: the parabola $y = x^2$, shifted down $2$", r"TEXT:The line is on top.",
                      r"x^2 - 2 = x", r"x^2 - x - 2 = 0", r"(x - 2)(x + 1) = 0", r"x = -1, \ \ x = 2", r"TEXT:Intersections: $(-1, -1)$ and $(2, 2)$",
                      r"TEXT:Check $x = 0$: line $0$, parabola $-2$.", r"TEXT:Sliver height: top $-$ bottom $= x - (x^2 - 2)$",
                      r"A = \int_{-1}^{2} \big(x - (x^2 - 2)\big)\,dx", r"= \int_{-1}^{2} \left(x - x^2 + 2\right) dx", r"= \left[\tfrac{x^2}{2} - \tfrac{x^3}{3} + 2x\right]_{-1}^{2}",
                      r"= \left(2 - \tfrac83 + 4\right) - \left(\tfrac12 + \tfrac13 - 2\right)", r"= \tfrac{10}{3} - \left(-\tfrac76\right)", r"= \tfrac{27}{6} = \tfrac92"],
                     at=[1, 2, 3, 4, 5, 5, 5, 6, 7, 8, 8, 8, 9, 10, 10, 11], figure=VGroup(ax), figure_at=1, size=42,
                     cues={0: draw_cue(line), 1: sketch_parabola, 2: draw_cue(shade), 7: draw_cue(pts), 9: draw_cue(sl)}, overlays=(line, ghost, para, shade, pts, sl),
                     notes_graph=dict(fns=[("x", -2, 2.8), ("x^2-2", -2, 2.2)], xr=(-2, 3), yr=(-2.5, 3)), follow=True)

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"\text{Area} = \int_a^b (\text{top} - \text{bottom})\,dx", 46, ACCUM), ACCUM), T("sketch first: which is on top?", 36),
                          T("limits: where the curves meet", 36), T("label the intersection points", 36, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        # Example 1: root and line
        ax, _ = plot_axes([0, 5, 1], [0, 2.5, 1], w=5, h=2.8)
        r1 = VGroup(ax.plot(np.sqrt, x_range=[0, 5], color=FUNC, stroke_width=4), M(r"y = \sqrt x", 26, FUNC).move_to(ax.c2p(0.9, 1.75)))
        l1 = VGroup(ax.plot(lambda s: s / 2, x_range=[0, 5], color=DERIV, stroke_width=4), M(r"y = \tfrac x2", 26, DERIV).move_to(ax.c2p(3.4, 0.95)))
        sh1 = region(ax, np.sqrt, lambda s: s / 2, 0, 4, opacity=0.3)
        p1 = VGroup(point_label(ax, 0, 0, "(0, 0)", (-0.55, 0.35)), point_label(ax, 4, 2, "(4, 2)", (4.45, 1.55)))
        s1 = sliver(ax, np.sqrt, lambda s: s / 2, 1.5)
        self.example("Example 1: Root and line", r"Find the area between $y = \sqrt x$ and $y = \frac x2$.",
                     [r"TEXT:$y = \sqrt x$: the top half of a sideways parabola, from the origin", r"TEXT:$y = \tfrac x2$: a line through the origin, slope $\tfrac12$",
                      r"TEXT:The root is on top, then they cross.", r"\sqrt x = \tfrac x2", r"x = \tfrac{x^2}{4}", r"x^2 - 4x = 0", r"x(x - 4) = 0, \text{ so } x = 0, \ x = 4",
                      r"TEXT:Intersections: $(0, 0)$ and $(4, 2)$", r"TEXT:Sliver height: $\sqrt x - \tfrac x2$",
                      r"A = \int_0^4 \left(\sqrt x - \tfrac x2\right) dx", r"= \left[\tfrac23x^{3/2} - \tfrac{x^2}{4}\right]_0^4", r"= \tfrac{16}{3} - 4 = \tfrac43"],
                     at=[1, 2, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5], figure=VGroup(ax), figure_at=1, size=42,
                     cues={0: draw_cue(r1), 1: draw_cue(l1), 2: draw_cue(sh1), 7: draw_cue(p1), 8: draw_cue(s1)}, overlays=(r1, l1, sh1, p1, s1),
                     notes_graph=dict(fns=[("sqrt(x)", 0, 5), ("x/2", 0, 5)], xr=(0, 5), yr=(0, 2.5)))
        # Example 2: sine and cosine
        ax, _ = plot_axes([0, 1.7, 0.5], [0, 1.3, 0.5], w=4.2, h=3.2, coords=False)
        q = np.pi / 4
        c2 = VGroup(ax.plot(np.cos, x_range=[0, 1.6], color=FUNC, stroke_width=4), M(r"y = \cos x", 26, FUNC).move_to(ax.c2p(0.4, 1.19)))
        s2c = VGroup(ax.plot(np.sin, x_range=[0, 1.6], color=DERIV, stroke_width=4), M(r"y = \sin x", 26, DERIV).move_to(ax.c2p(1.38, 0.62)))
        ticks = VGroup(M(r"\tfrac\pi4", 26, DIM).next_to(ax.c2p(q, 0), DOWN, buff=0.12), M("1", 24, DIM).next_to(ax.c2p(0, 1), LEFT, buff=0.1))
        p2 = point_label(ax, q, np.sqrt(2) / 2, r"\left(\tfrac\pi4, \tfrac{\sqrt2}{2}\right)", (1.25, 0.86))
        sh2 = VGroup(region(ax, np.cos, np.sin, 0, q, opacity=0.3), sliver(ax, np.cos, np.sin, 0.35))
        self.example("Example 2: Sine and cosine", r"Find the area between $y = \cos x$ and $y = \sin x$ for $0 \le x \le \frac\pi4$.",
                     [r"TEXT:$y = \cos x$ starts at $1$ and falls; $y = \sin x$ starts at $0$ and rises.", r"TEXT:They meet at $x = \tfrac\pi4$: $\left(\tfrac\pi4, \tfrac{\sqrt2}{2}\right)$",
                      r"TEXT:$\cos x$ is on top.", r"A = \int_0^{\pi/4} (\cos x - \sin x)\,dx", r"= \left[\sin x + \cos x\right]_0^{\pi/4}",
                      r"= \left(\tfrac{\sqrt2}{2} + \tfrac{\sqrt2}{2}\right) - (0 + 1)", r"= \sqrt2 - 1 \approx 0.414"],
                     at=[1, 2, 2, 3, 3, 4, 4], figure=VGroup(ax, ticks), figure_at=1,
                     cues={0: draw_cue(c2, s2c, rt=1.4), 1: draw_cue(p2), 2: draw_cue(sh2)}, overlays=(c2, s2c, p2, sh2))
        # Example 3: three boundaries
        ax, _ = plot_axes([0, 2.5, 1], [0, 8, 2], w=3.8, h=3.6)
        e3 = VGroup(ax.plot(np.exp, x_range=[0, 2.08], color=FUNC, stroke_width=4), M(r"y = e^x", 26, FUNC).move_to(ax.c2p(1.0, 6.4)))
        h3 = VGroup(Line(ax.c2p(0, 1), ax.c2p(2.5, 1), color=DERIV, stroke_width=4), M("y = 1", 26, DERIV).move_to(ax.c2p(2.3, 1.7)),
                    DashedLine(ax.c2p(2, 0), ax.c2p(2, 8), color=DIM), M("x = 2", 26, DIM).move_to(ax.c2p(2.45, 4.2)))
        p3 = point_label(ax, 0, 1, "(0, 1)", (-0.55, 1.0))
        sh3 = VGroup(region(ax, np.exp, lambda s: 1, 0, 2, opacity=0.3), sliver(ax, np.exp, lambda s: 1, 1.3))
        self.example("Example 3: Three boundaries", r"Find the area of the region bounded by $y = e^x$, $y = 1$, and $x = 2$.",
                     [r"TEXT:$y = e^x$: through $(0, 1)$, rising fast", r"TEXT:$y = 1$: a horizontal line; $x = 2$: a vertical line",
                      r"TEXT:$e^x = 1$ at $x = 0$: the point $(0, 1)$", r"TEXT:$e^x$ is on top, from $x = 0$ to $x = 2$.", r"A = \int_0^2 \left(e^x - 1\right) dx", r"= \left[e^x - x\right]_0^2",
                      r"= \left(e^2 - 2\right) - (1 - 0)", r"= e^2 - 3 \approx 4.39"],
                     at=[1, 1, 2, 2, 3, 3, 3, 4], figure=VGroup(ax), figure_at=1,
                     cues={0: draw_cue(e3), 1: draw_cue(h3), 2: draw_cue(p3), 3: draw_cue(sh3)}, overlays=(e3, h3, p3, sh3))
        self.finish()
