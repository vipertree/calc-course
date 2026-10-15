"""Topic 6.10: Long division and completing the square. Narration comes from transcripts/6_10.md.

Adder's 6.10 notes (2026-10-14): students won't remember polynomial long division, so introduce it slowly (17 / 5 first,
then one move at a time with the four moves listed beside it); show synthetic division with at least one example, side by
side with the long division, and be clear that it only applies to dividing by x - c; take completing the square slowly too
(its own example before the arctangent integral). These are algebra skills students haven't touched in a while.
"""
import numpy as np
from manim import *

from kit import *
from style import *

ARCTAN = r"\int \frac{du}{a^2 + u^2} = \frac1a\arctan\frac ua + C"
ARCSIN = r"\int \frac{du}{\sqrt{a^2 - u^2}} = \arcsin\frac ua + C"


def division_frame(divisor, left, right, top, depth, size=46):
    """The long-division bracket: a bar over the dividend from x = left to x = right at height top, a ')' down `depth`."""
    bar = Line([left, top, 0], [right, top, 0], color=INK, stroke_width=3)
    hook = ArcBetweenPoints([left, top, 0], [left - 0.12, top - depth, 0], angle=-PI / 5, color=INK, stroke_width=3)
    dv = M(divisor, size).next_to(hook, LEFT, buff=0.2)
    return VGroup(bar, hook), dv


class LongDivision:
    """x^2 + 3x + 5 divided by x + 1, laid out in columns by power (x^2, x, constant)."""

    def __init__(self, x0=-3.6, y0=1.5, colw=1.45, rowh=0.85, size=46):
        self.size, self.rowh = size, rowh
        self.cols = [x0 + k * colw for k in range(3)]          # x^2, x, 1
        self.y0 = y0

    def term(self, tex, col, row, color=INK):
        return M(tex, self.size, color).move_to([self.cols[col], self.y0 - row * self.rowh, 0])

    def build(self):
        s = self
        p = {}
        p["dividend"] = VGroup(s.term("x^2", 0, 0), s.term("+\\,3x", 1, 0), s.term("+\\,5", 2, 0))
        p["frame"], p["divisor"] = division_frame("x + 1", s.cols[0] - 0.55, s.cols[2] + 0.55, s.y0 + 0.5 * s.rowh, 0.9 * s.rowh, s.size)
        p["q1"] = s.term("x", 1, -1, SECANT)
        p["q2"] = s.term("+\\,2", 2, -1, SECANT)
        p["m1"] = VGroup(s.term("-(x^2", 0, 1), s.term("+\\,x)", 1, 1))
        p["l1"] = Line([s.cols[0] - 0.6, s.y0 - 1.42 * s.rowh, 0], [s.cols[1] + 0.6, s.y0 - 1.42 * s.rowh, 0], color=INK, stroke_width=2.5)
        p["d1"] = s.term("2x", 1, 2)
        p["down"] = s.term("+\\,5", 2, 2)
        p["m2"] = VGroup(s.term("-(2x", 1, 3), s.term("+\\,2)", 2, 3))
        p["l2"] = Line([s.cols[1] - 0.6, s.y0 - 3.42 * s.rowh, 0], [s.cols[2] + 0.6, s.y0 - 3.42 * s.rowh, 0], color=INK, stroke_width=2.5)
        p["r"] = s.term("3", 2, 4, TANGENT)
        return p


def synthetic(c, coeffs, size=46, colw=1.15):
    """A synthetic-division table: c in the corner, the coefficients across the top, then the products row and the sums.
    Returns a VGroup with .c, .top, .mid (None for the first column), .bot, .frame, .rbox."""
    g = VGroup()
    xs = [k * colw for k in range(len(coeffs))]
    g.c = M(c, size, DERIV).move_to([-1.0, 0, 0])
    g.top = VGroup(*[M(str(v), size).move_to([x, 0, 0]) for v, x in zip(coeffs, xs)])
    g.frame = VGroup(Line([-0.5, 0.4, 0], [-0.5, -1.25, 0], color=INK, stroke_width=3),
                     Line([-0.5, -1.25, 0], [xs[-1] + 0.5, -1.25, 0], color=INK, stroke_width=3))
    sums, mids = [coeffs[0]], [None]
    for v in coeffs[1:]:
        prod = sums[-1] * int(c)
        mids.append(prod)
        sums.append(v + prod)
    g.mid = [None] + [M(str(m), size, DIM).move_to([x, -0.8, 0]) for m, x in zip(mids[1:], xs[1:])]
    g.bot = VGroup(*[M(str(v), size, SECANT).move_to([x, -1.75, 0]) for v, x in zip(sums, xs)])
    g.bot[-1].set_color(TANGENT)
    g.rbox = SurroundingRectangle(g.bot[-1], color=TANGENT, buff=0.12)
    g.add(g.c, g.top, g.frame, *g.mid[1:], g.bot, g.rbox)
    g.sums = sums
    return g


