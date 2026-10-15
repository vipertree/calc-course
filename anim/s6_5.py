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
        # the parent function on top, the graph being accumulated below (as in 5.9 and 6.4), each tagged and labeled
        top, tl = plot_axes([0, 7, 1], [-1, 4, 1], w=8.6, h=2.7, xlabel="x", ylabel="g")
        bot, bl = plot_axes([0, 7, 1], [-2, 2.5, 1], w=8.6, h=2.7, xlabel="t", ylabel="f")
        ttag = T("graph of $g$", 30, ACCUM).next_to(tl[1], RIGHT, buff=0.35)
        btag = T("graph of $f$", 30, FUNC).next_to(bl[1], RIGHT, buff=0.35)
        VGroup(top, tl, ttag).to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.6)
        VGroup(bot, bl, btag).next_to(VGroup(top, tl, ttag), DOWN, buff=0.45).align_to(top, LEFT)
        defn = M(r"g(x) = \int_0^x f(t)\,dt", 40, ACCUM).to_corner(UR, buff=0.5)
        X = ValueTracker(0.01)
        zs = [z for z in np.linspace(0, 7, 7001)[1:] if f(z - 0.001) * f(z) < 0]
        with self.beat("Rising and falling totals") as b:
            fc = bot.plot(f, x_range=[0, 7], color=FUNC, stroke_width=5)
            self.play(FadeIn(top), FadeIn(tl), FadeIn(ttag), FadeIn(bot), FadeIn(bl), FadeIn(btag), Create(fc), FadeIn(defn),
                      FadeIn(M("f(t)", 40, FUNC).move_to(bot.c2p(2.0, 2.0))), run_time=1.2)

            def shaded():
                xv = max(X.get_value(), 0.02)
                cuts = [0] + [z for z in zs if z < xv] + [xv]
                return VGroup(*[bot.get_area(bot.plot(f, x_range=[a, c]), x_range=[a, c], color=DERIV if f((a + c) / 2) > 0 else TANGENT, opacity=0.45)
                                for a, c in zip(cuts, cuts[1:]) if c - a > 0.01])
            self.add(always_redraw(shaded), always_redraw(lambda: top.plot(G, x_range=[0, max(X.get_value(), 0.02)], color=ACCUM, stroke_width=5)),
                     always_redraw(lambda: Dot(top.c2p(X.get_value(), G(X.get_value())), color=ACCUM)))
            self.bring_to_front(fc)
            b.line(1)
            self.play(X.animate.set_value(6.9), run_time=6, rate_func=linear)
            self.play(FadeIn(M("g(x)", 40, ACCUM).move_to(top.c2p(4.6, 3.3))), run_time=0.5)
            b.line(2)
            self.play(*[Create(DashedLine(bot.c2p(z, 0), top.c2p(z, G(z)), color=DIM)) for z in zs], run_time=1)
        self.clear()
        self.title()

        with self.beat("Read g from f") as b:
            head = M(r"g(x) = \int_a^x f(t)\,dt, \quad \text{so} \quad g' = f, \ \ g'' = f'", 44).to_edge(UP, buff=0.5)
            self.play(Write(head), run_time=1.2)
            # same layout as Topic 5.9's chart: the function on the left, its derivative (here the graph of f) on the right.
            # The definition above stays on screen (Adder: the chart used to cover it).
            rows = [(r"$g$ increasing", r"$f$ positive"), (r"$g$ decreasing", r"$f$ negative"), (r"$g$ has a relative max", r"$f$ changes sign, $+$ to $-$"),
                    (r"$g$ has a relative min", r"$f$ changes sign, $-$ to $+$"), (r"$g$ concave up", r"$f$ increasing"), (r"$g$ concave down", r"$f$ decreasing"),
                    (r"$g$ has an inflection point", r"$f$ has a max or min")]
            cells = VGroup(*[VGroup(T(l, 30, ACCUM), T(r, 30, FUNC)) for l, r in rows])
            for k, c in enumerate(cells):
                c[0].move_to(LEFT * 2.8 + UP * (1.45 - 0.56 * k))
                c[1].move_to(RIGHT * 2.6 + UP * (1.45 - 0.56 * k))
            hdr = VGroup(T("function $g$", 32, ACCUM).move_to(LEFT * 2.8 + UP * 2.15), T("graph of $f$, which is $g'$", 32, FUNC).move_to(RIGHT * 2.6 + UP * 2.15))
            rule = Line(LEFT * 5.6 + UP * 1.85, RIGHT * 5.6 + UP * 1.85, color=DIM)
            self.play(FadeIn(hdr), Create(rule), run_time=0.6)
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
            note = T("Topic 5.9's chart, one level up: $g$ plays $f$, and $f$ plays $f'$.", 30, DIM).to_edge(DOWN, buff=0.3)
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
        mark = lambda xv, yv, w: (lambda sc: sc.play(FadeIn(VGroup(Dot(ga.c2p(xv, yv), color=SECANT), T(w, 24, SECANT).next_to(ga.c2p(xv, yv), UR, buff=0.08))), run_time=0.5))
        self.example("Reading the graph of f",
                     r"The graph of $f$ on $[-4, 6]$ is a semicircle and two segments. Let $g(x) = \int_0^x f(t)\,dt$. (a) Find $g(2)$, $g(4)$, $g(6)$, $g(-4)$.",
                     [r"g(2) = -\tfrac12(2)(2) = -2", r"g(4) = -2 - 2 = -4", r"g(6) = -4 + 2 = -2", r"g(-4) = -\int_{-4}^{0} f(t)\,dt = -\tfrac12\pi(2)^2 = -2\pi",
                      r"PART:(b) Where does $g$ have relative extrema?", r"\text{rel. extrema of } g: \text{ where } g' = f \text{ changes sign}",
                      r"f: + \to - \text{ at } x = 0: \text{ rel. max}; \ \ - \to + \text{ at } x = 4: \text{ rel. min}",
                      r"PART:(c) Absolute max and min of $g$ on $[-4, 6]$?", r"g(-4) = -2\pi \approx -6.28, \ g(0) = 0, \ g(4) = -4, \ g(6) = -2",
                      r"\text{abs. max } 0 \text{ at } x = 0; \ \ \text{abs. min } -2\pi \text{ at } x = -4",
                      r"PART:(d) Inflection points of $g$?", r"\text{inflection points of } g: \text{ where } g'' = f' \text{ changes sign}",
                      r"f \text{ turns at } x = -2 \text{ and } x = 2: \text{ inflection points of } g"],
                     at=[1, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10, 11, 11], figure=fig,
                     cues={0: sh(A1), 1: sh(A2), 2: sh(A3), 3: sh(A0), 6: lambda sc: (mark(0, 0, "max")(sc), mark(4, 0, "min")(sc)),
                           12: lambda sc: sc.play(Indicate(VGroup(Dot(ga.c2p(-2, 2)), Dot(ga.c2p(2, -2))), color=SECANT), FadeIn(Dot(ga.c2p(-2, 2), color=SECANT)),
                                                  FadeIn(Dot(ga.c2p(2, -2), color=SECANT)), run_time=0.8)},
                     text=r"The graph of $f$ on $[-4, 6]$ consists of the upper half of the circle of radius $2$ centered at $(-2, 0)$, a segment from $(0, 0)$ to "
                          r"$(2, -2)$, and a segment from $(2, -2)$ to $(6, 2)$. Let $g(x) = \int_0^x f(t)\,dt$. (a) Find $g(2)$, $g(4)$, $g(6)$ and $g(-4)$. "
                          r"(b) Where does $g$ have relative extrema? (c) Find the absolute maximum and minimum values of $g$ on $[-4, 6]$. (d) Find the inflection points of $g$.",
                     notes_graph=dict(fns=[("sqrt(abs(4-(x+2)^2))", -4, 0), ("-x", 0, 2), ("x-4", 2, 6)], xr=(-4, 6), yr=(-3, 3), ylabel="f(t)", xlabel="t"), follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"g(x) = \int_a^x f(t)\,dt, \quad \text{so} \quad g' = f, \ \ g'' = f'", 44, ACCUM),
                          T(r"Increasing, decreasing, relative extrema of $g$: the sign of $f$.", 32),
                          T(r"Concavity and inflection points of $g$: $f$ rising or falling.", 32),
                          T("Values of $g$: areas, with area below the axis counted as negative. Backward limits flip the sign.", 32)).arrange(DOWN, buff=0.5)
            card.set_max_width(12.6)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        c1 = staged_chart([-2, 2], ["+", "-", "+"], words=["inc", "dec", "inc"], name="g'", width=7)
        self.example("Example 1: A formula for f", r"$g(x) = \displaystyle\int_0^x \left(t^2 - 4\right) dt$. Find where $g$ is increasing and where it has relative extrema.",
                     [r"\text{increasing: } g'(x) > 0", r"\text{rel. extrema: } g' \text{ changes sign}",
                      r"g'(x) = x^2 - 4 \ \ \text{(FTC)}", r"(x - 2)(x + 2) = 0, \ \ x = \pm 2", r"g'(-3) = 9 - 4 = 5 > 0", r"g'(0) = -4 < 0", r"g'(3) = 9 - 4 = 5 > 0",
                      r"\text{increasing on } (-\infty, -2),\ (2, \infty)", r"\text{rel. max at } x = -2, \ \ \text{rel. min at } x = 2"], at=[1, 1, 2, 3, 4, 5, 6, 7, 7],
                     figure=c1, figure_at=3, cues={4: reveal_sign(c1, 0), 5: reveal_sign(c1, 1), 6: lambda sc: (reveal_sign(c1, 2)(sc), reveal_words(c1)(sc)),
                                                   8: lambda sc: (mark_point(c1, 0, "max")(sc), mark_point(c1, 1, "min")(sc))})
        self.example("Example 2: A tangent line to g", r"$g(x) = \displaystyle\int_1^x \sqrt{t + 3}\,dt$. Write an equation for the line tangent to the graph of $g$ at $x = 1$.",
                     [r"\text{point: } g(1) = \int_1^1 \sqrt{t + 3}\,dt = 0, \ \ (1, 0)", r"g'(x) = \sqrt{x + 3}", r"\text{slope: } m = g'(1) = \sqrt4 = 2",
                      r"\boxed{\text{point } (1, 0), \ \ \text{slope } m = 2}", r"y - 0 = 2(x - 1)", r"y = 2(x - 1)"], at=[1, 2, 2, 3, 4, 4])
        ca, cl = plot_axes([0, 6, 1], [-3, 5, 1], w=4.6, h=3.6, xlabel="t", ylabel="f(t)")
        up_seg, dn_seg = Line(ca.c2p(0, -2), ca.c2p(3, 4), color=FUNC, stroke_width=4), Line(ca.c2p(3, 4), ca.c2p(6, 1), color=FUNC, stroke_width=4)
        cfig = VGroup(ca, cl, up_seg, dn_seg)
        self.example("Example 3: Concavity from a graph",
                     r"The graph of $f$ is shown. Let $g(x) = \int_0^x f(t)\,dt$. On what intervals is $g$ concave up? Concave down?",
                     [r"\text{concave up: } g'' > 0; \ \ \text{concave down: } g'' < 0", r"g' = f \ \text{(FTC)}, \ \text{so} \ g'' = f'",
                      r"\text{look at the slope of } f", r"f \text{ increasing on } (0, 3): \ g \text{ concave up}",
                      r"f \text{ decreasing on } (3, 6): \ g \text{ concave down, inflection at } x = 3"], at=[1, 2, 3, 4, 5], figure=cfig,
                     cues={3: lambda sc: sc.play(up_seg.animate.set_color(DERIV), run_time=0.5), 4: lambda sc: sc.play(dn_seg.animate.set_color(TANGENT), run_time=0.5)},
                     text=r"The graph of $f$ consists of a segment from $(0, -2)$ to $(3, 4)$ and a segment from $(3, 4)$ to $(6, 1)$. Let $g(x) = \int_0^x f(t)\,dt$. "
                          r"On what intervals is the graph of $g$ concave up? Concave down?",
                     notes_graph=dict(fns=[("2*x-2", 0, 3), ("4-(x-3)", 3, 6)], xr=(0, 6), yr=(-3, 5), ylabel="f(t)", xlabel="t"))
        self.finish()
