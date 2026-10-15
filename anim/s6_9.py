"""Topic 6.9: Integrating using substitution. Narration comes from transcripts/6_9.md.

Adder's 6.9 notes (2026-10-14): the cold open promises "essentially a reverse chain rule, but not as simple as running
the chain rule backward" (substitution isn't "the method for spotting that"). Then name it (substitution, often
u-substitution) and its goal (rewrite as a simple function of u). Every integral keeps its dx. The first example calls the
inside u and substitutes right away, leaving a mix of x's and u's (2x cos u dx); the 2x and the dx must go too, so take
the derivative of u: du/dx = 2x is "a slight change in u per slight change in x", so du = 2x dx. When replacing, the parts
of the original being replaced are underlined/boxed. The divide-by-2 example and the definite example go slowly, the
second one first keeping the limits labeled as x values, finishing the long way, crossing it off, then changing the limits
by plugging the x values into u ("When x = 0" in words, an arrow to u = 1). Example 3 ponders sin or cos for u.
The lesson examples use a side-work column (u, du, limits) beside the main integral column so every line stays visible.
"""
import numpy as np
from manim import *

from kit import *
from style import *

REF = r"u = \text{inside},\ \ du = u'(x)\,dx"


def ref_card():
    return formula_box(M(REF, 30), DERIV).set_max_width(3.9).to_corner(UR, buff=0.3)


def under(mob, color=DERIV):
    return Line(mob.get_corner(DL) + DOWN * 0.1, mob.get_corner(DR) + DOWN * 0.1, color=color, stroke_width=6)


def when(xv, uv, size=40):
    """'When x = 0' in words on one line, then an arrow to the u value under it (Adder: not 'x = 0 : u = 1').
    Parts: [0] the word, [1] the x value, [2] the arrow, [3] the u value."""
    words = VGroup(T("When", size - 2), M(xv, size)).arrange(RIGHT, buff=0.18)
    arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=DIM, stroke_width=4, max_tip_length_to_length_ratio=0.35)
    val = M(uv, size, SECANT)
    VGroup(arrow, val).arrange(RIGHT, buff=0.18).next_to(words, DOWN, buff=0.15, aligned_edge=LEFT).shift(RIGHT * 0.5)
    return VGroup(words[0], words[1], arrow, val)


class Column:
    """A column of lines that grows downward from (x, y), left-aligned, never scrolling."""

    def __init__(self, x, y, width, buff=0.35):
        self.x, self.y, self.width, self.buff, self.last = x, y, width, buff, None

    def put(self, mob):
        mob.set_max_width(self.width)
        if self.last is None:
            mob.move_to([self.x, self.y, 0], aligned_edge=UL)
        else:
            mob.next_to(self.last, DOWN, buff=self.buff, aligned_edge=LEFT)
        self.last = mob
        return mob


