"""Topic 0.4: Graphs of sine, cosine, and tangent. Narration comes from transcripts/0_4.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def level(ax, y, x0, x1, color=DIM, tex=None, size=26):
    """A dashed horizontal level line with an optional label at its right end."""
    g = VGroup(DashedLine(ax.c2p(x0, y), ax.c2p(x1, y), color=color))
    if tex:
        g.add(M(tex, size, color).next_to(ax.c2p(x1, y), RIGHT, buff=0.12))
    return g


def asymptotes(ax, xs, ymax, color=DIM):
    return VGroup(*[DashedLine(ax.c2p(v, -ymax), ax.c2p(v, ymax), color=color) for v in xs])


class Lesson(TranscriptScene):
    NUM = "0.4"

    def construct(self):
        with self.beat("Unrolling the circle") as b:
            uc = TrigCircle(r=1.4, center=LEFT * 5 + UP * 0.2, ticks=False)
            ax, labs = pi_axes(0, 2.2, [-1.4, 1.4, 1], w=8.6, h=2.8, ylabel=r"\sin\theta")
            VGroup(ax, labs).next_to(uc, RIGHT, buff=0.8).align_to(uc, DOWN).shift(UP * (uc.c[1] - ax.c2p(0, 0)[1]))
            self.play(Create(uc), FadeIn(ax), FadeIn(labs), run_time=1)
            th = ValueTracker(0)
            p = always_redraw(lambda: uc.dot(th.get_value(), FUNC))
            q = always_redraw(lambda: Dot(ax.c2p(th.get_value(), np.sin(th.get_value())), radius=0.09, color=FUNC))
            link = always_redraw(lambda: DashedLine(uc.pt(th.get_value()), ax.c2p(th.get_value(), np.sin(th.get_value())), color=DIM))
            trace = TracedPath(q.get_center, stroke_color=FUNC, stroke_width=4)
            self.add(p, q, link, trace)
            self.play(th.animate.set_value(2 * PI), run_time=5, rate_func=linear)
            b.line(1)
            self.play(th.animate.set_value(2.2 * PI), run_time=0.8, rate_func=linear)
            self.play(FadeIn(T("one trip around = one wave", 32, FUNC).next_to(ax, DOWN, buff=0.6)), run_time=0.6)
            b.line(2)
            props = VGroup(T("tides", 30, DIM), T("sound", 30, DIM), T("seasons", 30, DIM)).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(m) for m in props], lag_ratio=0.3), run_time=1.2)
        self.clear()
        self.title()

        with self.beat("The graph of sine") as b:
            ax, labs = pi_axes(-2, 2, [-1.6, 1.6, 1], w=11, h=3.6)
            VGroup(ax, labs).shift(DOWN * 0.4)
            self.play(FadeIn(ax), FadeIn(labs), run_time=0.6)
            self.play(Create(ax.plot(np.sin, x_range=[0, 2 * PI], color=FUNC, stroke_width=5)), run_time=2.4)
            self.play(FadeIn(Dot(ax.c2p(PI / 2, 1), color=SECANT)), FadeIn(M(r"\left(\tfrac{\pi}{2}, 1\right)", 26, SECANT).next_to(ax.c2p(PI / 2, 1), UP, buff=0.12)),
                      FadeIn(Dot(ax.c2p(3 * PI / 2, -1), color=SECANT)), FadeIn(M(r"\left(\tfrac{3\pi}{2}, -1\right)", 26, SECANT).next_to(ax.c2p(3 * PI / 2, -1), DOWN, buff=0.12)), run_time=0.8)
            b.line(1)
            self.play(Create(ax.plot(np.sin, x_range=[-2 * PI, 0], color=FUNC, stroke_width=5)), run_time=1.4)
            br = BraceBetweenPoints(ax.c2p(0, 1.45), ax.c2p(2 * PI, 1.45), UP, color=TANGENT)
            self.play(FadeIn(br), FadeIn(M(r"\text{period } 2\pi", 34, TANGENT).next_to(br, UP, buff=0.1)), run_time=0.8)
            b.line(2)
            self.play(FadeIn(level(ax, 1, -2 * PI, 2 * PI)), FadeIn(level(ax, -1, -2 * PI, 2 * PI)), FadeIn(M(r"-1 \le \sin x \le 1", 34).to_corner(UL, buff=0.6)), run_time=0.8)
            self.play(*[FadeIn(Dot(ax.c2p(k * PI, 0), color=DERIV)) for k in range(-2, 3)], FadeIn(M(r"\sin x = 0 \text{ at } x = k\pi", 32, DERIV).to_corner(UR, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("The graph of cosine") as b:
            ax, labs = pi_axes(-2, 2, [-1.6, 1.6, 1], w=11, h=3.6)
            VGroup(ax, labs).shift(DOWN * 0.4)
            sin_g = ax.plot(np.sin, x_range=[-2 * PI, 2 * PI], color=FUNC, stroke_width=3).set_opacity(0.5)
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(sin_g), run_time=0.6)
            cos_g = ax.plot(np.cos, x_range=[-2 * PI, 2 * PI], color=DERIV, stroke_width=5)
            self.play(Create(cos_g), FadeIn(Dot(ax.c2p(0, 1), color=DERIV)), FadeIn(M(r"(0, 1)", 26, DERIV).next_to(ax.c2p(0, 1), UR, buff=0.1)), run_time=2)
            b.line(1)
            slide = ax.plot(np.sin, x_range=[-1.5 * PI, 2 * PI], color=FUNC, stroke_width=5)
            self.play(slide.animate.shift(ax.c2p(-PI / 2, 0) - ax.c2p(0, 0)), run_time=1.6)
            self.play(FadeIn(M(r"\cos x = \sin\left(x + \tfrac{\pi}{2}\right)", 38, DERIV).to_edge(UP, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("Amplitude and period") as b:
            ax, labs = pi_axes(0, 2, [-3.4, 3.4, 1], w=8.4, h=4.6, yticks=(3, 1, -1, -3))
            VGroup(ax, labs).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
            self.play(FadeIn(ax), FadeIn(labs), Create(ax.plot(np.sin, x_range=[0, 2 * PI], color=DIM, stroke_width=3)), run_time=0.8)
            g3 = ax.plot(lambda v: 3 * np.sin(v), x_range=[0, 2 * PI], color=FUNC, stroke_width=5)
            self.play(Create(g3), FadeIn(M(r"y = 3\sin x", 34, FUNC).to_edge(RIGHT, buff=0.6).shift(UP * 2.4)), run_time=1.2)
            self.play(FadeIn(DoubleArrow(ax.c2p(PI / 2, 0), ax.c2p(PI / 2, 3), buff=0, color=FUNC, stroke_width=3)), FadeIn(T("amplitude 3", 30, FUNC).to_edge(RIGHT, buff=0.6).shift(UP * 1.8)), run_time=0.8)
            b.line(1)
            g2 = ax.plot(lambda v: np.sin(2 * v), x_range=[0, 2 * PI], color=TANGENT, stroke_width=5)
            self.play(Create(g2), FadeIn(M(r"y = \sin 2x", 34, TANGENT).to_edge(RIGHT, buff=0.6).shift(UP * 0.8)), run_time=1.2)
            br = BraceBetweenPoints(ax.c2p(0, -1.2), ax.c2p(PI, -1.2), DOWN, color=TANGENT)
            self.play(FadeIn(br), FadeIn(T(r"period $\pi$", 30, TANGENT).to_edge(RIGHT, buff=0.6).shift(UP * 0.2)), run_time=0.8)
            b.line(2)
            box = formula_box(VGroup(M(r"y = A\sin(Bx)", 40), M(r"\text{amplitude } |A|", 36, FUNC), M(r"\text{period } \frac{2\pi}{|B|}", 36, TANGENT)).arrange(DOWN, buff=0.25), ACCUM)
            self.play(FadeIn(box.to_edge(RIGHT, buff=0.5).shift(DOWN * 1.8)), run_time=0.8)
        self.clear()

        with self.beat("Shifts") as b:
            ax, labs = pi_axes(-0.5, 2.5, [-1.4, 3.4, 1], w=9.6, h=4.6, yticks=(1, 2, 3, -1))
            VGroup(ax, labs).shift(DOWN * 0.6 + LEFT * 0.8)
            base = ax.plot(np.sin, x_range=[-0.5 * PI, 2.5 * PI], color=DIM, stroke_width=3)
            self.play(FadeIn(ax), FadeIn(labs), Create(base), run_time=0.8)
            moved = ax.plot(np.sin, x_range=[-0.5 * PI, 2.5 * PI], color=FUNC, stroke_width=5)
            self.play(FadeIn(moved), run_time=0.3)
            self.play(moved.animate.shift(ax.c2p(0, 2) - ax.c2p(0, 0)), run_time=1.2)
            self.play(FadeIn(level(ax, 2, -0.5 * PI, 2.5 * PI, ACCUM, r"\text{midline } y = D")), run_time=0.6)
            b.line(1)
            self.play(moved.animate.shift(ax.c2p(PI / 4, 0) - ax.c2p(0, 0)), run_time=1.2)
            self.play(FadeIn(T(r"$x - C$: slides right $C$", 32, SECANT).to_edge(UP, buff=0.5).shift(LEFT * 2.4)), run_time=0.6)
            b.line(2)
            self.play(FadeIn(formula_box(M(r"y = A\sin\big(B(x - C)\big) + D", 44, ACCUM), ACCUM).to_edge(UP, buff=0.4).shift(RIGHT * 3)), run_time=0.8)
        self.clear()

        ax, labs = pi_axes(0, 2, [-2.6, 4.6, 1], w=6, h=4.2, yticks=(4, 1, -2))
        fig = VGroup(ax, labs, ax.plot(lambda v: 3 * np.cos(2 * v) + 1, x_range=[0, 2 * PI], color=FUNC, stroke_width=4),
                     level(ax, 1, 0, 2 * PI, ACCUM), level(ax, 4, 0, 2 * PI, SECANT), level(ax, -2, 0, 2 * PI, SECANT))
        self.example("Describing a cosine graph", r"For $y = 3\cos(2x) + 1$, find the amplitude, period, midline, maximum, and minimum.",
                     [r"\text{amplitude } |3| = 3", r"\text{period } \frac{2\pi}{2} = \pi", r"\text{midline } y = 1", r"\text{maximum } 1 + 3 = 4", r"\text{minimum } 1 - 3 = -2"],
                     at=[1, 2, 3, 4, 5], figure=fig, figure_at=3, follow=True)

        with self.beat("The graph of tangent") as b:
            ax, labs = pi_axes(-1.5, 1.5, [-4, 4, 1], w=10, h=5.2, yticks=(2, -2))
            VGroup(ax, labs).shift(DOWN * 0.3)
            self.play(FadeIn(ax), FadeIn(labs), run_time=0.6)
            self.play(*[FadeIn(Dot(ax.c2p(k * PI, 0), color=DERIV)) for k in (-1, 0, 1)], FadeIn(T(r"zeros where $\sin x = 0$", 30, DERIV).to_corner(UL, buff=0.5)), run_time=0.8)
            b.line(1)
            asy = asymptotes(ax, [-1.5 * PI, -PI / 2, PI / 2, 1.5 * PI], 4)
            mid = clipped_plot(ax, np.tan, -PI / 2 + 0.01, PI / 2 - 0.01, 4, TANGENT, 5)
            self.play(Create(mid), run_time=1.4)
            self.play(Create(asy[1:3]), FadeIn(T(r"asymptotes where $\cos x = 0$", 30, DIM).to_corner(UR, buff=0.5)), run_time=0.8)
            b.line(2)
            self.play(Create(clipped_plot(ax, np.tan, -1.5 * PI + 0.01, -PI / 2 - 0.01, 4, TANGENT, 5)), Create(clipped_plot(ax, np.tan, PI / 2 + 0.01, 1.5 * PI - 0.01, 4, TANGENT, 5)),
                      Create(asy[0]), Create(asy[3]), run_time=1.4)
            br = BraceBetweenPoints(ax.c2p(-PI / 2, -3.6), ax.c2p(PI / 2, -3.6), DOWN, color=SECANT)
            self.play(FadeIn(br), FadeIn(T(r"period $\pi$", 30, SECANT).next_to(br, DOWN, buff=0.08)), run_time=0.6)
        self.clear()

        with self.beat("Secant, cosecant, cotangent") as b:
            ax, labs = pi_axes(-1.5, 1.5, [-3.5, 3.5, 1], w=10, h=4.6, yticks=(1, -1))
            VGroup(ax, labs).shift(DOWN * 0.4)
            self.play(FadeIn(ax), FadeIn(labs), Create(DashedVMobject(ax.plot(np.cos, x_range=[-1.5 * PI, 1.5 * PI], color=DERIV, stroke_width=3), num_dashes=60)), run_time=0.8)
            sec = clipped_plot(ax, lambda v: 1 / np.cos(v), -1.5 * PI, 1.5 * PI, 3.5, ACCUM, 5)
            self.play(Create(sec), FadeIn(M(r"y = \sec x = \frac{1}{\cos x}", 36, ACCUM).to_corner(UL, buff=0.5)), run_time=1.6)
            b.line(1)
            self.play(Create(asymptotes(ax, [-PI / 2, PI / 2], 3.5)), run_time=0.6)
            self.play(FadeOut(sec), run_time=0.4)
            self.play(Create(DashedVMobject(ax.plot(np.sin, x_range=[-1.5 * PI, 1.5 * PI], color=FUNC, stroke_width=3), num_dashes=60)),
                      Create(clipped_plot(ax, lambda v: 1 / np.sin(v), -1.5 * PI, 1.5 * PI, 3.5, SECANT, 5)), FadeIn(M(r"y = \csc x = \frac{1}{\sin x}", 36, SECANT).to_corner(UR, buff=0.5)), run_time=1.6)
            b.line(2)
            self.play(FadeIn(T(r"$\cot x = \frac{\cos x}{\sin x}$: falling branches, asymptotes at $k\pi$", 30, DIM).to_edge(DOWN, buff=0.3)), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"\sin, \ \cos: \ \text{period } 2\pi, \ \ -1 \le y \le 1", 42),
                          M(r"y = A\sin\big(B(x - C)\big) + D", 46, ACCUM),
                          M(r"\text{amplitude } |A|, \ \ \text{period } \frac{2\pi}{|B|}, \ \ \text{shift } C, \ \ \text{midline } y = D", 38),
                          M(r"\tan: \ \text{period } \pi, \ \text{asymptotes where } \cos x = 0", 40, TANGENT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, labs = plot_axes([0, 12, 3], [0, 8, 1], w=6, h=4, coords=False)
        f1 = VGroup(ax, labs, ax.plot(lambda v: -2 * np.sin(PI * v / 3) + 5, x_range=[0, 12], color=FUNC, stroke_width=4), level(ax, 5, 0, 12, ACCUM, "5"), level(ax, 7, 0, 12, SECANT, "7"),
                    level(ax, 3, 0, 12, SECANT, "3"), *[M(str(v), 22, DIM).next_to(ax.c2p(v, 0), DOWN, buff=0.1) for v in (3, 6, 9, 12)])
        self.example("Example 1: A reflected sine", r"For $y = -2\sin\left(\frac{\pi x}{3}\right) + 5$, find the amplitude, period, midline, maximum, and minimum.",
                     [r"\text{amplitude } |-2| = 2", r"\text{period } \frac{2\pi}{\pi/3} = 2\pi \cdot \frac{3}{\pi} = 6", r"\text{midline } y = 5", r"\text{maximum } 5 + 2 = 7, \ \ \text{minimum } 5 - 2 = 3",
                      r"TEXT:The negative $A$ flips the wave: it starts at the midline going down."], at=[1, 2, 3, 3, 4], figure=f1, figure_at=4)
        ax, labs = plot_axes([0, 8, 1], [-2, 6, 1], w=6, h=4)
        f2 = VGroup(ax, labs, ax.plot(lambda v: 3 * np.cos(PI * v / 2) + 2, x_range=[0, 8], color=FUNC, stroke_width=4),
                    Dot(ax.c2p(0, 5), color=SECANT), Dot(ax.c2p(2, -1), color=SECANT), Dot(ax.c2p(4, 5), color=SECANT))
        self.example("Example 2: An equation from a graph", VGroup(T("Write an equation for this graph.", 42)),
                     [r"D = \frac{5 + (-1)}{2} = 2", r"A = \frac{5 - (-1)}{2} = 3", r"\text{period } 4: \ \frac{2\pi}{B} = 4, \ \ B = \frac{\pi}{2}", r"\text{starts at a maximum: cosine}",
                      r"y = 3\cos\left(\frac{\pi x}{2}\right) + 2"], at=[1, 2, 3, 4, 4], figure=f2,
                     text=r"Write an equation for the graph: a maximum of $5$ at $x = 0$, a minimum of $-1$ at $x = 2$, the next maximum at $x = 4$.",
                     notes_graph=dict(fns=[("3*cos(deg(pi*x/2))+2", 0, 8)], xr=(-0.3, 8.3), yr=(-2, 6), closed=[(0, 5), (2, -1), (4, 5)]))
        self.example("Example 3: A Ferris wheel", r"A Ferris wheel has radius $20$ m, its center is $25$ m above the ground, and it turns once every $4$ minutes. A rider starts at the bottom. Write the rider's height $h(t)$ after $t$ minutes, and find $h(1)$ and $h(2)$.",
                     [r"\text{midline } 25, \ \ \text{amplitude } 20", r"\text{period } 4: \ B = \frac{2\pi}{4} = \frac{\pi}{2}", r"\text{starts at a minimum: } -\cos",
                      r"h(t) = 25 - 20\cos\left(\frac{\pi t}{2}\right)", r"h(1) = 25 - 20\cos\tfrac{\pi}{2} = 25 \text{ m}", r"h(2) = 25 - 20\cos\pi = 45 \text{ m}"],
                     at=[1, 2, 3, 3, 4, 4], figure=ferris_wheel(1.6))
        ax, labs = pi_axes(0, 1, [-4, 4, 1], w=5, h=4, step=0.25, yticks=())
        f4 = VGroup(ax, labs, *[clipped_plot(ax, lambda v: np.tan(2 * v), a, c, 4, TANGENT, 4) for a, c in ((0, PI / 4 - 0.01), (PI / 4 + 0.01, 3 * PI / 4 - 0.01), (3 * PI / 4 + 0.01, PI))],
                    asymptotes(ax, [PI / 4, 3 * PI / 4], 4))
        self.example("Example 4: Asymptotes of a tangent", r"Find the vertical asymptotes of $y = \tan(2x)$ for $0 \le x \le \pi$, and its period.",
                     [r"\tan u \text{ undefined at } u = \tfrac{\pi}{2} + k\pi", r"2x = \frac{\pi}{2} + k\pi", r"x = \frac{\pi}{4} + \frac{k\pi}{2}", r"x = \frac{\pi}{4}, \ \frac{3\pi}{4}",
                      r"\text{period } \frac{\pi}{2}"], at=[1, 2, 2, 3, 4], figure=f4, figure_at=3)
        self.finish()
