"""Topic 10.1 (BC): Convergent and divergent series. Narration comes from transcripts/10_1.md."""
import numpy as np
from manim import *

from kit import *
from props import bar_counter, bartender, beer_glass, face, pint_fill
from style import *


class Lesson(TranscriptScene):
    NUM = "10.1"

    def construct(self):
        with self.beat("A bar joke") as b:
            # Adder (2026-10-14): the chocolate bar read as subtraction; tell the bar joke and pour the orders together
            top = -1.7
            tender = face(bartender(4.6), -1).move_to([5.4, top - 1.55, 0], aligned_edge=DOWN)
            counter = bar_counter(top).set_z_index(1)       # in front of the bartender
            self.play(FadeIn(counter), run_time=0.8)
            sizes = [r"\tfrac12", r"\tfrac14", r"\tfrac18", r"\tfrac1{16}", r"\tfrac1{32}"]
            xs = [-6.0, -4.7, -3.4, -2.1, -0.8]
            orders, labels = [], []
            for k, (x, lab) in enumerate(zip(xs, sizes)):
                g = beer_glass(0.5 ** (k + 1), 1.9).move_to([x, top, 0], aligned_edge=DOWN)
                t = M(lab, 40).next_to(g, UP, buff=0.12)
                orders.append(g)
                labels.append(t)
                self.play(FadeIn(g, shift=DOWN * 0.2), FadeIn(t), run_time=0.55)
            dots = M(r"\cdots", 44).move_to([0.3, top + 0.7, 0])
            self.play(FadeIn(dots), run_time=0.4)
            b.line(2)
            self.play(FadeIn(tender, shift=LEFT * 1.4), run_time=1.4)
            said = T("``Oh, brother.''", 36).next_to(tender, UP, buff=0.25)
            self.play(FadeIn(said), run_time=0.5)
            pint = beer_glass(0.0, 3.0).move_to([3.4, top, 0], aligned_edge=DOWN)
            self.add(pint)
            self.bring_to_front(counter)
            self.play(pint_fill(pint, 0.0, 1.0), run_time=1.6)
            self.play(FadeOut(said), run_time=0.3)
            face(tender, 1)
            self.play(FadeOut(tender, shift=RIGHT * 2.0), run_time=1.6)
            self.remove(tender)
            b.line(3)
            question = M(r"\tfrac12 + \tfrac14 + \tfrac18 + \tfrac1{16} + \cdots = \ ?", 44).to_edge(UP, buff=0.25)
            self.play(pint.animate.shift(RIGHT * 2.0), FadeIn(question), run_time=0.8)
            glass = beer_glass(0.0, 3.0).move_to([2.2, top, 0], aligned_edge=DOWN)
            self.play(FadeIn(glass), run_time=0.5)
            total = None
            level = 0.0
            for k, (g, t) in enumerate(zip(orders, labels)):
                new = 0.5 ** (k + 1)
                # tip the glass past level so its mouth faces down over the big glass, then pour straight down
                tilt = -2.0
                rim_y = glass.get_top()[1] - 0.13 * glass.height        # the image's top 13% is room for a head
                lip_at = np.array([glass.get_center()[0] - 0.25, rim_y + 0.95, 0])     # high enough to clear the glass
                to_lip = rotate_vector(UP * 0.37 * 1.9, tilt)
                rt = 1.0 if k < 3 else 0.6
                self.play(g.animate.rotate(tilt).move_to(lip_at - to_lip), FadeOut(t), run_time=0.5 * rt + 0.2)
                stream = Line(lip_at, [lip_at[0], rim_y - 0.35, 0], stroke_color="#F2A93B", stroke_width=6)
                tot_tex = [r"\tfrac12", r"\tfrac34", r"\tfrac78", r"\tfrac{15}{16}", r"\tfrac{31}{32}"][k]
                tot = M(tot_tex, 48, SECANT).next_to(glass, RIGHT, buff=0.25).shift(UP * 0.6)
                self.play(Create(stream), pint_fill(glass, level, level + new), pint_fill(g, 0.5 ** (k + 1), 0.0),
                          FadeIn(tot) if total is None else ReplacementTransform(total, tot), run_time=0.9 * rt + 0.2)
                self.play(FadeOut(stream), FadeOut(g), run_time=0.3)
                level += new
                total = tot
                if k == 1:
                    b.line(4)
            self.play(FadeOut(dots), run_time=0.3)
            b.line(5)
            done = M(r"\tfrac12 + \tfrac14 + \tfrac18 + \tfrac1{16} + \cdots = 1", 44).move_to(question)
            self.play(pint_fill(glass, level, 1.0), ReplacementTransform(question, done), ReplacementTransform(total, M("1", 48, SECANT).move_to(total)), run_time=2.0)
        self.clear()
        self.title()

        with self.beat("Separate numbers, added up") as b:
            # Adder: say early that this is not integration; these are separate values added together
            axL, _ = plot_axes([0, 5, 1], [0, 3, 1], w=5.2, h=3.2, coords=False, xlabel="x", ylabel="y")
            f = lambda x: 1.2 + 0.9 * np.sin(1.1 * x) + 0.12 * x
            left = VGroup(axL, region(axL, f, lambda x: 0, 0.5, 4.5), axL.plot(f, x_range=[0, 5], color=FUNC, stroke_width=4))
            capL = T("Units 6 to 8: an integral adds up a continuous function", 28, DIM).set_max_width(5.6)
            axR, _ = plot_axes([0, 6, 1], [0, 3, 1], w=5.2, h=3.2, coords=False, xlabel="n", ylabel="a_n")
            hs = [2.6, 1.9, 1.4, 1.05, 0.8]
            bars = VGroup(*[Rectangle(width=0.42, height=axR.c2p(0, h)[1] - axR.c2p(0, 0)[1], stroke_color=SECANT, stroke_width=2, fill_color=SECANT, fill_opacity=0.6)
                            .move_to(axR.c2p(k, 0), aligned_edge=DOWN) for k, h in enumerate(hs, start=1)])
            names = VGroup(*[M(f"a_{k}", 30, SECANT).next_to(bar, UP, buff=0.1) for k, bar in enumerate(bars, start=1)])
            right = VGroup(axR, bars, names)
            capR = T("Unit 10: separate numbers, added one at a time", 28, SECANT).set_max_width(5.6)
            colL = VGroup(left, capL).arrange(DOWN, buff=0.3)
            colR = VGroup(right, capR).arrange(DOWN, buff=0.3)
            VGroup(colL, colR).arrange(RIGHT, buff=1.0).move_to(ORIGIN)
            self.play(FadeIn(colL), run_time=1.0)
            b.line(2)
            cross = VGroup(Line(left.get_corner(UL), left.get_corner(DR)), Line(left.get_corner(DL), left.get_corner(UR))).set_stroke(TANGENT, 6)
            self.play(colL.animate.set_opacity(0.35), Create(cross), run_time=0.8)
            self.play(FadeIn(axR), run_time=0.5)
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bar, DOWN), FadeIn(nm)) for bar, nm in zip(bars, names)], lag_ratio=0.5), run_time=3.0)
            self.play(FadeIn(capR), run_time=0.6)
        self.clear()

        with self.beat("Partial sums") as b:
            rows = VGroup(M(r"\sum_{n=1}^{\infty} a_n = a_1 + a_2 + a_3 + \cdots", 46), M(r"S_n = a_1 + a_2 + \cdots + a_n", 46, SECANT),
                          M(r"\text{converges to } S \text{ if } \lim_{n\to\infty} S_n = S; \ \text{otherwise diverges}", 38, ACCUM), T("keep a running total; if it settles on a number, that's the sum", 32, DIM)).arrange(DOWN, buff=0.45)
            self.play(Write(rows[0]), run_time=1)
            b.line(1)
            self.play(Write(rows[1]), run_time=1)
            b.line(2)
            self.play(Write(rows[2]), run_time=1)
            b.line(3)
            self.play(FadeIn(rows[3]), run_time=0.6)
        self.clear()

        with self.beat("Three ways to behave") as b:
            def panel(vals, yr, lab, color):
                ax, _ = plot_axes([0, 9, 2], yr, w=3.6, h=2.8, coords=False, xlabel="n", ylabel="S_n")
                dots = VGroup(*[Dot(ax.c2p(k, v), color=color, radius=0.07) for k, v in enumerate(vals, start=1)])
                return VGroup(ax, dots, T(lab, 26, color).next_to(ax, DOWN, buff=0.25))
            p1 = panel(list(range(1, 9)), [0, 9, 2], "$\\sum 1$: diverges to $\\infty$", TANGENT)
            p2 = panel([1, 0, 1, 0, 1, 0, 1, 0], [-0.5, 1.5, 1], "$\\sum (-1)^{n+1}$: no single value", TANGENT)
            p3 = panel([1 - 0.5**k for k in range(1, 9)], [0, 1.2, 0.5], "$\\sum (\\frac12)^n$: converges to $1$", DERIV)
            VGroup(p1, p2, p3).arrange(RIGHT, buff=0.4)
            self.play(FadeIn(p1), run_time=1)
            b.line(1)
            self.play(FadeIn(p2), run_time=1)
            b.line(2)
            self.play(FadeIn(p3), run_time=1)
        self.clear()

        with self.beat("The terms settle, the sum doesn't") as b:
            # Adder: an example where the sequence converges but the series diverges, so the two words come apart
            N = 9
            terms = [k / (k + 1) for k in range(1, N + 1)]
            sums = list(np.cumsum(terms))
            axA, _ = plot_axes([0, N + 1, 2], [0, 1.4, 0.5], w=5.4, h=2.6, coords=False, xlabel="n", ylabel="a_n")
            axS, _ = plot_axes([0, N + 1, 2], [0, 9, 2], w=5.4, h=2.6, coords=False, xlabel="n", ylabel="S_n")
            one = DashedLine(axA.c2p(0, 1), axA.c2p(N + 1, 1), color=DIM, dash_length=0.12)
            one_lab = M("1", 28, DIM).next_to(axA.c2p(0, 1), LEFT, buff=0.15)
            dA = VGroup(*[Dot(axA.c2p(k, v), color=DERIV, radius=0.07) for k, v in enumerate(terms, start=1)])
            dS = VGroup(*[Dot(axS.c2p(k, v), color=TANGENT, radius=0.07) for k, v in enumerate(sums, start=1)])
            headA = T("the sequence: the list of terms", 30, DERIV)
            headS = T("the series: the running total", 30, TANGENT)
            footA = T("the sequence converges to $1$", 28, DERIV)
            footS = T("the series diverges", 28, TANGENT)
            colA = VGroup(headA, VGroup(axA, one, one_lab, dA), footA).arrange(DOWN, buff=0.3)
            colS = VGroup(headS, VGroup(axS, dS), footS).arrange(DOWN, buff=0.3)
            VGroup(colA, colS).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.9)
            formula = M(r"a_n = \frac{n}{n + 1}: \quad \tfrac12,\ \tfrac23,\ \tfrac34,\ \tfrac45,\ \ldots", 40).to_edge(UP, buff=0.2)
            VGroup(colA, colS).next_to(formula, DOWN, buff=0.4)
            self.play(FadeIn(formula), run_time=0.8)
            b.line(2)
            self.play(FadeIn(headA), FadeIn(axA), Create(one), FadeIn(one_lab), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dA], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(footA), run_time=0.5)
            b.line(3)
            self.play(FadeIn(headS), FadeIn(axS), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dS], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(footS), run_time=0.5)
            b.line(4)
            words = T("sequence: a list of numbers \\qquad series: the sum of that list", 32, SECANT).next_to(VGroup(colA, colS), DOWN, buff=0.45)
            self.play(FadeIn(words), run_time=0.8)
        self.clear()

        # the definitions stay up in the corner through every worked example (Adder: formulas stay on screen)
        self.example_ref = r"\begin{aligned}S_n &= a_1 + a_2 + \cdots + a_n\\ \textstyle\sum a_n &= \lim_{n\to\infty} S_n\end{aligned}"
        self.example("A telescoping series", r"Find the sum of $\displaystyle\sum_{n=1}^{\infty} \frac{1}{n(n + 1)}$.",
                     [r"\frac{1}{n(n + 1)} = \frac1n - \frac{1}{n + 1}", r"S_n = \left(1 - \tfrac12\right) + \left(\tfrac12 - \tfrac13\right) + \left(\tfrac13 - \tfrac14\right) + \cdots + \left(\tfrac1n - \tfrac{1}{n + 1}\right)",
                      r"TEXT:The middle terms cancel in pairs.", r"S_n = 1 - \frac{1}{n + 1}", r"\lim_{n\to\infty} S_n = 1", r"TEXT:The series converges to $1$."], at=[1, 2, 3, 3, 4, 4], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T("sequence: a list; series: its sum", 38, DERIV), M(r"S_n = a_1 + \cdots + a_n", 44, SECANT), T("converges to $S$ if $S_n \\to S$; otherwise diverges", 36), T("telescoping: terms cancel, leaving the first and last", 34, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: Partial sums that grow", r"Does $\displaystyle\sum_{n=1}^{\infty} 2$ converge?", [r"S_n = 2 + 2 + \cdots + 2 = 2n", r"\lim_{n\to\infty} 2n = \infty: \ \text{diverges}"], at=[1, 1])
        # first of its kind (a formula for S_n, not for a_n): follow along (Adder: stop and say what S_n is)
        self.example("Example 2: A partial sum from a formula", r"The $n$th partial sum of a series is $S_n = \frac{3n}{n + 1}$. Does the series converge? If so, to what?",
                     [r"S_n = a_1 + a_2 + \cdots + a_n = \frac{3n}{n + 1} \quad \text{(a total, not a term)}", r"\lim_{n\to\infty} \frac{3n}{n + 1}",
                      r"= \lim_{n\to\infty} \frac{3n}{n} \quad \text{(only the leading terms matter)}", r"= \lim_{n\to\infty} 3 = 3, \ \text{so the series converges to } 3", r"a_1 = S_1 = \tfrac32"],
                     at=[2, 3, 4, 5, 6], follow=True, size=40)
        self.example("Example 3: Another telescoping sum", r"Find $\displaystyle\sum_{n=1}^{\infty} \left(\frac1n - \frac{1}{n + 2}\right)$.",
                     [r"S_n = \left(1 - \tfrac13\right) + \left(\tfrac12 - \tfrac14\right) + \left(\tfrac13 - \tfrac15\right) + \cdots",
                      r"\qquad + \left(\tfrac{1}{n - 1} - \tfrac{1}{n + 1}\right) + \left(\tfrac1n - \tfrac{1}{n + 2}\right)", r"TEXT:The middle terms cancel.",
                      r"S_n = 1 + \tfrac12 - \tfrac{1}{n + 1} - \tfrac{1}{n + 2}", r"\lim_{n\to\infty} S_n = 1 + \tfrac12 - 0 - 0", r"= \tfrac32"], at=[2, 2, 3, 4, 5, 5], size=40)
        self.finish()
