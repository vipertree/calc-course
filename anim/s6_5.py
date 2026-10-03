"""Topic 6.5: Interpreting the behavior of accumulation functions. Narration comes from transcripts/6_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "6.5"

    def construct(self):
        f = lambda s: 1.6 * np.sin(1.1 * s) + 0.3
        G = lambda s: 1.6 * (1 - np.cos(1.1 * s)) / 1.1 + 0.3 * s
        top, tl = plot_axes([0, 7, 1], [-2, 2.5, 1], w=9.4, h=2.7, xlabel="t", ylabel="f")
        bot, bl = plot_axes([0, 7, 1], [-1, 4, 1], w=9.4, h=2.7, xlabel="x", ylabel="g")
        VGroup(top, tl).to_edge(UP, buff=0.4)
        VGroup(bot, bl).next_to(VGroup(top, tl), DOWN, buff=0.5)
        X = ValueTracker(0.01)
        zs = [z for z in np.linspace(0, 7, 7001)[1:] if f(z - 0.001) * f(z) < 0]
        with self.beat("Rising and falling totals") as b:
            self.play(FadeIn(top), FadeIn(tl), FadeIn(bot), FadeIn(bl), Create(top.plot(f, x_range=[0, 7], color=FUNC, stroke_width=5)), run_time=1.2)

            def shaded():
                xv = max(X.get_value(), 0.02)
                cuts = [0] + [z for z in zs if z < xv] + [xv]
                return VGroup(*[top.get_area(top.plot(f, x_range=[a, c]), x_range=[a, c], color=DERIV if f((a + c) / 2) > 0 else TANGENT, opacity=0.45)
                                for a, c in zip(cuts, cuts[1:]) if c - a > 0.01])
            self.add(always_redraw(shaded), always_redraw(lambda: bot.plot(G, x_range=[0, max(X.get_value(), 0.02)], color=ACCUM, stroke_width=5)),
                     always_redraw(lambda: Dot(bot.c2p(X.get_value(), G(X.get_value())), color=ACCUM)))
            b.line(1)
            self.play(X.animate.set_value(6.9), run_time=6, rate_func=linear)
            b.line(2)
            self.play(*[Create(DashedLine(top.c2p(z, 0), bot.c2p(z, G(z)), color=DIM)) for z in zs], run_time=1)
        self.clear()
        self.title()

        with self.beat("Read g from f") as b:
            head = M(r"g(x) = \int_a^x f(t)\,dt, \quad \text{so} \quad g' = f, \ \ g'' = f'", 44).to_edge(UP, buff=0.5)
            self.play(Write(head), run_time=1.2)
            rows = [(r"$f$ positive", r"$g$ increasing"), (r"$f$ negative", r"$g$ decreasing"), (r"$f$ changes sign, $+$ to $-$", r"$g$ has a relative max"),
                    (r"$f$ changes sign, $-$ to $+$", r"$g$ has a relative min"), (r"$f$ increasing", r"$g$ concave up"), (r"$f$ decreasing", r"$g$ concave down"),
                    (r"$f$ has a max or min", r"$g$ has an inflection point")]
            cells = VGroup(*[VGroup(T(l, 30, FUNC), T(r, 30, ACCUM)) for l, r in rows])
            for k, c in enumerate(cells):
                c[0].move_to(LEFT * 2.8 + UP * (1.9 - 0.62 * k))
                c[1].move_to(RIGHT * 2.6 + UP * (1.9 - 0.62 * k))
            hdr = VGroup(T("graph of $f$", 32, FUNC).move_to(LEFT * 2.8 + UP * 2.6), T("$g$", 32, ACCUM).move_to(RIGHT * 2.6 + UP * 2.6))
            rule = Line(LEFT * 5.6 + UP * 2.3, RIGHT * 5.6 + UP * 2.3, color=DIM)
            self.play(FadeOut(head), FadeIn(hdr), Create(rule), run_time=0.6)
            b.line(1)
            self.play(FadeIn(cells[0]), run_time=0.5)
            self.play(FadeIn(cells[1]), run_time=0.5)
            b.line(2)
            self.play(FadeIn(cells[2]), run_time=0.5)
            self.play(FadeIn(cells[3]), run_time=0.5)
            b.line(3)
            for k in (4, 5, 6):
                self.play(FadeIn(cells[k]), run_time=0.5)
            b.line(4)
            note = T("Topic 5.9's chart, one level up: $g$ plays $f$, and $f$ plays $f'$.", 30, DIM).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(note), run_time=0.6)
        self.clear()

        ga, gl = plot_axes([-4, 6, 1], [-3, 3, 1], w=6, h=3.6, xlabel="t", ylabel="f(t)")
        semi = lambda s: np.sqrt(max(4 - (s + 2) ** 2, 0))
        pcs = VGroup(ga.plot(semi, x_range=[-4, 0, 0.01], color=FUNC, stroke_width=4), Line(ga.c2p(0, 0), ga.c2p(2, -2), color=FUNC, stroke_width=4),
                     Line(ga.c2p(2, -2), ga.c2p(6, 2), color=FUNC, stroke_width=4))
        fig = VGroup(ga, gl, pcs)
        A1 = Polygon(ga.c2p(0, 0), ga.c2p(2, 0), ga.c2p(2, -2), stroke_width=0, fill_color=TANGENT, fill_opacity=0.45)
        A2 = Polygon(ga.c2p(2, 0), ga.c2p(4, 0), ga.c2p(2, -2), stroke_width=0, fill_color=TANGENT, fill_opacity=0.45)
        A3 = Polygon(ga.c2p(4, 0), ga.c2p(6, 0), ga.c2p(6, 2), stroke_width=0, fill_color=DERIV, fill_opacity=0.45)
        A0 = ga.get_area(ga.plot(semi, x_range=[-4, 0, 0.01]), x_range=[-4, 0], color=DERIV, opacity=0.45)
        sh = lambda m: (lambda sc: sc.play(FadeIn(m), run_time=0.5))
        mark = lambda xv, yv, w: (lambda sc: sc.play(FadeIn(VGroup(Dot(ga.c2p(xv, yv), color=SECANT), T(w, 24, SECANT).next_to(ga.c2p(xv, yv), UP, buff=0.12))), run_time=0.5))
        self.example("Reading the graph of f",
                     r"The graph of $f$ on $[-4, 6]$ is a semicircle and two segments. Let $g(x) = \int_0^x f(t)\,dt$. (a) Find $g(2)$, $g(4)$, $g(6)$, $g(-4)$.",
                     [r"g(2) = -\tfrac12(2)(2) = -2", r"g(4) = -2 - 2 = -4", r"g(6) = -4 + 2 = -2", r"g(-4) = -\int_{-4}^{0} f(t)\,dt = -\tfrac12\pi(2)^2 = -2\pi",
                      r"PART:(b) Where does $g$ have relative extrema?", r"f: + \to - \text{ at } x = 0: \text{ rel. max}; \ \ - \to + \text{ at } x = 4: \text{ rel. min}",
                      r"PART:(c) Absolute max and min of $g$ on $[-4, 6]$?", r"g(-4) = -2\pi \approx -6.28, \ g(0) = 0, \ g(4) = -4, \ g(6) = -2",
                      r"\text{abs. max } 0 \text{ at } x = 0; \ \ \text{abs. min } -2\pi \text{ at } x = -4",
                      r"PART:(d) Inflection points of $g$?", r"f \text{ turns at } x = -2 \text{ and } x = 2: \text{ inflection points of } g"],
                     at=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], figure=fig,
                     cues={0: sh(A1), 1: sh(A2), 2: sh(A3), 3: sh(A0), 5: lambda sc: (mark(0, 0, "max")(sc), mark(4, 0, "min")(sc)),
                           10: lambda sc: sc.play(Indicate(VGroup(Dot(ga.c2p(-2, 2)), Dot(ga.c2p(2, -2))), color=SECANT), FadeIn(Dot(ga.c2p(-2, 2), color=SECANT)),
                                                  FadeIn(Dot(ga.c2p(2, -2), color=SECANT)), run_time=0.8)},
                     text=r"The graph of $f$ on $[-4, 6]$ consists of the upper half of the circle of radius $2$ centered at $(-2, 0)$, a segment from $(0, 0)$ to "
                          r"$(2, -2)$, and a segment from $(2, -2)$ to $(6, 2)$. Let $g(x) = \int_0^x f(t)\,dt$. (a) Find $g(2)$, $g(4)$, $g(6)$ and $g(-4)$. "
                          r"(b) Where does $g$ have relative extrema? (c) Find the absolute maximum and minimum values of $g$ on $[-4, 6]$. (d) Find the inflection points of $g$.",
                     notes_graph=dict(fns=[("sqrt(abs(4-(x+2)^2))", -4, 0), ("-x", 0, 2), ("x-4", 2, 6)], xr=(-4, 6), yr=(-3, 3), ylabel="f(t)", xlabel="t"))

        with self.beat("Close") as b:
            card = VGroup(T(r"$g' = f$: the sign of $f$ gives $g$'s direction; its sign changes give $g$'s extrema.", 32),
                          T(r"$g'' = f'$: $f$ rising or falling gives $g$'s concavity; peaks and valleys of $f$ give inflection points.", 32),
                          T("Values of $g$: signed areas. Backward limits flip the sign.", 32, ACCUM)).arrange(DOWN, buff=0.5)
            card.set_max_width(12.6)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        c1 = staged_chart([-2, 2], ["+", "-", "+"], words=["inc", "dec", "inc"], name="g'", width=7)
        self.example("Example 1: A formula for f", r"$g(x) = \displaystyle\int_0^x \left(t^2 - 4\right) dt$. Find where $g$ is increasing and where it has relative extrema.",
                     [r"g'(x) = x^2 - 4 \ \ \text{(FTC)}", r"(x - 2)(x + 2) = 0, \ \ x = \pm 2", r"g'(-3) = 9 - 4 = 5 > 0", r"g'(0) = -4 < 0", r"g'(3) = 9 - 4 = 5 > 0",
                      r"\text{increasing on } (-\infty, -2),\ (2, \infty)", r"\text{rel. max at } x = -2, \ \ \text{rel. min at } x = 2"], at=[1, 2, 3, 4, 5, 6, 6],
                     figure=c1, figure_at=2, cues={2: reveal_sign(c1, 0), 3: reveal_sign(c1, 1), 4: lambda sc: (reveal_sign(c1, 2)(sc), reveal_words(c1)(sc)),
                                                   6: lambda sc: (mark_point(c1, 0, "max")(sc), mark_point(c1, 1, "min")(sc))})
        self.example("Example 2: A tangent line to g", r"$g(x) = \displaystyle\int_1^x \sqrt{t + 3}\,dt$. Write an equation for the line tangent to the graph of $g$ at $x = 1$.",
                     [r"g(1) = \int_1^1 \sqrt{t + 3}\,dt = 0", r"g'(x) = \sqrt{x + 3}", r"g'(1) = \sqrt4 = 2", r"y - 0 = 2(x - 1), \ \ y = 2(x - 1)"], at=[1, 2, 2, 3])
        ca, cl = plot_axes([0, 6, 1], [-3, 5, 1], w=4.6, h=3.6, xlabel="t", ylabel="f(t)")
        up_seg, dn_seg = Line(ca.c2p(0, -2), ca.c2p(3, 4), color=FUNC, stroke_width=4), Line(ca.c2p(3, 4), ca.c2p(6, 1), color=FUNC, stroke_width=4)
        cfig = VGroup(ca, cl, up_seg, dn_seg)
        self.example("Example 3: Concavity from a graph",
                     r"The graph of $f$ is shown. Let $g(x) = \int_0^x f(t)\,dt$. On what intervals is $g$ concave up? Concave down?",
                     [r"g'' = f' \ \ \text{(is } f \text{ rising or falling?)}", r"f \text{ increasing on } (0, 3): \ g \text{ concave up}",
                      r"f \text{ decreasing on } (3, 6): \ g \text{ concave down, inflection at } x = 3"], at=[1, 2, 3], figure=cfig,
                     cues={1: lambda sc: sc.play(up_seg.animate.set_color(DERIV), run_time=0.5), 2: lambda sc: sc.play(dn_seg.animate.set_color(TANGENT), run_time=0.5)},
                     text=r"The graph of $f$ consists of a segment from $(0, -2)$ to $(3, 4)$ and a segment from $(3, 4)$ to $(6, 1)$. Let $g(x) = \int_0^x f(t)\,dt$. "
                          r"On what intervals is the graph of $g$ concave up? Concave down?",
                     notes_graph=dict(fns=[("2*x-2", 0, 3), ("4-(x-3)", 3, 6)], xr=(0, 6), yr=(-3, 5), ylabel="f(t)", xlabel="t"))
        self.finish()
