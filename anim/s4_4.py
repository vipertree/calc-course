"""Topic 4.4: Introduction to related rates. Narration comes from transcripts/4_4.md.

Adder (2026-10-23): 4.4 and 4.5 go through the SAME problems in the same order (ripple, ladder, two cars, shadow, cone).
Here no problem gives a rate or a value at an instant: each asks for the equation relating the quantities, then its
derivative with respect to time. Four steps (draw and label, name what changes, relate, differentiate); a fixed quantity
is noted when the equation is written, never as a step of its own. Topic 4.5 adds the numbers and solves."""
import numpy as np
from manim import *

from kit import *
from style import *
from props import fig_cars, fig_cone, fig_ladder, fig_ripple, fig_shadow, pond_ripple, water_cone


def stone():
    s = Ellipse(width=0.42, height=0.3).set_fill(DIM, 1).set_stroke(INK, 2)
    return VGroup(s, Ellipse(width=0.14, height=0.07).set_fill(WHITE, 0.45).set_stroke(width=0).move_to(s).shift(UP * 0.06 + LEFT * 0.07))


class Lesson(TranscriptScene):
    NUM = "4.4"

    def construct(self):
        R = ValueTracker(0.05)
        center = LEFT * 3
        pond = Ellipse(width=7.2, height=6.4).set_fill(FUNC, 0.1).set_stroke(FUNC, 2, opacity=0.35).move_to(center)
        ring = always_redraw(lambda: pond_ripple(R.get_value(), center))
        read = always_redraw(lambda: VGroup(M(rf"r = {R.get_value() * 4:.1f}\text{{ cm}}", 40, SECANT),
                                            M(rf"A = {np.pi * (R.get_value() * 4) ** 2:.0f}\text{{ cm}}^2", 40, FUNC)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=1.2))
        with self.beat("A ripple") as b:
            st = stone().move_to(center + UP * 3.4)
            self.play(FadeIn(pond), run_time=0.6)
            self.play(st.animate.move_to(center).scale(0.6), run_time=0.8, rate_func=rate_functions.ease_in_quad)
            self.play(FadeOut(st, scale=0.3), run_time=0.2)
            self.add(ring, read)
            self.play(R.animate.set_value(1.25), run_time=3, rate_func=linear)
            b.line(1)
            self.play(R.animate.set_value(2.5), run_time=3, rate_func=linear)
            b.line(2)
            self.play(Indicate(read, color=SECANT), run_time=1)
        self.clear()
        self.title()

        with self.beat("Everything depends on time") as b:
            eq = M(r"A", r"=", r"\pi", r"r", r"^2", 80).shift(UP * 0.6)
            self.play(Write(eq), run_time=1)
            tags = VGroup(M(r"A(t)", 34, FUNC).next_to(eq[0], DOWN, buff=0.5), M(r"r(t)", 34, SECANT).next_to(eq[3], DOWN, buff=0.5))
            self.play(FadeIn(tags), run_time=0.8)
            b.line(1)
            dd = M(r"\frac{d}{dt}", 60, DIM).next_to(eq, LEFT, buff=0.4)
            self.play(FadeIn(dd), run_time=0.6)
        self.clear()

        with self.beat("The chain rule on every variable") as b:
            l1 = M(r"\frac{d}{dt}\big[A\big] = \frac{d}{dt}\big[\pi r^2\big]", 60).shift(UP * 1.2)
            self.play(Write(l1), run_time=1.2)
            b.line(1)
            l2 = M(r"\frac{dA}{dt} = 2\pi r\cdot", r"\frac{dr}{dt}", 64).next_to(l1, DOWN, buff=0.8)
            self.play(Write(l2), run_time=1.2)
            b.line(2)
            self.play(l2[1].animate.set_color(SECANT), Circumscribe(l2[1], color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("Formulas you need") as b:
            head = T(r"No formula sheet on the AP exam", 46, SECANT).to_edge(UP, buff=0.5)
            self.play(FadeIn(head), run_time=0.8)
            b.line(1)
            know = VGroup(T(r"Know these by heart:", 36, DIM),
                          M(r"\text{circle: } A = \pi r^2, \quad C = 2\pi r", 40),
                          M(r"\text{triangle: } A = \tfrac12 bh \qquad \text{rectangle: } A = lw", 40),
                          M(r"a^2 + b^2 = c^2 \qquad \text{similar triangles}", 40)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            know.next_to(head, DOWN, buff=0.5)
            for m in know:
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
            b.line(2)
            given = callout(r"Cone, cylinder, sphere: the volume formula \\ is given in the problem when you need it.", INK, 34)
            given.next_to(know, DOWN, buff=0.5)
            self.play(FadeIn(given), run_time=0.8)
        self.clear()

        with self.beat("Where the equation comes from") as b:
            tri = VGroup(Polygon(ORIGIN, RIGHT * 2, RIGHT * 2 + UP * 1.4, color=INK), M(r"x^2 + y^2 = z^2", 32))
            sim = VGroup(VGroup(Polygon(ORIGIN, RIGHT * 2.2, UP * 1.5, color=INK), Polygon(ORIGIN, RIGHT * 1.1, UP * 0.75, color=SECANT)), M(r"\frac{r}{h} = \frac{R}{H}", 32))
            cone, _, _ = water_cone(0.6, H=1.6, R=0.8)
            vol = VGroup(cone, M(r"V = \tfrac13\pi r^2 h \ \ (\text{given})", 30))
            ang = VGroup(VGroup(Polygon(ORIGIN, RIGHT * 2, RIGHT * 2 + UP * 1.4, color=INK), Arc(0.5, 0, np.arctan(0.7), color=TANGENT)), M(r"\tan\theta = \frac{y}{x}", 32))
            cards = VGroup(tri, sim, vol, ang)
            for c in cards:
                c.arrange(DOWN, buff=0.35)
            cards.arrange_in_grid(2, 2, buff=(1.6, 0.8)).shift(DOWN * 0.2)
            b.line(1)
            self.play(FadeIn(tri), run_time=0.6)
            self.play(FadeIn(sim), run_time=0.6)
            b.line(2)
            self.play(FadeIn(vol), FadeIn(ang), run_time=0.8)
        self.clear()

        steps = VGroup(T(r"1. \textbf{Draw and label} a picture", 38),
                       T(r"2. \textbf{Name what changes:} each changing quantity is a variable", 38),
                       T(r"3. \textbf{Relate:} an equation that holds at every moment", 38),
                       T(r"4. \textbf{Differentiate} both sides with respect to $t$", 38)).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        steps.set_max_width(12.4)
        with self.beat("Four steps to the equation") as b:
            for i, m in enumerate(steps):
                b.line(i + 1)
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.6)
        self.clear()

        self.example("The ripple",
                     r"A stone drops into a pond, and a circular ripple spreads out. Write an equation that relates the area inside the ripple and its radius, then differentiate with respect to time.",
                     [r"TEXT:Changing: $r$ and $A$.", r"A = \pi r^2", r"\frac{d}{dt}\big[A\big] = \frac{d}{dt}\big[\pi r^2\big]",
                      r"\frac{dA}{dt} = 2\pi r\,\frac{dr}{dt}"], at=[1, 2, 3, 4], figure=fig_ripple(), follow=True)

        with self.beat("Close") as b:
            again = steps.copy().scale(0.9)
            self.play(FadeIn(again), run_time=0.8)
            b.line(1)
            self.play(again[3].animate.set_color(SECANT), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: The ladder",
                     r"A $13$-ft ladder leans against a wall, and its bottom slides away from the wall. Write an equation that relates the bottom's distance from the wall and the height of the top, then differentiate with respect to time.",
                     [r"TEXT:Changing: $x$ and $y$.", r"TEXT:The ladder stays $13$ ft.",
                      r"x^2 + y^2 = 13^2", r"\frac{d}{dt}\big[x^2 + y^2\big] = \frac{d}{dt}\big[13^2\big]", r"2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt} = 0"],
                     at=[1, 2, 3, 4, 5], figure=fig_ladder(), follow=True)
        self.example("Example 2: Two cars",
                     r"Priya drives west toward an intersection, and Kai drives north away from it. Write an equation that relates the distance between the two cars to each car's distance from the intersection, then differentiate with respect to time.",
                     [r"TEXT:Changing: $x$, $y$ and $z$.",
                      r"z^2 = x^2 + y^2", r"\frac{d}{dt}\big[z^2\big] = \frac{d}{dt}\big[x^2 + y^2\big]",
                      r"2z\,\frac{dz}{dt} = 2x\,\frac{dx}{dt} + 2y\,\frac{dy}{dt}"], at=[1, 2, 3, 4], figure=fig_cars())
        self.example("Example 3: A shadow",
                     r"Ana, who is $5$ ft tall, walks away from a $15$-ft lamppost. Write an equation that relates her distance from the post and the length of her shadow, then differentiate with respect to time.",
                     [r"TEXT:Changing: $x$ and $s$.", r"TEXT:The heights stay $15$ and $5$ ft.",
                      r"\frac{15}{x + s} = \frac{5}{s}", r"15s = 5x + 5s", r"10s = 5x,\ \text{so}\ s = \frac x2", r"\frac{ds}{dt} = \frac12\,\frac{dx}{dt}"],
                     at=[1, 2, 3, 4, 5, 6], figure=fig_shadow(), follow=True)
        self.example("Example 4: Filling a cone",
                     r"Water pours into a cone, point down, that is $9$ ft tall with radius $3$ ft at the top. Write an equation that relates the volume of the water and its depth, then differentiate with respect to time. (The volume of a cone with radius $r$ and height $h$ is $V = \tfrac13\pi r^2 h$.)",
                     [r"TEXT:Changing: $V$, $h$ and $r$.", r"TEXT:The cone stays $9$~ft tall, radius~$3$~ft.",
                      r"\frac rh = \frac39,\ \text{so}\ r = \frac h3", r"V = \frac13\pi\left(\frac h3\right)^2 h", r"V = \frac{\pi}{27}h^3",
                      r"\frac{dV}{dt} = \frac{\pi}{9}h^2\,\frac{dh}{dt}"], at=[1, 2, 3, 4, 5, 6], figure=fig_cone())
        self.finish()