class Lesson(TranscriptScene):
    NUM = "6.9"
    example_ref = REF        # the substitution recipe stays in the corner during examples (Adder: keep the rule on screen)

    def construct(self):
        with self.beat("The chain rule, backward") as b:
            d = M(r"\frac{d}{dx}\sin\left(", r"x^2", r"\right) = \cos\left(x^2\right) \cdot ", r"2x", 56).shift(UP * 2.0)
            br = Brace(d[1], DOWN, color=SECANT)
            self.play(Write(d), run_time=1.2)
            self.play(FadeIn(br), FadeIn(T("inside", 28, SECANT).next_to(br, DOWN, buff=0.1)), d[3].animate.set_color(DERIV), run_time=0.8)
            b.line(1)
            i = M(r"\int ", r"2x", r"\cos\left(", r"x^2", r"\right)\,dx = \sin\left(x^2\right) + C", 56).shift(DOWN * 0.3)
            i[1].set_color(DERIV)
            self.play(Write(i), run_time=1.2)
            b.line(2)
            self.play(Indicate(i[3], color=SECANT), run_time=0.8)
            self.play(Indicate(i[1], color=DERIV), run_time=0.8)
            b.line(3)
            self.play(FadeIn(T("essentially a reverse chain rule", 36, ACCUM).next_to(i, DOWN, buff=0.9)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Substitution") as b:
            head = VGroup(T("Substitution", 56, ACCUM), T("(often called $u$-substitution)", 32, DIM)).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.6)
            self.play(FadeIn(head[0]), run_time=0.7)
            self.play(FadeIn(head[1]), run_time=0.6)
            b.line(1)
            goal = formula_box(T("Goal: rewrite the integral as a simple function of $u$,\\\\one we know how to integrate.", 36), ACCUM, buff=0.35)
            goal.next_to(head, DOWN, buff=0.6)
            self.play(FadeIn(goal), run_time=0.8)
            b.line(2)
            ex = M(r"\int 2x\cos\left(x^2\right)", r"\,dx", 56).next_to(goal, DOWN, buff=0.8)
            self.play(Write(ex), run_time=1)
            ring = Ellipse(width=ex[1].width + 0.4, height=ex[1].height + 0.35, color=TANGENT, stroke_width=4).move_to(ex[1])
            note = T("every integral has its $dx$", 30, TANGENT).next_to(ring, RIGHT, buff=0.3)
            self.play(Create(ring), FadeIn(note), run_time=0.8)
        self.clear()

        # ---------------------------------------------------------------- the first example, slowly: call the inside u right away
        def first():
            return M(r"\int ", r"2x", r"\cos\left(", r"x^2", r"\right)", r"\,dx", 60)
        with self.beat("Call the inside u") as b:
            top = first().move_to([-1.0, 2.5, 0])
            self.play(Write(top), run_time=1)
            br = Brace(top[3], DOWN, color=SECANT, buff=0.08)
            ins = T("inside", 30, SECANT).next_to(br, DOWN, buff=0.06)
            udef = M(r"u = x^2", 52, SECANT).next_to(top, RIGHT, buff=1.2)
            self.play(FadeIn(br), FadeIn(ins), run_time=0.6)
            self.play(Write(udef), run_time=0.8)
            b.line(1)
            mix = M(r"\int ", r"2x", r"\cos\left(", r"u", r"\right)", r"\,dx", 60).move_to([-1.0, 0.4, 0])
            mix[3].set_color(SECANT)
            self.play(TransformFromCopy(top[0:3], mix[0:3]), TransformFromCopy(top[4:], mix[4:]), TransformFromCopy(udef[0][0], mix[3]), run_time=1.2)
            b.line(2)
            ux = VGroup(under(mix[1]), under(mix[5]))
            labx = VGroup(T("$x$", 36, DERIV).next_to(ux[0], DOWN, buff=0.1), T("$x$", 36, DERIV).next_to(ux[1], DOWN, buff=0.1))
            uu = under(mix[3], SECANT)
            labu = T("$u$", 36, SECANT).next_to(uu, DOWN, buff=0.1)
            self.play(Create(ux), FadeIn(labx), Create(uu), FadeIn(labu), run_time=0.8)
            mixed = T("a mix of $x$'s and $u$'s: not done yet", 36).move_to([0, -0.75, 0])
            self.play(FadeIn(mixed), run_time=0.6)
            want = T("We want the whole integral in $u$, even the $dx$.", 36).next_to(mixed, DOWN, buff=0.4)
            self.play(FadeIn(want), Indicate(mix[5], color=DERIV), run_time=0.9)
            b.line(3)
            acc = T("$dx$ becomes $du$: accumulate change in $u$, not in $x$", 34, ACCUM).next_to(want, DOWN, buff=0.4)
            self.play(FadeIn(acc), run_time=0.7)
            so = T("so: take the derivative of $u$", 34, SECANT).next_to(acc, DOWN, buff=0.4)
            self.play(FadeIn(so), run_time=0.6)
        self.clear()

        with self.beat("Finding du") as b:
            udef = M(r"u = x^2", 52, SECANT).to_edge(UP, buff=0.6)
            self.play(FadeIn(udef), run_time=0.5)
            e1 = M(r"\frac{du}{dx}", r" = 2x", 56).move_to([0, 1.5, 0])
            self.play(Write(e1), run_time=1)
            b.line(1)
            w1 = T("a slight change in $u$ for every slight change in $x$", 32, DIM).next_to(e1, DOWN, buff=0.3)
            self.play(FadeIn(w1), Indicate(e1[0], color=DERIV), run_time=0.9)
            b.line(2)
            times = T("multiply both sides by $dx$", 28, DIM).next_to(w1, DOWN, buff=0.4)
            e2 = M(r"du", r" = 2x \cdot ", r"dx", 56).next_to(times, DOWN, buff=0.4)
            self.play(FadeIn(times), run_time=0.5)
            self.play(Write(e2), run_time=1)
            w2 = T("a slight change in $u$ is $2x$ times a slight change in $x$", 32, DIM).next_to(e2, DOWN, buff=0.3)
            self.play(FadeIn(w2), run_time=0.7)
            box = SurroundingRectangle(e2, color=DERIV, buff=0.15)
            self.play(Create(box), run_time=0.6)
            b.line(3)
            alt = T(r"You could work with $\frac{du}{dx} = 2x$, but $du = 2x\,dx$ lines up with the pieces of the integral.", 28, DIM)
            alt.set_max_width(12.5).to_edge(DOWN, buff=0.45)
            self.play(FadeIn(alt), run_time=0.7)
        self.clear()

        with self.beat("Rewrite in u") as b:
            sep = Line([-2.7, 2.9, 0], [-2.7, -3.4, 0], color=DIM, stroke_width=2)
            side = Column(-6.6, 2.6, 3.6, buff=0.4)
            s1 = side.put(M(r"u = x^2", 46, SECANT))
            s2 = side.put(M(r"du = 2x\,dx", 46, DERIV))
            top = first().move_to([1.8, 2.2, 0])
            self.play(FadeIn(VGroup(sep, s1, s2)), Write(top), run_time=1)
            ux = VGroup(under(top[1]), under(top[5]))
            du = M(r"du", 46, DERIV).move_to([top[3].get_center()[0], 0.9, 0])
            arrs = VGroup(*[Arrow(u.get_center() + DOWN * 0.05, du.get_corner(UL if k == 0 else UR), buff=0.08, color=DERIV, stroke_width=4,
                                  max_tip_length_to_length_ratio=0.2) for k, u in enumerate(ux)])
            self.play(Create(ux), Indicate(s2, color=DERIV), run_time=0.8)
            self.play(GrowArrow(arrs[0]), GrowArrow(arrs[1]), FadeIn(du), run_time=0.8)
            b.line(1)
            bx = SurroundingRectangle(top[3], color=SECANT, buff=0.06)
            ulab = M(r"u", 46, SECANT).next_to(bx, UP, buff=0.5)
            ua = Arrow(bx.get_top(), ulab.get_bottom(), buff=0.05, color=SECANT, stroke_width=4, max_tip_length_to_length_ratio=0.3)
            self.play(Create(bx), Indicate(s1, color=SECANT), run_time=0.7)
            self.play(GrowArrow(ua), FadeIn(ulab), run_time=0.6)
            b.line(2)
            main = Column(-2.1, 0.2, 8.6, buff=0.4)
            l1 = main.put(M(r"\int \cos", r"u", r"\,", r"du", 52))
            l1[1].set_color(SECANT)
            l1[3].set_color(DERIV)
            l1.move_to([top.get_center()[0], l1.get_center()[1], 0])
            main.last = l1
            self.play(TransformFromCopy(ulab, l1[1]), TransformFromCopy(du, l1[3]), FadeIn(l1[0]), FadeIn(l1[2]), run_time=1.2)
            b.line(3)
            l2 = M(r"= \sin u + C", 52).next_to(l1, DOWN, buff=0.45).align_to(l1, LEFT)
            self.play(Write(l2), run_time=0.9)
            b.line(4)
            l3 = M(r"= \sin\left(x^2\right) + C", 52, ACCUM).next_to(l2, DOWN, buff=0.45).align_to(l1, LEFT)
            back = T("put $x$ back: $u = x^2$", 28, DIM).next_to(l3, RIGHT, buff=0.5)
            self.play(Write(l3), FadeIn(back), Indicate(s1, color=SECANT), run_time=1.1)
        self.clear()

        with self.beat("The steps") as b:
            steps = VGroup(T(r"1. Choose $u$: an inside function.", 40), T(r"2. Find $du = u'(x)\,dx$.", 40),
                           T(r"3. Rewrite the whole integral in $u$, including the $dx$.", 40), T(r"4. Integrate, then put $x$ back.", 40, ACCUM))
            steps.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to(ORIGIN).set_max_width(12.5)
            for s in steps:
                self.play(FadeIn(s, shift=RIGHT * 0.2), run_time=0.7)
                self.wait(0.6)
        self.clear()

        self.fixing_a_constant()
        self.changing_limits()

        with self.beat("Close") as b:
            card = VGroup(T("$u$: an inside function whose derivative is a factor (up to a constant).", 34), M(r"du = u'(x)\,dx; \ \ \text{divide to fix a constant}", 40),
                          T("Rewrite everything in $u$, even the $dx$. Integrate, then put $x$ back.", 34),
                          T("Definite: plug the $x$ limits into $u$ to get $u$ limits.", 34, ACCUM)).arrange(DOWN, buff=0.5)
            card.set_max_width(12.8)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A linear inside", r"Find $\displaystyle\int e^{3x}\,dx$.",
                     [r"u = 3x", r"du = 3\,dx", r"\tfrac13\,du = dx", r"\int e^u \cdot \tfrac13\,du = \tfrac13 e^u + C", r"= \tfrac13 e^{3x} + C"], at=[1, 2, 2, 3, 4])
        self.example("Example 2: A logarithm inside", r"Find $\displaystyle\int \frac{\ln x}{x}\,dx$.",
                     [r"u = \ln x", r"du = \frac1x\,dx", r"\int u\,du = \frac{u^2}{2} + C", r"= \frac{(\ln x)^2}{2} + C"], at=[1, 2, 3, 3])

        # Example 3: ponder sin or cos for u, on the right, before the board
        c1 = VGroup(M(r"u = \sin x\,?", 40), M(r"du = \cos x\,dx", 34, DIM)).arrange(DOWN, buff=0.2)
        c2 = VGroup(M(r"u = \cos x\,?", 40), M(r"du = -\sin x\,dx", 34, DIM)).arrange(DOWN, buff=0.2)
        pick = VGroup(T("Which $u$?", 32), VGroup(c1, c2).arrange(RIGHT, buff=0.7)).arrange(DOWN, buff=0.35)

        box = SurroundingRectangle(c2, color=SECANT, buff=0.15).set_stroke(opacity=0)
        why = VGroup(T(r"$\cos x$ is inside the square,", 28), T(r"and its derivative matches $\sin x\,dx$", 28)).arrange(DOWN, buff=0.1)
        why.set_max_width(pick.width).next_to(pick, DOWN, buff=0.35).set_opacity(0)
        pick.add(box, why)

        def choose(sc):
            sc.play(box.animate.set_stroke(opacity=1), c1.animate.set_opacity(0.4), run_time=0.7)
            sc.play(why.animate.set_opacity(1), run_time=0.6)
        self.example("Example 3: Trig with new limits", r"Evaluate $\displaystyle\int_0^{\pi/2} \cos^2 x\,\sin x\,dx$.",
                     [r"u = \cos x", r"du = -\sin x\,dx, \ \text{so} \ -du = \sin x\,dx", r"\text{When } x = 0 \ \longrightarrow\ u = \cos 0 = 1",
                      r"\text{When } x = \tfrac\pi2 \ \longrightarrow\ u = \cos\tfrac\pi2 = 0", r"-\int_1^0 u^2\,du = \int_0^1 u^2\,du",
                      r"= \left[\frac{u^3}{3}\right]_0^1 = \frac13"], at=[2, 3, 4, 5, 6, 7], figure=pick, figure_at=1, cues={0: choose})
        self.finish()

    # ---------------------------------------------------------------- lesson examples with a side-work column
    def setup_example(self, problem):
        card = ref_card()
        prob = problem.set_max_width(12.5 - card.width - 0.6).to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.5)
        self.play(FadeIn(card), FadeIn(prob, shift=DOWN * 0.2), run_time=0.8)
        return card, prob

    def fixing_a_constant(self):
        with self.beat("Fixing a constant") as b:
            prob = M(r"\text{Find } \int ", r"x", r"\sqrt{", r"x^2 + 4", r"}", r"\,dx", r".", 46)
            card, prob = self.setup_example(prob)
            sep = Line([-2.2, 2.4, 0], [-2.2, -3.5, 0], color=DIM, stroke_width=2)
            side = Column(-6.6, 2.2, 4.1, buff=0.4)
            main = Column(-1.7, 2.2, 8.2, buff=0.45)
            self.play(Create(sep), run_time=0.4)
            b.line(1)
            bx = SurroundingRectangle(prob[3], color=SECANT, buff=0.06)
            s1 = side.put(M(r"u = x^2 + 4", 42, SECANT))
            self.play(Create(bx), run_time=0.5)
            self.play(Write(s1), run_time=0.8)
            b.line(2)
            s2 = side.put(M(r"du = 2x\,dx", 42))
            self.play(Write(s2), run_time=0.8)
            b.line(3)
            ux = VGroup(under(prob[1]), under(prob[5]))
            s3 = side.put(T(r"we have $x\,dx$, not $2x\,dx$", 28, DERIV))
            self.play(Create(ux), run_time=0.6)
            self.play(FadeIn(s3), Indicate(s2, color=DERIV), run_time=0.8)
            b.line(4)
            s4 = side.put(T("divide both sides by 2", 28, DIM))
            self.play(FadeIn(s4), run_time=0.5)
            s5 = side.put(M(r"\tfrac12\,du = x\,dx", 42, DERIV))
            s5b = SurroundingRectangle(s5, color=DERIV, buff=0.12)
            self.play(Write(s5), run_time=0.8)
            self.play(Create(s5b), run_time=0.5)
            b.line(5)
            m1 = main.put(M(r"\int \sqrt{", r"u", r"} \cdot ", r"\tfrac12\,du", 48))
            m1[1].set_color(SECANT)
            m1[3].set_color(DERIV)
            self.play(FadeIn(m1[0]), FadeIn(m1[2]), TransformFromCopy(prob[3], m1[1]), TransformFromCopy(s5[0][0:4], m1[3]), run_time=1.3)
            b.line(6)
            m2 = main.put(M(r"= \tfrac12\int u^{1/2}\,du", 48))
            self.play(Write(m2), run_time=1)
            b.line(7)
            m3 = main.put(M(r"= \tfrac12 \cdot \frac{u^{3/2}}{3/2} + C = \tfrac13 u^{3/2} + C", 48))
            self.play(Write(m3), run_time=1.3)
            b.line(8)
            m4 = main.put(M(r"= \tfrac13\left(x^2 + 4\right)^{3/2} + C", 48, ACCUM))
            self.play(Write(m4), Indicate(s1, color=SECANT), run_time=1.2)
        self.wait(1.2)
        self.clear()
        self.wait(1.0)

    def changing_limits(self):
        with self.beat("Definite integrals: change the limits") as b:
            prob = M(r"\text{Evaluate } \int_{", r"0", r"}^{", r"2", r"} x\,(", r"x^2 + 1", r")^3\,dx", r".", 46)
            card, prob = self.setup_example(prob)
            sep = Line([-1.8, 2.4, 0], [-1.8, -3.5, 0], color=DIM, stroke_width=2)
            side = Column(-6.7, 2.2, 4.7, buff=0.35)
            main = Column(-1.3, 2.2, 7.9, buff=0.4)
            self.play(Create(sep), run_time=0.4)
            b.line(1)
            s1 = side.put(M(r"u = x^2 + 1", 42, SECANT))
            self.play(Create(SurroundingRectangle(prob[5], color=SECANT, buff=0.06)), Write(s1), run_time=0.9)
            s2 = side.put(M(r"du = 2x\,dx", 42))
            self.play(Write(s2), run_time=0.7)
            s3 = side.put(M(r"\tfrac12\,du = x\,dx", 42, DERIV))
            self.play(Write(s3), run_time=0.7)
            b.line(2)
            rings = VGroup(*[Circle(radius=0.2, color=TANGENT, stroke_width=4).move_to(prob[k]) for k in (1, 3)])
            lim = T("limits of integration: $x$ values", 30, TANGENT).move_to([2.6, 1.9, 0])
            self.play(Create(rings), run_time=0.6)
            self.play(FadeIn(lim), run_time=0.5)
            b.line(3)
            m1 = main.put(M(r"\tfrac12\int_{", r"x = 0", r"}^{", r"x = 2", r"} ", r"u^3\,du", 50))
            m1[1].set_color(TANGENT)
            m1[3].set_color(TANGENT)
            self.play(FadeOut(lim), run_time=0.3)
            self.play(Write(m1), run_time=1.2)
            b.line(4)
            l1 = main.put(M(r"= \left[\tfrac18 u^4\right]_{x = 0}^{x = 2}", 46, DIM))
            self.play(Write(l1), run_time=1)
            b.line(5)
            l2 = main.put(M(r"= \left[\tfrac18\left(x^2 + 1\right)^4\right]_0^2", 46, DIM))
            self.play(Write(l2), run_time=1)
            l3 = main.put(M(r"= \tfrac18(625) - \tfrac18(1) = 78", 46, DIM))
            self.play(Write(l3), run_time=1)
            b.line(6)
            long = VGroup(l1, l2, l3)
            x = VGroup(Line(long.get_corner(UL), long.get_corner(DR), color=TANGENT, stroke_width=6),
                       Line(long.get_corner(DL), long.get_corner(UR), color=TANGENT, stroke_width=6))
            never = T("we never do this", 32, TANGENT).next_to(long, DOWN, buff=0.15)
            self.play(Create(x), run_time=0.8)
            self.play(FadeIn(never), run_time=0.5)
            b.line(7)
            self.play(FadeOut(VGroup(long, x, never)), run_time=0.6)
            main.last = m1
            self.play(Indicate(s1, color=SECANT), run_time=0.9)
            b.line(8)
            w0 = side.put(when(r"x = 0", r"u = 0^2 + 1 = 1"))
            side.buff = 0.3
            self.play(FadeIn(w0[0:3]), run_time=0.6)
            self.play(Write(w0[3]), run_time=0.9)
            w2 = side.put(when(r"x = 2", r"u = 2^2 + 1 = 5"))
            self.play(FadeIn(w2[0:3]), run_time=0.6)
            self.play(Write(w2[3]), run_time=0.9)
            b.line(9)
            m2 = M(r"\tfrac12\int_{", r"1", r"}^{", r"5", r"} ", r"u^3\,du", 50).move_to(m1, aligned_edge=LEFT)
            m2[1].set_color(SECANT)
            m2[3].set_color(SECANT)
            self.play(*[ReplacementTransform(m1[k], m2[k]) for k in (0, 2, 4, 5)], FadeOut(m1[1]), FadeOut(m1[3]),
                      TransformFromCopy(w0[3][0][-1], m2[1]), TransformFromCopy(w2[3][0][-1], m2[3]), run_time=1.3)
            self.remove(m1)
            main.last = m2
            b.line(10)
            m3 = main.put(M(r"= \tfrac12\left[\frac{u^4}{4}\right]_1^5 = \tfrac18\left(625 - 1\right)", 48))
            self.play(Write(m3), run_time=1.2)
            b.line(11)
            m4 = main.put(M(r"= \frac{624}{8} = 78", 48, ACCUM))
            same_ = T("same answer, no trip back to $x$", 30, DIM).next_to(m4, RIGHT, buff=0.5)
            self.play(Write(m4), run_time=1)
            self.play(FadeIn(same_), run_time=0.5)
        self.wait(1.2)
        self.clear()
        self.wait(1.0)
