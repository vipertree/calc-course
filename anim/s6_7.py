"""Topic 6.7: The Fundamental Theorem of Calculus and definite integrals. Narration comes from transcripts/6_7.md.

Adder's 6.7 notes (2026-10-14): the cold open is a teaser (the Riemann-sum limit we want, hard to compute; the FTC gives
area as another function), not the shortcut. After the title it picks up where 6.4 left off: big F, the accumulation
function, graphed above f. F's change from where it starts to where it ends is the area f accumulates. A concrete
integral side by side with the general notation ("what is the F here? where does it start and end?"). +C shown by
plugging in random constants: same derivative, and C cancels in the change. No A(x) anywhere. Then the theorem (with
fanfare), why it's so useful, the power rule reversed as two steps with think pauses, a spaced-out chart (x^(n+1) used to
run into the row above), and the first example done with F(4) and F(1) before the bracket notation.
"""
import os

import numpy as np
from manim import *

from kit import *
from style import *

# the rule kept in the corner during the examples (formulas stay on screen)
REF = r"\begin{array}{c} \int_a^b f(x)\,dx = F(b) - F(a) \\ \text{where } F'(x) = f(x) \end{array}"
LIMIT = r"\lim_{n \to \infty} \sum_{k=1}^{n} \left(\frac{3k}{n}\right)^2 \cdot \frac{3}{n}"


