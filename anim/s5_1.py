"""Topic 5.1: The Mean Value Theorem. Narration comes from transcripts/5_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.1"

    def construct(self):
        with self.beat("A speeding ticket") as b:
            road = Line(LEFT * 5.5, RIGHT * 5.5, color=DIM, stroke_width=8).shift(DOWN * 0.5)
            booths = VGroup(*[VGroup(Rectangle(width=0.5, height=0.9, color=INK, fill_color=PANEL, fill_opacity=1), T(lab, 30, DIM).shift(UP * 0.8))
                              .move_to(road.point_from_proportion(p) + UP * 0.45) for p, lab in ((0.05, "1:00"), (0.95, "3:00"))])
            car = VGroup(RoundedRectangle(width=0.9, height=0.4, corner_radius=0.1, color=SECANT, fill_color=SECANT, fill_opacity=1),
                         Dot(LEFT * 0.25 + DOWN * 0.22, radius=0.08, color=INK), Dot(RIGHT * 0.25 + DOWN * 0.22, radius=0.08, color=INK)).move_to(road.point_from_proportion(0.05) + UP * 0.3)
            miles = M(r"120 \text{ miles}", 40).next_to(road, DOWN, buff=0.4)
            self.play(Create(road), FadeIn(booths), FadeIn(car), run_time=1)
            self.play(car.animate.move_to(road.point_from_proportion(0.95) + UP * 0.3), FadeIn(miles), run_time=3, rate_func=rate_functions.ease_in_out_sine)
            b.line(1)
            ticket = VGroup(RoundedRectangle(width=5.6, height=1.2, corner_radius=0.1, color=TANGENT), M(r"\text{average speed} = \frac{120}{2} = 60 \text{ mph}", 40, TANGENT))
            ticket[1].move_to(ticket[0])
            ticket.shift(UP * 2.3)
            self.play(FadeIn(ticket), run_time=0.8)
            b.line(2)
            gauge = M(r"\text{speedometer: } 60", 40, DERIV).next_to(miles, DOWN, buff=0.5)
            self.play(FadeIn(gauge), run_time=0.6)
        self.clear()
        self.title()

        ax, al = plot_axes([0, 5, 1], [0, 5, 1], w=7.4, h=5.4, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        f = lambda s: 0.2 * s**3 - 1.5 * s**2 + 3.2 * s + 1
        df = lambda s: 0.6 * s**2 - 3 * s + 3.2
        a, bb = 0.4, 4.6
        m = (f(bb) - f(a)) / (bb - a)
        cs = [r.real for r in np.roots([0.6, -3, 3.2 - m]) if abs(r.imag) < 1e-9 and a < r.real < bb]
        c = min(cs)
        line_at = lambda k: ax.plot(lambda s: f(a) + m * (s - a) + k, x_range=[0.1, 4.9], color=SECANT, stroke_width=4)
        with self.beat("Slide the secant") as b:
            curve = ax.plot(f, x_range=[0.1, 4.9], color=FUNC, stroke_width=5)
            self.play(FadeIn(ax), FadeIn(al), Create(curve), run_time=1.2)
            pts = VGroup(Dot(ax.c2p(a, f(a)), color=INK), Dot(ax.c2p(bb, f(bb)), color=INK))
            ab = VGroup(M("a", 34).next_to(ax.c2p(a, 0), DOWN, buff=0.15), M("b", 34).next_to(ax.c2p(bb, 0), DOWN, buff=0.15))
            sec = line_at(0)
            self.play(FadeIn(pts), FadeIn(ab), Create(sec), run_time=1)
            avg = M(r"\text{slope} = \frac{f(b) - f(a)}{b - a}", 40, SECANT).to_edge(RIGHT, buff=0.5).shift(UP * 2.2)
            self.play(FadeIn(avg), run_time=0.6)
            b.line(1)
            K = ValueTracker(0)
            copy = always_redraw(lambda: line_at(K.get_value()).set_stroke(TANGENT, 4))
            self.add(copy)
            target = f(c) - (f(a) + m * (c - a))
            self.play(K.animate.set_value(target), run_time=3, rate_func=rate_functions.ease_in_out_sine)
            b.line(2)
            cdot = Dot(ax.c2p(c, f(c)), color=TANGENT, radius=0.1)
            clab = M("c", 34, TANGENT).next_to(ax.c2p(c, 0), DOWN, buff=0.15)
            self.play(FadeIn(cdot), FadeIn(clab), Create(DashedLine(ax.c2p(c, 0), ax.c2p(c, f(c)), color=DIM)), run_time=0.8)
            tl = M(r"f'(c) = \text{slope of the secant}", 40, TANGENT).next_to(avg, DOWN, buff=0.6)
            self.play(FadeIn(tl), run_time=0.6)
            b.line(3)
            self.play(Indicate(tl, color=TANGENT), run_time=1)
        self.clear()

        thm = VGroup(T(r"If $f$ is continuous on $[a, b]$", 42), T(r"and differentiable on $(a, b)$,", 42),
                     M(r"\text{then } f'(c) = \frac{f(b) - f(a)}{b - a} \text{ for some } c \text{ in } (a, b).", 46, TANGENT)).arrange(DOWN, buff=0.4)
        with self.beat("The theorem") as b:
            frame = SurroundingRectangle(thm, color=TANGENT, buff=0.35)
            head = T("The Mean Value Theorem", 48, SECANT).next_to(frame, UP, buff=0.4)
            self.play(FadeIn(head), Create(frame), FadeIn(thm[0]), FadeIn(thm[1]), run_time=1.2)
            b.line(1)
            self.play(Write(thm[2]), run_time=1.6)
        self.clear()

        ax, al = plot_axes([-1, 2, 1], [0, 2, 1], w=6.6, h=4.6, coords=False)
        VGroup(ax, al).to_edge(LEFT, buff=0.8).shift(DOWN * 0.3)
        with self.beat("When it fails") as b:
            g = ax.plot(lambda s: abs(s), x_range=[-1, 2, 0.5], color=FUNC, stroke_width=5)
            sec = Line(ax.c2p(-1, 1), ax.c2p(2, 2), color=SECANT, stroke_width=4)
            self.play(FadeIn(ax), FadeIn(al), Create(g), run_time=1)
            b.line(1)
            self.play(Create(sec), FadeIn(M(r"\text{secant slope} = \frac13", 40, SECANT).to_edge(RIGHT, buff=0.7).shift(UP * 1.8)), run_time=1)
            slopes = VGroup(M(r"\text{left of } 0:\ f' = -1", 38, TANGENT), M(r"\text{right of } 0:\ f' = 1", 38, TANGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            slopes.to_edge(RIGHT, buff=0.7).shift(UP * 0.2)
            self.play(FadeIn(slopes), run_time=0.8)
            b.line(2)
            ring = Circle(radius=0.3, color=TANGENT).move_to(ax.c2p(0, 0))
            self.play(Create(ring), FadeIn(T("not differentiable at $0$", 36, TANGENT).next_to(slopes, DOWN, buff=0.6).align_to(slopes, LEFT)), run_time=1)
        self.clear()
        self.example("From given values", r"$f$ is differentiable, $f(1) = 4$ and $f(5) = 12$. Must $f'(c) = 2$ for some $c$ in $(1, 5)$?",
                     [r"\text{differentiable},\ \text{so}\ \text{continuous on } [1, 5], \text{ differentiable on } (1, 5)", r"\frac{f(5) - f(1)}{5 - 1} = \frac{12 - 4}{4} = 2", r"\text{MVT: } f'(c) = 2 \text{ for some } c \text{ in } (1, 5)"], at=[1, 2, 3])

        with self.beat("Close") as b:
            thm2 = thm.copy()
            frame = SurroundingRectangle(thm2, color=TANGENT, buff=0.35)
            self.play(FadeIn(thm2), Create(frame), run_time=0.8)
            self.play(thm2[0].animate.set_color(DERIV), thm2[1].animate.set_color(DERIV), run_time=0.6)
            ap = T("On the AP exam: name the theorem and check both conditions.", 36, DIM).next_to(frame, DOWN, buff=0.5)
            self.play(FadeIn(ap), run_time=0.6)
        self.clear()

        self.examples_card()
        self.example("Example 1: Finding c", r"Find every $c$ guaranteed by the Mean Value Theorem for $f(x) = x^3 - x$ on $[0, 2]$.",
                     [r"TEXT:$f$ is a polynomial: continuous and differentiable everywhere.", r"\frac{f(2) - f(0)}{2 - 0} = \frac{6 - 0}{2} = 3",
                      r"f'(c) = 3c^2 - 1 = 3", r"c^2 = \frac43,\ \ c = \frac{2}{\sqrt3} \approx 1.15"], at=[1, 2, 3, 4])
        self.example("Example 2: Does it apply?", r"Does the Mean Value Theorem apply to $f(x) = \dfrac{1}{x - 3}$ on $[1, 5]$?",
                     [r"TEXT:$f$ is undefined at $x = 3$, so it is not continuous there.", r"TEXT:$3$ is in $[1, 5]$: the theorem does not apply."], at=[1, 2])
        self.example("Example 3: The speedometer",
                     r"A car's position $s(t)$ is differentiable. It travels $120$ miles from $t = 1$ to $t = 3$ hours. Show that its velocity was exactly $60$ mph at some time.",
                     [r"TEXT:$s$ is differentiable, so it is continuous on $[1, 3]$ and differentiable on $(1, 3)$.",
                      r"\text{MVT: } s'(c) = \frac{s(3) - s(1)}{3 - 1} = \frac{120}{2}", r"= 60 \text{ mph for some } c \text{ in } (1, 3)"], at=[1, 2, 3])
        self.finish()
