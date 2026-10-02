"""A short sampler of a lesson's usual pieces, for judging a video theme. Render with CALC_THEME=<theme>.

    CALC_THEME=parchment manim -qm theme_demo.py Demo
"""
import os

import numpy as np
from manim import *

import kit
from kit import *
from style import *


def s(t):
    return t ** 3 - 9 * t ** 2 + 24 * t


class Demo(LessonScene):
    def fade_all(self):
        mobs = [m for m in self.mobjects if not isinstance(m, ValueTracker)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=0.6)

    def construct(self):
        # title card with the intro music
        card = title_card("2.1", "Defining Average and Instantaneous Rates of Change", f"Unit 2 \\textperiodcentered{{}} {UNIT_NAMES[2]}")
        self.add_sound(os.path.join(kit.ASSETS, "intro_guitar.wav"), gain=-4)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.2)
        self.wait(1.8)
        self.play(FadeOut(card), run_time=0.6)

        # a graph: the function, a secant settling onto a tangent, a table of slopes
        ax, al = plot_axes([0, 4.5, 1], [0, 24, 4], w=6.6, h=4.8, xlabel="t", ylabel="s")
        VGroup(ax, al).to_edge(LEFT, buff=0.6).shift(DOWN * 0.4)
        curve = ax.plot(s, x_range=[0, 4.5], color=FUNC, stroke_width=5)
        lab = M(r"s(t) = t^3 - 9t^2 + 24t", 40, FUNC).to_edge(RIGHT, buff=0.6).shift(UP * 2.4)
        self.play(FadeIn(ax), FadeIn(al), Create(curve), Write(lab), run_time=1.6)
        h = ValueTracker(2)
        sec = always_redraw(lambda: ax.plot(lambda x: 16 + (s(1 + h.get_value()) - 16) / h.get_value() * (x - 1), x_range=[0.2, 3.4], color=SECANT, stroke_width=4))
        p2 = always_redraw(lambda: closed_dot(ax, 1 + h.get_value(), s(1 + h.get_value()), SECANT))
        self.play(FadeIn(closed_dot(ax, 1, 16, INK)), Create(sec), FadeIn(p2), run_time=1)
        tb = table(["h", r"\text{slope}"], [["2", "1"], ["1", "4"], ["0.5", "6.25"], ["0.1", "8.41"]], size=34).to_edge(RIGHT, buff=1.4).shift(DOWN * 0.4)
        self.play(FadeIn(tb), run_time=0.8)
        self.play(h.animate.set_value(0.1), run_time=2.4)
        self.play(Create(tangent_line(ax, s, 1, 9, [0.2, 1.8])), FadeIn(T("tangent: slope 9", 32, TANGENT).next_to(ax.c2p(1.8, 23), RIGHT, buff=0.1)), run_time=1)
        self.wait(0.8)
        self.fade_all()

        # worked algebra: a problem, a board that strikes out canceled terms, the power rule drawn
        head = T(r"Use the definition to find $f'(3)$ for $f(x) = x^2$.", 42).to_edge(UP, buff=0.5)
        self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
        board = Board().next_to(head, DOWN, buff=0.5)
        board.write(self, r"f'(3) = \lim_{h\to0}\frac{(3 + h)^2 - 9}{h} = \lim_{h\to0}\frac{\cancel{9} + 6h + h^2 - \cancel{9}}{h}")
        board.write(self, r"= \lim_{h\to0}\frac{\cancel{h}(6 + h)}{\cancel{h}} = \lim_{h\to0}(6 + h) = 6", color=DERIV)
        board.write(self, "POWER:x|5|4")
        self.wait(0.6)
        self.fade_all()

        # a formula card and a panel, the other two common props
        rule = formula_box(M(r"(uv)' = u'v + uv'", 60), DERIV).shift(UP * 1.2)
        panel = VGroup(RoundedRectangle(width=5.6, height=2.2, corner_radius=0.15, color=DIM, fill_color=PANEL, fill_opacity=1),
                       VGroup(T("Instantaneous rate of change", 34, TANGENT), M(r"9 \text{ mi/hr}", 48)).arrange(DOWN, buff=0.3)).shift(DOWN * 1.6)
        panel[1].move_to(panel[0])
        self.play(FadeIn(rule), run_time=0.8)
        self.play(FadeIn(panel), run_time=0.8)
        self.wait(1.2)
        self.fade_all()

        # the outro card and music
        self.NUM, self.topic_title = "2.1", "Defining Average and Instantaneous Rates of Change"
        TranscriptScene.outro(self)