def steps_list(size=34):
    return VGroup(T("1. Divide the leading terms.", size), T("2. Multiply.", size), T("3. Subtract.", size),
                  T("4. Bring down the next term.", size)).arrange(DOWN, aligned_edge=LEFT, buff=0.32)


class Lesson(TranscriptScene):
    NUM = "6.10"

    def construct(self):
        with self.beat("Two rewrites") as b:
            L = VGroup(M(r"\int \frac{x^2 + 3x + 5}{x + 1}\,dx", 48), T("top degree $\\ge$ bottom degree: divide", 30, SECANT)).arrange(DOWN, buff=0.4)
            R = VGroup(M(r"\int \frac{1}{x^2 + 4x + 13}\,dx", 48), T("quadratic bottom, no real roots: complete the square", 30, ACCUM)).arrange(DOWN, buff=0.4)
            VGroup(L, R).arrange(RIGHT, buff=1.0).shift(UP * 0.6)
            VGroup(L, R).set_max_width(13)
            self.play(FadeIn(L[0]), FadeIn(R[0]), run_time=1)
            b.line(1)
            self.play(FadeIn(L[1]), run_time=0.6)
            b.line(2)
            self.play(FadeIn(R[1]), run_time=0.6)
            self.play(FadeIn(T("rewrite into a form you know", 34, DIM).to_edge(DOWN, buff=0.8)), run_time=0.6)
        self.clear()
        self.title()

        # ---------------------------------------------------------------- 17 / 5 first
        with self.beat("Division with numbers") as b:
            cols = [-1.5, -1.12]
            num = VGroup(M("1", 56).move_to([cols[0], 0.8, 0]), M("7", 56).move_to([cols[1], 0.8, 0]))
            frame, dv = division_frame("5", cols[0] - 0.45, cols[1] + 0.45, 1.3, 0.8, 56)
            q = M("3", 56, SECANT).move_to([cols[1], 1.85, 0])
            sub = M("-", "15", 56)
            sub.shift([(cols[0] + cols[1]) / 2 - sub[1].get_center()[0], -0.15 - sub.get_center()[1], 0])    # the 15 sits under the 17
            ln = Line([cols[0] - 0.5, -0.6, 0], [cols[1] + 0.4, -0.6, 0], color=INK, stroke_width=3)
            r = M("2", 56, TANGENT).move_to([cols[1], -1.1, 0])
            grp = VGroup(num, frame, dv, q, sub, ln, r).shift(LEFT * 2.2)
            self.play(FadeIn(dv), Create(frame), FadeIn(num), run_time=0.8)
            self.play(Write(q), run_time=0.6)
            self.play(Write(sub), run_time=0.6)
            self.play(Create(ln), Write(r), run_time=0.7)
            labq = T("quotient", 28, SECANT).next_to(q, RIGHT, buff=0.35)
            labr = T("remainder", 28, TANGENT).next_to(r, RIGHT, buff=0.35)
            self.play(FadeIn(labq), FadeIn(labr), run_time=0.6)
            b.line(1)
            res = M(r"\frac{17}{5} = ", r"3", r" + \frac{", r"2", r"}{5}", 60).move_to([3.4, 0.6, 0])
            res[1].set_color(SECANT)
            res[3].set_color(TANGENT)
            words = M(r"\text{quotient} + \frac{\text{remainder}}{\text{divisor}}", 40, DIM).next_to(res, DOWN, buff=0.5)
            self.play(Write(res), run_time=1)
            self.play(FadeIn(words), run_time=0.7)
            b.line(2)
            self.play(Circumscribe(words, color=SECANT), run_time=1)
        self.clear()

        # ---------------------------------------------------------------- the long division, one move at a time
        ld = LongDivision()
        p = ld.build()
        lst = steps_list().move_to([4.3, 2.0, 0])
        with self.beat("Polynomial long division") as b:
            self.play(FadeIn(p["divisor"]), Create(p["frame"]), FadeIn(p["dividend"]), run_time=1.2)
            ghost = lst.copy().set_opacity(0.35)
            self.play(FadeIn(ghost), run_time=0.6)
            side = None

            def light(k):
                return [Transform(ghost[k], lst[k].copy().set_color(SECANT))] + [Transform(ghost[j], lst[j].copy().set_opacity(0.35)) for j in range(4) if j != k]

            def say(tex):
                nonlocal side
                new = M(tex, 40, DIM).move_to([4.3, -0.6, 0])
                anims = [FadeIn(new)] + ([FadeOut(side)] if side is not None else [])
                side = new
                return anims
            b.line(1)
            self.play(*light(0), run_time=0.6)
            self.play(Indicate(p["dividend"][0], color=SECANT), Indicate(p["divisor"][0][0], color=SECANT), run_time=0.9)
            self.play(*say(r"x^2 \div x = x"), run_time=0.6)
            self.play(Write(p["q1"]), run_time=0.6)
            b.line(2)
            self.play(*light(1), *say(r"x(x + 1) = x^2 + x"), run_time=0.8)
            self.play(Write(p["m1"]), run_time=1)
            b.line(3)
            self.play(*light(2), run_time=0.6)
            self.play(Create(p["l1"]), run_time=0.5)
            self.play(*say(r"3x - x = 2x"), run_time=0.6)
            self.play(Write(p["d1"]), run_time=0.7)
            b.line(4)
            self.play(*light(3), run_time=0.6)
            arr = Arrow(p["dividend"][2].get_bottom() + DOWN * 0.05, p["down"].get_top() + UP * 0.05, buff=0.05, color=DERIV, stroke_width=4,
                        max_tip_length_to_length_ratio=0.12)
            self.play(GrowArrow(arr), TransformFromCopy(p["dividend"][2], p["down"]), run_time=1)
            b.line(5)
            self.play(*light(0), *say(r"2x \div x = 2"), run_time=0.8)
            self.play(Write(p["q2"]), run_time=0.6)
            b.line(6)
            self.play(*light(1), *say(r"2(x + 1) = 2x + 2"), run_time=0.8)
            self.play(Write(p["m2"]), run_time=0.9)
            self.play(*light(2), Create(p["l2"]), run_time=0.6)
            self.play(*say(r"5 - 2 = 3"), run_time=0.5)
            self.play(Write(p["r"]), run_time=0.6)
            b.line(7)
            self.play(*[Transform(ghost[j], lst[j].copy().set_opacity(0.35)) for j in range(4)], FadeOut(side), run_time=0.5)
            labq = T("quotient", 28, SECANT).next_to(VGroup(p["q1"], p["q2"]), UP, buff=0.15)
            labr = T("remainder", 28, TANGENT).next_to(p["r"], RIGHT, buff=0.35)
            stop = T("degree of 3 is lower than degree of $x + 1$: stop", 30).set_max_width(5.0).move_to([4.3, -1.4, 0])
            self.play(FadeIn(stop), run_time=0.6)
            self.play(FadeIn(labq), FadeIn(labr), run_time=0.6)
        self.clear()

        with self.beat("The result") as b:
            n = M(r"\frac{17}{5} = ", r"3", r" + \frac{", r"2", r"}{5}", 52)
            n[1].set_color(SECANT)
            n[3].set_color(TANGENT)
            pq = M(r"\frac{x^2 + 3x + 5}{x + 1} = ", r"x + 2", r" + \frac{", r"3", r"}{x + 1}", 52)
            pq[1].set_color(SECANT)
            pq[3].set_color(TANGENT)
            VGroup(n, pq).arrange(DOWN, buff=0.6).to_edge(UP, buff=0.6)
            n.shift(RIGHT * (pq[0].get_right()[0] - n[0].get_right()[0]))         # line up the equals signs
            self.play(FadeIn(n), run_time=0.6)
            self.play(Write(pq), run_time=1.2)
            labs = VGroup(T("quotient", 26, SECANT).next_to(pq[1], DOWN, buff=0.25),
                          T("remainder over divisor", 26, TANGENT).next_to(VGroup(pq[2], pq[4]), DOWN, buff=0.2))
            self.play(FadeIn(labs), run_time=0.6)
            b.line(1)
            chk = VGroup(M(r"\text{check: } (x + 1)(x + 2) + 3", 44), M(r"= x^2 + 3x + 2 + 3", 44), M(r"= x^2 + 3x + 5", 44, ACCUM))
            chk.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(labs, DOWN, buff=0.6)
            for c in chk:
                self.play(Write(c), run_time=0.9)
        self.clear()

        # ---------------------------------------------------------------- synthetic division beside the long division
        with self.beat("Synthetic division") as b:
            ld2 = LongDivision(x0=-4.9, y0=1.1, colw=1.05, rowh=0.62, size=36)
            p2 = ld2.build()
            left = VGroup(*[v for v in p2.values()])
            lh = T("Long division", 34, DIM).move_to([-4.3, 3.2, 0])
            rule = Line([-1.6, 3.4, 0], [-1.6, -3.4, 0], color=DIM, stroke_width=2)
            rh = T("Synthetic division", 34, DIM).move_to([2.7, 3.2, 0])
            only = formula_box(T("only for dividing by $x - c$", 32, DERIV), DERIV).next_to(rh, DOWN, buff=0.3)
            self.play(FadeIn(lh), FadeIn(left), Create(rule), run_time=1)
            self.play(FadeIn(rh), FadeIn(only), run_time=0.8)
            b.line(1)
            cc = M(r"x + 1 = x - (-1), \ \ \text{so } c = -1", 36).next_to(only, DOWN, buff=0.35)
            syn = synthetic("-1", [1, 3, 5], size=46).move_to([3.0, -0.9, 0])
            self.play(Write(cc), run_time=1)
            self.play(FadeIn(syn.c), Create(syn.frame), FadeIn(syn.top), run_time=0.9)
            b.line(2)
            self.play(TransformFromCopy(syn.top[0], syn.bot[0]), run_time=0.8)
            b.line(3)
            self.play(TransformFromCopy(syn.bot[0], syn.mid[1]), Indicate(syn.c, color=DERIV), run_time=0.9)
            self.play(Write(syn.bot[1]), run_time=0.7)
            b.line(4)
            self.play(TransformFromCopy(syn.bot[1], syn.mid[2]), Indicate(syn.c, color=DERIV), run_time=0.9)
            self.play(Write(syn.bot[2]), run_time=0.7)
            b.line(5)
            self.play(Create(syn.rbox), run_time=0.5)
            read = M(r"1x + 2, \ \ \text{remainder } 3", 36, SECANT).next_to(syn, DOWN, buff=0.35)
            self.play(Write(read), run_time=0.9)
            b.line(6)
            self.play(Indicate(VGroup(p2["q1"], p2["q2"]), color=SECANT), Indicate(syn.bot[0:2], color=SECANT), run_time=1)
            self.play(Indicate(p2["r"], color=TANGENT), Indicate(syn.bot[2], color=TANGENT), run_time=1)
            b.line(7)
            self.play(Circumscribe(only, color=DERIV), run_time=1)
            nope = T(r"dividing by $x^2 + 1$ or $2x + 1$: use long division", 30, DERIV).next_to(read, DOWN, buff=0.35)
            self.play(FadeIn(nope), run_time=0.6)
        self.clear()

        with self.beat("Integrate the pieces") as b:
            l1 = M(r"\int \frac{x^2 + 3x + 5}{x + 1}\,dx = \int \left(x + 2 + \frac{3}{x + 1}\right) dx", 50).to_edge(UP, buff=0.8)
            self.play(Write(l1), run_time=1.4)
            b.line(1)
            l2 = M(r"= \frac{x^2}{2}", r" + 2x", r" + 3\ln|x + 1|", r" + C", 50).next_to(l1, DOWN, buff=0.7).align_to(l1, LEFT).shift(RIGHT * 2.2)
            self.play(Write(l2[0]), run_time=0.7)
            self.play(Write(l2[1]), run_time=0.6)
            b.line(2)
            note = M(r"u = x + 1, \ \ du = dx", 36, DIM).next_to(l2[2], DOWN, buff=0.6)
            self.play(FadeIn(note), run_time=0.6)
            self.play(Write(l2[2]), run_time=0.9)
            b.line(3)
            self.play(Write(l2[3]), run_time=0.5)
            self.play(Circumscribe(l2, color=ACCUM), run_time=1)
        self.clear()

        with self.beat("Two more forms") as b:
            r1 = formula_box(M(ARCTAN, 46, ACCUM), ACCUM)
            r2 = formula_box(M(ARCSIN, 46, ACCUM), ACCUM)
            VGroup(r1, r2).arrange(DOWN, buff=0.7).shift(UP * 0.5)
            src = T("from the inverse trig derivatives, with $a^2$ in place of $1$", 30, DIM).to_edge(UP, buff=0.5)
            self.play(FadeIn(src), run_time=0.6)
            b.line(1)
            self.play(FadeIn(r1), run_time=0.8)
            b.line(2)
            self.play(FadeIn(r2), run_time=0.8)
            b.line(3)
            tip = T("Complete the square to make $a^2 + u^2$ or $a^2 - u^2$.", 34, SECANT).to_edge(DOWN, buff=0.7)
            self.play(FadeIn(tip), run_time=0.6)
        self.clear()

        self.example("Complete the square", r"Rewrite $x^2 + 4x + 13$ by completing the square.",
                     [r"\text{goal: } \left(x + \underline{\quad}\right)^2 + \underline{\quad}", r"\text{half of } 4 \text{ is } 2, \ \text{and } 2^2 = 4", r"x^2 + 4x + 13 = \left(x^2 + 4x + 4\right) + 9", r"= (x + 2)^2 + 9",
                      r"\text{check: } (x + 2)^2 + 9 = x^2 + 4x + 4 + 9 = x^2 + 4x + 13"], at=[1, 2, 3, 4, 5], follow=True)
        self.example("An arctangent", r"Find $\displaystyle\int \frac{1}{x^2 + 4x + 13}\,dx$.",
                     [r"x^2 + 4x + 13 = (x + 2)^2 + 9 = (x + 2)^2 + 3^2", r"u = x + 2, \ \ du = dx, \ \ a = 3", r"\int \frac{du}{u^2 + 3^2} = \frac13\arctan\frac u3 + C",
                      r"= \frac13\arctan\frac{x + 2}{3} + C"], at=[1, 2, 3, 4], follow=True, ref=ARCTAN)

        with self.beat("Close") as b:
            card = VGroup(T(r"Top degree $\ge$ bottom degree: divide first (long division, or synthetic for $x - c$).", 34, SECANT),
                          T("Quadratic bottom that won't factor: complete the square.", 34),
                          M(ARCTAN, 40, ACCUM), M(ARCSIN, 40, ACCUM)).arrange(DOWN, buff=0.45)
            card.set_max_width(12.8)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        syn = synthetic("1", [1, 0, 0, 1], size=46)
        for m in (*syn.mid[1:], syn.bot, syn.rbox):
            m.set_opacity(0)

        def fill(sc):
            sc.play(syn.bot[0].animate.set_opacity(1), run_time=0.5)
            for k in (1, 2, 3):
                sc.play(syn.mid[k].animate.set_opacity(1), run_time=0.5)
                sc.play(syn.bot[k].animate.set_opacity(1), run_time=0.5)
            sc.play(syn.rbox.animate.set_stroke(opacity=1), run_time=0.4)
        self.example("Example 1: A cubic over a line", r"Find $\displaystyle\int \frac{x^3 + 1}{x - 1}\,dx$.",
                     [r"c = 1", r"x^3 + 0x^2 + 0x + 1", r"\text{bottom row: } 1, \ 1, \ 1 \ \big| \ 2", r"\frac{x^3 + 1}{x - 1} = x^2 + x + 1 + \frac{2}{x - 1}",
                      r"\int = \frac{x^3}{3} + \frac{x^2}{2} + x + 2\ln|x - 1| + C"], at=[1, 2, 3, 4, 5], figure=syn, figure_at=2, cues={2: fill})
        self.example("Example 2: An arcsine", r"Find $\displaystyle\int \frac{1}{\sqrt{-x^2 + 6x - 5}}\,dx$.",
                     [r"-x^2 + 6x - 5 = -\left(x^2 - 6x\right) - 5", r"= -\left(x^2 - 6x + 9\right) + 9 - 5", r"= -(x - 3)^2 + 4 = 4 - (x - 3)^2",
                      r"u = x - 3, \ \ du = dx, \ \ a = 2", r"\int \frac{du}{\sqrt{2^2 - u^2}} = \arcsin\frac u2 + C = \arcsin\frac{x - 3}{2} + C"],
                     at=[2, 3, 4, 5, 6], ref=ARCSIN)
        self.example("Example 3: A definite integral", r"Evaluate $\displaystyle\int_0^1 \frac{x}{x + 1}\,dx$.",
                     [r"x \div (x + 1)\text{: quotient } 1, \ \text{remainder } x - (x + 1) = -1", r"\frac{x}{x + 1} = 1 - \frac{1}{x + 1}",
                      r"\int_0^1 \left(1 - \frac{1}{x + 1}\right) dx = \left[x - \ln|x + 1|\right]_0^1", r"= (1 - \ln 2) - (0 - \ln 1)", r"= 1 - \ln 2"],
                     at=[1, 2, 3, 4, 5])
        self.finish()
