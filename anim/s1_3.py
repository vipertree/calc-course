"""Topic 1.3: Estimating limit values from graphs. Narration comes from transcripts/1_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import car_on_graph


def jump_graph(w=7.4, h=5.2):
    ax, al = plot_axes([0, 4, 1], [0, 6, 1], w=w, h=h)
    left = ax.plot(lambda x: 1 + x, x_range=[0, 2], color=FUNC, stroke_width=5)
    right = ax.plot(lambda x: 4 + 0.5 * (x - 2), x_range=[2, 4], color=FUNC, stroke_width=5)
    return ax, al, left, right, open_dot(ax, 2, 3), closed_dot(ax, 2, 4, FUNC)


class Lesson(TranscriptScene):
    NUM = "1.3"

    def construct(self):
        ax, al, L, R, o, c = jump_graph()
        g = VGroup(ax, al, L, R, o, c).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        xl, xr = ValueTracker(0.3), ValueTracker(3.7)
        cl = car_on_graph(ax, lambda u: 1 + u, xl, 1)
        cr = car_on_graph(ax, lambda u: 4 + 0.5 * (u - 2), xr, -1)
        hl = always_redraw(lambda: DashedLine(ax.c2p(0, 1 + xl.get_value()), ax.c2p(xl.get_value(), 1 + xl.get_value()), color=SECANT))
        hr = always_redraw(lambda: DashedLine(ax.c2p(0, 4 + 0.5 * (xr.get_value() - 2)), ax.c2p(xr.get_value(), 4 + 0.5 * (xr.get_value() - 2)), color=TANGENT))
        with self.beat("Two roads to one point") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(L), Create(R), FadeIn(o), FadeIn(c), run_time=1.6)
            self.add(cl, cr)
            b.line(1)
            self.add(hl, hr)
            b.line(2)
            self.play(xl.animate.set_value(1.97), run_time=1.6)
            self.play(xr.animate.set_value(2.03), run_time=1.6)
        self.clear()
        self.title()

        ax, al, L, R, o, c = jump_graph(6.4, 4.6)
        VGroup(ax, al, L, R, o, c).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        self.add(ax, al, L, R, o, c)
        with self.beat("One-sided limits") as b:
            l1 = MathTex(r"\lim_{x\to2^-} f(x) = 3", font_size=50, color=SECANT).to_edge(RIGHT, buff=0.8).shift(UP * 1.4)
            self.play(Write(l1), run_time=1.2)
            self.play(Indicate(l1[0][4], color=INK, scale_factor=2), run_time=0.8)
            b.line(1)
            l2 = MathTex(r"\lim_{x\to2^+} f(x) = 4", font_size=50, color=TANGENT).next_to(l1, DOWN, buff=0.5)
            self.play(Write(l2), run_time=1.2)

        with self.beat("When the two sides disagree") as b:
            ne = M(r"3 \ne 4", 50).next_to(l2, DOWN, buff=0.6)
            self.play(Write(ne), run_time=0.8)
            b.line(1)
            dne = M(r"\lim_{x\to2} f(x)\ \text{does not exist}", 44).next_to(ne, DOWN, buff=0.5)
            self.play(Write(dne), run_time=1.2)
            b.line(2)
            self.play(Indicate(c, scale_factor=2.2, color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("The rule") as b:
            rule = callout(r"If $f$ is defined on both sides of $c$: \quad $\displaystyle\lim_{x\to c} f(x) = L$ \ exactly when both one-sided limits equal $L$.", INK, 36)
            rule.set_max_width(12.5).shift(UP * 0.8)
            self.play(FadeIn(rule), run_time=1.2)
            b.line(1)
            red = T("Different one-sided limits: the limit does not exist.", 40, TANGENT).next_to(rule, DOWN, buff=0.6)
            self.play(FadeIn(red, shift=UP * 0.2), run_time=1)
        self.clear()

        ax2, al2 = plot_axes([-2, 4, 1], [-1, 3, 1], w=7.6, h=4.6)
        VGroup(ax2, al2).shift(DOWN * 0.3)
        with self.beat("At the edge of the domain") as b:
            self.play(FadeIn(ax2), FadeIn(al2), run_time=0.8)
            shade = Rectangle(width=abs(ax2.c2p(0, 0)[0] - ax2.c2p(-2, 0)[0]), height=ax2.y_length, fill_color=DIM, fill_opacity=0.25,
                              stroke_width=0).move_to(ax2.c2p(-1, 1))
            nolab = T(r"no function \\ here", 30, DIM).move_to(shade).shift(DOWN * 0.7 + LEFT * 0.2)
            b.line(1)
            self.play(Create(ax2.plot(np.sqrt, x_range=[0, 4], color=FUNC, stroke_width=5)), FadeIn(shade), FadeIn(nolab), run_time=1.4)
            xv = ValueTracker(3.5)
            cc = car_on_graph(ax2, lambda u: np.sqrt(max(u, 0)), xv, -1)
            self.add(cc)
            self.play(xv.animate.set_value(0.02), run_time=2)
            b.line(2)
            st = M(r"\lim_{x\to0^+}\sqrt{x} = 0", 50, TANGENT).to_corner(UR, buff=0.7)
            self.play(Write(st), run_time=1.2)
        self.clear()

        with self.beat("Three ways a limit can fail") as b:
            boxes = []
            for k, (fn, rng) in enumerate([(lambda x: np.sign(x), [-2, 2]), (lambda x: 1 / x ** 2, [-2, 2]), (lambda x: np.sin(1 / x), [-1, 1])]):
                a, _ = plot_axes([rng[0], rng[1], 1], [-2, 4, 1] if k == 1 else [-2, 2, 1], w=3.6, h=2.8, coords=False)
                if k == 0:
                    pl = VGroup(a.plot(fn, x_range=[-2, -0.01], color=FUNC), a.plot(fn, x_range=[0.01, 2], color=FUNC))
                elif k == 1:
                    pl = VGroup(a.plot(fn, x_range=[-2, -0.5], color=FUNC), a.plot(fn, x_range=[0.5, 2], color=FUNC))
                else:
                    pl = a.plot(fn, x_range=[0.02, 1], color=FUNC, use_smoothing=False).add(a.plot(fn, x_range=[-1, -0.02], color=FUNC, use_smoothing=False))
                boxes.append(VGroup(a, pl))
            row = VGroup(*boxes).arrange(RIGHT, buff=0.6).shift(UP * 0.4)
            names = VGroup(*[T(n_, 34, SECANT).next_to(bx, DOWN, buff=0.3) for n_, bx in zip(["jump", "unbounded", "oscillation"], boxes)])
            for i in range(3):
                b.line(i + 1 if i < 2 else 2)
                self.play(FadeIn(boxes[i]), FadeIn(names[i]), run_time=0.9)
            b.line(3)
            inf = M(r"\lim_{x\to0}\frac{1}{x^2} = \infty \ \ (\text{still does not exist})", 40).to_edge(DOWN, buff=0.6)
            self.play(Write(inf), run_time=1.2)
        self.clear()

        with self.beat("Oscillation") as b:
            a, _ = plot_axes([-1, 1, 0.5], [-1.5, 1.5, 0.5], w=10, h=5, coords=False)
            curve = VGroup(a.plot(lambda x: np.sin(1 / x), x_range=[0.005, 1], color=FUNC, use_smoothing=False),
                           a.plot(lambda x: np.sin(1 / x), x_range=[-1, -0.005], color=FUNC, use_smoothing=False))
            self.play(FadeIn(a), Create(curve), run_time=2)
            b.line(1)
            self.play(self.camera.frame.animate.scale(0.35).move_to(a.c2p(0, 0)), run_time=2.5)
            self.play(self.camera.frame.animate.scale(0.5).move_to(a.c2p(0, 0)), run_time=2)
            b.line(2)
            self.play(self.camera.frame.animate.scale(1 / (0.35 * 0.5)).move_to(ORIGIN + DOWN * (config.frame_height * 0.22 / 2 - 0.45)), run_time=1.6)
        self.clear()

        with self.beat("Graphs can hide things") as b:
            screen = RoundedRectangle(width=7, height=4.6, corner_radius=0.25, color=DIM, stroke_width=6, fill_color="#20302A", fill_opacity=1).shift(LEFT * 2)
            a, _ = plot_axes([-1, 3, 1], [-1, 4, 1], w=6, h=3.8, coords=False)
            a.move_to(screen)
            ln = a.plot(lambda x: x + 1, x_range=[-1, 3], color=DERIV, stroke_width=4)
            self.play(FadeIn(screen), FadeIn(a), Create(ln), run_time=1.4)
            b.line(1)
            inset = VGroup(Circle(radius=1.4, color=SECANT, stroke_width=4), Line(LEFT * 1.3 + DOWN * 0.6, RIGHT * 1.3 + UP * 0.6, color=DERIV, stroke_width=6),
                           Circle(radius=0.16, color=DERIV, stroke_width=5, fill_color=BG, fill_opacity=1)).shift(RIGHT * 4.6 + UP * 0.3)
            pointer = Line(a.c2p(1, 2), inset.get_left(), color=SECANT, stroke_width=2)
            self.play(Create(pointer), FadeIn(inset), run_time=1.2)
            b.line(2)
            tips = T("check with a table or algebra", 34, SECANT).next_to(inset, DOWN, buff=0.4)
            self.play(FadeIn(tips), run_time=0.8)
        self.clear()

        ax3, al3 = plot_axes([-3, 4, 1], [-2, 4, 1], w=8.2, h=5.2)
        VGroup(ax3, al3).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        pieces = VGroup(ax3.plot(lambda x: x + 3, x_range=[-3, -1], color=FUNC, stroke_width=5),
                        ax3.plot(lambda x: 1 - x, x_range=[-1, 2], color=FUNC, stroke_width=5),
                        ax3.plot(lambda x: x - 1, x_range=[2, 4], color=FUNC, stroke_width=5))
        dots = VGroup(open_dot(ax3, -1, 2), closed_dot(ax3, -1, 0, SECANT), open_dot(ax3, 2, -1), closed_dot(ax3, 2, 1, FUNC))
        with self.beat("Reading a full graph") as b:
            self.play(FadeIn(ax3), FadeIn(al3), Create(pieces), FadeIn(dots), run_time=1.6)
            r1 = VGroup(M(r"\lim_{x\to-1} f(x) = 2", 40), M(r"f(-1) = 0", 40, SECANT)).arrange(DOWN, aligned_edge=LEFT).to_edge(RIGHT, buff=0.6).shift(UP * 1.4)
            self.play(Write(r1), run_time=1.4)
            b.line(1)
            r2 = VGroup(M(r"\lim_{x\to2^-} f(x) = -1", 40), M(r"\lim_{x\to2^+} f(x) = 1", 40), M(r"\lim_{x\to2} f(x)\ \text{DNE}", 40, TANGENT)).arrange(DOWN, aligned_edge=LEFT).next_to(r1, DOWN, buff=0.6, aligned_edge=LEFT)
            self.play(Write(r2), run_time=2)
        self.clear()

        with self.beat("Close") as b:
            ax4, al4 = plot_axes([0, 4, 1], [0, 5, 1], w=7.4, h=4.8)
            VGroup(ax4, al4).shift(DOWN * 0.3)
            f4 = lambda x: 4 - (x - 2) ** 2 / 2
            xa, xb = ValueTracker(0.3), ValueTracker(3.7)
            ca = car_on_graph(ax4, f4, xa, 1)
            cb = car_on_graph(ax4, f4, xb, -1)
            self.play(FadeIn(ax4), FadeIn(al4), Create(ax4.plot(f4, x_range=[0, 4], color=FUNC, stroke_width=5)), FadeIn(open_dot(ax4, 2, 4)), run_time=1.4)
            self.add(ca, cb)
            self.play(xa.animate.set_value(1.85), xb.animate.set_value(2.15), run_time=2.4)
        self.clear()

        # ---------------------------------------------------------------- worked examples
        self.examples_card()
        a1, _ = plot_axes([-4, 0, 1], [-1, 5, 1], w=5.4, h=4.6)
        fig1 = VGroup(a1, a1.plot(lambda x: x + 3, x_range=[-4, -2], color=FUNC, stroke_width=4), a1.plot(lambda x: -x - 1, x_range=[-2, 0], color=FUNC, stroke_width=4),
                      open_dot(a1, -2, 1), closed_dot(a1, -2, 4, SECANT))
        self.example("Example 1: A hole with a stray dot", r"Find the one-sided limits, the limit, and $g(-2)$.",
                     [r"\lim_{x\to-2^-} g(x) = 1", r"\lim_{x\to-2^+} g(x) = 1", r"\lim_{x\to-2} g(x) = 1", r"g(-2) = 4"], figure=fig1, at=[1, 2, 3, 4],
                     notes_graph=dict(fns=[("x+3", -4, -2), ("-x-1", -2, 0)], xr=(-4, 0), yr=(-1, 5), open=[(-2, 1)], closed=[(-2, 4)], ylabel="g(x)"))
        a2, _ = plot_axes([-1, 3, 1], [-1, 4, 1], w=5.4, h=4.6)
        fig2 = VGroup(a2, a2.plot(lambda x: x * x, x_range=[-1, 1], color=FUNC, stroke_width=4), a2.plot(lambda x: 3 - x, x_range=[1, 3], color=FUNC, stroke_width=4),
                      open_dot(a2, 1, 1), closed_dot(a2, 1, 2, FUNC))
        self.example("Example 2: A jump", r"Find the one-sided limits, the limit, and $g(1)$.",
                     [r"\lim_{x\to1^-} g(x) = 1,\quad \lim_{x\to1^+} g(x) = 2", r"\lim_{x\to1} g(x)\ \text{does not exist}", r"g(1) = 2"], figure=fig2, at=[2, 3, 4],
                     notes_graph=dict(fns=[("x^2", -1, 1), ("3-x", 1, 3)], xr=(-1, 3), yr=(-1, 4), open=[(1, 1)], closed=[(1, 2)], ylabel="g(x)"))
        a3, _ = plot_axes([0, 6, 1], [-5, 5, 1], w=5.4, h=4.6)
        fig3 = VGroup(a3, a3.plot(lambda x: 1 / (x - 3), x_range=[0, 2.8], color=FUNC, stroke_width=4),
                      a3.plot(lambda x: 1 / (x - 3), x_range=[3.2, 6], color=FUNC, stroke_width=4), asymptote(a3, 3, [-5, 5]))
        self.example("Example 3: Running off to infinity", r"Find the one-sided limits and the limit of $h(x) = \dfrac{1}{x - 3}$ at $x = 3$.",
                     [r"\lim_{x\to3^-} h(x) = -\infty", r"\lim_{x\to3^+} h(x) = \infty", r"\lim_{x\to3} h(x)\ \text{does not exist}"], figure=fig3, at=[1, 2, 3])
        self.finish()
