"""Topic 3.6: Higher-order derivatives. Narration comes from transcripts/3_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def stack3(xr, yranges, labels, w=7.2, h=1.75):
    """Three axes stacked over a shared horizontal range."""
    out = []
    for yr, lab in zip(yranges, labels):
        ax, al = plot_axes(xr, yr, w=w, h=h, coords=False, ylabel=lab)
        out.append(VGroup(ax, al))
    g = VGroup(*out).arrange(DOWN, buff=0.3)
    return [o[0] for o in out], g


class Lesson(TranscriptScene):
    NUM = "3.6"

    def fstack(self):
        xr = [-2.2, 2.2, 1]
        axs, g = stack3(xr, [[-3, 3, 1], [-4, 12, 4], [-14, 14, 7]], ["f", "f'", "f''"])
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.1)
        return axs, g

    def construct(self):
        axs, g = self.fstack()
        f = lambda x: x ** 3 - 3 * x
        plots = [axs[0].plot(f, x_range=[-2.1, 2.1], color=FUNC, stroke_width=4), axs[1].plot(lambda x: 3 * x * x - 3, x_range=[-2.1, 2.1], color=DERIV, stroke_width=4)]
        labs = VGroup(M(r"f(x) = x^3 - 3x", 40, FUNC).to_edge(RIGHT, buff=0.8).shift(UP * 2.4), M(r"f'(x) = 3x^2 - 3", 40, DERIV).to_edge(RIGHT, buff=0.8).shift(UP * 0.4))
        with self.beat("A derivative is a function") as b:
            self.play(FadeIn(g[0]), Create(plots[0]), FadeIn(labs[0]), run_time=1.2)
            self.play(FadeIn(g[1]), Create(plots[1]), FadeIn(labs[1]), run_time=1.2)
            b.line(1)
            q = M("?", 72, SECANT).move_to(axs[2])
            self.play(FadeIn(g[2]), FadeIn(q), run_time=0.8)
        self.clear()
        self.title()

        axs, g = self.fstack()
        plots = [axs[0].plot(f, x_range=[-2.1, 2.1], color=FUNC, stroke_width=4), axs[1].plot(lambda x: 3 * x * x - 3, x_range=[-2.1, 2.1], color=DERIV, stroke_width=4)]
        labs = VGroup(M(r"f(x) = x^3 - 3x", 40, FUNC).to_edge(RIGHT, buff=0.8).shift(UP * 2.4), M(r"f'(x) = 3x^2 - 3", 40, DERIV).to_edge(RIGHT, buff=0.8).shift(UP * 0.4))
        self.play(FadeIn(g), *[FadeIn(m) for m in plots], FadeIn(labs), run_time=0.8)
        with self.beat("The second derivative") as b:
            self.play(Create(axs[2].plot(lambda x: 6 * x, x_range=[-2.1, 2.1], color=TANGENT, stroke_width=4)), run_time=1)
            lab = M(r"f''(x) = 6x", 40, TANGENT).to_edge(RIGHT, buff=0.8).shift(DOWN * 1.6)
            self.play(Write(lab), run_time=0.8)
            b.line(2)
            self.clear(0.5)
            names = VGroup(M(r"f''(x)", 50), M(r"y''", 50), M(r"\frac{d^2y}{dx^2}", 50, SECANT), M(r"\frac{d^2}{dx^2}\big[f(x)\big]", 50)).arrange(RIGHT, buff=0.9).shift(UP * 0.6)
            self.play(FadeIn(names), run_time=1)
            self.play(FadeIn(M(r"= \frac{d}{dx}\left(\frac{dy}{dx}\right)", 44, SECANT).next_to(names[2], DOWN, buff=0.6)), run_time=0.8)
        self.clear()

        with self.beat("Keep going") as b:
            # Adder: polynomials run out to 0; sine's derivatives cycle every four
            chain = VGroup(*[M(t_, 44, c_) for t_, c_ in ((r"x^3 - 3x", FUNC), (r"3x^2 - 3", DERIV), (r"6x", TANGENT), (r"6", SECANT), (r"0", INK), (r"0", INK))])
            arrows = VGroup()
            row = VGroup()
            for i, m in enumerate(chain):
                row.add(m)
                if i < len(chain) - 1:
                    row.add(M(r"\to", 40, DIM))
            row.arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.9)
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.2) for m in row], lag_ratio=0.25), run_time=2.4)
            b.line(1)
            self.play(Indicate(chain[4], color=SECANT, scale_factor=1.4), run_time=0.8)
            b.line(2)
            spots = [UP, RIGHT, DOWN, LEFT]
            loop = VGroup(*[M(t_, 44, c_).move_to(DOWN * 1.2 + sp_ * 1.6 + (RIGHT * 1.0 if sp_ is RIGHT else LEFT * 1.0 if sp_ is LEFT else ORIGIN))
                            for t_, c_, sp_ in zip([r"\sin x", r"\cos x", r"-\sin x", r"-\cos x"], [FUNC, DERIV, TANGENT, SECANT], spots)])
            arcs = VGroup(*[CurvedArrow(loop[k].get_center() + 0.55 * (spots[(k + 1) % 4] - spots[k]) * 0.6 + spots[k] * -0.1,
                                        loop[(k + 1) % 4].get_center() - 0.55 * (spots[(k + 1) % 4] - spots[k]) * 0.6,
                                        angle=-PI / 3, color=DIM, stroke_width=3) for k in range(4)])
            for k in range(4):
                self.play(FadeIn(loop[k]), run_time=0.5)
                self.play(Create(arcs[k]), run_time=0.5)
            b.line(3)
            self.play(Indicate(loop[0], color=FUNC, scale_factor=1.3), run_time=0.8)
        self.clear()

        s = lambda t: t ** 3 - 6 * t * t + 9 * t
        v = lambda t: 3 * t * t - 12 * t + 9
        a = lambda t: 6 * t - 12
        axs, g = stack3([0, 4.5, 1], [[-1, 9, 3], [-4, 16, 4], [-14, 16, 7]], ["s", "v", "a"], w=7.6, h=1.55)
        g.to_edge(LEFT, buff=0.8).shift(DOWN * 0.45)
        track = Line(LEFT * 3.6, RIGHT * 3.6, color=DIM, stroke_width=4).next_to(g, UP, buff=0.35).align_to(g, LEFT)
        T_ = ValueTracker(0)
        car = always_redraw(lambda: RoundedRectangle(width=0.5, height=0.26, corner_radius=0.08, color=SECANT, fill_color=SECANT, fill_opacity=1)
                            .move_to(track.point_from_proportion(min(max(s(T_.get_value()) / 9, 0), 1)) + UP * 0.2))
        cursor = always_redraw(lambda: Line(axs[0].c2p(T_.get_value(), 9), axs[2].c2p(T_.get_value(), -14), color=INK, stroke_width=2, stroke_opacity=0.6))
        with self.beat("Position, velocity, acceleration") as b:
            eqs = VGroup(M(r"s(t) = t^3 - 6t^2 + 9t", 34, FUNC), M(r"v(t) = 3t^2 - 12t + 9", 34, DERIV), M(r"a(t) = 6t - 12", 34, TANGENT))
            self.play(FadeIn(g), Create(track), FadeIn(car), run_time=1)
            for ax, fn, col, e in zip(axs, (s, v, a), (FUNC, DERIV, TANGENT), eqs):
                self.play(Create(ax.plot(fn, x_range=[0, 4.4], color=col, stroke_width=4)), run_time=0.6)
                e.next_to(ax, RIGHT, buff=0.3)
                self.play(FadeIn(e), run_time=0.3)
            b.line(1)
            self.play(Indicate(eqs[1]), run_time=0.8)
            b.line(2)
            self.play(Indicate(eqs[2]), run_time=0.8)
            b.line(3)
            self.add(cursor)
            self.play(T_.animate.set_value(2), run_time=2.5, rate_func=linear)
            self.play(T_.animate.set_value(4.3), run_time=2.5, rate_func=linear)
        with self.beat("Reading t = 3") as b:
            self.play(T_.animate.set_value(3), run_time=1)
            rd = VGroup(M(r"v(3) = 0", 38, DERIV), M(r"a(3) = 6", 38, TANGENT)).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.25).shift(RIGHT * 2)
            self.play(FadeIn(rd), Flash(axs[1].c2p(3, 0), color=DERIV), run_time=1)
            b.line(1)
            self.play(T_.animate.set_value(3.6), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.clear()

        with self.beat("Implicit second derivatives") as b:
            board = Board()
            board.anchor = UP * 3.3
            board.write(self, r"x^2 + y^2 = 25", color=FUNC, size=44)
            b.line(1)
            board.write(self, r"y' = -\frac{x}{y}", size=44)
            b.line(2)
            board.write(self, r"y'' = -\frac{y \cdot 1 - x\,y'}{y^2} = -\frac{y + \frac{x^2}{y}}{y^2}", size=44)
            b.line(3)
            board.write(self, r"= -\frac{y^2 + x^2}{y^3} = -\frac{25}{y^3}", size=44)
            b.line(4)
            self.play(Indicate(board[-1], color=DERIV), run_time=1)
        self.clear()

        with self.beat("Close") as b:
            axs, g = self.fstack()
            self.play(FadeIn(g), *[Create(ax.plot(fn, x_range=[-2.1, 2.1], color=c, stroke_width=4))
                                   for ax, fn, c in zip(axs, (f, lambda x: 3 * x * x - 3, lambda x: 6 * x), (FUNC, DERIV, TANGENT))], run_time=1.4)
            nxt = VGroup(Arrow(axs[2].get_right(), axs[2].get_right() + RIGHT * 1.6, color=DIM), M(r"f'''", 50, DIM))
            nxt[1].next_to(nxt[0], RIGHT, buff=0.2)
            self.play(GrowArrow(nxt[0]), FadeIn(nxt[1]), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: A second derivative", r"Find $f''(x)$ for $f(x) = x^4 - 3x^2 + e^{2x}$.",
                     [r"f'(x) = 4x^3 - 6x + 2e^{2x}", r"f''(x) = 12x^2 - 6 + 4e^{2x}"], at=[1, 2])
        self.example("Example 2: A particle", r"$s(t) = 2t^3 - 9t^2 + 12t$. Find the acceleration at $t = 2$, and when it is zero.",
                     [r"v(t) = 6t^2 - 18t + 12, \quad a(t) = 12t - 18", r"a(2) = 24 - 18 = 6", r"12t - 18 = 0,\ \text{so}\ t = 1.5"], at=[1, 2, 3])
        self.example("Example 3: Implicit, with a product", r"For $xy = 4$, find $y''$.",
                     [r"y + x\,y' = 0,\ \text{so}\ y' = -\frac{y}{x}", r"y'' = -\frac{x\,y' - y}{x^2}", r"= -\frac{x\left(-\frac{y}{x}\right) - y}{x^2} = -\frac{-2y}{x^2} = \frac{2y}{x^2}"],
                     at=[1, 2, 3])
        self.finish()
