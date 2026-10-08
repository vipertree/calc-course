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
        c, c2 = min(cs), max(cs)   # this cubic has two MVT points (about 1.29 and 3.71); the theorem promises one
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
            b.line(4)
            target2 = f(c2) - (f(a) + m * (c2 - a))
            self.play(K.animate.set_value(target2), run_time=3, rate_func=rate_functions.ease_in_out_sine)
            c2dot = Dot(ax.c2p(c2, f(c2)), color=TANGENT, radius=0.1)
            c2lab = M("c_2", 34, TANGENT).next_to(ax.c2p(c2, 0), DOWN, buff=0.15)
            self.play(FadeIn(c2dot), FadeIn(c2lab), Create(DashedLine(ax.c2p(c2, 0), ax.c2p(c2, f(c2)), color=DIM)), run_time=0.8)
            b.line(5)
            once = VGroup(T("two points here,", 36, DIM), T("but only one $c$ is guaranteed", 36, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            once.next_to(tl, DOWN, buff=0.6).align_to(tl, LEFT)
            self.play(FadeIn(once), run_time=0.8)
        self.clear()

        thm = VGroup(T(r"If $f$ is continuous on $[a, b]$", 42), T(r"and differentiable on $(a, b)$,", 42),
                     M(r"\text{then } f'(c) = \frac{f(b) - f(a)}{b - a} \text{ for some } c \text{ in } (a, b).", 46, TANGENT)).arrange(DOWN, buff=0.4).shift(UP * 0.6)
        with self.beat("The theorem") as b:
            frame = SurroundingRectangle(thm, color=TANGENT, buff=0.35)
            head = T("The Mean Value Theorem", 48, SECANT).next_to(frame, UP, buff=0.4)
            self.play(FadeIn(head), Create(frame), FadeIn(thm[0]), FadeIn(thm[1]), run_time=1.2)
            b.line(1)
            self.play(Write(thm[2]), run_time=1.6)
            b.line(2)
            words = VGroup(T(r"In words: at some $c$ between $a$ and $b$,", 38, INK),
                           T(r"instantaneous rate of change $=$ average rate of change over $[a, b]$", 38, TANGENT)).arrange(DOWN, buff=0.15)
            words.set_max_width(12.4).next_to(frame, DOWN, buff=0.5)
            self.play(FadeIn(words), run_time=1)
        self.clear()

        with self.beat("Closed and open") as b:
            conds = VGroup(
                VGroup(T(r"continuous on $[a, b]$", 40, DERIV), T("endpoints included", 32, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
                VGroup(T(r"differentiable on $(a, b)$", 40, DERIV), T("endpoints don't need a derivative", 32, DIM)).arrange(DOWN, aligned_edge=LEFT, buff=0.15),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
            b.line(1)
            self.play(FadeIn(conds[0]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(conds[1]), run_time=0.8)
            b.line(3)
            pax, pal = plot_axes([-2, 2, 1], [-4, 4, 2], w=5.4, h=4.8, coords=False)
            VGroup(pax, pal).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
            pa, pb = -0.5, 1.5
            band = Polygon(pax.c2p(pa, -4), pax.c2p(pb, -4), pax.c2p(pb, 4), pax.c2p(pa, 4), stroke_width=0, fill_color=SECANT, fill_opacity=0.18)
            ends = VGroup(M("a", 34, SECANT).next_to(pax.c2p(pa, -4), DOWN, buff=0.15), M("b", 34, SECANT).next_to(pax.c2p(pb, -4), DOWN, buff=0.15))
            poly = pax.plot(lambda s: s**3 - s, x_range=[-1.7, 1.7], color=FUNC, stroke_width=5)
            self.play(FadeIn(pax), FadeIn(pal), FadeIn(band), FadeIn(ends), run_time=0.8)
            self.play(Create(poly), run_time=1.6)
            why = VGroup(M(r"y = x^3 - x", 36, FUNC), T("a polynomial: continuous and", 32, INK), T("differentiable everywhere", 32, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            why.next_to(conds, DOWN, buff=0.6).align_to(conds, LEFT)
            self.play(FadeIn(why), run_time=0.8)
            b.line(4)
            just = VGroup(T("Justify with both:", 36, TANGENT), T("continuous and differentiable", 36, TANGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            just.next_to(why, DOWN, buff=0.5).align_to(conds, LEFT)
            self.play(FadeIn(just), run_time=0.8)
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
                      r"f'(c) = 3c^2 - 1 = 3", r"3c^2 = 4", r"c^2 = \frac43", r"c = \pm\sqrt{\frac43} = \pm\frac{2}{\sqrt3}",
                      r"\frac{2}{\sqrt3} \approx 1.15 \text{ is in } (0, 2);\ \ -\frac{2}{\sqrt3} \text{ is not}", r"c = \frac{2}{\sqrt3}"], at=[1, 2, 3, 4, 5, 6, 7, 8])
        self.example("Example 2: Does it apply?", r"Does the Mean Value Theorem apply to $f(x) = \dfrac{1}{x - 3}$ on $[1, 5]$?",
                     [r"TEXT:$f$ is undefined at $x = 3$, so it is not continuous there.", r"TEXT:$3$ is in $[1, 5]$: the theorem does not apply."], at=[1, 2])
        self.example("Example 3: The speedometer",
                     r"A car's position $s(t)$ is differentiable. It travels $120$ miles from $t = 1$ to $t = 3$ hours. Show that its velocity was exactly $60$ mph at some time.",
                     [r"TEXT:$s$ is differentiable, so it is continuous on $[1, 3]$ and differentiable on $(1, 3)$.",
                      r"\text{MVT: } s'(c) = \frac{s(3) - s(1)}{3 - 1} = \frac{120}{2}", r"= 60 \text{ mph for some } c \text{ in } (1, 3)"], at=[1, 2, 3])
        gt = table(["t", "0", "2", "5", "9", "10"], [["g(t)", "4", "10", "1", "13", "7"]], size=38)

        def pick(scene):
            scene.play(*[gt.cells[r][c].animate.set_color(SECANT) for r in (0, 1) for c in (2, 3)], run_time=0.6)
        self.example("Example 4: From a table",
                     VGroup(T(r"$g$ is differentiable. Must there be a value $c$, with $0 < c < 10$, for which $g'(c) = -3$?", 36), gt).arrange(DOWN, buff=0.3),
                     [r"TEXT:Need: two $t$ values with average rate of change $-3$.", r"\frac{g(10) - g(0)}{10 - 0} = \frac{7 - 4}{10} = 0.3 \quad \text{(no help)}",
                      r"\frac{g(5) - g(2)}{5 - 2} = \frac{1 - 10}{3} = -3",
                      r"TEXT:$g$ is differentiable, so it is continuous on $[2, 5]$ and differentiable on $(2, 5)$.",
                      r"\text{MVT: } g'(c) = -3 \text{ for some } c \text{ in } (2, 5), \text{ inside } (0, 10)",
                      r"TEXT:Tables: try pairs until one gives the rate you need."], at=[1, 2, 3, 4, 5, 6], cues={2: pick},
                     text=r"$g$ is differentiable, with selected values in the table. "
                          r"\[ \begin{array}{c|ccccc} t & 0 & 2 & 5 & 9 & 10 \\ \hline g(t) & 4 & 10 & 1 & 13 & 7 \end{array} \] "
                          r"Must there be a value $c$, with $0 < c < 10$, for which $g'(c) = -3$? Justify your answer.")
        self.finish()
