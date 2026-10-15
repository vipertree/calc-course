"""Topic 6.4: The Fundamental Theorem of Calculus and accumulation functions. Narration comes from transcripts/6_4.md.

Adder's 6.4 rewrite (2026-10-14): the accumulation function is big F; F(1) and F(2) worked as triangle areas; F graphed as
a function of its own; the theorem shown with both graphs (F on top, f below) and a nudge; fanfare; plain substitution
examples before any chain rule, and the first chain-rule example names the inner function g(x). Every graph carries a
"graph of F" / "graph of f" tag and a large curve label, so it is always clear which level we are looking at.
"""
import os

import numpy as np
from manim import *

from kit import *
from style import *

# the rule kept in the corner during the examples (formulas stay on screen)
REF_FTC = r"\begin{array}{c} F(x) = \int_a^x f(t)\,dt \\ \text{so } F'(x) = f(x) \end{array}"
REF_CHAIN = r"\begin{array}{c} F(x) = \int_a^x f(t)\,dt \\ \tfrac{d}{dx}F(g(x)) = F'(g(x)) \cdot g'(x) \end{array}"


def stack(xr, yF, yf, w=8.0, hF=2.7, hf=2.3, coords=True, Flab="F", flab="f"):
    """F's graph on top, f's graph below, on one x-scale, each tagged with which graph it is (Adder: always make clear
    which level we are looking at). Returns (top, top_labels, top_tag, bot, bot_labels, bot_tag), placed at the left."""
    top, tl = plot_axes(xr, yF, w=w, h=hF, coords=coords, xlabel="x", ylabel=Flab)
    bot, bl = plot_axes(xr, yf, w=w, h=hf, coords=coords, xlabel="t", ylabel=flab)
    ttag = T("graph of $F$", 30, ACCUM).next_to(tl[1], RIGHT, buff=0.35)
    btag = T("graph of $f$", 30, FUNC).next_to(bl[1], RIGHT, buff=0.35)
    up, down = VGroup(top, tl, ttag), VGroup(bot, bl, btag)
    up.to_edge(UP, buff=0.3).to_edge(LEFT, buff=0.6)
    down.next_to(up, DOWN, buff=0.45)
    down.shift(RIGHT * (top.c2p(xr[0], 0)[0] - bot.c2p(xr[0], 0)[0]))
    return top, tl, ttag, bot, bl, btag


