"""Topic 5.3: Increasing and decreasing intervals. Narration comes from transcripts/5_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.3"

    def construct(self):
        ax, al = plot_axes([0, 6, 1], [-2, 3, 1], w=10, h=4.6, coords=False)
        VGroup(ax, al).shift(UP * 0.3)
        f = lambda s: np.sin(1.2 * s) + 0.25 * s
        df = lambda s: 1.2 * np.cos(1.2 * s) + 0.25
        with self.beat("Uphill and downhill") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)), run_time=1.2)
            S = ValueTracker(0.1)
            tan = always_redraw(lambda: tangent_line(ax, f, S.get_value(), df(S.get_value()), [S.get_value() - 0.5, S.get_value() + 0.5],
                                                     color=DERIV if df(S.get_value()) > 0 else TANGENT).set_stroke(width=6))
            self.add(tan)
            self.play(S.animate.set_value(5.9), run_time=5, rate_func=linear)
            b.line(1)
            roots = [r for r in np.linspace(0, 6, 6001) if abs(df(r)) < 2e-3]
            cuts = [0] + sorted({round(r, 1) for r in roots}) + [6]
            bars = VGroup()
            for lo, hi in zip(cuts, cuts[1:]):
                up = df((lo + hi) / 2) > 0
                seg = Line(ax.c2p(lo, -2) + DOWN * 0.5, ax.c2p(hi, -2) + DOWN * 0.5, color=DERIV if up else TANGENT, stroke_width=8)
                bars.add(VGroup(seg, T("increasing" if up else "decreasing", 26, DERIV if up else TANGENT).next_to(seg, DOWN, buff=0.15)))
            self.play(FadeIn(bars), run_time=1)
            b.line(2)
        self.clear()
        self.title()

        g = lambda s: np.sin(1.2 * s) + 0.25 * s - 0.5          # the opening curve, lowered so it dips below the axis
        dg = lambda s: 1.2 * np.cos(1.2 * s) + 0.25
        zs = [(np.arccos(-0.25 / 1.2) + k) / 1.2 for k in (0, 2 * np.pi - 2 * np.arccos(-0.25 / 1.2))]   # zeros of g': about 1.48 and 3.75
        top, tl = plot_axes([0, 6, 1], [-1.5, 2, 1], w=10, h=2.9, coords=False, ylabel="f(x)")
        bot, bl = plot_axes([0, 6, 1], [-1.5, 1.5, 1], w=10, h=2.6, coords=False, ylabel="f'(x)")
        VGroup(top, tl).move_to(UP * 1.75)
        VGroup(bot, bl).move_to(DOWN * 1.95)
        with self.beat("f and f prime together") as b:
            fcurve = top.plot(g, x_range=[0, 6], color=FUNC, stroke_width=5)
            self.play(FadeIn(top), FadeIn(tl), FadeIn(bot), FadeIn(bl), Create(fcurve), run_time=1.4)
            b.line(1)
            S = ValueTracker(0.05)
            tan = always_redraw(lambda: tangent_line(top, g, S.get_value(), dg(S.get_value()), [S.get_value() - 0.45, S.get_value() + 0.45]).set_stroke(width=5))
            dot = always_redraw(lambda: Dot(bot.c2p(S.get_value(), dg(S.get_value())), color=DERIV, radius=0.09))
            trace = TracedPath(lambda: bot.c2p(S.get_value(), dg(S.get_value())), stroke_color=DERIV, stroke_width=4)
            self.add(tan, trace, dot)
            self.play(S.animate.set_value(5.95), run_time=6, rate_func=linear)
            b.line(2)
            cuts = [0] + zs + [6]
            paint = VGroup()
            for lo, hi in zip(cuts, cuts[1:]):
                c = DERIV if dg((lo + hi) / 2) > 0 else TANGENT
                paint.add(top.plot(g, x_range=[lo, hi], color=c, stroke_width=7), bot.plot(dg, x_range=[lo, hi], color=c, stroke_width=7))
            self.play(FadeOut(tan), FadeOut(dot), FadeIn(paint), run_time=1)
            b.line(3)
            links = VGroup(*[DashedLine(top.c2p(z, g(z)), bot.c2p(z, 0), color=DIM, stroke_width=2) for z in zs])
            self.play(Create(links), *[Flash(bot.c2p(z, 0), color=INK) for z in zs], run_time=1.2)

        with self.beat("Height is not slope") as b:
            self.play(FadeOut(links), run_time=0.4)
            b.line(1)
            for k, (x0, ftxt, fptxt) in enumerate(((2, r"f > 0", r"f' < 0"), (4.2, r"f < 0", r"f' > 0"))):
                if k == 1:
                    b.line(2)
                pt, pb = top.c2p(x0, g(x0)), bot.c2p(x0, dg(x0))
                v = DashedLine(top.c2p(x0, 2), bot.c2p(x0, -1.5), color=SECANT, stroke_width=2)
                lt = M(ftxt, 34, FUNC).next_to(pt, UR if g(x0) > 0 else DR, buff=0.15)
                lb = M(fptxt, 34, DERIV if dg(x0) > 0 else TANGENT).next_to(pb, UR if dg(x0) > 0 else DR, buff=0.15)
                self.play(Create(v), FadeIn(Dot(pt, color=SECANT)), FadeIn(Dot(pb, color=SECANT)), run_time=0.8)
                self.play(FadeIn(lt), run_time=0.5)
                self.play(FadeIn(lb), run_time=0.5)
            b.line(3)
            self.clear()
            sumup = VGroup(T(r"sign of $f$: where the graph is", 46, FUNC), T(r"sign of $f'$: which way it's going", 46, DERIV)).arrange(DOWN, buff=0.6)
            self.play(FadeIn(sumup[0]), run_time=0.6)
            self.play(FadeIn(sumup[1]), run_time=0.6)
        self.clear()

        with self.beat("The rule") as b:
            r1 = M(r"f'(x) > 0 \text{ on an interval},\ \text{so}\ f \text{ is increasing there}", 46, DERIV)
            r2 = M(r"f'(x) < 0 \text{ on an interval},\ \text{so}\ f \text{ is decreasing there}", 46, TANGENT)
            VGroup(r1, r2).arrange(DOWN, buff=0.8)
            self.play(Write(r1), run_time=1.2)
            b.line(1)
            self.play(Write(r2), run_time=1.2)
        self.clear()

        with self.beat("A sign chart") as b:
            fp = M(r"f'(x) = 3x^2 - 12 = 3(x - 2)(x + 2)", 50).to_edge(UP, buff=0.7)
            self.play(Write(fp), run_time=1.2)
            b.line(1)
            ch = sign_chart([-2, 2], ["+", "-", "+"], words=["inc", "dec", "inc"]).shift(DOWN * 0.4)
            self.play(Create(ch[0]), FadeIn(ch[1]), FadeIn(ch[2]), FadeIn(ch[5]), run_time=1)
            b.line(2)
            tests = [r"f'(-3) = 15", r"f'(0) = -12", r"f'(3) = 15"]
            for k, tx in enumerate(tests):
                tm = M(tx, 32, DIM).next_to(ch[3][k], UP, buff=0.3)
                self.play(FadeIn(tm), FadeIn(ch[3][k]), run_time=0.7)
            b.line(3)
            self.play(FadeIn(ch[4]), run_time=0.8)
        self.clear()
        ch = staged_chart([0, 2], ["+", "-", "+"], words=["inc", "dec", "inc"], width=7)
        self.example("Increasing from a sign chart", r"Where is $f(x) = x^3 - 3x^2 + 4$ increasing?",
                     [r"TEXT:Increasing means $f'(x) > 0$. When is $f'(x) > 0$?", r"f'(x) = 3x^2 - 6x", r"= 3x(x - 2)",
                      r"3x = 0 \text{ or } x - 2 = 0", r"x = 0 \text{ or } x = 2", r"TEXT:Test values: $-1$, $1$, $3$.",
                      r"f'(-1) = 3 + 6 = 9 > 0", r"f'(1) = 3 - 6 = -3 < 0", r"f'(3) = 27 - 18 = 9 > 0",
                      r"\text{increasing on } (-\infty, 0) \text{ and } (2, \infty)"], at=[1, 2, 3, 4, 4, 6, 7, 8, 9, 10],
                     figure=ch, figure_at=5, cues={6: reveal_sign(ch, 0), 7: reveal_sign(ch, 1), 8: reveal_sign(ch, 2), 9: reveal_words(ch)})

        gax, _ = plot_axes([-4, 6, 1], [-2.5, 2.5, 1], w=6, h=3.6, ylabel="f'(x)")
        pieces = [Line(gax.c2p(-4, 2), gax.c2p(-2, 0), color=FUNC, stroke_width=5),
                  gax.plot(lambda s: -np.sqrt(max(4 - s * s, 0)), x_range=[-2, 2, 0.01], color=FUNC, stroke_width=5),
                  VGroup(Line(gax.c2p(2, 0), gax.c2p(4, 2), color=FUNC, stroke_width=5), Line(gax.c2p(4, 2), gax.c2p(6, 2), color=FUNC, stroke_width=5))]
        fpfig = VGroup(gax, _, *pieces)

        def paint(k, c):
            return lambda scene: scene.play(pieces[k].animate.set_color(c), run_time=0.6)
        self.example("From the graph of f prime",
                     r"The graph of $f'$ (line segments and a semicircle) is shown. Where is $f$ increasing? Decreasing? Where does $f$ change direction?",
                     [r"TEXT:Graph of $f'$: read its sign.", r"(-4, -2):\ f' > 0, \text{ so } f \text{ increasing}",
                      r"(-2, 2):\ f' < 0, \text{ so } f \text{ decreasing}", r"(2, 6):\ f' > 0, \text{ so } f \text{ increasing}",
                      r"\text{rel. max at } x = -2,\ \ \text{rel. min at } x = 2",
                      r"TEXT:$f'$ is decreasing on $(-4, -2)$ but still positive, so $f$ is still increasing."], at=[1, 2, 3, 4, 5, 6],
                     figure=fpfig, cues={1: paint(0, DERIV), 2: paint(1, TANGENT), 3: paint(2, DERIV),
                                         5: lambda scene: scene.play(Indicate(pieces[0], color=DERIV), run_time=1)},
                     text=r"The graph of $f'$ on $[-4, 6]$ consists of line segments and a semicircle, as shown. Where is $f$ increasing? "
                          r"Decreasing? Where does $f$ change direction?",
                     notes_graph=dict(fns=[("-x-2", -4, -2), ("-sqrt(abs(4-x^2))", -2, 2), ("x-2", 2, 4), ("2+0*x", 4, 6)], xr=(-4, 6), yr=(-3, 3), ylabel="f'(x)"), follow=True)

        with self.beat("Justify with the derivative") as b:
            s = T(r"$f$ is decreasing on $(-2, 2)$ \textbf{because} $f'(x) < 0$ there.", 46)
            self.play(Write(s), run_time=1.4)
            self.play(Circumscribe(s, color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            ch = sign_chart([-2, 2], ["+", "-", "+"], words=["inc", "dec", "inc"]).shift(UP * 0.4)
            self.play(FadeIn(ch), run_time=0.8)
            self.play(FadeIn(T(r"the sign of $f'$ is the direction of $f$", 42, SECANT).next_to(ch, DOWN, buff=0.7)), run_time=0.8)
        self.clear()

        self.examples_card()
        c1 = staged_chart([-2, 2], ["+", "-", "+"], words=["inc", "dec", "inc"], width=7)
        self.example("Example 1: A cubic", r"On what intervals is $f(x) = x^3 - 12x + 1$ increasing? Decreasing?",
                     [r"f'(x) = 3x^2 - 12", r"= 3(x^2 - 4) = 3(x - 2)(x + 2)", r"x = 2 \text{ or } x = -2",
                      r"f'(-3) = 27 - 12 = 15 > 0", r"f'(0) = -12 < 0", r"f'(3) = 27 - 12 = 15 > 0",
                      r"\text{increasing on } (-\infty, -2) \text{ and } (2, \infty)", r"\text{decreasing on } (-2, 2)"], at=[1, 2, 3, 4, 5, 6, 7, 7],
                     figure=c1, figure_at=3, cues={3: reveal_sign(c1, 0), 4: reveal_sign(c1, 1), 5: reveal_sign(c1, 2), 6: reveal_words(c1)})
        c2 = staged_chart([1], ["+", "-"], words=["inc", "dec"], width=7)
        self.example("Example 2: An exponential", r"On what intervals is $f(x) = xe^{-x}$ increasing? Decreasing?",
                     [r"f'(x) = e^{-x} - xe^{-x}", r"= (1 - x)e^{-x}", r"TEXT:$e^{-x} > 0$, so $f'$ has the sign of $1 - x$.", r"1 - x = 0 \text{ at } x = 1",
                      r"f'(0) = (1)(1) = 1 > 0", r"f'(2) = (-1)e^{-2} < 0",
                      r"\text{increasing on } (-\infty, 1)", r"\text{decreasing on } (1, \infty)"], at=[1, 2, 3, 3, 4, 5, 6, 6],
                     figure=c2, figure_at=3, cues={4: reveal_sign(c2, 0), 5: reveal_sign(c2, 1), 6: reveal_words(c2)})
        c3 = staged_chart([-1, 3], ["-", "+", "+"], words=["dec", "inc", "inc"], width=7)
        self.example("Example 3: A repeated factor", r"$f'(x) = (x + 1)(x - 3)^2$. On what intervals is $f$ increasing?",
                     [r"x + 1 = 0 \text{ or } x - 3 = 0", r"x = -1 \text{ or } x = 3", r"f'(-2) = (-1)(25) = -25 < 0", r"f'(0) = (1)(9) = 9 > 0",
                      r"f'(4) = (5)(1) = 5 > 0", r"TEXT:No sign change at $3$: $(x - 3)^2$ is never negative.",
                      r"\text{increasing on } (-1, 3) \text{ and } (3, \infty)"], at=[1, 1, 2, 3, 4, 5, 6],
                     figure=c3, figure_at=1, cues={2: reveal_sign(c3, 0), 3: reveal_sign(c3, 1), 4: reveal_sign(c3, 2), 6: reveal_words(c3)})
        h = lambda s: (s**3 - 6 * s**2 + 9 * s) / 2 + 1
        hax, hl = plot_axes([0, 4, 1], [0, 4, 1], w=5, h=3.6, ylabel="f(x)")
        hfig = VGroup(hax, hl, hax.plot(h, x_range=[0, 4], color=FUNC, stroke_width=5))
        fall = hax.plot(h, x_range=[1, 3], color=TANGENT, stroke_width=7)
        self.example("Example 4: From the graph of f", r"The graph of $f$ is shown. On what intervals is $f'$ negative? Is $f'(2)$ positive or negative?",
                     [r"TEXT:$f$ is decreasing on $(1, 3)$, so $f'(x) < 0$ on $(1, 3)$.", r"f(2) = 2 > 0",
                      r"TEXT:But $f$ is falling at $x = 2$, so $f'(2) < 0$."], at=[1, 2, 3], figure=hfig,
                     cues={0: lambda scene: scene.play(Create(fall), run_time=0.8),
                           1: lambda scene: scene.play(FadeIn(Dot(hax.c2p(2, 2), color=SECANT)), run_time=0.5)},
                     text=r"The graph of $f$ on $[0, 4]$ is shown. On what intervals is $f'$ negative? Is $f'(2)$ positive or negative?",
                     notes_graph=dict(fns=[("(x^3-6*x^2+9*x)/2+1", 0, 4)], xr=(0, 4), yr=(0, 4), ylabel="f(x)"))
        self.finish()
