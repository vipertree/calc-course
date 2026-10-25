"""Topic 10.3 (BC): The nth term test for divergence. Narration comes from transcripts/10_3.md."""
import numpy as np
from manim import *

from kit import *
from props import cola_glass, fountain_counter
from style import *


class Lesson(TranscriptScene):
    NUM = "10.3"

    def construct(self):
        with self.beat("Orders that stay big") as b:
            # Adder (2026-10-14): the shrinking blocks didn't read. Back to 10.1's soda fountain (Adder 2026-10-23): orders
            # that head to half a cola
            top = -1.75
            counter = fountain_counter(top)
            self.play(FadeIn(counter), run_time=0.6)
            fr = [r"1", r"\tfrac23", r"\tfrac35", r"\tfrac47", r"\tfrac59", r"\tfrac6{11}"]
            tab_head = T("total so far", 30, DIM).move_to([4.6, 0.9, 0])
            tab = M("0", 52, TANGENT).next_to(tab_head, DOWN, buff=0.3)
            self.play(FadeIn(tab_head), FadeIn(tab), run_time=0.5)
            total = 0.0
            for k in range(1, 7):
                g = cola_glass(k / (2 * k - 1), 1.7).move_to([-6.0 + 1.3 * (k - 1), top, 0], aligned_edge=DOWN)
                lab = M(fr[k - 1], 38).next_to(g, UP, buff=0.12)
                total += k / (2 * k - 1)
                new_tab = M(f"{total:.2f}" if k > 1 else "1", 52, TANGENT).move_to(tab)
                self.play(FadeIn(g, shift=DOWN * 0.2), FadeIn(lab), ReplacementTransform(tab, new_tab), run_time=0.75)
                tab = new_tab
            more = M(r"\cdots", 44).move_to([1.7, top + 0.7, 0])
            self.play(FadeIn(more), run_time=0.4)
            b.line(2)
            inf = M(r"\to \infty", 44, TANGENT).next_to(tab, RIGHT, buff=0.25)
            self.play(FadeIn(inf), run_time=0.8)
            b.line(3)
            seq = T(r"the sequence (each order): $1, \tfrac23, \tfrac35, \tfrac47, \ldots \to \tfrac12$", 34, DERIV).to_edge(UP, buff=0.45).to_edge(LEFT, buff=0.6)
            self.play(FadeIn(seq), run_time=0.8)
            ser_head = T("the series (the total)", 30, TANGENT).move_to(tab_head)
            self.play(ReplacementTransform(tab_head, ser_head), run_time=0.8)
            b.line(4)
            self.play(FadeIn(T("if the terms don't shrink to zero, the total can't settle", 32, SECANT).next_to(seq, DOWN, buff=0.35).to_edge(LEFT, buff=0.6)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("Sequence or series") as b:
            # Adder: hammer the words. A sequence is the list; a series adds the list up
            left = VGroup(T("sequence: a list", 44, DERIV), M(r"a_1,\ a_2,\ a_3,\ \ldots", 46), M(r"\tfrac12,\ \tfrac14,\ \tfrac18,\ \ldots", 46), T("converges to $0$", 34, DERIV)).arrange(DOWN, buff=0.55)
            right = VGroup(T("series: a sum", 44, TANGENT), M(r"a_1 + a_2 + a_3 + \cdots", 46), M(r"\tfrac12 + \tfrac14 + \tfrac18 + \cdots", 46), T("converges to $1$", 34, TANGENT)).arrange(DOWN, buff=0.55)
            for r_, l_ in zip(right, left):
                r_.set_y(l_.get_y())
            VGroup(left, right).arrange(RIGHT, buff=1.6).move_to(UP * 0.3)
            for r_, l_ in zip(right, left):
                r_.set_y(l_.get_y())
            divider = Line(UP * 2.6, DOWN * 2.2, color=DIM, stroke_width=2).set_x((left.get_right()[0] + right.get_left()[0]) / 2)
            self.play(FadeIn(left[0]), FadeIn(left[1]), Create(divider), run_time=0.8)
            self.play(FadeIn(right[0]), FadeIn(right[1]), run_time=0.8)
            b.line(2)
            self.play(FadeIn(left[2]), run_time=0.6)
            self.play(FadeIn(left[3]), run_time=0.5)
            self.play(FadeIn(right[2]), run_time=0.6)
            self.play(FadeIn(right[3]), run_time=0.5)
            b.line(3)
            self.play(Indicate(left[0], color=DERIV), run_time=0.8)
            self.play(Indicate(right[0], color=TANGENT), run_time=0.8)
        self.clear()

        with self.beat("The test") as b:
            rule = M(r"\text{If } ", r"\lim_{n\to\infty} a_n", r" \ne 0 \text{ (or DNE), then } ", r"\sum a_n", r"\text{ diverges.}", 42).to_edge(UP, buff=0.6)
            rule[1].set_color(DERIV)
            rule[3].set_color(TANGENT)
            braces = VGroup(Brace(rule[1], DOWN, color=DERIV), Brace(rule[3], DOWN, color=TANGENT))
            names = VGroup(T("the sequence", 28, DERIV).next_to(braces[0], DOWN, buff=0.1), T("the series", 28, TANGENT).next_to(braces[1], DOWN, buff=0.1))
            self.play(Write(rule), run_time=1.2)
            self.play(GrowFromCenter(braces[0]), FadeIn(names[0]), GrowFromCenter(braces[1]), FadeIn(names[1]), run_time=0.8)
            b.line(2)
            why = M(r"\sum a_n = S \ \text{ means } \ a_n = S_n - S_{n-1} \to S - S = 0", 38).next_to(names, DOWN, buff=0.7).set_x(0)
            self.play(Write(why), run_time=1.2)
            b.line(3)
            warn = T("If $\\lim a_n = 0$, the test says nothing.", 38, TANGENT).next_to(why, DOWN, buff=0.7)
            self.play(FadeIn(warn), run_time=0.8)
        self.clear()

        # the test stays up in the corner through the worked examples (Adder: formulas stay on screen)
        self.example_ref = r"\begin{aligned}&\lim_{n\to\infty} a_n \ne 0 \text{ or DNE:}\\ &\textstyle\sum a_n \text{ diverges}\end{aligned}"
        self.example("Using the test", r"Does $\displaystyle\sum_{n=1}^{\infty} \frac{n}{2n + 1}$ converge or diverge?",
                     [r"a_n = \frac{n}{2n + 1}", r"\lim_{n\to\infty} \frac{n}{2n + 1} = \lim \frac{1}{2 + 1/n} = \frac12", r"\tfrac12 \ne 0", r"TEXT:By the $n$th term test, the series diverges."], at=[1, 2, 3, 3], follow=True)

        with self.beat("Zero isn't enough") as b:
            def panel(f, lab, col, yr):
                ax, _ = plot_axes([0, 40, 10], yr, w=4.6, h=3, coords=False, xlabel="n", ylabel="S_n")
                s, vals = 0, []
                for k in range(1, 41):
                    s += f(k)
                    vals.append(s)
                return VGroup(ax, VGroup(*[Dot(ax.c2p(k, v), color=col, radius=0.04) for k, v in enumerate(vals, start=1)]), T(lab, 28, col).next_to(ax, DOWN, buff=0.2))
            p1 = panel(lambda k: 1 / k, r"sequence $\frac1n \to 0$; series diverges (10.5)", TANGENT, [0, 5, 1])
            p2 = panel(lambda k: 1 / k**2, r"sequence $\frac{1}{n^2} \to 0$; series converges", DERIV, [0, 2, 1])
            VGroup(p1, p2).arrange(RIGHT, buff=0.8)
            self.play(FadeIn(p1), run_time=1.2)
            b.line(1)
            self.play(FadeIn(p2), run_time=1.2)
            b.line(2)
            self.play(FadeIn(T("sequence $\\to 0$: the test is silent; use another test", 34, SECANT).to_edge(DOWN, buff=0.4)), run_time=0.6)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(T("sequence: a list; series: its sum", 38, DERIV), T("$\\lim a_n \\ne 0$ or does not exist: $\\sum a_n$ diverges", 38, ACCUM), T("$\\lim a_n = 0$: inconclusive", 38, TANGENT), T("check it first; it's quick", 34, DIM)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: An oscillating series", r"Does $\sum (-1)^n$ converge?", [r"a_n = (-1)^n: \ -1, 1, -1, \ldots", r"\lim a_n \text{ does not exist: diverges}"], at=[1, 1])
        self.example("Example 2: A limit that's e", r"Does $\displaystyle\sum_{n=1}^{\infty} \left(1 + \frac1n\right)^n$ converge?", [r"\lim_{n\to\infty} \left(1 + \tfrac1n\right)^n = e \ne 0", r"\text{diverges}"], at=[1, 1])
        self.example("Example 3: When the test is silent", r"What does the $n$th term test say about $\displaystyle\sum_{n=1}^{\infty} \frac{1}{\sqrt n}$?",
                     [r"\lim \frac{1}{\sqrt n} = 0", r"TEXT:The test is inconclusive.", r"\text{(it diverges: a } p\text{-series with } p = \tfrac12\text{, topic 10.5)}"], at=[1, 2, 3])
        self.finish()
