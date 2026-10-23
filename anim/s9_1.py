"""Topic 9.1 (BC): Parametric equations and their derivatives. Narration comes from transcripts/9_1.md."""
import numpy as np
from manim import *

from kit import *
from props import walk_along
from style import *


class Lesson(TranscriptScene):
    NUM = "9.1"

    def construct(self):
        X = lambda s: s * s - 1
        Y = lambda s: s**3 - 3 * s
        DYDX = r"\frac{dy}{dx} = \frac{dy/dt}{dx/dt}"
        with self.beat("A path with a clock") as b:
            # the same curve the table plots after the title (Adder, 2026-10-14: the opening and the table must match)
            ax, al = plot_axes([-1.6, 3.6, 1], [-2.8, 2.8, 1], w=5.4, h=5.6)
            VGroup(ax, al).to_edge(LEFT, buff=0.8)
            tt = ValueTracker(-2)
            trail = always_redraw(lambda: param_curve(ax, X, Y, -2, max(-1.99, tt.get_value())))
            bug = walk_along(ladybug(0.42), ax, X, Y, tt)
            clock = VGroup(Circle(radius=0.5, stroke_color=INK, stroke_width=3), M("t", 32)).to_corner(UR, buff=0.6)
            self.add(trail)
            self.play(FadeIn(ax), FadeIn(al), FadeIn(bug), FadeIn(clock), run_time=0.8)
            self.play(tt.animate.set_value(2), run_time=5, rate_func=linear)
            trail.clear_updaters()
            stamps = VGroup(*[Dot(ax.c2p(X(s), Y(s)), color=SECANT) for s in (-2, -1, 0, 1, 2)])
            self.play(FadeIn(stamps), FadeIn(M(r"(x(t),\ y(t))", 36, SECANT).next_to(clock, LEFT, buff=0.4)), run_time=0.8)
            b.line(1)
            # one x, two heights: she comes back over x values she has already passed
            r2 = np.sqrt(2)
            vl = DashedLine(ax.c2p(1, -2.8), ax.c2p(1, 2.8), color=TANGENT, stroke_width=3, dash_length=0.12)
            hits = VGroup(Dot(ax.c2p(1, r2), radius=0.1, color=TANGENT), Dot(ax.c2p(1, -r2), radius=0.1, color=TANGENT))
            self.play(Create(vl), run_time=0.8)
            self.play(FadeIn(hits, scale=1.6), run_time=0.6)
            vlt = VGroup(T("one $x$, two heights:", 32, TANGENT), T("not a function of $x$", 32, TANGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            vlt.next_to(ax, RIGHT, buff=0.9).shift(UP * 0.6)
            self.play(FadeIn(vlt), run_time=0.8)
            b.line(2)
            eqs = VGroup(M(r"x(t) = t^2 - 1", 40), M(r"y(t) = t^3 - 3t", 40)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(vlt, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(FadeOut(vl), FadeOut(hits), FadeIn(eqs), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Plotting a parametric curve") as b:
            ts = [-2, -1, 0, 1, 2]
            tab = table(["t", "x = t^2 - 1", "y = t^3 - 3t"], [[str(s), str(X(s)), str(Y(s))] for s in ts], size=32).to_edge(LEFT, buff=0.5)
            ax, al = plot_axes([-1.6, 3.6, 1], [-2.8, 2.8, 1], w=5, h=5)
            VGroup(ax, al).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(tab), FadeIn(ax), FadeIn(al), run_time=1)
            dots = VGroup(*[Dot(ax.c2p(X(s), Y(s)), color=SECANT) for s in ts])
            self.play(LaggedStart(*[FadeIn(d, scale=1.5) for d in dots], lag_ratio=0.3), run_time=1.4)
            curve = param_curve(ax, X, Y, -2, 2)
            arrows = VGroup(*[Arrow(ax.c2p(X(s), Y(s)), ax.c2p(X(s + 0.15), Y(s + 0.15)), buff=0, color=FUNC, stroke_width=4, max_tip_length_to_length_ratio=0.9) for s in (-1.5, -0.5, 0.5, 1.5)])
            b.line(1)
            self.play(Create(curve), FadeIn(arrows), run_time=1.6)
            b.line(2)
            self.play(Indicate(dots[1]), Indicate(dots[3]), run_time=1)
        self.clear()

        with self.beat("The slope of a parametric curve") as b:
            # the chain rule on top, the boxed formula well below it, the little picture off to the side (Adder: the
            # box sat over the dy/dt line)
            r1 = M(r"\frac{dy}{dt} = \frac{dy}{dx}\cdot\frac{dx}{dt}", 50).move_to(LEFT * 2.6 + UP * 1.9)
            self.play(Write(r1), run_time=1)
            b.line(1)
            box = formula_box(VGroup(M(DYDX, 54, ACCUM), T(r"provided $\frac{dx}{dt} \ne 0$", 28, DIM)).arrange(DOWN, buff=0.2), ACCUM)
            box.next_to(r1, DOWN, buff=0.9)
            self.play(FadeIn(box), run_time=1)
            b.line(2)
            ax, _ = plot_axes([0, 3, 1], [0, 2, 1], w=3.6, h=2.4, coords=False)
            ax.move_to(RIGHT * 3.6 + DOWN * 0.2)
            p, q = ax.c2p(0.8, 0.6), ax.c2p(2.0, 1.5)
            c = np.array([q[0], p[1], 0])
            self.play(FadeIn(ax), Create(Line(p, q, color=FUNC, stroke_width=5)), Create(Line(p, c, color=DIM)), Create(Line(c, q, color=DIM)),
                      FadeIn(M("dx", 30).next_to(Line(p, c), DOWN, buff=0.08)), FadeIn(M("dy", 30).next_to(Line(c, q), RIGHT, buff=0.08)), run_time=1)
        self.clear()

        ax, _ = plot_axes([-1.6, 4.4, 1], [-2.8, 3.6, 1], w=4.2, h=4.4)
        fig = VGroup(ax, param_curve(ax, X, Y, -2, 2.15), Dot(ax.c2p(3, 2), color=TANGENT), Line(ax.c2p(1.2, 2 - 9 / 4 * 1.8), ax.c2p(4.2, 2 + 9 / 4 * 1.2), color=TANGENT, stroke_width=4))
        self.example("A tangent line", r"For $x = t^2 - 1$, $y = t^3 - 3t$, find $\frac{dy}{dx}$ and the equation of the tangent line at $t = 2$.",
                     [r"\frac{dx}{dt} = 2t", r"\frac{dy}{dt} = 3t^2 - 3", r"\frac{dy}{dx} = \frac{3t^2 - 3}{2t}", r"t = 2: \ \frac{dy}{dx} = \frac{12 - 3}{4} = \frac94",
                      r"x(2) = 3, \ \ y(2) = 8 - 6 = 2", r"y - 2 = \tfrac94(x - 3)"], at=[1, 1, 2, 3, 4, 5], figure=fig, figure_at=4, follow=True, ref=DYDX)

        TANS = r"\begin{aligned}&\text{horizontal: } \tfrac{dy}{dt} = 0,\ \tfrac{dx}{dt} \ne 0\\ &\text{vertical: } \tfrac{dx}{dt} = 0,\ \tfrac{dy}{dt} \ne 0\end{aligned}"
        ax, al = plot_axes([-1.6, 3.6, 1], [-2.8, 2.8, 1], w=4.8, h=4.8)
        VGroup(ax, al).to_edge(LEFT, buff=0.6)
        with self.beat("Horizontal and vertical tangents") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(param_curve(ax, X, Y, -2, 2)), run_time=1)
            board = VGroup(M(r"\text{horizontal: } \tfrac{dy}{dt} = 0, \ \tfrac{dx}{dt} \ne 0", 34, DERIV), M(r"\text{vertical: } \tfrac{dx}{dt} = 0, \ \tfrac{dy}{dt} \ne 0", 34, SECANT),
                           T("both $0$: look closer", 30, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
            self.play(Write(board[0]), run_time=1)
            b.line(1)
            self.play(Write(board[1]), FadeIn(board[2]), run_time=1)

        with self.beat("Why a zero on the bottom means vertical") as b:
            # Adder, 2026-10-14: pause on the vertical tangent. The tangent line steepens as dx/dt shrinks to 0.
            self.play(FadeOut(board), run_time=0.5)
            f1 = M(r"\frac{dy}{dx} = \frac{3t^2 - 3}{2t}", 44).to_edge(RIGHT, buff=1.2).to_edge(UP, buff=0.6)
            self.play(Write(f1), run_time=1)
            tv = ValueTracker(0.9)

            def tangent():
                u = tv.get_value()
                p = np.array(ax.c2p(X(u), Y(u)))
                d = np.array(ax.c2p(X(u) + 2 * u, Y(u) + 3 * u * u - 3)) - np.array(ax.c2p(0, 0))
                d = d / np.linalg.norm(d)
                return VGroup(Line(p - 1.1 * d, p + 1.1 * d, color=SECANT, stroke_width=5), Dot(p, color=SECANT))
            tan = always_redraw(tangent)
            self.play(FadeIn(tan), run_time=0.5)
            rows = [["0.5", "1", "-2.25"], ["0.2", "0.4", "-7.2"], ["0.05", "0.1", r"\approx -29.9"]]
            tab = table(["t", r"\frac{dx}{dt}", r"\frac{dy}{dx}"], rows, size=36, gap=0.3).next_to(f1, DOWN, buff=0.5)
            for cell in tab.cells[1:]:
                for m in cell:
                    m.set_opacity(0)
            self.play(FadeIn(tab), run_time=0.5)
            b.line(1)
            for k, u in enumerate((0.5, 0.2, 0.05)):
                self.play(tv.animate.set_value(u), run_time=1.2)
                self.play(*[m.animate.set_opacity(1) for m in tab.cells[k + 1]], run_time=0.5)
            self.play(tv.animate.set_value(0), run_time=1.2)
            b.line(2)
            inf = VGroup(T(r"bottom $\to 0$, so the slope", 30, SECANT), T(r"goes off to infinity:", 30, SECANT), T("a vertical line", 30, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            inf.next_to(tab, DOWN, buff=0.5)
            self.play(FadeIn(inf), Indicate(tan), run_time=1)
            b.line(3)
            # the same thing on a regular function: 3.2's circle, slope -x/y, vertical where y = 0
            self.play(FadeOut(tab), FadeOut(inf), FadeOut(f1), run_time=0.6)
            cax, _ = plot_axes([-6, 6, 2], [-6, 6, 2], w=3, h=3, coords=False)
            cax.to_edge(RIGHT, buff=1.0).shift(UP * 0.9)
            circ = ParametricFunction(lambda s: cax.c2p(5 * np.cos(s), 5 * np.sin(s)), t_range=[0, TAU], color=FUNC, stroke_width=4)
            vts = VGroup(*[Line(cax.c2p(sx * 5, -2.2), cax.c2p(sx * 5, 2.2), color=SECANT, stroke_width=5) for sx in (-1, 1)])
            cl = VGroup(M(r"x^2 + y^2 = 25", 32), M(r"\frac{dy}{dx} = \frac{-x}{y}", 36), T("bottom $0$ at $y = 0$: vertical", 30, SECANT)).arrange(DOWN, buff=0.2).next_to(cax, DOWN, buff=0.35)
            self.play(FadeIn(cax), Create(circ), FadeIn(cl[0]), run_time=1)
            self.play(FadeIn(cl[1]), run_time=0.6)
            self.play(Create(vts), FadeIn(cl[2]), run_time=1)

        with self.beat("The tangents on our curve") as b:
            self.play(*[FadeOut(m) for m in (cax, circ, vts, cl, tan)], run_time=0.6)
            board = VGroup(M(r"\text{horizontal: } \tfrac{dy}{dt} = 0, \ \tfrac{dx}{dt} \ne 0", 34, DERIV), M(r"\text{vertical: } \tfrac{dx}{dt} = 0, \ \tfrac{dy}{dt} \ne 0", 34, SECANT)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(UP * 1.6)
            self.play(FadeIn(board), run_time=0.6)
            hs = VGroup(*[Line(ax.c2p(-0.7, yy), ax.c2p(0.7, yy), color=DERIV, stroke_width=5) for yy in (-2, 2)])
            vs = Line(ax.c2p(-1, -0.8), ax.c2p(-1, 0.8), color=SECANT, stroke_width=5)
            notes = VGroup(M(r"3t^2 - 3 = 0: \ t = \pm1", 32, DERIV), M(r"(0, -2), \ (0, 2)", 32, DERIV), M(r"2t = 0: \ t = 0", 32, SECANT), M(r"(-1, 0)", 32, SECANT)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(board, DOWN, buff=0.6, aligned_edge=LEFT)
            self.play(FadeIn(notes[0]), run_time=0.8)
            self.play(Create(hs), FadeIn(notes[1]), run_time=1)
            b.line(1)
            self.play(FadeIn(notes[2]), run_time=0.8)
            self.play(Create(vs), FadeIn(notes[3]), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"x = x(t), \ \ y = y(t): \ t \text{ is the parameter}", 40), formula_box(M(r"\frac{dy}{dx} = \frac{dy/dt}{dx/dt}", 50, ACCUM), ACCUM),
                          M(r"\text{horizontal: } \tfrac{dy}{dt} = 0; \quad \text{vertical: } \tfrac{dx}{dt} = 0", 38, SECANT)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        ax, _ = plot_axes([-1.4, 1.4, 1], [-1.4, 1.4, 1], w=3.4, h=3.4, coords=False)
        r2 = np.sqrt(2) / 2
        fig1 = VGroup(ax, param_curve(ax, np.cos, np.sin, 0, TAU), Dot(ax.c2p(r2, r2), color=TANGENT), Line(ax.c2p(r2 - 0.6, r2 + 0.6), ax.c2p(r2 + 0.6, r2 - 0.6), color=TANGENT, stroke_width=4))
        self.example("Example 1: Around a circle", r"For $x = \cos t$, $y = \sin t$, find $\frac{dy}{dx}$ and the slope at $t = \frac\pi4$.",
                     [r"\frac{dx}{dt} = -\sin t, \ \ \frac{dy}{dt} = \cos t", r"\frac{dy}{dx} = \frac{\cos t}{-\sin t} = -\cot t", r"t = \tfrac\pi4: \ -\cot\tfrac\pi4 = -1"], at=[1, 2, 2], figure=fig1, ref=DYDX)
        self.example("Example 2: Finding the tangents", r"Find the points where $x = t^2 - 2t$, $y = t^3 - 12t$ has horizontal or vertical tangents.",
                     [r"\frac{dy}{dt} = 3t^2 - 12 = 0 \text{ at } t = \pm2, \text{ where } \frac{dx}{dt} = 2t - 2 \ne 0", r"t = 2: \ (0, -16); \quad t = -2: \ (8, 16) \quad \text{(horizontal)}",
                      r"\frac{dx}{dt} = 2t - 2 = 0 \text{ at } t = 1, \text{ where } \frac{dy}{dt} = -9 \ne 0", r"t = 1: \ (-1, -11) \quad \text{(vertical)}"], at=[1, 1, 2, 3], ref=TANS)
        self.example("Example 3: Eliminating the parameter", r"Write $x = 2t + 1$, $y = t^2$ as an equation in $x$ and $y$, and check the slope both ways.",
                     [r"t = \tfrac{x - 1}{2}", r"y = \left(\tfrac{x - 1}{2}\right)^2 = \tfrac{(x - 1)^2}{4}", r"\frac{dy}{dx} = \tfrac{x - 1}{2}", r"\text{parametric: } \frac{dy}{dx} = \frac{2t}{2} = t = \tfrac{x - 1}{2}"], at=[1, 2, 3, 3], ref=DYDX)
        self.finish()
