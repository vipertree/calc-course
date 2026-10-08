"""Topic 3.2: Implicit differentiation. Narration comes from transcripts/3_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def circle_axes():
    ax, al = plot_axes([-6, 6, 2], [-6, 6, 2], w=5.6, h=5.6)
    return ax, al


class Lesson(TranscriptScene):
    NUM = "3.2"

    def construct(self):
        ax, al = circle_axes()
        VGroup(ax, al).shift(DOWN * 0.2 + LEFT * 2.6)
        circ = ax.plot_parametric_curve(lambda t: np.array([5 * np.cos(t), 5 * np.sin(t)]), t_range=[0, TAU], color=FUNC, stroke_width=5)
        with self.beat("A curve with no formula for y") as b:
            eq = M(r"x^2 + y^2 = 25", 52, FUNC).to_edge(RIGHT, buff=0.8).shift(UP * 2)
            self.play(FadeIn(ax), FadeIn(al), Create(circ), Write(eq), run_time=1.6)
            b.line(1)
            vlt = T(r"vertical line test: a function has \\ exactly one output for each input", 30, DIM).next_to(eq, DOWN, buff=0.5)
            self.play(FadeIn(vlt), run_time=0.8)
            b.line(2)
            x3 = Line(ax.c2p(3, -6), ax.c2p(3, 6), color=SECANT, stroke_width=3)
            d3 = VGroup(Dot(ax.c2p(3, 4), color=SECANT), Dot(ax.c2p(3, -4), color=SECANT))
            l3 = VGroup(M(r"(3, 4)", 30, SECANT).next_to(d3[0], RIGHT, buff=0.15), M(r"(3, -4)", 30, SECANT).next_to(d3[1], RIGHT, buff=0.15))
            two = T(r"one input, two outputs", 32, SECANT).next_to(vlt, DOWN, buff=0.5)
            self.play(Create(x3), FadeIn(d3), FadeIn(l3), FadeIn(two), run_time=1.2)
            self.wait(1.0)
            self.play(FadeOut(x3), FadeOut(d3), FadeOut(l3), run_time=0.4)
            xv = ValueTracker(-4.5)
            vl = always_redraw(lambda: Line(ax.c2p(xv.get_value(), -6), ax.c2p(xv.get_value(), 6), color=SECANT, stroke_width=3))
            hits = always_redraw(lambda: VGroup(*[Dot(ax.c2p(xv.get_value(), s * np.sqrt(max(25 - xv.get_value() ** 2, 0))), color=SECANT) for s in (1, -1)]))
            self.play(FadeIn(vl), FadeIn(hits), run_time=0.4)
            self.play(xv.animate.set_value(4.5), run_time=2)
            self.play(FadeOut(vl), FadeOut(hits), run_time=0.3)
            b.line(3)
            ok = T(r"That's okay: it still has tangent lines.", 32, DERIV).next_to(two, DOWN, buff=0.5)
            self.play(FadeIn(ok), run_time=0.8)
            b.line(4)
            self.camera.frame.save_state()
            self.play(FadeIn(closed_dot(ax, 3, 4, INK)), run_time=0.3)
            self.play(self.camera.frame.animate.scale(0.15).move_to(ax.c2p(3, 4)), run_time=2.5)
            self.wait(0.8)
            self.play(Restore(self.camera.frame), run_time=1.5)
        self.clear()
        self.title()

        with self.beat("Pretend y is a function") as b:
            eq = M(r"x^2 + ", r"y", r"^2 = 25", 64).shift(UP * 1.8)
            self.play(Write(eq), run_time=1)
            b.line(1)
            self.play(eq[1].animate.set_color(SECANT), run_time=0.5)
            note = T(r"$y(x)$: unknown, but real", 34, SECANT).next_to(eq[1], DOWN, buff=0.6)
            self.play(FadeIn(note), GrowArrow(Arrow(note.get_top(), eq[1].get_bottom(), color=SECANT, buff=0.1)), run_time=0.8)
            b.line(2)
            a2, _ = plot_axes([0, 6, 2], [0, 6, 2], w=3.6, h=3.6, coords=False)
            a2.shift(DOWN * 1.6)
            arc = a2.plot_parametric_curve(lambda t: np.array([5 * np.cos(t), 5 * np.sin(t)]), t_range=[0.1, PI / 2 - 0.1], color=FUNC, stroke_width=4)
            th = ValueTracker(0.93)
            pt = always_redraw(lambda: Dot(a2.c2p(5 * np.cos(th.get_value()), 5 * np.sin(th.get_value())), color=SECANT))
            self.play(FadeIn(a2), Create(arc), FadeIn(pt), run_time=0.8)
            self.play(th.animate.set_value(0.5), run_time=1.2)
            self.play(th.animate.set_value(1.2), run_time=1.2)
        self.clear()

        with self.beat("The chain rule on y squared") as b:
            q = M(r"\frac{d}{dx}\big[y^2\big] = \ ?", 56).to_edge(UP, buff=0.5)
            self.play(Write(q), run_time=1)
            b.line(1)
            odd = T(r"a derivative with respect to $x$ of something written in $y$?", 34, TANGENT).next_to(q, DOWN, buff=0.35)
            self.play(FadeIn(odd), Indicate(q, color=TANGENT, scale_factor=1.05), run_time=1.2)
            b.line(2)
            chain = M(r"\frac{d}{dx}\big[y^2\big] = \frac{d}{dy}\big[y^2\big]\cdot", r"\frac{dy}{dx}", 50).next_to(odd, DOWN, buff=0.45)
            why = T(r"the chain rule relates the rates", 30, DIM).next_to(chain, RIGHT, buff=0.4)
            self.play(Write(chain), FadeIn(why), run_time=1.4)
            b.line(3)
            ans = M(r"= 2y \cdot ", r"\frac{dy}{dx}", 50).next_to(chain, DOWN, buff=0.35).align_to(chain[0], LEFT).shift(RIGHT * 1.2)
            self.play(Write(ans), run_time=1)
            self.play(ans[1].animate.set_color(SECANT), Indicate(ans[1], color=SECANT, scale_factor=1.3), run_time=1.2)
            b.line(4)
            key = formula_box(T(r"Every time we take the derivative of $y$ (or of something in $y$) \\ with respect to $x$, we multiply by $\frac{dy}{dx}$.", 34), SECANT)
            key.next_to(ans, DOWN, buff=0.45).set_x(0)
            self.play(FadeIn(key), run_time=1)
        self.clear()

        with self.beat("Differentiate both sides") as b:
            board = Board()
            board.anchor = UP * 3.3
            board.write(self, r"x^2 + y^2 = 25", color=FUNC)
            board.write(self, r"\frac{d}{dx}\left(x^2 + y^2\right) = \frac{d}{dx}\left(25\right)")
            b.line(1)
            board.write(self, r"2x + 2y\,\frac{dy}{dx} = 0")
            b.line(2)
            board.write(self, r"2y\,\frac{dy}{dx} = -2x")
            board.write(self, r"\frac{dy}{dx} = -\frac{x}{y}", color=DERIV)
            b.line(3)
            board.write(self, r"(3, 4):\ \ \frac{dy}{dx} = -\frac34", color=TANGENT)
        self.clear()

        ax, al = circle_axes()
        VGroup(ax, al).shift(DOWN * 0.2 + LEFT * 2.6)
        circ = ax.plot_parametric_curve(lambda t: np.array([5 * np.cos(t), 5 * np.sin(t)]), t_range=[0, TAU], color=FUNC, stroke_width=5)
        with self.beat("Why the answer has y in it") as b:
            self.play(FadeIn(ax), Create(circ), run_time=1)
            b.line(1)
            self.play(Create(DashedLine(ax.c2p(3, -6), ax.c2p(3, 6), color=DIM)), FadeIn(closed_dot(ax, 3, 4, INK)), FadeIn(closed_dot(ax, 3, -4, INK)), run_time=0.8)
            t1 = ax.plot(lambda x: 4 - 0.75 * (x - 3), x_range=[1, 5.2], color=TANGENT, stroke_width=4)
            t2 = ax.plot(lambda x: -4 + 0.75 * (x - 3), x_range=[1, 5.2], color=SECANT, stroke_width=4)
            labs = VGroup(M(r"(3, 4):\ -\tfrac34", 40, TANGENT), M(r"(3, -4):\ \tfrac34", 40, SECANT)).arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_edge(RIGHT, buff=0.8)
            self.play(Create(t1), Create(t2), FadeIn(labs), run_time=1.2)
            b.line(2)
            self.play(FadeIn(M(r"-\frac{x}{y}", 52, DERIV).next_to(labs, UP, buff=0.6)), run_time=0.8)
        self.clear()

        a4, _ = circle_axes()
        fig4 = VGroup(a4, a4.plot_parametric_curve(lambda t: np.array([5 * np.cos(t), 5 * np.sin(t)]), t_range=[0, TAU], color=FUNC, stroke_width=4),
                      a4.plot(lambda x: 4 - 0.75 * (x - 3), x_range=[0.5, 6], color=TANGENT, stroke_width=4),
                      a4.plot(lambda x: -4 + 0.75 * (x - 3), x_range=[0.5, 6], color=SECANT, stroke_width=4),
                      closed_dot(a4, 3, 4, INK), closed_dot(a4, 3, -4, INK))
        self.example("All tangent lines at x = 3", r"Find the equations of all lines tangent to $x^2 + y^2 = 25$ at $x = 3$.",
                     [r"\frac{d}{dx}\left(x^2 + y^2\right) = \frac{d}{dx}(25)", r"2x + 2y\,\frac{dy}{dx} = 0", r"\frac{dy}{dx} = -\frac{x}{y}",
                      r"9 + y^2 = 25,\ \text{so } y = 4 \text{ or } y = -4", r"(3, 4):\ \ y - 4 = -\tfrac34(x - 3)", r"(3, -4):\ \ y + 4 = \tfrac34(x - 3)"],
                     figure=fig4, at=[1, 2, 2, 3, 4, 5], follow=True)

        with self.beat("A product term") as b:
            eq = M(r"x^2 + ", r"xy", r" + y^2 = 7", 50).to_edge(UP, buff=0.5)
            self.play(Write(eq), run_time=1)
            both = M(r"\frac{d}{dx}\left(x^2 + xy + y^2\right) = \frac{d}{dx}(7)", 44).next_to(eq, DOWN, buff=0.35)
            self.play(Write(both), run_time=1.2)
            b.line(1)
            box = SurroundingRectangle(eq[1], color=SECANT, buff=0.1)
            pr = M(r"\frac{d}{dx}[xy] = y + x\,\frac{dy}{dx}", 44, SECANT).next_to(both, DOWN, buff=0.35)
            self.play(Create(box), Write(pr), run_time=1.2)
            full = M(r"2x + y + x\,\frac{dy}{dx} + 2y\,\frac{dy}{dx} = 0", 44).next_to(pr, DOWN, buff=0.35)
            self.play(Write(full), run_time=1.2)
            b.line(2)
            col = M(r"(x + 2y)\,\frac{dy}{dx} = -(2x + y)", 44).next_to(full, DOWN, buff=0.35)
            self.play(Write(col), run_time=1.2)
            b.line(3)
            res = M(r"\frac{dy}{dx} = -\frac{2x + y}{x + 2y}, \qquad (1, 2):\ -\frac{4}{5}", 44, DERIV).next_to(col, DOWN, buff=0.35)
            self.play(Write(res), run_time=1.2)
        self.clear()

        ax, al = circle_axes()
        VGroup(ax, al).shift(DOWN * 0.2 + LEFT * 2.6)
        circ = ax.plot_parametric_curve(lambda t: np.array([5 * np.cos(t), 5 * np.sin(t)]), t_range=[0, TAU], color=FUNC, stroke_width=5)
        with self.beat("Horizontal and vertical tangents") as b:
            sl = M(r"\frac{dy}{dx} = -\frac{x}{y}", 52, DERIV).to_edge(RIGHT, buff=1.2).shift(UP * 2.6)
            self.play(FadeIn(ax), Create(circ), Write(sl), run_time=1.2)
            b.line(1)
            h1 = T(r"horizontal: slope $0$, so $\frac{dy}{dx} = 0$", 32, TANGENT).next_to(sl, DOWN, buff=0.4).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(h1), run_time=0.8)
            b.line(2)
            h2 = T(r"numerator $= 0$: $\ x = 0$", 32, TANGENT).next_to(h1, DOWN, buff=0.25).align_to(h1, LEFT)
            self.play(FadeIn(h2), Indicate(sl, color=TANGENT, scale_factor=1.1), run_time=0.8)
            b.line(3)
            self.play(*[Create(Line(ax.c2p(-1.6, s * 5), ax.c2p(1.6, s * 5), color=TANGENT, stroke_width=5)) for s in (1, -1)],
                      *[FadeIn(closed_dot(ax, 0, s * 5, TANGENT)) for s in (1, -1)], run_time=1)
            b.line(4)
            v1 = T(r"vertical: $\frac{dy}{dx}$ blows up \\ (dividing by $0$)", 32, SECANT).next_to(h2, DOWN, buff=0.5).align_to(h1, LEFT)
            self.play(FadeIn(v1), run_time=0.8)
            b.line(5)
            v2 = T(r"denominator $= 0$: $\ y = 0$", 32, SECANT).next_to(v1, DOWN, buff=0.25).align_to(h1, LEFT)
            self.play(FadeIn(v2), run_time=0.8)
            b.line(6)
            self.play(*[Create(Line(ax.c2p(s * 5, -1.6), ax.c2p(s * 5, 1.6), color=SECANT, stroke_width=5)) for s in (1, -1)],
                      *[FadeIn(closed_dot(ax, s * 5, 0, SECANT)) for s in (1, -1)], run_time=1)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(T(r"1. Write $\frac{d}{dx}(\text{left side}) = \frac{d}{dx}(\text{right side})$. Each time you take \\ the derivative of something in $y$, multiply by $\frac{dy}{dx}$.", 38),
                          T(r"2. Solve for $\frac{dy}{dx}$.", 38)).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            self.play(FadeIn(formula_box(card, DERIV)), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Two y terms", r"Find $\dfrac{dy}{dx}$ for $3x^2 + y^2 = 12$.",
                     [r"\frac{d}{dx}\left(3x^2 + y^2\right) = \frac{d}{dx}(12)", r"6x + 2y\,\frac{dy}{dx} = 0", r"\frac{dy}{dx} = -\frac{6x}{2y} = -\frac{3x}{y}"], at=[1, 2, 3])
        a2, _ = plot_axes([-1, 3, 1], [0, 3, 1], w=5, h=3.8)
        ys = np.linspace(0.05, 2.08, 200)
        pts = [a2.c2p(np.cbrt(9 - y ** 3), y) for y in ys]
        cur = VMobject(color=FUNC, stroke_width=4).set_points_smoothly(pts)
        fig = VGroup(a2, cur, a2.plot(lambda x: 2 - 0.25 * (x - 1), x_range=[-1, 3], color=TANGENT, stroke_width=4), closed_dot(a2, 1, 2, INK))
        self.example("Example 2: A tangent line", r"Find the equation for the line tangent to $x^3 + y^3 = 9$ at $(1, 2)$.",
                     [r"1 + 8 = 9 \ \checkmark", r"\frac{d}{dx}\left(x^3 + y^3\right) = \frac{d}{dx}(9)", r"3x^2 + 3y^2\,\frac{dy}{dx} = 0", r"\frac{dy}{dx} = -\frac{x^2}{y^2}",
                      r"(1, 2):\ -\frac14, \quad y - 2 = -\frac14(x - 1)"],
                     figure=fig, at=[1, 2, 2, 3, 4])
        self.example("Example 3: Trig and exponential", r"Find $\dfrac{dy}{dx}$ for $\sin y + e^x = y$.",
                     [r"\frac{d}{dx}\left(\sin y + e^x\right) = \frac{d}{dx}(y)", r"\cos y\,\frac{dy}{dx} + e^x = \frac{dy}{dx}", r"\frac{dy}{dx}\,(1 - \cos y) = e^x",
                      r"\frac{dy}{dx} = \frac{e^x}{1 - \cos y}"], at=[1, 2, 3, 4])
        self.example("Example 4: Every tangent line at one x", r"Find the equations of all lines tangent to $x^2 + 4y^2 = 20$ at $x = 2$.",
                     [r"\frac{d}{dx}\left(x^2 + 4y^2\right) = \frac{d}{dx}(20)", r"2x + 8y\,\frac{dy}{dx} = 0", r"\frac{dy}{dx} = -\frac{2x}{8y} = -\frac{x}{4y}",
                      r"4 + 4y^2 = 20, \quad y^2 = 4, \quad \text{so } y = 2 \text{ or } y = -2",
                      r"(2, 2):\ \ \frac{dy}{dx} = -\frac14, \qquad y - 2 = -\frac14(x - 2)", r"(2, -2):\ \ \frac{dy}{dx} = \frac14, \qquad y + 2 = \frac14(x - 2)"],
                     at=[1, 2, 2, 3, 4, 5])
        self.finish()
