"""Topic 7.1: Modeling situations with differential equations. Narration comes from transcripts/7_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "7.1"

    def construct(self):
        with self.beat("A rule for the rate") as b:
            mug = coffee_mug(1.5).to_edge(LEFT, buff=1.0).shift(UP * 1.9)
            therm = T(r"$90^\circ$F \quad room $70^\circ$F", 28, DIM).next_to(mug, RIGHT, buff=0.5)
            ax, al = plot_axes([0, 40, 10], [60, 95, 10], w=5.4, h=3.0, xlabel="t", ylabel="T", font=22)
            VGroup(ax, al).to_edge(RIGHT, buff=0.7).to_edge(UP, buff=0.9)
            temp = lambda s: 70 + 20 * np.exp(-0.08 * s)
            self.play(FadeIn(mug), FadeIn(therm), FadeIn(ax), FadeIn(al), run_time=1)
            self.play(Create(ax.plot(temp, x_range=[0, 40], color=FUNC, stroke_width=5)), Create(DashedLine(ax.c2p(0, 70), ax.c2p(40, 70), color=DIM)), run_time=2)
            hint = T("the hotter it is than the room, the faster it cools", 26, SECANT).next_to(ax, DOWN, buff=0.45)
            self.play(FadeIn(hint), run_time=0.8)
            b.line(1)
            # the equation, built slowly: each piece with its words under it (Adder, 7.1)
            de = M(r"\frac{dT}{dt}", r"=", r"-", r"k", r"(T - 70)", 64).move_to([0, -1.55, 0])
            words = {0: r"change in temperature\\with respect to time", 4: r"how far $T$ is from\\room temperature", 3: r"some\\constant", 2: "decreasing"}
            cols = {0: DERIV, 4: SECANT, 3: ACCUM, 2: TANGENT}
            labs = {}
            for k, w in words.items():
                labs[k] = T(w, 24, cols[k]).next_to(de[k], DOWN, buff=0.35)
            labs[3].shift(LEFT * 0.15)
            labs[2].next_to(de[2], DOWN, buff=1.25)
            ln = Line(labs[2].get_top() + UP * 0.05, de[2].get_bottom() + DOWN * 0.08, color=TANGENT, stroke_width=3)
            b.line(2)
            self.play(Write(de[0]), de[0].animate.set_color(DERIV), FadeIn(labs[0]), run_time=1)
            b.line(3)
            self.play(FadeIn(de[1]), Write(de[4]), FadeIn(labs[4]), run_time=1)
            self.play(de[4].animate.set_color(SECANT), run_time=0.4)
            b.line(4)
            self.play(Write(de[3]), de[3].animate.set_color(ACCUM), FadeIn(labs[3]), run_time=0.9)
            b.line(5)
            self.play(Write(de[2]), de[2].animate.set_color(TANGENT), Create(ln), FadeIn(labs[2]), run_time=0.9)
            b.line(6)
            self.play(FadeOut(VGroup(*labs.values(), ln)), run_time=0.5)
            box = SurroundingRectangle(de, color=ACCUM, buff=0.2)
            name = T("a differential equation", 32, ACCUM).next_to(box, DOWN, buff=0.3)
            self.play(Create(box), FadeIn(name), run_time=0.9)
        self.clear()
        self.title()

        with self.beat("What a differential equation is") as b:
            head = T("differential equation: an equation with a derivative in it", 36, ACCUM).to_edge(UP, buff=0.6)
            self.play(FadeIn(head), run_time=0.8)
            b.line(1)
            exs = VGroup(M(r"\frac{dy}{dx} = 3x^2", 44), M(r"\frac{dP}{dt} = 0.2P", 44), M(r"\frac{dy}{dx} = \frac xy", 44)).arrange(RIGHT, buff=1.2).next_to(head, DOWN, buff=0.8)
            self.play(LaggedStart(*[FadeIn(e) for e in exs], lag_ratio=0.3), run_time=1.2)
            b.line(2)
            sol = T("a solution is a function, not a number", 34, SECANT).next_to(exs, DOWN, buff=0.6)
            self.play(FadeIn(sol), run_time=0.7)
            b.line(3)
            ax, _ = plot_axes([-2, 2, 1], [-4, 4, 2], w=3.6, h=2.6, coords=False)
            fam = VGroup(ax, *[ax.plot(lambda s, c=c: s**3 + c, x_range=[-1.55, 1.55], color=FUNC, stroke_width=3) for c in (-2, -1, 0, 1, 2)]).next_to(sol, DOWN, buff=0.3).shift(LEFT * 2.2)
            side = VGroup(M(r"y = x^3 + C", 40, FUNC), T(r"you've solved these already:\\antiderivatives", 28, DIM)).arrange(DOWN, buff=0.25).next_to(fam, RIGHT, buff=0.6)
            self.play(Indicate(exs[0], color=FUNC), FadeIn(fam), FadeIn(side), run_time=1.4)
        self.clear()

        with self.beat("Where this goes") as b:
            r1 = VGroup(T("algebra:", 34, DIM), M(r"x^3 - 2x = 5x^2 + \frac1x", 46)).arrange(RIGHT, buff=0.5)
            r2 = VGroup(T("later courses:", 34, DIM), M(r"x^2y'' + y\,y' - \left(y'\right)^2 = \sin x", 46)).arrange(RIGHT, buff=0.5)
            rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.9).shift(UP * 0.9)
            self.play(FadeIn(r1), run_time=0.8)
            xs = [r1[1][0][i] for i in (0, 4, 7, 12)]
            self.play(*[Indicate(m, color=SECANT) for m in xs], run_time=0.9)
            self.play(FadeIn(r2), run_time=0.8)
            self.play(Indicate(r2[1], color=DERIV), run_time=0.9)
            b.line(1)
            ours = T("this course: relatively simple, but not always easy", 36, ACCUM).next_to(rows, DOWN, buff=1.0)
            self.play(FadeIn(ours), run_time=0.8)
        self.clear()

        with self.beat("Translating words") as b:
            rows = [("the rate of change of $y$ is proportional to $y$", r"\frac{dy}{dt} = ky"), ("proportional to the square root of $y$", r"\frac{dy}{dt} = k\sqrt y"),
                    ("inversely proportional to $y$", r"\frac{dy}{dt} = \frac ky"), ("proportional to the difference between $y$ and $70$", r"\frac{dy}{dt} = k(y - 70)"),
                    ("jointly proportional to $y$ and $1000 - y$", r"\frac{dy}{dt} = ky(1000 - y)")]
            cells = VGroup(*[VGroup(T(l, 28), M(r, 36, ACCUM)) for l, r in rows])
            for k, c in enumerate(cells):
                c[0].move_to(LEFT * 2.6 + UP * (2.4 - 1.1 * k))
                c[1].move_to(RIGHT * 4.0 + UP * (2.4 - 1.1 * k))
            self.play(FadeIn(cells[0][0]), run_time=0.6)
            b.line(1)
            self.play(FadeIn(cells[0][1]), run_time=0.6)
            b.line(2)
            self.play(FadeIn(cells[1]), run_time=0.6)
            self.play(FadeIn(cells[2]), run_time=0.6)
            b.line(3)
            self.play(FadeIn(cells[3]), run_time=0.6)
            self.play(FadeIn(cells[4]), run_time=0.6)
        self.clear()

        self.example("Reading the rate", r"$\dfrac{dP}{dt} = 0.3P\left(1 - \dfrac{P}{500}\right)$. (a) Find $\dfrac{dP}{dt}$ when $P = 100$. (b) Is $P$ increasing or decreasing when $P = 600$?",
                     [r"\text{(a) } 0.3(100)\left(1 - \tfrac{100}{500}\right) = 30(0.8) = 24", r"TEXT:When $P = 100$, the population grows at $24$ individuals per unit of time.",
                      r"\text{(b) } 0.3(600)\left(1 - \tfrac{600}{500}\right) = 180(-0.2) = -36", r"-36 < 0: \ P \text{ is decreasing}"], at=[1, 2, 3, 4], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T("A differential equation gives the rate of change.", 38, ACCUM), T("Its solutions are functions.", 36), T("Proportional to: a constant $k$ times.", 36),
                          T("Plug in to read the rate and its sign.", 36, SECANT)).arrange(DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A rumor", r"In a school of $1000$ students, a rumor spreads at a rate jointly proportional to the number $N$ who have heard it and the number who have not. Write a differential equation for $N$.",
                     [r"\text{rate of change: } \frac{dN}{dt}; \ \ \text{heard: } N; \ \ \text{not heard: } 1000 - N", r"\text{jointly proportional: } k \cdot (\text{product})", r"\frac{dN}{dt} = kN(1000 - N)"], at=[1, 2, 3])
        self.example("Example 2: A slope at a point", r"$\dfrac{dy}{dx} = x^2 - y$. Find $\dfrac{dy}{dx}$ at the point $(2, 1)$. Is $y$ increasing or decreasing there?",
                     [r"\frac{dy}{dx} = 2^2 - 1 = 3", r"3 > 0: \ \text{increasing}"], at=[1, 2])
        self.example("Example 3: Cooling coffee", r"Coffee cools according to $\dfrac{dT}{dt} = -0.1(T - 70)$, with $T$ in $^\circ$F and $t$ in minutes. Find $\dfrac{dT}{dt}$ when $T = 130$ and interpret it.",
                     [r"\frac{dT}{dt} = -0.1(130 - 70) = -0.1(60) = -6", r"TEXT:When the coffee is $130^\circ$F, its temperature is decreasing at $6^\circ$F per minute."], at=[1, 2])
        self.finish()
