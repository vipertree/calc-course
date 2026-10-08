"""Topic 4.2: Straight-line motion. Narration comes from transcripts/4_2.md.
Running example x(t) = t^3 - 6t^2 + 9t: at rest at t = 1, 3; distance on [0, 4] is 12.

Adder (2026-10-03): take this one slowly. The car faces the way it moves and turns around at t = 1 and t = 3; the sign
analysis of v shows its work (standard form, factoring, zeros, why one test value per section is enough, test values,
factor signs); speeding up and slowing down get all four cases."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import car_sprite, face


def X(t):
    return t ** 3 - 6 * t * t + 9 * t


def V(t):
    return 3 * t * t - 12 * t + 9


class Lesson(TranscriptScene):
    NUM = "4.2"

    def track(self):
        nl = NumberLine(x_range=[-1, 6.5, 1], length=9.6, color=DIM, include_numbers=True, font_size=26).to_edge(UP, buff=1.3)
        return nl

    def turn(self, car, way, run_time=0.6):
        """A visible turnaround: the car squeezes to nothing and opens out facing the other way."""
        self.play(car.animate.stretch(-1, 0), run_time=run_time, rate_func=rate_functions.ease_in_out_sine)
        car.facing = way

    def case_row(self, y, v_sign, a_sign, word):
        """One of the four cases: signs of v and a with direction arrows, a road, a car that will move, and the verdict.
        Returns (label, road, car, verdict, S, trail) where S (0..1) drives the car."""
        vc = SECANT
        ac = TANGENT
        arrow = lambda s, c: Arrow(LEFT * 0.35 * s, RIGHT * 0.35 * s, buff=0, color=c, stroke_width=5, max_tip_length_to_length_ratio=0.4)
        lab = VGroup(VGroup(M(r"v " + (">" if v_sign > 0 else "<") + " 0", 36, vc), arrow(v_sign, vc)).arrange(RIGHT, buff=0.2),
                     VGroup(M(r"a " + (">" if a_sign > 0 else "<") + " 0", 36, ac), arrow(a_sign, ac)).arrange(RIGHT, buff=0.2)
                     ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([-5.3, y, 0])
        road = Line([-3.0, y - 0.3, 0], [2.6, y - 0.3, 0], color=DIM, stroke_width=4)
        x0, x1 = (-2.5, 2.1) if v_sign > 0 else (2.1, -2.5)
        speeding = v_sign == a_sign
        prog = (lambda s: s * s) if speeding else (lambda s: 1 - (1 - s) ** 2)
        S = ValueTracker(0)
        car = car_sprite(0.95)
        face(car, v_sign)
        car.add_updater(lambda m: m.move_to([x0 + (x1 - x0) * prog(S.get_value()), y - 0.3 + m.height / 2 + 0.03, 0]))
        car.update()
        # where the car was at equal time steps: the gaps grow when it speeds up and shrink when it slows down
        trail = always_redraw(lambda: VGroup(*[Dot([x0 + (x1 - x0) * prog(k / 5), y - 0.42, 0], radius=0.05, color=INK)
                                               for k in range(6) if k / 5 <= S.get_value() + 1e-6]))
        verdict = T(word, 34, DERIV if speeding else TANGENT).move_to([4.75, y - 0.05, 0])
        return lab, road, car, verdict, S, trail

    def construct(self):
        nl = self.track()
        T_ = ValueTracker(0)
        car = car_sprite(1.0)
        car.add_updater(lambda m: m.move_to(nl.n2p(X(T_.get_value())) + UP * (m.height / 2 + 0.08)))
        car.update()
        ax, al = plot_axes([0, 4.5, 1], [-1, 6, 1], w=7.6, h=3.4, xlabel="t", ylabel="x(t)")
        VGroup(ax, al).to_edge(DOWN, buff=0.4)
        curve = always_redraw(lambda: ax.plot(X, x_range=[0, max(T_.get_value(), 0.01)], color=FUNC, stroke_width=4))
        with self.beat("Back and forth on a line") as b:
            self.play(Create(nl), FadeIn(ax), FadeIn(al), FadeIn(car), run_time=1)
            self.add(curve)
            self.play(T_.animate.set_value(1), run_time=2.2, rate_func=rate_functions.ease_out_sine)
            self.turn(car, -1)
            self.play(T_.animate.set_value(3), run_time=3.6, rate_func=rate_functions.ease_in_out_sine)
            self.turn(car, 1)
            self.play(T_.animate.set_value(4.2), run_time=2.4, rate_func=rate_functions.ease_in_sine)
            b.line(1)
            self.play(FadeIn(M(r"x(t) = t^3 - 6t^2 + 9t", 38, FUNC).next_to(ax, RIGHT, buff=0.2).shift(UP * 1.2)), run_time=0.8)
            b.line(2)
            note = T(r"the graph is \emph{not} the path", 34, TANGENT).next_to(nl, DOWN, buff=0.35)
            self.play(FadeIn(note), Indicate(car, scale_factor=1.15), run_time=1)
        car.clear_updaters()
        self.clear()
        self.title()

        with self.beat("Three functions") as b:
            rows = [(M(r"x(t)", 52, FUNC), T("position", 36), T("m", 32, DIM)),
                    (M(r"v(t) = x'(t)", 52, SECANT), T("velocity", 36), T("m/s", 32, DIM)),
                    (M(r"a(t) = v'(t)", 52, TANGENT), T("acceleration", 36), T(r"m/s$^2$", 32, DIM))]
            for k, (f, n, u) in enumerate(rows):
                yy = 2.5 - 1.25 * k
                f.move_to([-3.6, yy, 0], aligned_edge=LEFT).align_to(LEFT * 4.6, LEFT)
                n.move_to([1.6, yy, 0])
                u.move_to([3.9, yy, 0])
            also_x = T(r"(you may also see $s(t)$ or $y(t)$)", 28, DIM).next_to(rows[0][0], DOWN, buff=0.12).align_to(rows[0][0], LEFT)
            also_a = T(r"(also $x''(t)$)", 28, DIM).next_to(rows[2][0], DOWN, buff=0.12).align_to(rows[2][0], LEFT)
            self.play(FadeIn(VGroup(*rows[0])), run_time=0.8)
            self.play(FadeIn(also_x), run_time=0.6)
            b.line(2)
            self.play(FadeIn(VGroup(*rows[1]), shift=RIGHT * 0.2), run_time=0.9)
            b.line(4)
            self.play(FadeIn(VGroup(*rows[2]), shift=RIGHT * 0.2), run_time=0.9)
            self.play(FadeIn(also_a), run_time=0.6)
            b.line(5)
            ours = VGroup(M(r"v(t) = 3t^2 - 12t + 9", 46, SECANT), M(r"a(t) = 6t - 12", 46, TANGENT)).arrange(DOWN, buff=0.35).to_edge(DOWN, buff=0.6)
            self.play(Write(ours), run_time=1.4)
        self.clear()

        with self.beat("Direction") as b:
            q = T(r"$v > 0$: moving right \qquad $v < 0$: moving left", 38).to_edge(UP, buff=0.5)
            self.play(FadeIn(q), run_time=0.8)
            b.line(1)
            l1 = M(r"v(t) = 3t^2 - 12t + 9", 50, SECANT)
            l2 = M(r"= 3(t^2 - 4t + 3)", 50, SECANT)
            l3 = M(r"= 3(t - 1)(t - 3)", 50, SECANT)
            work = VGroup(l1, l2, l3).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(q, DOWN, buff=0.5).to_edge(LEFT, buff=1.4)
            l2.align_to(l1[0][4], LEFT)
            l3.align_to(l1[0][4], LEFT)
            self.play(Write(l1), run_time=1)
            self.play(Write(l2), run_time=1)
            b.line(2)
            self.play(Write(l3), run_time=1)
            b.line(3)
            zp = VGroup(M(r"t - 1 = 0 \ \ \text{or}\ \ t - 3 = 0", 44), M(r"t = 1 \ \ \text{or}\ \ t = 3", 46, SECANT)).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            zp.next_to(work, RIGHT, buff=1.0).align_to(l2, UP)
            self.play(FadeIn(zp[0]), run_time=0.8)
            self.play(Write(zp[1]), run_time=0.8)
            b.line(4)
            why = callout(r"$v$ is a polynomial, so it is continuous: \\ it can change sign only at its zeros. \\ One test value per section is enough.", INK, 34)
            why.next_to(work, DOWN, buff=0.5).set_x(0)
            self.play(FadeIn(why), run_time=1)
        self.clear()

        with self.beat("Testing each section") as b:
            top = M(r"v(t) = 3t^2 - 12t + 9 = 3(t - 1)(t - 3)", 40, SECANT).to_edge(UP, buff=0.35)
            px = lambda tv: -4.2 + tv * (9.0 / 4.6)
            yl = 1.55
            line = Arrow([px(0), yl, 0], [px(4.6) + 0.3, yl, 0], buff=0, color=DIM, stroke_width=4, max_tip_length_to_length_ratio=0.03)
            t0 = VGroup(Line([px(0), yl - 0.12, 0], [px(0), yl + 0.12, 0], color=DIM, stroke_width=3), M("0", 32, DIM).move_to([px(0), yl - 0.42, 0]))
            ticks = VGroup(*[VGroup(Line([px(k), yl - 0.3, 0], [px(k), yl + 0.3, 0], color=SECANT, stroke_width=7),
                                    M(str(k), 42, SECANT).move_to([px(k), yl - 0.62, 0])) for k in (1, 3)])
            tlab = M("t", 36, DIM).next_to(line, RIGHT, buff=0.15)
            centers = [0.5, 2.0, 3.8]
            self.play(FadeIn(top), Create(line), FadeIn(t0), FadeIn(tlab), run_time=1)
            self.play(FadeIn(ticks, scale=1.3), run_time=0.8)
            tests = [(r"t = 0", r"v(0) = 9 > 0", "+"), (r"t = 2", r"v(2) = 12 - 24 + 9 = -3 < 0", "-"), (r"t = 4", r"v(4) = 48 - 48 + 9 = 9 > 0", "+")]
            signs = VGroup()
            for k, (c, (tv, calc, sg)) in enumerate(zip(centers, tests)):
                b.line(k + 1)
                col = DERIV if sg == "+" else TANGENT
                qm = M("?", 48, DIM).move_to([px(c), yl + 0.55, 0])
                self.play(FadeIn(qm), Indicate(Line([px(c) - 0.5, yl, 0], [px(c) + 0.5, yl, 0], color=SECANT, stroke_width=8)), run_time=0.8)
                tst = VGroup(M(tv, 30, DIM), M(calc, 30)).arrange(DOWN, buff=0.12).move_to([px(c), yl - 1.25, 0])
                tst.set_max_width(3.6 if k == 1 else 2.2)
                self.play(FadeIn(tst), run_time=1)
                s_ = M(sg, 60, col).move_to([px(c), yl + 0.55, 0])
                self.play(ReplacementTransform(qm, s_), run_time=0.6)
                signs.add(s_)
            b.line(4)
            fac = [("3", "+++"), ("t - 1", "-++"), ("t - 3", "--+")]
            rows = VGroup()
            for r_, (name, sg) in enumerate(fac):
                yy = -1.0 - 0.62 * r_
                row = VGroup(M(name, 34, DIM).move_to([-5.6, yy, 0]),
                             *[M(s, 40, DERIV if s == "+" else TANGENT).move_to([px(c), yy, 0]) for s, c in zip(sg, centers)])
                rows.add(row)
            rule = Line([-6.3, -2.62, 0], [px(4.6), -2.62, 0], color=DIM, stroke_width=2)
            prod = VGroup(M(r"v", 36, SECANT).move_to([-5.6, -3.05, 0]),
                          *[M(s, 44, DERIV if s == "+" else TANGENT).move_to([px(c), -3.05, 0]) for s, c in zip("+-+", centers)])
            for row in rows:
                self.play(FadeIn(row, shift=DOWN * 0.1), run_time=0.7)
            self.play(Create(rule), FadeIn(prod), run_time=0.8)
            b.line(5)
            dirs = VGroup(*[T(w, 30, DERIV if w == "right" else TANGENT).move_to([px(c), yl + 1.15, 0]) for w, c in zip(["right", "left", "right"], centers)])
            rests = VGroup(*[T("rest", 26, SECANT).move_to([px(k), yl + 0.55, 0]) for k in (1, 3)])
            self.play(FadeIn(dirs), Indicate(prod[1:], color=SECANT), run_time=1)
            self.play(FadeIn(rests), *[Flash([px(k), yl, 0], color=SECANT) for k in (1, 3)], run_time=1)
        self.clear()

        with self.beat("Speed") as b:
            pair = VGroup(VGroup(M(r"v = -5", 52, TANGENT), Arrow(RIGHT, LEFT, color=TANGENT)).arrange(DOWN),
                          VGroup(M(r"v = 5", 52, DERIV), Arrow(LEFT, RIGHT, color=DERIV)).arrange(DOWN)).arrange(RIGHT, buff=2.5).shift(UP * 0.6)
            self.play(FadeIn(pair), run_time=1)
            b.line(1)
            sp_ = M(r"\text{speed} = |v(t)| = 5", 52, SECANT).shift(DOWN * 1.8)
            self.play(Write(sp_), run_time=1)
        self.clear()

        with self.beat("Speeding up and slowing down") as b:
            q = T(r"Speeding up when $a > 0$?", 44).to_edge(UP, buff=0.4)
            self.play(FadeIn(q), run_time=0.8)
            cases = [(1, 1, "speeding up"), (-1, -1, "speeding up"), (1, -1, "slowing down"), (-1, 1, "slowing down")]
            ys = [2.1, 0.55, -1.0, -2.55]
            rowsg = []
            for k, ((vs, as_, word), y) in enumerate(zip(cases, ys)):
                b.line(k + 1)
                if k == 0:
                    self.play(FadeOut(q), run_time=0.4)
                lab, road, car, verdict, S, trail = self.case_row(y, vs, as_, word)
                self.play(FadeIn(lab), Create(road), FadeIn(car), run_time=0.8)
                self.add(trail)
                self.play(S.animate.set_value(1), run_time=3.2, rate_func=linear)
                self.play(FadeIn(verdict, shift=LEFT * 0.2), run_time=0.6)
                car.clear_updaters()
                rowsg += [lab, road, car, verdict, trail]
            b.line(5)
            self.play(*[FadeOut(m) for m in rowsg], run_time=0.6)
            box = formula_box(VGroup(T(r"Check the signs of $v$ and $a$.", 42),
                                     T(r"Same signs: \textbf{speeding up}", 42, DERIV),
                                     T(r"Different signs: \textbf{slowing down}", 42, TANGENT)).arrange(DOWN, buff=0.35), SECANT)
            self.play(FadeIn(box), run_time=1)
        self.clear()

        nl = self.track().shift(DOWN * 0.4)
        with self.beat("Distance versus displacement") as b:
            ask = T(r"What is the total distance traveled from $t = 0$ to $t = 4$?", 38).to_edge(UP, buff=0.35)
            self.play(FadeIn(ask), Create(nl), run_time=0.8)
            b.line(1)
            self.play(FadeIn(Dot(nl.n2p(0), color=INK)), FadeIn(Dot(nl.n2p(4), color=INK)), run_time=0.4)
            disp = M(r"\text{displacement} = x(4) - x(0) = 4 - 0 = 4", 42).shift(DOWN * 1.9)
            self.play(Write(disp), run_time=1.2)
            b.line(2)
            legs = VGroup(Arrow(nl.n2p(0), nl.n2p(4), buff=0, color=SECANT).shift(DOWN * 0.5),
                          Arrow(nl.n2p(4), nl.n2p(0), buff=0, color=TANGENT).shift(DOWN * 0.9),
                          Arrow(nl.n2p(0), nl.n2p(4), buff=0, color=SECANT).shift(DOWN * 1.3))
            self.play(disp.animate.set_opacity(0.45), run_time=0.4)
            for g in legs:
                self.play(GrowArrow(g), run_time=0.8)
            dist = M(r"\text{total distance} = 4 + 4 + 4 = 12", 44, SECANT).next_to(disp, DOWN, buff=0.4)
            self.play(Write(dist), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"v(t) = x'(t), \qquad a(t) = v'(t) = x''(t)", 44), T(r"sign of $v$: direction", 38), T(r"$|v|$: speed", 38),
                          T(r"$v$ and $a$ with the same sign: speeding up", 38)).arrange(DOWN, buff=0.4)
            self.play(FadeIn(formula_box(card, DERIV)), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: When is it moving left?", r"$x(t) = t^3 - 6t^2 + 9t$ for $t \ge 0$. When is the particle at rest? When is it moving left?",
                     [r"TEXT:At rest means $v(t) = 0$. Moving left means $v(t) < 0$.",
                      r"v(t) = 3t^2 - 12t + 9 = 3(t - 1)(t - 3)", r"v(t) = 0 \text{ at } t = 1 \text{ and } t = 3",
                      r"v(t) < 0 \text{ for } 1 < t < 3:\ \text{moving left}"],
                     at=[1, 2, 3, 4])
        self.example("Example 2: Speeding up or slowing down?",
                     r"For $x(t) = t^3 - 6t^2 + 9t$, is the particle speeding up or slowing down at $t = 1.5$? At $t = 2.5$?",
                     [r"TEXT:Speeding up means $v$ and $a$ have the same sign; slowing down means opposite signs.",
                      r"v(t) = 3t^2 - 12t + 9, \qquad a(t) = 6t - 12",
                      r"t = 1.5:\ \ v = -2.25,\ \ a = -3,\ \text{same sign, so}\ \text{speeding up}",
                      r"t = 2.5:\ \ v = -2.25,\ \ a = 3,\ \text{opposite signs, so}\ \text{slowing down}"], at=[1, 2, 3, 4])
        self.example("Example 3: Total distance", r"For $x(t) = t^3 - 6t^2 + 9t$, find the total distance traveled from $t = 0$ to $t = 4$.",
                     [r"TEXT:Total distance adds every stretch traveled. Split the trip where $v$ changes sign.",
                      r"\text{turning points: } t = 1,\ 3", r"x(0) = 0,\ x(1) = 4,\ x(3) = 0,\ x(4) = 4",
                      r"|4 - 0| + |0 - 4| + |4 - 0| = 12", r"\text{displacement: } x(4) - x(0) = 4"], at=[1, 2, 2, 3, 4])
        self.finish()
