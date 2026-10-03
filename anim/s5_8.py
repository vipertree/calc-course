"""Topic 5.8: Sketching f, f' and f''. Narration comes from transcripts/5_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def stacked(f, df, xr=(-2.5, 2.5)):
    """f on top, f' below, sharing x positions."""
    top, tl = plot_axes([xr[0], xr[1], 1], [-3, 3, 1], w=7.6, h=2.8, coords=False, ylabel="f")
    bot, bl = plot_axes([xr[0], xr[1], 1], [-2, 6, 2], w=7.6, h=2.8, coords=False, ylabel="f'")
    VGroup(VGroup(top, tl), VGroup(bot, bl)).arrange(DOWN, buff=0.5).to_edge(LEFT, buff=0.6).shift(DOWN * 0.1)
    return top, tl, bot, bl


class Lesson(TranscriptScene):
    NUM = "5.8"

    def construct(self):
        f = lambda s: 0.5 * s**3 - 1.5 * s
        df = lambda s: 1.5 * s**2 - 1.5
        top, tl, bot, bl = stacked(f, df)
        with self.beat("Two graphs, one story") as b:
            self.play(FadeIn(top), FadeIn(tl), Create(top.plot(f, x_range=[-2.3, 2.3], color=FUNC, stroke_width=5)), FadeIn(bot), FadeIn(bl), run_time=1.4)
            S = ValueTracker(-2.2)
            tan = always_redraw(lambda: tangent_line(top, f, S.get_value(), df(S.get_value()), [S.get_value() - 0.4, S.get_value() + 0.4]).set_stroke(width=5))
            trace = always_redraw(lambda: bot.plot(df, x_range=[-2.2, max(S.get_value(), -2.19)], color=DERIV, stroke_width=5))
            pen = always_redraw(lambda: Dot(bot.c2p(S.get_value(), df(S.get_value())), color=DERIV))
            self.add(tan, trace, pen)
            b.line(1)
            self.play(S.animate.set_value(2.2), run_time=6, rate_func=linear)
            b.line(2)
            links = VGroup(*[DashedLine(top.c2p(s, f(s)), bot.c2p(s, 0), color=DIM) for s in (-1, 1)])
            self.play(Create(links), run_time=1)
        self.clear()
        self.title()

        top, tl, bot, bl = stacked(f, df)
        with self.beat("Reading the graph of f prime") as b:
            self.play(FadeIn(top), FadeIn(tl), Create(top.plot(f, x_range=[-2.3, 2.3], color=FUNC, stroke_width=5)),
                      FadeIn(bot), FadeIn(bl), Create(bot.plot(df, x_range=[-2.2, 2.2], color=DERIV, stroke_width=5)), run_time=1.4)
            b.line(1)
            turns = VGroup(*[DashedLine(top.c2p(s, f(s)), bot.c2p(s, 0), color=DIM) for s in (-1, 1)])
            l1 = T(r"$f'$ crosses zero: $f$ turns", 34, SECANT).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.6)
            self.play(Create(turns), FadeIn(l1), run_time=1)
            b.line(2)
            l2 = T(r"$f'$ rising: $f$ concave up", 34, DERIV).next_to(l1, DOWN, buff=0.3).align_to(l1, LEFT)
            self.play(FadeIn(l2), run_time=0.6)
            b.line(3)
            inf = DashedLine(top.c2p(0, 0), bot.c2p(0, -1.5), color=TANGENT)
            l3 = T(r"valley of $f'$: inflection of $f$", 34, TANGENT).next_to(l2, DOWN, buff=0.3).align_to(l1, LEFT)
            self.play(Create(inf), FadeIn(Dot(top.c2p(0, 0), color=TANGENT)), FadeIn(Dot(bot.c2p(0, -1.5), color=TANGENT)), FadeIn(l3), run_time=1)
        self.clear()
        ra, rl = plot_axes([-3, 4, 1], [-6, 6, 2], w=5, h=3.8, ylabel="f'(x)")
        rfig = VGroup(ra, rl, ra.plot(lambda x: 0.5 * (x + 2) * (x - 1) * (x - 3), x_range=[-2.6, 3.7], color=DERIV, stroke_width=4))
        self.example("Reading this graph", r"The graph of $f'(x) = \frac12(x + 2)(x - 1)(x - 3)$ is shown. Where does $f$ have a relative maximum? A relative minimum?",
                     [r"x = 1: \ f' \text{ changes from } + \text{ to } -: \ \text{relative max}", r"x = -2,\ 3: \ f' \text{ changes from } - \text{ to } +: \ \text{relative min}"], at=[1, 2], figure=rfig)

        ax, al = plot_axes([-3, 3, 1], [-5, 5, 1], w=7, h=5, coords=False, ylabel="f'(x)")
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
        with self.beat("The trap") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(lambda s: 4 - s * s, x_range=[-3, 3], color=DERIV, stroke_width=5)), run_time=1)
            ring = Circle(radius=0.3, color=TANGENT).move_to(ax.c2p(0, 4))
            wrong = T(r"maximum of $f$?", 36, DIM).to_edge(RIGHT, buff=1).shift(UP * 1.4)
            self.play(Create(ring), FadeIn(wrong), run_time=0.8)
            b.line(1)
            self.play(Create(Cross(wrong, stroke_color=TANGENT, scale_factor=0.9)), run_time=0.5)
            right = T(r"inflection point of $f$", 36, TANGENT).next_to(wrong, DOWN, buff=0.6)
            self.play(FadeIn(right), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            tab = table([r"\text{graph of } f'", r"f"], [[r"\text{above the axis}", r"\text{rises}"], [r"\text{crosses zero}", r"\text{turns}"],
                                                      [r"\text{rising}", r"\text{concave up}"], [r"\text{peak or valley}", r"\text{inflection}"]], size=36)
            self.play(FadeIn(tab), run_time=1)
        self.clear()

        self.examples_card()
        a1, l1 = plot_axes([-2.5, 2.5, 1], [-3, 3, 1], w=5, h=3.6, coords=False, ylabel="f(x)")
        fig1 = VGroup(a1, l1, a1.plot(lambda s: s**3 - 3 * s, x_range=[-2.1, 2.1], color=FUNC, stroke_width=4))
        self.example("Example 1: Sketching the derivative", r"Sketch the graph of $f'$ for $f(x) = x^3 - 3x$.",
                     [r"f'(x) = 3x^2 - 3", r"f'(x) = 0 \text{ at } x = \pm 1", r"f' > 0 \text{ for } |x| > 1,\ \ f' < 0 \text{ for } |x| < 1",
                      r"\text{parabola, vertex } (0, -3)"], figure=fig1, at=[1, 2, 3, 4],
                     notes_graph=dict(fns=[("x^3-3*x", -2.1, 2.1)], xr=(-2.5, 2.5), yr=(-3, 3), ylabel="f(x)"))
        a2, l2 = plot_axes([-3, 3, 1], [-5, 5, 1], w=5, h=3.6, coords=False, ylabel="f'(x)")
        fig2 = VGroup(a2, l2, a2.plot(lambda s: 4 - s * s, x_range=[-3, 3], color=DERIV, stroke_width=4))
        self.example("Example 2: From f prime to f",
                     r"The graph of $f'(x) = 4 - x^2$ is shown. Describe $f$: where it increases, its extrema, its concavity.",
                     [r"f' > 0 \text{ on } (-2, 2):\ f \text{ increasing}", r"\text{rel. min at } -2,\ \ \text{rel. max at } 2",
                      r"f' \text{ rising for } x < 0:\ \text{concave up}", r"f' \text{ falling for } x > 0:\ \text{concave down}", r"\text{inflection at } x = 0"],
                     figure=fig2, at=[1, 2, 3, 3, 4],
                     notes_graph=dict(fns=[("4-x^2", -3, 3)], xr=(-3, 3), yr=(-5, 5), ylabel="f'(x)"))
        self.example("Example 3: From conditions to a sketch",
                     r"Sketch a continuous $f$ with $f(0) = 1$, $f'(x) < 0$ for $x < 0$, $f'(x) > 0$ for $x > 0$, and $f''(x) > 0$ for all $x$.",
                     [r"TEXT:$f$ falls, then rises: the minimum is at $(0, 1)$.", r"TEXT:$f'' > 0$ everywhere: concave up the whole way.",
                      r"TEXT:A bowl with its lowest point at $(0, 1)$."], at=[1, 2, 3])
        self.finish()