class Lesson(TranscriptScene):
    NUM = "6.4"

    def construct(self):
        f = lambda s: 1 + 0.5 * np.sin(1.3 * s) + 0.15 * s
        F = lambda s: s + 0.5 * (1 - np.cos(1.3 * s)) / 1.3 + 0.075 * s * s     # the exact running total of f from 0
        defn = M(r"F(x) = \int_0^x f(t)\,dt", 44, ACCUM).to_corner(UR, buff=0.5)

        # ---------------------------------------------------------------- cold open: F traced on top of f
        top, tl, ttag, bot, bl, btag = stack([0, 6, 1], [0, 9, 3], [0, 3, 1])
        X = ValueTracker(0.01)
        with self.beat("A running total") as b:
            fcurve = bot.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)
            flab = M("f(t)", 44, FUNC).move_to(bot.c2p(3.5, 1.9))
            self.play(FadeIn(bot), FadeIn(bl), FadeIn(btag), Create(fcurve), FadeIn(flab), FadeIn(defn), run_time=1.2)
            # the shading is built on the plotted curve itself, so it always matches the graph
            region = always_redraw(lambda: bot.get_area(bot.plot(f, x_range=[0, max(X.get_value(), 0.02)]), x_range=[0, max(X.get_value(), 0.02)],
                                                        color=AREA, opacity=0.5))
            mark = always_redraw(lambda: DashedLine(bot.c2p(X.get_value(), 0), bot.c2p(X.get_value(), f(X.get_value())), color=SECANT))
            xl = always_redraw(lambda: M("x", 30, SECANT).next_to(bot.c2p(X.get_value(), 0), DOWN, buff=0.12))
            self.add(region, mark, xl)
            self.bring_to_front(fcurve)
            self.play(X.animate.set_value(1.5), run_time=1.2)
            b.line(1)
            self.play(FadeIn(top), FadeIn(tl), FadeIn(ttag), run_time=0.5)
            trace = always_redraw(lambda: top.plot(F, x_range=[0, max(X.get_value(), 0.02)], color=ACCUM, stroke_width=5))
            pen = always_redraw(lambda: Dot(top.c2p(X.get_value(), F(X.get_value())), color=ACCUM))
            self.add(trace, pen)
            self.play(X.animate.set_value(5.8), run_time=5, rate_func=linear)
            self.play(FadeIn(M("F(x)", 44, ACCUM).move_to(top.c2p(2.4, 6.4))), run_time=0.6)
            b.line(2)
            self.play(Indicate(defn, color=ACCUM), run_time=1)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- the definition
        with self.beat("Accumulation functions") as b:
            eq = M(r"F(x)", r"=", r"\int_a^x", r"f(t)\,dt", 72).to_edge(UP, buff=0.8)
            eq[0].set_color(ACCUM)
            self.play(Write(eq), run_time=1.2)
            b.line(1)
            la = T("$a$: a fixed start", 30, SECANT).next_to(eq[2], DL, buff=0.25)
            lx = T("$x$: the moving end, the input of $F$", 30, SECANT).next_to(eq[2], UR, buff=0.15).shift(RIGHT * 0.6)
            self.play(FadeIn(la), FadeIn(lx), run_time=0.8)
            b.line(2)
            lt = T("$t$: runs from $a$ to $x$", 30, FUNC).next_to(eq[3], DOWN, buff=0.35)
            self.play(FadeIn(lt), run_time=0.6)
            mini, _ = plot_axes([0, 5, 1], [0, 3, 1], w=4.6, h=2.4, coords=False)
            g = lambda s: 1.2 + 0.3 * np.sin(s)
            gc = mini.plot(g, x_range=[0, 5], color=FUNC, stroke_width=4)
            pic = VGroup(mini, mini.get_area(mini.plot(g, x_range=[1, 3.5]), x_range=[1, 3.5], color=AREA, opacity=0.5), gc,
                         M("a", 28).next_to(mini.c2p(1, 0), DOWN, buff=0.1), M("x", 28, SECANT).next_to(mini.c2p(3.5, 0), DOWN, buff=0.1),
                         M("f(t)", 36, FUNC).next_to(mini.c2p(4.6, g(4.6)), UP, buff=0.15)).shift(DOWN * 1.3 + LEFT * 2.5)
            self.play(FadeIn(pic), run_time=0.8)
            b.line(3)
            zero = M(r"F(a) = \int_a^a f(t)\,dt = 0", 40, ACCUM).next_to(pic, RIGHT, buff=1)
            self.play(Write(zero), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- F(1) and F(2) as triangle areas
        ax, al = plot_axes([0, 3.5, 1], [0, 7, 1], w=5.0, h=4.6, xlabel="t", ylabel="f")
        atag = T("graph of $f$", 30, FUNC).next_to(al[1], RIGHT, buff=0.35)
        VGroup(ax, al, atag).to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        with self.beat("Two values of F") as b:
            d2 = M(r"F(x) = \int_0^x 2t\,dt", 44, ACCUM).to_edge(UP, buff=0.5).to_edge(RIGHT, buff=0.8)
            line = ax.plot(lambda s: 2 * s, x_range=[0, 3.3], color=FUNC, stroke_width=5)
            llab = M("f(t) = 2t", 40, FUNC).move_to(ax.c2p(1.0, 5.2))
            self.play(FadeIn(ax), FadeIn(al), FadeIn(atag), Create(line), FadeIn(llab), FadeIn(d2), run_time=1.2)
            b.line(1)
            tri1 = Polygon(ax.c2p(0, 0), ax.c2p(1, 0), ax.c2p(1, 2), stroke_width=0, fill_color=AREA, fill_opacity=0.55)
            h1 = nudge_arrow(ax.c2p(1, 0), ax.c2p(1, 2), "2", side=RIGHT, color=SECANT, offset=0.15)
            r1 = M(r"F(1) = \int_0^1 2t\,dt = \tfrac12(1)(2) = 1", 40).next_to(d2, DOWN, buff=0.8).align_to(d2, RIGHT)
            self.play(FadeIn(tri1), FadeIn(h1), run_time=0.8)
            self.play(Write(r1), run_time=1.2)
            b.line(2)
            tri2 = Polygon(ax.c2p(0, 0), ax.c2p(2, 0), ax.c2p(2, 4), stroke_width=0, fill_color=ACCUM, fill_opacity=0.45)
            h2 = nudge_arrow(ax.c2p(2, 0), ax.c2p(2, 4), "4", side=RIGHT, color=SECANT, offset=0.15)
            r2 = M(r"F(2) = \int_0^2 2t\,dt = \tfrac12(2)(4) = 4", 40).next_to(r1, DOWN, buff=0.5).align_to(r1, LEFT)
            self.play(FadeOut(tri1), FadeOut(h1), FadeIn(tri2), FadeIn(h2), run_time=0.8)
            self.play(Write(r2), run_time=1.2)
            b.line(3)
            one = T("one input $x$, one area, one output $F(x)$", 32, DIM).next_to(r2, DOWN, buff=0.7).align_to(r1, LEFT)
            self.play(FadeIn(one), run_time=0.6)
        self.clear()

        # ---------------------------------------------------------------- F graphed as its own function
        top, tl, ttag, bot, bl, btag = stack([0, 3.5, 1], [0, 10, 2], [0, 7, 1], w=5.2, hF=2.8, hf=2.5)
        with self.beat("F is a function") as b:
            line = bot.plot(lambda s: 2 * s, x_range=[0, 3.3], color=FUNC, stroke_width=5)
            llab = M("f(t) = 2t", 36, FUNC).next_to(bot.c2p(3.3, 6.6), RIGHT, buff=0.2)
            self.play(FadeIn(bot), FadeIn(bl), FadeIn(btag), Create(line), FadeIn(llab), FadeIn(top), FadeIn(tl), FadeIn(ttag), run_time=1.2)
            vals = VGroup(*[M(rf"F({k}) = {k * k}", 40) for k in range(3)], M(r"F(3) = \tfrac12(3)(6) = 9", 40))
            vals.arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=1.0).shift(UP * 1.2)
            tri, keep = None, []

            def show(k):
                nonlocal tri
                new = Polygon(bot.c2p(0, 0), bot.c2p(k, 0), bot.c2p(k, 2 * k), stroke_width=0, fill_color=AREA, fill_opacity=0.5) if k else VMobject()
                dot = Dot(top.c2p(k, k * k), color=ACCUM, radius=0.07)
                link = DashedLine(bot.c2p(k, 2 * k), top.c2p(k, k * k), color=DIM, stroke_width=2) if k else VMobject()
                anims = [FadeIn(new), Create(link), FadeIn(dot, scale=1.6), Write(vals[k])]
                if tri is not None:
                    anims.append(FadeOut(tri))
                self.play(*anims, run_time=0.9)
                tri = new
                keep.append(link)
            for k in range(3):
                show(k)
            b.line(1)
            show(3)
            b.line(2)
            curve = top.plot(lambda s: s * s, x_range=[0, 3.15], color=ACCUM, stroke_width=5)
            flab = M("F(x) = x^2", 44, ACCUM).move_to(top.c2p(1.4, 6.6))
            sq = M(r"F(x) = x^2", 48, ACCUM).next_to(vals, DOWN, buff=0.6).align_to(vals, LEFT)
            self.play(FadeOut(tri), *[FadeOut(m) for m in keep], Create(curve), FadeIn(flab), Write(sq), run_time=1.4)
            b.line(3)
            ask = M(r"F'(x) = \ ?", 48, DERIV).next_to(sq, DOWN, buff=0.5).align_to(sq, LEFT)
            self.play(FadeIn(ask), run_time=0.6)
        self.clear()

        # ---------------------------------------------------------------- the nudge: dF is the sliver of area under f
        top, tl, ttag, bot, bl, btag = stack([0, 6, 1], [0, 9, 3], [0, 3, 1], coords=False)
        x0 = 5.0
        DX = ValueTracker(0.8)

        def parts():
            d = DX.get_value()
            x1 = x0 + d
            sliver = bot.get_area(bot.plot(f, x_range=[x0, x1]), x_range=[x0, x1], color=SECANT, opacity=0.75)
            rect = Rectangle(width=bot.c2p(x1, 0)[0] - bot.c2p(x0, 0)[0], height=bot.c2p(0, f(x0))[1] - bot.c2p(0, 0)[1],
                             stroke_color=INK, stroke_width=2, fill_opacity=0).move_to(bot.c2p(x0, 0), aligned_edge=DL)
            hgt = nudge_arrow(bot.c2p(x1, 0), bot.c2p(x1, f(x0)), "f(x)", side=RIGHT, color=SECANT, offset=0.15)
            dxb = nudge_arrow(bot.c2p(x0, 0), bot.c2p(x1, 0), r"\Delta x", side=DOWN, color=INK, offset=0.5)
            p0, p1, corner = top.c2p(x0, F(x0)), top.c2p(x1, F(x1)), top.c2p(x1, F(x0))
            run = DashedLine(p0, corner, color=DIM, stroke_width=2)
            dxt = nudge_arrow(p0, corner, r"\Delta x", side=DOWN, color=INK, offset=0.18)
            rise = Line(corner, p1, color=SECANT, stroke_width=5)
            dF = M(r"\Delta F", 34, SECANT).next_to(rise, RIGHT, buff=0.12)
            dots = VGroup(Dot(p0, color=ACCUM, radius=0.06), Dot(p1, color=ACCUM, radius=0.06))
            links = VGroup(DashedLine(bot.c2p(x0, f(x0)), p0, color=DIM, stroke_width=1.5), DashedLine(bot.c2p(x1, f(x1)), p1, color=DIM, stroke_width=1.5))
            return dict(sliver=sliver, rect=rect, hgt=hgt, dxb=dxb, run=run, dxt=dxt, rise=rise, dF=dF, dots=dots, links=links)

        with self.beat("How fast F grows") as b:
            fc = bot.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)
            Fc = top.plot(F, x_range=[0, 6], color=ACCUM, stroke_width=5)
            base = bot.get_area(bot.plot(f, x_range=[0, x0]), x_range=[0, x0], color=AREA, opacity=0.45)
            labs = VGroup(M("F(x)", 44, ACCUM).move_to(top.c2p(2.4, 6.4)), M("f(t)", 44, FUNC).move_to(bot.c2p(3.5, 1.9)))
            xl = M("x", 30).next_to(bot.c2p(x0, 0), DOWN, buff=0.12)
            self.play(FadeIn(VGroup(top, tl, ttag, bot, bl, btag)), Create(Fc), Create(fc), FadeIn(base), FadeIn(labs), FadeIn(xl), FadeIn(defn), run_time=1.4)
            P = parts()
            self.play(FadeIn(P["dots"][0]), FadeIn(P["dxb"]), FadeIn(P["dxt"]), FadeIn(P["run"]), run_time=0.8)
            b.line(1)
            self.play(Create(P["rise"]), FadeIn(P["dots"][1]), FadeIn(P["dF"]), run_time=0.8)
            b.line(2)
            rows = VGroup(M(r"\Delta F = \text{area of the sliver}", 36), M(r"\Delta F \approx f(x) \cdot \Delta x", 38),
                          M(r"\frac{\Delta F}{\Delta x} \approx f(x)", 38), M(r"F'(x) = \lim_{\Delta x \to 0} \frac{\Delta F}{\Delta x} = f(x)", 38, ACCUM))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).set_max_width(4.7)
            rows.next_to(defn, DOWN, buff=0.8).to_edge(RIGHT, buff=0.4)
            self.play(FadeIn(P["sliver"]), Create(P["links"]), run_time=0.8)
            self.play(Write(rows[0]), run_time=1)
            b.line(3)
            self.play(Create(P["rect"]), FadeIn(P["hgt"]), run_time=0.8)
            self.play(Write(rows[1]), run_time=1)
            b.line(4)
            self.play(Write(rows[2]), run_time=1)
            b.line(5)
            # the same pieces, now redrawn from DX, so the nudge can shrink
            static = list(P.values())
            live = always_redraw(lambda: VGroup(*parts().values()))
            self.remove(*static)
            self.add(live)
            self.play(DX.animate.set_value(0.2), run_time=2.4)
            self.play(Write(rows[3]), run_time=1.2)
        self.clear()

        # ---------------------------------------------------------------- the theorem, with fanfare
        with self.beat("The Fundamental Theorem") as b:
            head = T("The Fundamental Theorem of Calculus", 54, ACCUM)
            stmt = M(r"\text{If } F(x) = \int_a^x f(t)\,dt, \ \text{ then } \ F'(x) = f(x).", 52)
            cond = T("($f$ continuous)", 28, DIM)
            thm = formula_box(VGroup(head, stmt, cond).arrange(DOWN, buff=0.35), ACCUM, buff=0.45).to_edge(UP, buff=0.6)
            thm[0].set_stroke(width=5)
            self.add_sound(os.path.join(ASSETS, "fanfare.wav"), gain=-9)
            self.play(GrowFromCenter(thm), run_time=1.0)
            self.play(Circumscribe(thm, color=SECANT, buff=0.12), run_time=1.2)
            b.line(1)
            self.play(Indicate(stmt, color=ACCUM, scale_factor=1.06), run_time=1.2)
            b.line(2)
            words = T("A running total of area grows at a rate equal to the height of the graph being added up.", 32, INK).set_max_width(12)
            words.next_to(thm, DOWN, buff=0.6)
            self.play(FadeIn(words), run_time=0.8)
            b.line(3)
            chk = M(r"F(x) = x^2, \quad F'(x) = 2x = f(x)", 44, DERIV).next_to(words, DOWN, buff=0.6)
            self.play(Write(chk), run_time=1.2)
        self.clear()

        # ---------------------------------------------------------------- the two halves of the course, joined
        with self.beat("Two halves, joined") as b:
            a1, a2 = Arrow(LEFT, RIGHT, color=INK, buff=0).set_length(1.7), Arrow(LEFT, RIGHT, color=INK, buff=0).set_length(1.7)
            chain = VGroup(M(r"f", 52, FUNC), a1, M(r"F(x) = \int_a^x f(t)\,dt", 46, ACCUM), a2, M(r"F'(x) = f(x)", 46, FUNC)).arrange(RIGHT, buff=0.3)
            chain.set_max_width(12.5).to_edge(UP, buff=0.9)
            w1 = T("integrate up to $x$", 26, DIM).next_to(a1, UP, buff=0.15)
            w2 = T("take the derivative", 26, DIM).next_to(a2, UP, buff=0.15)
            self.play(FadeIn(chain[0]), run_time=0.4)
            self.play(GrowArrow(a1), FadeIn(w1), FadeIn(chain[2]), run_time=0.9)
            self.play(GrowArrow(a2), FadeIn(w2), FadeIn(chain[4]), run_time=0.9)
            b.line(1)
            inv = T("inverse operations", 36, SECANT).next_to(chain, DOWN, buff=0.45)
            self.play(FadeIn(inv), Indicate(chain[0], color=SECANT), Indicate(chain[4], color=SECANT), run_time=1)
            b.line(2)
            L = formula_box(VGroup(T("Derivatives", 40, DERIV), T("Units 2 to 5", 28, DIM), T("slopes and rates of change", 30)).arrange(DOWN, buff=0.2), DERIV)
            R = formula_box(VGroup(T("Integrals", 40, AREA), T("Topics 6.1 to 6.3", 28, DIM), T("Riemann sums, areas, running totals", 30)).arrange(DOWN, buff=0.2), AREA)
            cards = VGroup(L, R).arrange(RIGHT, buff=2.4).next_to(inv, DOWN, buff=0.8)
            cards.set_max_width(12.5)
            self.play(FadeIn(L), run_time=0.7)
            self.play(FadeIn(R), run_time=0.7)
            b.line(3)
            link = DoubleArrow(L.get_right(), R.get_left(), buff=0.15, color=ACCUM, stroke_width=6)
            ftc = T("the Fundamental Theorem", 30, ACCUM).next_to(cards, DOWN, buff=0.5)
            self.play(GrowFromCenter(link), FadeIn(ftc), run_time=1)
            self.play(Circumscribe(VGroup(cards, link), color=ACCUM, buff=0.15), run_time=1.2)
        self.clear()

        # ---------------------------------------------------------------- examples: plain substitution first
        self.example("Just substitute", r"$F(x) = \displaystyle\int_1^x \sqrt{1 + t^3}\,dt$. Find $F'(x)$ and $F'(2)$.",
                     [r"\text{top limit: just } x", r"F'(x) = \sqrt{1 + x^3}", r"F'(2) = \sqrt{1 + 8} = \sqrt9 = 3"], at=[1, 2, 3], ref=REF_FTC, follow=True)
        self.example("Using the theorem", r"Let $g(x) = \displaystyle\int_2^x \left(t^2 - 3t\right) dt$. Find $g'(x)$, $g'(4)$ and $g(2)$.",
                     [r"g'(x) = x^2 - 3x \ \ \text{(FTC)}", r"g'(4) = 16 - 12 = 4", r"g(2) = \int_2^2 \left(t^2 - 3t\right) dt = 0"], at=[1, 2, 3], ref=REF_FTC)
        # the first chain-rule example: every piece named (Adder: call the inner function g(x), then F'(g(x)) g'(x))
        self.example("With the chain rule", r"$h(x) = \displaystyle\int_1^{x^2} \cos t\,dt$. Find $h'(x)$.",
                     [r"F(x) = \int_1^x \cos t\,dt, \ \ F'(x) = \cos x", r"g(x) = x^2 \ \ \text{(inner function)}, \ \ g'(x) = 2x", r"h(x) = F(g(x))",
                      r"h'(x) = F'(g(x)) \cdot g'(x)", r"F'(g(x)) = \cos\left(x^2\right)", r"h'(x) = \cos\left(x^2\right) \cdot 2x = 2x\cos\left(x^2\right)"],
                     at=[1, 2, 3, 4, 5, 6], ref=REF_CHAIN, follow=True)

        with self.beat("Close") as b:
            card = VGroup(M(r"F(x) = \int_a^x f(t)\,dt: \ \text{a running total of area}", 42, ACCUM),
                          formula_box(M(r"\text{If } F(x) = \int_a^x f(t)\,dt, \ \text{ then } \ F'(x) = f(x)", 44), ACCUM),
                          M(r"\text{a function of } x \text{ on top: } \ F'(g(x)) \cdot g'(x)", 40), M(r"F(a) = 0", 40, DIM)).arrange(DOWN, buff=0.5)
            card.set_max_width(12.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A function on top", r"$k(x) = \displaystyle\int_3^{\sin x} e^{t^2}\,dt$. Find $k'(x)$.",
                     [r"F(x) = \int_3^x e^{t^2}\,dt, \ \ g(x) = \sin x, \ \ g'(x) = \cos x", r"F'(g(x)) = e^{(\sin x)^2}", r"k'(x) = e^{\sin^2 x} \cdot \cos x"],
                     at=[1, 2, 3], ref=REF_CHAIN)
        self.example("Example 2: x on the bottom", r"$m(x) = \displaystyle\int_x^5 \left(t^4 + 1\right) dt$. Find $m'(x)$.",
                     [r"m(x) = -\int_5^x \left(t^4 + 1\right) dt", r"m'(x) = -\left(x^4 + 1\right)"], at=[1, 2], ref=REF_FTC)
        self.example("Example 3: x at both ends", r"$R(x) = \displaystyle\int_{3x}^{x^2} \sqrt{t^4 + 1}\,dt$. Find $R'(x)$.",
                     [r"R(x) = \int_{3x}^{0} \sqrt{t^4 + 1}\,dt + \int_0^{x^2} \sqrt{t^4 + 1}\,dt", r"R(x) = -\int_0^{3x} \sqrt{t^4 + 1}\,dt + \int_0^{x^2} \sqrt{t^4 + 1}\,dt",
                      r"\text{first piece: } -\sqrt{(3x)^4 + 1} \cdot 3 = -3\sqrt{81x^4 + 1}", r"\text{second piece: } \sqrt{\left(x^2\right)^4 + 1} \cdot 2x = 2x\sqrt{x^8 + 1}",
                      r"R'(x) = 2x\sqrt{x^8 + 1} - 3\sqrt{81x^4 + 1}"], at=[1, 2, 3, 4, 5], ref=REF_CHAIN)
        self.finish()
