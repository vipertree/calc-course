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
        top, tl, bot, bl = stacked(lambda s: s**3 / 3, lambda s: s * s)
        with self.beat("Crossing, not touching") as b:
            self.play(FadeIn(top), FadeIn(tl), FadeIn(bot), FadeIn(bl), Create(top.plot(lambda s: s**3 / 3, x_range=[-2, 2], color=FUNC, stroke_width=5)),
                      Create(bot.plot(lambda s: s * s, x_range=[-2.3, 2.3], color=DERIV, stroke_width=5)), run_time=1.4)
            b.line(1)
            link = DashedLine(top.c2p(0, 0), bot.c2p(0, 0), color=DIM)
            flat_tan = Line(top.c2p(-0.8, 0), top.c2p(0.8, 0), color=TANGENT, stroke_width=4)
            la = T("flat for an instant, keeps rising", 30, FUNC).to_edge(RIGHT, buff=0.4).shift(UP * 1.8)
            lb = T(r"$f' = 0$, but no sign change", 30, DERIV).to_edge(RIGHT, buff=0.4).shift(DOWN * 1.4)
            self.play(Create(link), Create(flat_tan), FadeIn(Dot(bot.c2p(0, 0), color=SECANT)), run_time=0.8)
            self.play(FadeIn(lb), run_time=0.5)
            self.play(FadeIn(la), run_time=0.5)
            b.line(2)
            r1 = T(r"max or min: $f'$ must \emph{cross}", 32, SECANT).to_edge(RIGHT, buff=0.4).shift(UP * 0.5)
            self.play(FadeIn(r1), run_time=0.6)
            b.line(3)
            r2 = T(r"inflection: $f''$ must change sign", 32, TANGENT).next_to(r1, DOWN, buff=0.3).align_to(r1, LEFT)
            self.play(FadeIn(r2), run_time=0.6)
        self.clear()

        ra, rl = plot_axes([-3, 4, 1], [-6, 6, 2], w=5, h=3.8, ylabel="f'(x)")
        rfig = VGroup(ra, rl, ra.plot(lambda x: 0.5 * (x + 2) * (x - 1) * (x - 3), x_range=[-2.6, 3.7], color=DERIV, stroke_width=4))
        self.example("Reading this graph", r"The graph of $f'(x) = \frac12(x + 2)(x - 1)(x - 3)$ is shown. Where does $f$ have a relative maximum? A relative minimum?",
                     [r"TEXT:$f'$ crosses zero at $-2$, $1$ and $3$.", r"x = -2: \ - \text{ to } +, \ \text{relative min}",
                      r"x = 1: \ + \text{ to } -, \ \text{relative max}", r"x = 3: \ - \text{ to } +, \ \text{relative min}"], at=[1, 2, 3, 4], figure=rfig,
                     cues={k: (lambda xv, w: lambda sc: sc.play(FadeIn(T(w, 26, SECANT).next_to(ra.c2p(xv, 0), UP, buff=0.25)), run_time=0.5))(xv, w)
                           for k, (xv, w) in {1: (-2, "min"), 2: (1, "max"), 3: (3, "min")}.items()}, follow=True)

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
                     [r"f'(x) = 3x^2 - 3", r"3x^2 - 3 = 0, \ \ x^2 = 1, \ \ x = \pm 1", r"f' > 0 \text{ for } |x| > 1,\ \ f' < 0 \text{ for } |x| < 1",
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
        ca, cl = plot_axes([-4, 6, 1], [-3, 3, 1], w=6, h=3.6, ylabel="f'(x)")
        semi = lambda s: -np.sqrt(max(4 - (s - 2) ** 2, 0))
        up_pcs = VGroup(Line(ca.c2p(-4, -2), ca.c2p(-2, 2)), ca.plot(semi, x_range=[2, 4, 0.01]), Line(ca.c2p(4, 0), ca.c2p(6, 3)))
        dn_pcs = VGroup(Line(ca.c2p(-2, 2), ca.c2p(0, 0)), ca.plot(semi, x_range=[0, 2, 0.01]))
        for m in (*up_pcs, *dn_pcs):
            m.set_stroke(FUNC, 5)
        cfig = VGroup(ca, cl, up_pcs, dn_pcs)
        self.example("Example 4: Lines and a semicircle",
                     r"The graph of $f'$ (three segments and a semicircle) is shown. Where is $f$ increasing? Where are its relative extrema? "
                     r"Where is $f$ concave up? Find its inflection points.",
                     [r"f' > 0 \text{ on } (-3, 0) \text{ and } (4, 6): \ f \text{ increasing}", r"x = -3: \ - \text{ to } +, \ \text{rel. min}",
                      r"x = 0: \ + \text{ to } -, \ \text{rel. max}", r"x = 4: \ - \text{ to } +, \ \text{rel. min}",
                      r"f' \text{ rising on } (-4, -2),\ (2, 6): \ \text{concave up}", r"f' \text{ falling on } (-2, 2): \ \text{concave down}",
                      r"\text{inflection points at } x = -2 \text{ and } x = 2"], at=[1, 2, 2, 2, 3, 4, 5], figure=cfig,
                     cues={4: lambda sc: sc.play(up_pcs.animate.set_color(DERIV), run_time=0.6),
                           5: lambda sc: sc.play(dn_pcs.animate.set_color(TANGENT), run_time=0.6),
                           6: lambda sc: sc.play(FadeIn(Dot(ca.c2p(-2, 2), color=SECANT)), FadeIn(Dot(ca.c2p(2, -2), color=SECANT)), run_time=0.6)},
                     text=r"The graph of $f'$ on $[-4, 6]$ consists of three line segments and a semicircle, as shown. Where is $f$ increasing? "
                          r"Where does $f$ have relative extrema? Where is the graph of $f$ concave up? Find its inflection points.",
                     notes_graph=dict(fns=[("2*x+6", -4, -2), ("-x", -2, 0), ("-sqrt(abs(4-(x-2)^2))", 0, 4), ("1.5*(x-4)", 4, 6)], xr=(-4, 6), yr=(-3, 3),
                                      ylabel="f'(x)"))

        sa, sl = plot_axes([-1, 5, 1], [-1, 5, 1], w=5, h=3)
        s1 = staged_chart([1, 3], ["+", "-", "+"], words=["inc", "dec", "inc"], name="f'", width=6)
        s2 = staged_chart([2], ["-", "+"], words=["down", "up"], name="f''", width=6)
        sfig = VGroup(VGroup(sa, sl), s1, s2).arrange(DOWN, buff=0.35)
        cubic = lambda s: s**3 - 6 * s**2 + 9 * s
        self.example("Example 5: Sketching from scratch",
                     r"Sketch the graph of $f(x) = x^3 - 6x^2 + 9x$ by hand. Find its intercepts, relative extrema, concavity and inflection point.",
                     [r"f(x) = x(x - 3)^2: \ \text{zeros at } x = 0,\ 3", r"f'(x) = 3x^2 - 12x + 9 = 3(x - 1)(x - 3)",
                      r"f'(0) = 9 > 0, \ f'(2) = -3 < 0, \ f'(4) = 9 > 0", r"\text{rel. max } (1, 4), \ \text{rel. min } (3, 0)",
                      r"f''(x) = 6x - 12", r"f''(1) = -6 < 0, \ f''(3) = 6 > 0", r"\text{inflection point } (2, 2)",
                      r"TEXT:Plot $(0, 0)$, $(1, 4)$, $(2, 2)$, $(3, 0)$.", r"TEXT:Connect: bending down until $x = 2$, bending up after."],
                     at=[1, 2, 3, 4, 5, 5, 6, 7, 8], figure=sfig,
                     cues={2: lambda sc: (reveal_sign(s1, 0, 1, 2)(sc), reveal_words(s1)(sc)),
                           3: lambda sc: (mark_point(s1, 0, "max")(sc), mark_point(s1, 1, "min")(sc)),
                           5: lambda sc: (reveal_sign(s2, 0, 1)(sc), reveal_words(s2)(sc)),
                           6: mark_point(s2, 0, "inflection"),
                           7: lambda sc: sc.play(*[FadeIn(Dot(sa.c2p(px, py), color=SECANT)) for px, py in ((0, 0), (1, 4), (2, 2), (3, 0))], run_time=0.8),
                           8: lambda sc: sc.play(Create(sa.plot(cubic, x_range=[-0.08, 4.1], color=FUNC, stroke_width=4)), run_time=1.6)}, follow=True)
        self.finish()