def stack(xr, yF, yf, w=8.0, hF=2.7, hf=2.3, coords=True, Flab="F", flab="f"):
    """F's graph on top, f's graph below, on one x-scale, each tagged with which graph it is (as in 6.4)."""
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
    NUM = "6.7"

    def think(self, near, direction=DOWN, buff=0.4):
        cue = T("Pause and think.", 30, DIM).next_to(near, direction, buff=buff)
        self.play(FadeIn(cue), run_time=0.4)
        return cue

    def construct(self):
        sq = lambda s: s * s

        # ---------------------------------------------------------------- teaser: the limit we want, and a promise
        ax, al = plot_axes([0, 3.5, 1], [0, 10, 2], w=5.6, h=5.0)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.4)
        with self.beat("The area we want") as b:
            curve = ax.plot(sq, x_range=[0, 3.2], color=FUNC, stroke_width=5)
            clab = M("f(x) = x^2", 40, FUNC).move_to(ax.c2p(1.25, 7.4))
            boxes = riemann_boxes(ax, sq, np.linspace(0, 3, 7), "right", opacity=0.35)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), FadeIn(clab), run_time=1.2)
            self.play(FadeIn(boxes), run_time=0.8)
            self.bring_to_front(curve)
            b.line(1)
            area = M(r"\text{area} = " + LIMIT, 44).to_edge(RIGHT, buff=0.5).shift(UP * 0.2)
            self.play(Write(area), run_time=1.4)
            for n in (24, 60):
                nb = riemann_boxes(ax, sq, np.linspace(0, 3, n + 1), "right", opacity=0.35)
                self.play(ReplacementTransform(boxes, nb), run_time=1.2)
                boxes = nb
                self.bring_to_front(curve)
            b.line(2)
            hard = T("hard to compute", 34, DIM).next_to(area, DOWN, buff=0.45)
            self.play(FadeIn(hard), run_time=0.6)
            b.line(3)
            region = ax.get_area(ax.plot(sq, x_range=[0, 3]), x_range=[0, 3], color=AREA, opacity=0.5)
            promise = VGroup(T("the Fundamental Theorem of Calculus:", 32, ACCUM), T("area as another function, $F$", 32, ACCUM)).arrange(DOWN, buff=0.15)
            promise.next_to(area, UP, buff=0.7)
            self.play(FadeOut(boxes), FadeIn(region), run_time=1)
            self.bring_to_front(curve)
            self.play(FadeIn(promise, shift=DOWN * 0.2), run_time=0.8)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- big F again, picking up from 6.4
        f = lambda s: 1 + 0.5 * np.sin(1.3 * s) + 0.15 * s
        F = lambda s: s + 0.5 * (1 - np.cos(1.3 * s)) / 1.3 + 0.075 * s * s     # the exact running total of f from 0
        top, tl, ttag, bot, bl, btag = stack([0, 6, 1], [0, 9, 3], [0, 3, 1], hF=3.0, hf=2.2, coords=False)
        x0, dx = 3.0, 0.5
        with self.beat("Big F, again") as b:
            defn = VGroup(M(r"F(x) = \int_0^x f(t)\,dt", 44, ACCUM), M(r"F'(x) = f(x)", 44, ACCUM)).arrange(DOWN, buff=0.3).to_corner(UR, buff=0.5)
            fc = bot.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)
            Fc = top.plot(F, x_range=[0, 6], color=ACCUM, stroke_width=5)
            labs = VGroup(M("F(x)", 44, ACCUM).move_to(top.c2p(1.2, 6.6)), M("f(t)", 44, FUNC).move_to(bot.c2p(1.0, 2.5)))
            base = bot.get_area(bot.plot(f, x_range=[0, x0]), x_range=[0, x0], color=AREA, opacity=0.45)
            xl = M("x", 30).next_to(bot.c2p(x0, 0), DOWN, buff=0.12)
            self.play(FadeIn(VGroup(top, tl, ttag, bot, bl, btag)), Create(fc), Create(Fc), FadeIn(labs), FadeIn(defn[0]), run_time=1.4)
            self.play(FadeIn(base), FadeIn(xl), run_time=0.8)
            b.line(1)
            self.play(FadeIn(defn[1]), run_time=0.6)
            sliver = bot.get_area(bot.plot(f, x_range=[x0, x0 + dx]), x_range=[x0, x0 + dx], color=SECANT, opacity=0.8)
            p0, p1, corner = top.c2p(x0, F(x0)), top.c2p(x0 + dx, F(x0 + dx)), top.c2p(x0 + dx, F(x0))
            rise = VGroup(DashedLine(p0, corner, color=DIM, stroke_width=2), Line(corner, p1, color=SECANT, stroke_width=5),
                          Dot(p0, color=ACCUM, radius=0.06), Dot(p1, color=ACCUM, radius=0.06))
            dF = M(r"\Delta F", 32, SECANT).next_to(rise[1], RIGHT, buff=0.12)
            link = DashedLine(bot.c2p(x0 + dx / 2, f(x0 + dx / 2)), top.c2p(x0 + dx / 2, F(x0) - 0.1), color=DIM, stroke_width=1.5)
            self.play(FadeIn(sliver), Create(link), run_time=0.8)
            self.play(Create(rise), FadeIn(dF), run_time=0.8)
        self.play(FadeOut(VGroup(sliver, rise, dF, link, base, xl, defn)), run_time=0.6)

        # ---------------------------------------------------------------- where F starts and ends
        a, bb = 1.5, 4.6
        with self.beat("Where F starts and ends") as b:
            ab = VGroup(M("a", 30).next_to(bot.c2p(a, 0), DOWN, buff=0.12), M("b", 30).next_to(bot.c2p(bb, 0), DOWN, buff=0.12))
            edges = np.linspace(a, bb, 13)
            slivers = VGroup(*[bot.get_area(bot.plot(f, x_range=[u, v]), x_range=[u, v], color=SECANT if k % 2 else AREA, opacity=0.6)
                               for k, (u, v) in enumerate(zip(edges, edges[1:]))])
            self.play(FadeIn(ab), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(s) for s in slivers], lag_ratio=0.15), run_time=2)
            region = bot.get_area(bot.plot(f, x_range=[a, bb]), x_range=[a, bb], color=AREA, opacity=0.55)
            ilab = M(r"\int_a^b f(t)\,dt", 34).move_to(bot.c2p((a + bb) / 2, 0.55))
            self.play(ReplacementTransform(slivers, region), FadeIn(ilab), run_time=1)
            b.line(1)
            Fa, Fb = F(a), F(bb)
            da, db = Dot(top.c2p(a, Fa), color=ACCUM, radius=0.08), Dot(top.c2p(bb, Fb), color=ACCUM, radius=0.08)
            la = DashedLine(top.c2p(a, Fa), top.c2p(6.4, Fa), color=DIM, stroke_width=2)
            lb = DashedLine(top.c2p(bb, Fb), top.c2p(6.4, Fb), color=DIM, stroke_width=2)
            links = VGroup(DashedLine(bot.c2p(a, 0), top.c2p(a, Fa), color=DIM, stroke_width=1.5),
                           DashedLine(bot.c2p(bb, 0), top.c2p(bb, Fb), color=DIM, stroke_width=1.5))
            ta = VGroup(M("F(a)", 32, ACCUM), T("where $F$ starts", 26, DIM)).arrange(RIGHT, buff=0.2).next_to(la, RIGHT, buff=0.15)
            tb = VGroup(M("F(b)", 32, ACCUM), T("where $F$ ends", 26, DIM)).arrange(RIGHT, buff=0.2).next_to(lb, RIGHT, buff=0.15)
            self.play(Create(links), run_time=0.6)
            self.play(FadeIn(da), Create(la), FadeIn(ta), run_time=0.8)
            self.play(FadeIn(db), Create(lb), FadeIn(tb), run_time=0.8)
            b.line(2)
            arr = DoubleArrow(top.c2p(6.4, Fa) + RIGHT * 0.25, top.c2p(6.4, Fb) + RIGHT * 0.25, buff=0, color=SECANT, stroke_width=5,
                              tip_length=0.2, max_tip_length_to_length_ratio=0.2)
            chg = VGroup(M(r"F(b) - F(a)", 34, SECANT), T("how much $F$ changed", 26, DIM)).arrange(DOWN, buff=0.12).next_to(arr, RIGHT, buff=0.2)
            self.play(GrowFromCenter(arr), FadeIn(chg), run_time=0.8)
            board = VGroup(T("the change in $F$ = the area that $f$ accumulates", 30), M(r"\int_a^b f(t)\,dt = F(b) - F(a)", 46, ACCUM)).arrange(DOWN, buff=0.35)
            board.set_max_width(5.4).next_to(bot, RIGHT, buff=0.5).shift(UP * 0.2)
            self.play(FadeIn(board[0]), run_time=0.6)
            self.play(Write(board[1]), Indicate(region, color=AREA), Indicate(arr, color=SECANT), run_time=1.4)
        self.clear()

        # ---------------------------------------------------------------- side by side: general and concrete
        with self.beat("Side by side") as b:
            L = [T("In general", 36, DIM), M(r"\text{integrand: } f(x)", 38), M(r"F: \ F'(x) = f(x)", 38, ACCUM), M(r"\text{starts: } F(a)", 38),
                 M(r"\text{ends: } F(b)", 38), M(r"\int_a^b f(x)\,dx = F(b) - F(a)", 38, ACCUM)]
            R = [M(r"\text{For } \int_0^3 x^2\,dx", 36, DIM), M(r"\text{integrand: } x^2", 38), M(r"F(x) = \frac{x^3}{3}, \ \ \text{since } \frac{d}{dx}\left(\frac{x^3}{3}\right) = x^2", 38, ACCUM),
                 M(r"F(0) = 0", 38), M(r"F(3) = \frac{27}{3} = 9", 38), M(r"\int_0^3 x^2\,dx = 9 - 0 = 9", 38, ACCUM)]
            ys = [3.0, 2.0, 0.9, -0.3, -1.4, -2.7]
            for m, y in zip(L, ys):
                m.move_to([-3.6, y, 0])
            for m, y in zip(R, ys):
                m.move_to([2.9, y, 0])
            R[2].set_max_width(6.6).move_to([2.9, ys[2], 0])
            rule = Line([-0.3, 3.4, 0], [-0.3, -3.3, 0], color=DIM, stroke_width=2)
            self.play(FadeIn(L[0]), Create(rule), run_time=0.6)
            self.play(FadeIn(L[1]), run_time=0.5)
            self.play(FadeIn(L[2]), run_time=0.5)
            b.line(1)
            self.play(FadeIn(R[0]), FadeIn(R[1]), run_time=0.8)
            cue = self.think(R[1], DOWN, buff=0.35)
            b.line(2)
            self.play(FadeOut(cue), run_time=0.3)
            self.play(Write(R[2]), run_time=1.2)
            b.line(3)
            self.play(FadeIn(L[3]), FadeIn(R[3]), run_time=0.7)
            self.play(FadeIn(L[4]), FadeIn(R[4]), run_time=0.7)
            b.line(4)
            self.play(FadeIn(L[5]), Write(R[5]), run_time=1.2)
            self.play(Circumscribe(R[5], color=ACCUM), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- where + C comes from
        cs = [(0, ACCUM), (2, FUNC), (-1, TANGENT), (5, DERIV)]
        cax, cal = plot_axes([0, 3.4, 1], [-2, 15, 5], w=5.0, h=5.4, coords=True)
        VGroup(cax, cal).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        with self.beat("Where plus C comes from") as b:
            self.play(FadeIn(cax), FadeIn(cal), run_time=0.5)
            curves, labs = VGroup(), VGroup()
            for c, col in cs:
                g = (lambda s, c=c: s ** 3 / 3 + c)
                curves.add(cax.plot(g, x_range=[0, 3.15], color=col, stroke_width=4))
                txt = r"C = " + (str(c) if c >= 0 else r"-" + str(-c))
                labs.add(M(txt, 24, col).next_to(cax.c2p(3.15, g(3.15)), RIGHT, buff=0.1))
            self.play(Create(curves[0]), FadeIn(labs[0]), run_time=0.7)
            for k in range(1, 4):
                self.play(Create(curves[k]), FadeIn(labs[k]), run_time=0.6)
            b.line(1)
            tans = VGroup(*[tangent_line(cax, lambda s, c=c: s ** 3 / 3 + c, 2, 4, [1.6, 2.4], color=SECANT).set_stroke(width=4) for c, _ in cs])
            same_d = T("every one has derivative $x^2$", 30, SECANT).to_edge(UP, buff=0.4).to_edge(RIGHT, buff=0.5)
            self.play(Create(tans), FadeIn(same_d), run_time=1)
            fam = M(r"F(x) = \frac{x^3}{3} + C", 44, ACCUM).next_to(same_d, DOWN, buff=0.35)
            self.play(Write(fam), run_time=1)
            b.line(2)
            tab = table([r"C", r"F(3)", r"F(0)", r"F(3) - F(0)"], [["0", "9", "0", "9"], ["2", "11", "2", "9"], ["-1", "8", "-1", "9"], ["5", "14", "5", "9"]],
                        size=34, gap=0.28)
            tab.set_max_width(5.8).next_to(fam, DOWN, buff=0.45).to_edge(RIGHT, buff=0.5)
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab[1]), run_time=0.5)
            self.play(FadeIn(VGroup(*tab.cells[1])), run_time=0.5)
            self.play(FadeIn(VGroup(*tab.cells[2])), run_time=0.8)
            b.line(3)
            self.play(FadeIn(VGroup(*tab.cells[3])), run_time=0.6)
            self.play(FadeIn(VGroup(*tab.cells[4])), run_time=0.6)
            b.line(4)
            col = VGroup(*[tab.cells[r][3] for r in range(1, 5)])
            hl = SurroundingRectangle(col, color=SECANT, buff=0.12)
            gen = M(r"\left(F(b) + C\right) - \left(F(a) + C\right) = F(b) - F(a)", 34, ACCUM).set_max_width(6.2).next_to(tab, DOWN, buff=0.45).to_edge(RIGHT, buff=0.5)
            self.play(Create(hl), run_time=0.6)
            self.play(Write(gen), run_time=1.2)
        self.clear()

        # ---------------------------------------------------------------- the theorem, with fanfare
        with self.beat("The Fundamental Theorem, part 2") as b:
            head = T("The Fundamental Theorem of Calculus, part 2", 50, ACCUM)
            stmt = M(r"\text{If } F'(x) = f(x) \text{ on } [a, b], \ \text{ then } \ \int_a^b f(x)\,dx = F(b) - F(a).", 46)
            cond = T("($f$ continuous)", 28, DIM)
            thm = formula_box(VGroup(head, stmt, cond).arrange(DOWN, buff=0.35), ACCUM, buff=0.45).set_max_width(12.8).to_edge(UP, buff=0.7)
            thm[0].set_stroke(width=5)
            self.add_sound(os.path.join(ASSETS, "fanfare.wav"), gain=-9)
            self.play(GrowFromCenter(thm), run_time=1.0)
            self.play(Circumscribe(thm, color=SECANT, buff=0.12), run_time=1.2)
            b.line(1)
            self.play(Indicate(stmt, color=ACCUM, scale_factor=1.06), run_time=1.2)
            b.line(2)
            words = T("The area under $f$ from $a$ to $b$ is how much $F$ changes from $a$ to $b$.", 34, INK).set_max_width(12)
            words.next_to(thm, DOWN, buff=0.7)
            self.play(FadeIn(words), run_time=0.8)
        self.clear()

        # ---------------------------------------------------------------- why it matters
        with self.beat("Why it matters") as b:
            old = VGroup(M(LIMIT, 40, DIM), T("a limit of sums", 30, DIM)).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.7).shift(UP * 0.6)
            cross = Line(old[0].get_corner(DL), old[0].get_corner(UR), color=SECANT, stroke_width=4)
            self.play(FadeIn(old), run_time=0.6)
            self.play(Create(cross), run_time=0.6)
            b.line(1)
            steps = VGroup(T(r"1. Find an antiderivative $F$ ($F' = f$).", 36), T("2. Evaluate $F$ at the two endpoints.", 36),
                           T(r"3. Subtract: $F(b) - F(a)$.", 36)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.6).shift(UP * 0.9)
            for s in steps:
                self.play(FadeIn(s, shift=RIGHT * 0.2), run_time=0.6)
            ex = M(r"\int_0^3 x^2\,dx = 9 - 0 = 9", 42, ACCUM).next_to(steps, DOWN, buff=0.7).align_to(steps, LEFT)
            self.play(Write(ex), run_time=1)
            b.line(2)
            skill = T("the one skill: run derivative rules backward", 34, SECANT).to_edge(DOWN, buff=0.7)
            self.play(FadeIn(skill), run_time=0.6)
        self.clear()

        # ---------------------------------------------------------------- the power rule, reversed as two steps
        with self.beat("Reversing the power rule") as b:
            def chain(parts, ops, color):
                items = [M(parts[0], 40, color)]
                for p, o in zip(parts[1:], ops):
                    arr = Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, color=DIM, stroke_width=4, max_tip_length_to_length_ratio=0.3)
                    items += [VGroup(arr, M(o, 26, DIM).next_to(arr, UP, buff=0.08)), M(p, 40, color)]
                return VGroup(*items).arrange(RIGHT, buff=0.2)
            lhead = VGroup(T("Power rule", 36, DERIV), M(r"\frac{d}{dx}\, x^n = n\,x^{n-1}", 40, DERIV)).arrange(DOWN, buff=0.2)
            lsteps = VGroup(T("1. multiply by the power", 30), T("2. subtract 1 from the exponent", 30)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            lex = chain([r"x^3", r"3x^3", r"3x^2"], [r"\times 3", r"-1"], DERIV)
            left = VGroup(lhead, lsteps, lex).arrange(DOWN, buff=0.4).move_to([-3.5, 1.4, 0])
            rhead = VGroup(T("Reversed", 36, ACCUM), M(r"\text{antiderivative of } x^n", 40, ACCUM)).arrange(DOWN, buff=0.2)
            rsteps = VGroup(T("1. add 1 to the exponent", 30), T("2. divide by the new exponent", 30)).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            rex = chain([r"x^2", r"x^3", r"\frac{x^3}{3}"], [r"+1", r"\div 3"], ACCUM)
            right = VGroup(rhead, rsteps, rex).arrange(DOWN, buff=0.4).move_to([3.4, 1.4, 0])
            rule = Line([0, 3.5, 0], [0, -0.7, 0], color=DIM, stroke_width=2)
            self.play(FadeIn(lhead), run_time=0.6)
            self.play(FadeIn(lsteps[0]), run_time=0.5)
            self.play(FadeIn(lsteps[1]), run_time=0.5)
            self.play(FadeIn(lex), run_time=1)
            b.line(1)
            cue = self.think(rule, DOWN, buff=0.3)
            self.play(Create(rule), FadeIn(rhead), run_time=0.6)
            b.line(2)
            self.play(FadeOut(cue), run_time=0.3)
            self.play(FadeIn(rsteps[0]), run_time=0.5)
            self.play(FadeIn(rsteps[1]), run_time=0.5)
            self.play(FadeIn(rex), run_time=1.2)
            b.line(3)
            chk = M(r"\text{check: } \frac{d}{dx}\left(\frac{x^3}{3}\right) = \frac{3x^2}{3} = x^2", 36).next_to(right, DOWN, buff=0.45)
            self.play(Write(chk), run_time=1.2)
            b.line(4)
            gen = formula_box(M(r"x^n \ \text{ has antiderivative } \ \frac{x^{n+1}}{n + 1}, \quad n \ne -1", 40, ACCUM), ACCUM)
            gen.move_to([0, -1.75, 0])
            self.play(FadeIn(gen), FadeOut(chk), run_time=0.8)
            b.line(5)
            ask = M(r"\text{an antiderivative of } x^4\text{?}", 38).move_to([-2.4, -3.2, 0])
            self.play(FadeIn(ask), run_time=0.5)
            cue = self.think(ask, RIGHT, buff=0.5)
            b.line(6)
            ans = M(r"\frac{x^5}{5}", 44, ACCUM).next_to(ask, RIGHT, buff=0.5)
            self.play(FadeOut(cue), run_time=0.3)
            self.play(Write(ans), run_time=0.8)
        self.clear()

        # ---------------------------------------------------------------- the chart, with room between rows
        with self.beat("More rules backward") as b:
            tab = table([r"f(x)", r"\text{an antiderivative } F(x)"],
                        [[r"x^n \ (n \ne -1)", r"\frac{x^{n+1}}{n + 1}"], [r"\cos x", r"\sin x"], [r"\sin x", r"-\cos x"],
                         [r"e^x", r"e^x"], [r"\frac1x", r"\ln|x|"], [r"\sec^2 x", r"\tan x"]], size=36, gap=0.32)
            tab.set_max_height(6.6).to_edge(LEFT, buff=0.9)
            facts = VGroup(*[M(s, 34, DERIV) for s in (r"\frac{d}{dx}\sin x = \cos x", r"\frac{d}{dx}\cos x = -\sin x", r"\frac{d}{dx}e^x = e^x",
                                                       r"\frac{d}{dx}\ln|x| = \frac1x", r"\frac{d}{dx}\tan x = \sec^2 x")])
            fhead = T("from the derivative rules", 28, DIM)
            VGroup(fhead, *facts).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.7)
            self.play(FadeIn(VGroup(*tab.cells[0])), FadeIn(tab[1]), FadeIn(VGroup(*tab.cells[1])), *[FadeIn(tab.cells[r][0]) for r in range(2, 7)], run_time=1.2)
            self.play(FadeIn(fhead), run_time=0.4)
            b.line(1)
            self.play(Indicate(tab.cells[2][0], color=SECANT), run_time=0.8)
            cue = self.think(fhead, DOWN, buff=0.4)
            b.line(2)
            self.play(FadeOut(cue), run_time=0.3)
            self.play(FadeIn(tab.cells[2][1]), FadeIn(facts[0]), run_time=0.7)
            b.line(3)
            self.play(Indicate(tab.cells[3][0], color=SECANT), run_time=0.8)
            cue = self.think(facts[0], DOWN, buff=0.4)
            b.line(4)
            self.play(FadeOut(cue), run_time=0.3)
            self.play(FadeIn(facts[1]), run_time=0.6)
            self.play(FadeIn(tab.cells[3][1]), run_time=0.6)
            b.line(5)
            self.play(FadeIn(tab.cells[4][1]), FadeIn(facts[2]), run_time=0.7)
            b.line(6)
            self.play(FadeIn(tab.cells[5][1]), FadeIn(facts[3]), run_time=0.7)
            b.line(7)
            self.play(FadeIn(tab.cells[6][1]), FadeIn(facts[4]), run_time=0.7)
        self.clear()

        # ---------------------------------------------------------------- the first full example: F, F(4), F(1), then brackets
        self.example("Evaluating an integral", r"Evaluate $\displaystyle\int_1^4 \left(3x^2 - 2x\right) dx$.",
                     [r"F(x) = x^3 - x^2 \ \ \left(F'(x) = 3x^2 - 2x\right)", r"F(4) = 4^3 - 4^2 = 64 - 16 = 48", r"F(1) = 1^3 - 1^2 = 0",
                      r"\int_1^4 \left(3x^2 - 2x\right) dx = F(4) - F(1) = 48 - 0 = 48",
                      "TEXT:How we write it from now on:", r"\left[x^3 - x^2\right]_1^4", r"= \left(4^3 - 4^2\right) - \left(1^3 - 1^2\right)",
                      r"= 48 - 0 = 48"],
                     at=[1, 2, 3, 4, 5, 5, 6, 7], ref=REF, follow=True)

        with self.beat("Net change") as b:
            r1 = VGroup(M(r"\int_a^b f'(x)\,dx = f(b) - f(a)", 50, ACCUM), T("the integral of a rate of change is the net change", 32, DIM)).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.6)
            self.play(Write(r1[0]), run_time=1.2)
            b.line(1)
            self.play(FadeIn(r1[1]), run_time=0.6)
            b.line(2)
            r2 = VGroup(M(r"f(b) = f(a) + \int_a^b f'(x)\,dx", 50, FUNC), T("where it ends = where it starts + how much it changed", 32, DIM)).arrange(DOWN, buff=0.25).next_to(r1, DOWN, buff=0.8)
            self.play(Write(r2[0]), FadeIn(r2[1]), run_time=1.2)
            start = Rectangle(width=1.2, height=1.2, stroke_width=0, fill_color=FUNC, fill_opacity=0.4)
            add = Rectangle(width=1.2, height=0.8, stroke_width=0, fill_color=AREA, fill_opacity=0.6).next_to(start, UP, buff=0)
            pic = VGroup(start, add, T("$f(a)$", 26).move_to(start), T(r"$\int f'$", 26).move_to(add)).next_to(r2, DOWN, buff=0.5)
            self.play(FadeIn(pic), run_time=0.8)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"\int_a^b f(x)\,dx = F(b) - F(a), \ \ F' = f", 44, ACCUM), M(r"\left[F(x)\right]_a^b = F(b) - F(a)", 42),
                          T("Reverse the power rule: add 1 to the exponent, then divide by the new exponent.", 32),
                          M(r"\int_a^b f'(x)\,dx = f(b) - f(a): \ \text{net change}", 42)).arrange(DOWN, buff=0.5)
            card.set_max_width(12.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A trig integral", r"Evaluate $\displaystyle\int_0^\pi \sin x\,dx$.",
                     [r"F(x) = -\cos x \ \ \left(F'(x) = \sin x\right)", r"\left[-\cos x\right]_0^\pi = -\cos\pi - (-\cos 0)", r"= -(-1) - (-1)", r"= 1 + 1 = 2"],
                     at=[1, 2, 3, 4], ref=REF)
        self.example("Example 2: A root", r"Evaluate $\displaystyle\int_1^9 \sqrt x\,dx$.",
                     [r"\sqrt x = x^{1/2}", r"\text{add 1: } x^{3/2}, \ \ \text{divide by } \tfrac32\text{: } \frac{x^{3/2}}{3/2} = \tfrac23 x^{3/2}",
                      r"\left[\tfrac23 x^{3/2}\right]_1^9 = \tfrac23\left(9^{3/2}\right) - \tfrac23\left(1^{3/2}\right)", r"= \tfrac23(27) - \tfrac23", r"= 18 - \tfrac23 = \tfrac{52}{3}"],
                     at=[1, 2, 3, 4, 5], ref=REF)
        self.example("Example 3: Net change", r"A plant is $10$ cm tall at $t = 1$ week and grows at $h'(t) = 6t - 2$ cm per week. How tall is it at $t = 3$?",
                     [r"h(3) = h(1) + \int_1^3 h'(t)\,dt", r"\int_1^3 (6t - 2)\,dt = \left[3t^2 - 2t\right]_1^3", r"= (27 - 6) - (3 - 2) = 21 - 1 = 20", r"h(3) = 10 + 20 = 30 \text{ cm}"],
                     at=[1, 2, 3, 4], ref=REF)
        self.finish()
