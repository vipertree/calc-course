"""Topic 3.5: Choosing the right rule. Narration comes from transcripts/3_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *

TOOLS = ["power rule", "sum and constant rules", "product rule", "quotient rule", "chain rule", "implicit differentiation",
         r"$\sin, \cos, e^x, \ln x, \tan, \arcsin, \arctan$"]


class Lesson(TranscriptScene):
    NUM = "3.5"

    def toolbox(self, lid_text=None):
        box = VGroup(Rectangle(width=6, height=1.6, color=SECANT, fill_color=PANEL, fill_opacity=1, stroke_width=4),
                     Rectangle(width=1.4, height=0.35, color=SECANT, stroke_width=4)).arrange(UP, buff=0)
        if lid_text:
            box.add(T(lid_text, 30, SECANT).move_to(box[0]))
        return box

    def construct(self):
        with self.beat("A toolbox, not a recipe") as b:
            box = self.toolbox().to_edge(DOWN, buff=0.4)
            self.play(FadeIn(box), run_time=0.6)
            tags = VGroup(*[callout(t, INK, 28) for t in TOOLS]).arrange_in_grid(4, 2, buff=(0.4, 0.25)).next_to(box, UP, buff=0.5)
            for tg in tags:
                self.play(FadeIn(tg, shift=UP * 0.4), run_time=0.35)
            b.line(1)
            self.play(Indicate(tags, color=SECANT, scale_factor=1.03), run_time=1)
        self.clear()
        self.title()

        with self.beat("The outermost operation") as b:
            # Adder: read the outermost function or operation (not "the last thing you'd do to evaluate")
            f = M(r"x^2", r"\cdot", r"\sin(3x)", 72, FUNC).shift(UP * 0.8)
            self.play(Write(f), run_time=1)
            b.line(1)
            br = VGroup(Brace(f[0], DOWN, color=DIM), Brace(f[2], DOWN, color=DIM))
            self.play(GrowFromCenter(br[0]), GrowFromCenter(br[1]), run_time=0.9)
            self.play(f[1].animate.set_color(SECANT).scale(1.4), run_time=0.6)
            b.line(2)
            out = callout("outermost: a product", SECANT, 36).next_to(br, DOWN, buff=0.6)
            self.play(FadeIn(out), run_time=0.8)
        self.clear()

        with self.beat("Then repeat inside") as b:
            top = M(r"\frac{d}{dx}\Big[", r"x^2", r"\cdot", r"\sin(3x)", r"\Big]", 56).to_edge(UP, buff=0.6)
            self.play(Write(top), run_time=1)
            b.line(1)
            p1 = M(r"(x^2)' = 2x", 46).shift(LEFT * 3 + UP * 0.6)
            self.play(Indicate(top[1]), FadeIn(p1), run_time=0.8)
            b.line(2)
            self.play(top[3].animate.set_color(SECANT), run_time=0.5)
            p2 = M(r"\big(\sin(3x)\big)' = \cos(3x) \cdot 3", 46, SECANT).shift(RIGHT * 2.6 + UP * 0.6)
            self.play(FadeIn(p2), run_time=0.8)
            res = M(r"= 2x\sin(3x) + 3x^2\cos(3x)", 52, DERIV).shift(DOWN * 1.2)
            self.play(Write(res), run_time=1.2)
            b.line(3)
            self.play(Indicate(res, color=DERIV), run_time=1)
        self.clear()
        self.example("Layers", r"Find $\dfrac{d}{dx}\left[x^2\sin(3x)\right]$.",
                     [r"\text{outermost: a product } \underbrace{x^2}_{u}\,\underbrace{\sin(3x)}_{v}", r"u' = 2x, \qquad v' = \cos(3x)\cdot 3", r"u'v + uv' = 2x\sin(3x) + 3x^2\cos(3x)"], at=[1, 2, 3])

        with self.beat("Rewrite before you start") as b:
            f = M(r"\frac{x^3 - 2\sqrt{x}}{x}", 60).to_edge(UP, buff=0.5)
            self.play(Write(f), run_time=1)
            b.line(1)
            tmpl = M(r"\frac{x \cdot (\ \cdots\ ) - (x^3 - 2\sqrt{x}) \cdot 1}{x^2}", 44, DIM).next_to(f, DOWN, buff=0.5)
            self.play(FadeIn(tmpl), run_time=0.8)
            self.play(FadeOut(tmpl), run_time=0.6)
            rw = M(r"= x^2 - 2x^{-1/2}", 52).next_to(f, DOWN, buff=0.5)
            self.play(Write(rw), run_time=1)
            b.line(2)
            d = M(r"\frac{d}{dx}\left[\frac{x^3 - 2\sqrt{x}}{x}\right] = 2x + x^{-3/2}", 48, DERIV).next_to(rw, DOWN, buff=0.5)
            self.play(Write(d), run_time=1)
            b.line(3)
            tips = T(r"divide through \quad negative exponents \quad log rules", 34, SECANT).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(tips), run_time=0.8)
        self.clear()
        self.example("Rewrite first", r"Find $\dfrac{d}{dx}\left[\dfrac{x^3 - 2\sqrt x}{x}\right]$.",
                     [r"\frac{x^3 - 2x^{1/2}}{x} = x^2 - 2x^{-1/2}", r"\frac{d}{dx}\left[x^2 - 2x^{-1/2}\right] = 2x + x^{-3/2}", r"TEXT:Much shorter than the quotient rule."], at=[1, 2, 3])

        with self.beat("Close") as b:
            box = self.toolbox("What's the outermost operation?").scale(1.2)
            self.play(FadeIn(box), run_time=1)
        self.clear()

        self.examples_card()
        self.example("Example 1: Chain on the outside", r"Find $\dfrac{d}{dx}\sqrt{x e^x}$.",
                     [r"\text{outermost: square root},\ \text{so}\ \frac{1}{2\sqrt{x e^x}} \cdot (x e^x)'", r"(x e^x)' = e^x + x e^x",
                      r"\frac{d}{dx}\sqrt{x e^x} = \frac{e^x + x e^x}{2\sqrt{x e^x}}"], at=[1, 2, 3])
        self.example("Example 2: Logs first", r"Find $\dfrac{d}{dx}\ln\left(\dfrac{x^2}{x + 1}\right)$.",
                     [r"\ln\left(\frac{x^2}{x + 1}\right) = 2\ln x - \ln(x + 1)", r"\frac{d}{dx}\ln\left(\frac{x^2}{x + 1}\right) = \frac2x - \frac{1}{x + 1}"], at=[2, 3])
        self.example("Example 3: A composite from given values",
                     r"$f(3) = 1,\ f'(3) = 4,\ g(1) = 5,\ g'(1) = -2,\ g'(3) = 7$. \ $h(x) = x\,g(f(x))$. Find $h'(3)$.",
                     [r"h'(3) = 1 \cdot g\big(f(3)\big) + 3 \cdot g'\big(f(3)\big)\,f'(3)", r"f(3) = 1:\ \ g(1) = 5, \quad g'(1) = -2",
                      r"h'(3) = 5 + 3(-2)(4) = -19", r"TEXT:$g'(3) = 7$ was never needed."], at=[1, 3, 4, 4])
        self.finish()
