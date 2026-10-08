"""Topic 6.1: Exploring accumulations of change. Narration comes from transcripts/6_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def shade(ax, f, a, b, color=AREA, opacity=0.45):
    """The region between the graph of f and the t-axis on [a, b]."""
    return ax.get_area(ax.plot(f, x_range=[a, b]), x_range=[a, b], color=color, opacity=opacity)


class Lesson(TranscriptScene):
    NUM = "6.1"

    def construct(self):
        tank, water = water_tank(2.2, 3.2)
        tank.to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        ax, al = plot_axes([0, 5, 1], [0, 4, 1], w=6.4, h=4.2, xlabel="t\\ (\\text{min})", ylabel="\\text{rate (gal/min)}")
        VGroup(ax, al).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        T0 = ValueTracker(0.001)
        with self.beat("Filling a tank") as b:
            self.play(FadeIn(tank), FadeIn(ax), FadeIn(al), Create(ax.plot(lambda t: 3, x_range=[0, 4.6], color=FUNC, stroke_width=5)), run_time=1.2)
            wat = always_redraw(lambda: water(T0.get_value() * 3 / 16).move_to(tank[0], aligned_edge=DOWN).shift(UP * 0.04))
            rect = always_redraw(lambda: Rectangle(width=ax.c2p(T0.get_value(), 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 3)[1] - ax.c2p(0, 0)[1],
                                                   stroke_width=0, fill_color=AREA, fill_opacity=0.45).move_to(ax.c2p(0, 0), aligned_edge=DL))
            read = always_redraw(lambda: M(rf"\text{{water added}} = 3 \times {T0.get_value():.1f} = {3 * T0.get_value():.1f}\ \text{{gal}}", 32, ACCUM)
                                 .next_to(ax, UP, buff=0.3))
            self.add(wat, rect, read)
            self.play(T0.animate.set_value(4), run_time=4, rate_func=linear)
            b.line(1)
            self.play(Indicate(read, color=ACCUM), run_time=1)
            b.line(2)
            self.play(Circumscribe(rect, color=SECANT), run_time=1.2)
        # the title card sits between the opening and the next beat, which builds on the same graph
        opening = list(self.mobjects)
        self.play(*[FadeOut(m) for m in opening], run_time=0.5)
        self.title()
        self.play(*[FadeIn(m) for m in opening], run_time=0.5)

        with self.beat("Area means amount") as b:
            self.play(FadeOut(tank), FadeOut(wat), FadeOut(read), run_time=0.5)
            hl = M(r"3\ \text{gal/min}", 30, FUNC).next_to(ax.c2p(4, 1.5), RIGHT, buff=0.15)
            wl = M(r"4\ \text{min}", 30, FUNC).next_to(ax.c2p(2, 0), DOWN, buff=0.45)
            self.play(FadeIn(hl), FadeIn(wl), run_time=0.6)
            b.line(1)
            prod = M(r"(3\ \tfrac{\text{gal}}{\text{min}})(4\ \text{min})", r"= 12\ \text{gal}", 40).to_edge(LEFT, buff=0.7).shift(UP * 1.6)
            self.play(Write(prod), run_time=1.2)
            cancel = T("the minutes cancel", 30, DIM).next_to(prod, DOWN, buff=0.25).align_to(prod, LEFT)
            self.play(FadeIn(cancel), run_time=0.6)
            b.line(2)
            rule = VGroup(formula_box(T("area under a rate graph = amount of change", 32, ACCUM), ACCUM),
                          T("units: (rate units) $\\times$ (time units)", 30, DIM)).arrange(DOWN, buff=0.3).next_to(cancel, DOWN, buff=0.6).to_edge(LEFT, buff=0.5)
            rule[0].set_max_width(6.2)
            self.play(FadeIn(rule), run_time=0.8)
        self.clear()

        tank, water = water_tank(2.2, 3.2)
        tank.to_edge(LEFT, buff=1.0).shift(DOWN * 0.3)
        ax, al = plot_axes([0, 5, 1], [0, 7, 1], w=6.4, h=4.4, xlabel="t", ylabel="r")
        VGroup(ax, al).to_edge(RIGHT, buff=0.6).shift(DOWN * 0.2)
        T1 = ValueTracker(0.001)
        with self.beat("When the rate changes") as b:
            self.play(FadeIn(tank), FadeIn(ax), FadeIn(al), Create(ax.plot(lambda t: 2 + t, x_range=[0, 4.6], color=FUNC, stroke_width=5)), run_time=1.2)
            self.add(always_redraw(lambda: water((2 * T1.get_value() + T1.get_value() ** 2 / 2) / 20).move_to(tank[0], aligned_edge=DOWN).shift(UP * 0.04)))
            self.add(always_redraw(lambda: shade(ax, lambda t: 2 + t, 0, max(T1.get_value(), 0.01))))
            b.line(1)
            self.play(T1.animate.set_value(4), run_time=3, rate_func=linear)
            labs = VGroup(M("2", 30).next_to(ax.c2p(0, 2), LEFT, buff=0.15), M("6", 30).next_to(ax.c2p(4, 6), UR, buff=0.1),
                          DashedLine(ax.c2p(4, 0), ax.c2p(4, 6), color=DIM))
            self.play(FadeIn(labs), run_time=0.6)
            b.line(2)
            calc = M(r"\frac{2 + 6}{2} \cdot 4 = 16\ \text{gal}", 40, ACCUM).next_to(ax, UP, buff=0.2)
            self.play(Write(calc), run_time=1.2)
        self.clear()

        ax, al = plot_axes([0, 8, 1], [-2, 3, 1], w=8, h=3.4, xlabel="t\\ (\\text{s})", ylabel="v\\ (\\text{m/s})")
        VGroup(ax, al).to_edge(UP, buff=0.5)
        v = lambda t: 2 if t < 3 else -1
        with self.beat("Below the axis") as b:
            graph = VGroup(Line(ax.c2p(0, 2), ax.c2p(3, 2), color=FUNC, stroke_width=5), Line(ax.c2p(3, -1), ax.c2p(7, -1), color=FUNC, stroke_width=5))
            self.play(FadeIn(ax), FadeIn(al), Create(graph), run_time=1.2)
            b.line(1)
            up_r = Rectangle(width=ax.c2p(3, 0)[0] - ax.c2p(0, 0)[0], height=ax.c2p(0, 2)[1] - ax.c2p(0, 0)[1], stroke_width=0, fill_color=DERIV, fill_opacity=0.45).move_to(ax.c2p(0, 0), aligned_edge=DL)
            dn_r = Rectangle(width=ax.c2p(7, 0)[0] - ax.c2p(3, 0)[0], height=ax.c2p(0, 0)[1] - ax.c2p(0, -1)[1], stroke_width=0, fill_color=TANGENT, fill_opacity=0.45).move_to(ax.c2p(3, 0), aligned_edge=UL)
            nl = NumberLine(x_range=[0, 7, 1], length=7, color=DIM, include_numbers=True, font_size=24).to_edge(DOWN, buff=1.4)
            P = ValueTracker(0)
            walker = always_redraw(lambda: Dot(nl.n2p(P.get_value()), color=SECANT, radius=0.12))
            self.play(FadeIn(up_r), FadeIn(M("+6", 36, DERIV).move_to(up_r)), FadeIn(nl), FadeIn(walker), run_time=0.8)
            self.play(P.animate.set_value(6), run_time=1.6)
            self.play(FadeIn(dn_r), FadeIn(M("-4", 36, TANGENT).move_to(dn_r)), run_time=0.6)
            self.play(P.animate.set_value(2), run_time=1.6)
            b.line(2)
            net = M(r"\text{net change: } 6 - 4 = 2\ \text{m}", 36, ACCUM).to_edge(DOWN, buff=0.4).shift(LEFT * 3)
            self.play(FadeIn(net), run_time=0.6)
            b.line(3)
            tot = M(r"\text{total distance: } 6 + 4 = 10\ \text{m}", 36, SECANT).to_edge(DOWN, buff=0.4).shift(RIGHT * 3)
            self.play(FadeIn(tot), run_time=0.6)
        self.clear()

        ra, rl = plot_axes([0, 8, 1], [0, 0.5, 0.1], w=5.6, h=3.4, xlabel="t", ylabel="r")
        rain = lambda t: 0.2 * t if t < 2 else (0.4 if t < 6 else 0.4 - 0.2 * (t - 6))
        rfig = VGroup(ra, rl, ra.plot(rain, x_range=[0, 8, 0.01], color=FUNC, stroke_width=4))
        pieces = [shade(ra, rain, 0, 2), shade(ra, rain, 2, 6, color=ACCUM), shade(ra, rain, 6, 8)]
        self.example("Reading the area", r"Rain falls at the rate $r(t)$ shown, in inches per hour. How much rain fell from $t = 0$ to $t = 8$ hours?",
                     [r"\text{units: } \left(\tfrac{\text{in}}{\text{hr}}\right)(\text{hr}) = \text{in}", r"TEXT:Split into a triangle, a rectangle and a triangle.",
                      r"\tfrac12(2)(0.4) = 0.4", r"(4)(0.4) = 1.6", r"\tfrac12(2)(0.4) = 0.4", r"0.4 + 1.6 + 0.4 = 2.4 \text{ inches}"],
                     at=[1, 2, 3, 4, 5, 6], figure=rfig,
                     cues={k: (lambda m: lambda sc: sc.play(FadeIn(m), run_time=0.6))(pieces[k - 2]) for k in (2, 3, 4)},
                     text=r"Rain falls at the rate $r(t)$, in inches per hour, shown in the graph: $r$ rises steadily from $0$ to $0.4$ over the first $2$ hours, "
                          r"stays at $0.4$ until $t = 6$, then falls steadily to $0$ at $t = 8$. How much rain fell from $t = 0$ to $t = 8$ hours?",
                     notes_graph=dict(fns=[("0.2*x", 0, 2), ("0.4+0*x", 2, 6), ("0.4-0.2*(x-6)", 6, 8)], xr=(0, 8), yr=(0, 0.5), ystep=0.1, xlabel="t", ylabel="r(t)"))

        with self.beat("Close") as b:
            card = VGroup(T("Area under a rate graph = amount of change.", 40, ACCUM), T(r"Units: (rate units) $\times$ (time units).", 36),
                          T("Above the axis adds; below the axis subtracts.", 36), T("Total distance: add all the areas.", 36, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: What the area means",
                     r"$B(t)$ is the rate, in loaves per hour, at which a bakery sells bread, $t$ hours after it opens. What does the area under the graph of $B$ from $t = 0$ to $t = 3$ represent?",
                     [r"\text{height: loaves per hour; width: hours}", r"\left(\tfrac{\text{loaves}}{\text{hour}}\right)(\text{hours}) = \text{loaves}",
                      r"TEXT:The total number of loaves sold in the first $3$ hours after opening."], at=[1, 2, 3])
        va, vl = plot_axes([0, 4, 1], [-5, 5, 1], w=4.6, h=3.8, xlabel="t", ylabel="v")
        vfig = VGroup(va, vl, va.plot(lambda t: 4 - 2 * t, x_range=[0, 4], color=FUNC, stroke_width=4))
        tri_up, tri_dn = shade(va, lambda t: 4 - 2 * t, 0, 2, DERIV), shade(va, lambda t: 4 - 2 * t, 2, 4, TANGENT)
        self.example("Example 2: Net change and distance",
                     r"A particle's velocity is $v(t) = 4 - 2t$ meters per second for $0 \le t \le 4$. Find its displacement and the total distance it travels.",
                     [r"4 - 2t = 0, \ \ t = 2", r"\text{above: } \tfrac12(2)(4) = 4", r"\text{below: } \tfrac12(2)(4) = 4, \text{ counts negative}",
                      r"\text{displacement: } 4 - 4 = 0 \text{ m}", r"\text{distance: } 4 + 4 = 8 \text{ m}"], at=[1, 2, 3, 4, 5], figure=vfig,
                     cues={1: lambda sc: sc.play(FadeIn(tri_up), run_time=0.6), 2: lambda sc: sc.play(FadeIn(tri_dn), run_time=0.6)})
        da, dl = plot_axes([0, 5, 1], [0, 11, 2], w=4.6, h=3.8, xlabel="t", ylabel="r")
        dfig = VGroup(da, dl, da.plot(lambda t: 10 - 2 * t, x_range=[0, 5], color=FUNC, stroke_width=4))
        tri = shade(da, lambda t: 10 - 2 * t, 0, 5)
        self.example("Example 3: Draining a tank",
                     r"Water drains from a tank at $r(t) = 10 - 2t$ liters per minute for $0 \le t \le 5$. The tank held $60$ liters at $t = 0$. How much water is in the tank at $t = 5$?",
                     [r"\text{area} = \text{amount drained}", r"\tfrac12(5)(10) = 25 \text{ L}", r"60 - 25 = 35 \text{ L}"], at=[1, 3, 4], figure=dfig,
                     cues={1: lambda sc: sc.play(FadeIn(tri), run_time=0.6)})
        self.finish()
