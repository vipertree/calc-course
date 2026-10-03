"""Topic 3.1: The chain rule. Fixed-rate chains first (dy/dx notation), then why dy/du needs a location, then f'(g(x)) g'(x).
Narration comes from transcripts/3_1.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def dial(label, unit, color):
    c = Circle(radius=0.75, color=color, stroke_width=4)
    return VGroup(c, M(label, 48, color).move_to(c), T(unit, 26, DIM).next_to(c, DOWN, buff=0.15))


class Lesson(TranscriptScene):
    NUM = "3.1"

    def bakery(self):
        dials = VGroup(dial("t", "hours", DIM), dial("c", "cookies", SECANT), dial(r"\$", "dollars", DERIV)).arrange(RIGHT, buff=2.6)
        arrows = VGroup(Arrow(dials[0][0].get_right(), dials[1][0].get_left(), color=INK, buff=0.15), Arrow(dials[1][0].get_right(), dials[2][0].get_left(), color=INK, buff=0.15))
        return dials, arrows

    def construct(self):
        with self.beat("Rates that feed each other") as b:
            oven = RoundedRectangle(width=2.2, height=1.6, corner_radius=0.15, color=DIM, fill_color=PANEL, fill_opacity=1).shift(LEFT * 4.5 + UP * 0.8)
            jar = VGroup(Rectangle(width=1.4, height=1.8, color=DIM), T("jar", 26, DIM)).shift(RIGHT * 4.5 + UP * 0.6)
            jar[1].next_to(jar[0], DOWN, buff=0.1)
            self.play(FadeIn(oven), FadeIn(jar), FadeIn(T("oven", 26, DIM).next_to(oven, DOWN, buff=0.1)), run_time=0.8)
            for _ in range(3):
                ck = Circle(radius=0.22, color=SECANT, fill_color=SECANT, fill_opacity=0.9).move_to(oven.get_right())
                coin = M(r"\$3", 30, DERIV)
                self.play(ck.animate.move_to(UP * 0.8), run_time=0.5)
                coin.move_to(ck)
                self.play(ReplacementTransform(ck, coin), run_time=0.3)
                self.play(coin.animate.move_to(jar[0].get_center()).scale(0.8), run_time=0.5)
            read = VGroup(M(r"24\ \text{cookies/hour}", 40, SECANT), M(r"3\ \text{dollars/cookie}", 40, DERIV), M(r"?\ \text{dollars/hour}", 40)).arrange(RIGHT, buff=0.8).shift(DOWN * 2)
            self.play(FadeIn(read[0]), FadeIn(read[1]), run_time=0.8)
            b.line(1)
            self.play(FadeIn(read[2]), run_time=0.6)
            b.line(2)
            ans = M(r"24 \times 3 = 72\ \text{dollars/hour}", 46, INK).next_to(read, DOWN, buff=0.5)
            self.play(Write(ans), run_time=1.2)
        self.clear()

        with self.beat("Units cancel") as b:
            e = M(r"3\,\frac{\text{dollars}}{", r"\text{cookie}", r"} \times 24\,\frac{", r"\text{cookies}", r"}{\text{hour}}", 60)
            self.play(Write(e), run_time=1.4)
            b.line(1)
            strike = VGroup(Line(e[1].get_corner(DL), e[1].get_corner(UR), color=TANGENT, stroke_width=5), Line(e[3].get_corner(DL), e[3].get_corner(UR), color=TANGENT, stroke_width=5))
            self.play(Create(strike), run_time=0.8)
            res = M(r"= 72\,\frac{\text{dollars}}{\text{hour}}", 60, DERIV).next_to(e, DOWN, buff=0.7)
            self.play(Write(res), run_time=1)
            b.line(2)
            self.play(Indicate(res, color=DERIV), run_time=1)
        self.clear()
        self.title()

        dials, arrows = self.bakery()
        dials.shift(UP * 1.2)
        arrows.shift(UP * 1.2)
        with self.beat("In derivative notation") as b:
            self.play(FadeIn(dials), run_time=1)
            self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=0.8)
            b.line(1)
            r1 = M(r"\frac{dc}{dt} = 24", 40, SECANT).next_to(arrows[0], DOWN, buff=0.3)
            r2 = M(r"\frac{d\$}{dc} = 3", 40, DERIV).next_to(arrows[1], DOWN, buff=0.3)
            self.play(Write(r1), run_time=0.8)
            self.play(Write(r2), run_time=0.8)
            b.line(2)
            tot = M(r"\frac{d\$}{dt} = \frac{d\$}{", r"dc", r"}\cdot\frac{", r"dc", r"}{dt} = 3 \cdot 24 = 72", 52).shift(DOWN * 2.2)
            self.play(Write(tot), run_time=1.4)
            b.line(3)
            self.play(Indicate(tot[1], color=TANGENT), Indicate(tot[3], color=TANGENT), run_time=1.2)
        self.clear()

        lines = VGroup(*[NumberLine(x_range=[0, 6, 1], length=10, color=DIM, include_numbers=False) for _ in range(3)]).arrange(DOWN, buff=1.5).shift(DOWN * 0.2 + RIGHT * 0.5)
        names = VGroup(*[M(n, 40, c).next_to(l, LEFT, buff=0.4) for n, c, l in zip("xuy", (INK, SECANT, DERIV), lines)])
        with self.beat("When the rates change") as b:
            self.play(FadeIn(T(r"constant rates", 34, DIM).to_edge(UP, buff=0.4)), run_time=0.6)
            b.line(1)
            self.play(FadeIn(lines), FadeIn(names), run_time=1)
            b.line(2)
            segs = [(2.0, 2.5), (2.2, 3.2), (1.6, 4.0)]
            cols = (INK, SECANT, DERIV)
            bars = VGroup(*[Line(l.n2p(a), l.n2p(c), color=col, stroke_width=10) for l, (a, c), col in zip(lines, segs, cols)])
            self.play(Create(bars[0]), FadeIn(M(r"dx", 34).next_to(bars[0], UP, buff=0.1)), run_time=0.8)
            fan1 = Polygon(bars[0].get_start(), bars[0].get_end(), bars[1].get_end(), bars[1].get_start(), color=SECANT, fill_opacity=0.15, stroke_width=1)
            self.play(FadeIn(fan1), Create(bars[1]), FadeIn(T(r"stretched by $\frac{du}{dx}$", 32, SECANT).next_to(bars[1], RIGHT, buff=0.6).shift(UP * 0.6)), run_time=1)
            b.line(3)
            fan2 = Polygon(bars[1].get_start(), bars[1].get_end(), bars[2].get_end(), bars[2].get_start(), color=DERIV, fill_opacity=0.15, stroke_width=1)
            self.play(FadeIn(fan2), Create(bars[2]), FadeIn(T(r"stretched by $\frac{dy}{du}$", 32, DERIV).next_to(bars[2], RIGHT, buff=0.6).shift(UP * 0.6)), run_time=1)
            b.line(4)
            self.play(Indicate(bars[2], color=DERIV), run_time=1)
        self.clear()

        with self.beat("From the nudge to the limit") as b:
            e1 = M(r"\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}", 60).shift(UP * 1.2)
            note = M(r"(du \ne 0)", 34, DIM).next_to(e1, RIGHT, buff=0.4)
            self.play(Write(e1), FadeIn(note), run_time=1.4)
            b.line(1)
            e2 = T(r"let the nudge $dx$ shrink to $0$: each fraction settles on a derivative", 36, DIM).next_to(e1, DOWN, buff=0.7)
            self.play(Write(e2), run_time=1.4)
            b.line(2)
            e3 = formula_box(M(r"\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}", 60), DERIV).next_to(e2, DOWN, buff=0.6)
            self.play(FadeIn(e3), run_time=1)
        self.clear()

        with self.beat("Which u?") as b:
            b.line(1)
            defs = VGroup(M(r"y = u^3", 50), M(r"u = x^2 + 1", 50)).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.6)
            self.play(Write(defs), run_time=1)
            q = M(r"\frac{dy}{dx}\Big|_{x = 1} = \ ?", 46).next_to(defs, DOWN, buff=0.4)
            self.play(FadeIn(q), run_time=0.6)
            b.line(2)
            rates = VGroup(M(r"\frac{du}{dx} = 2x \ \to\ 2", 44, SECANT), M(r"\frac{dy}{du} = 3u^2", 44, DERIV)).arrange(RIGHT, buff=1.2).next_to(q, DOWN, buff=0.5)
            self.play(Write(rates[0]), run_time=0.8)
            self.play(Write(rates[1]), run_time=0.8)
            b.line(3)
            xl = NumberLine(x_range=[0, 3, 1], length=6, color=DIM, include_numbers=True, font_size=28).shift(DOWN * 1.6 + LEFT * 0.2)
            ul = NumberLine(x_range=[0, 3, 1], length=6, color=DIM, include_numbers=True, font_size=28).shift(DOWN * 3.0 + LEFT * 0.2)
            self.play(FadeIn(xl), FadeIn(ul), FadeIn(M("x", 34).next_to(xl, LEFT)), FadeIn(M("u", 34, SECANT).next_to(ul, LEFT)), run_time=0.8)
            self.play(GrowArrow(Arrow(xl.n2p(1), ul.n2p(2), color=SECANT, buff=0.1)), FadeIn(Dot(xl.n2p(1))), FadeIn(Dot(ul.n2p(2), color=SECANT)),
                      Indicate(rates[1], color=TANGENT), run_time=1.2)
        self.clear()

        with self.beat("The trap") as b:
            wrong = M(r"3(1)^2 \cdot 2 = 6", 52, TANGENT).shift(UP * 2 + LEFT * 3)
            self.play(Write(wrong), run_time=1)
            self.play(Create(Cross(wrong, stroke_color=TANGENT, scale_factor=0.9)), run_time=0.6)
            b.line(1)
            right = VGroup(M(r"x = 1 \ \Rightarrow\ u = 1^2 + 1 = 2", 44), M(r"\frac{dy}{du} = 3(2)^2 = 12", 44, DERIV))
            right.arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(UP * 0.2 + LEFT * 3)
            self.play(Write(right), run_time=1.4)
            b.line(2)
            fin = M(r"\frac{dy}{dx} = 12 \cdot 2 = 24", 52, DERIV).next_to(right, DOWN, buff=0.5).align_to(right, LEFT)
            self.play(Write(fin), run_time=1)
            ax, _ = plot_axes([0, 1.5, 0.5], [0, 30, 10], w=4.4, h=3.6)
            ax.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.4)
            hh = lambda x: (x * x + 1) ** 3
            self.play(FadeIn(ax), Create(ax.plot(hh, x_range=[0, 1.35], color=FUNC, stroke_width=4)), run_time=0.8)
            self.play(Create(tangent_line(ax, hh, 1, 24, [0.75, 1.25])), FadeIn(M(r"\text{slope } 24", 34, TANGENT).next_to(ax.c2p(1, 8), LEFT, buff=0.3)), run_time=0.8)
            b.line(3)
            self.play(FadeIn(T(r"$\frac{dy}{du}$: measured \emph{where?}", 36, SECANT).to_edge(DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        with self.beat("Function notation says where") as b:
            mf = VGroup(RoundedRectangle(width=2.6, height=1.4, corner_radius=0.15, color=SECANT), M(r"g(x) = x^2 + 1", 32, SECANT))
            mg = VGroup(RoundedRectangle(width=2.6, height=1.4, corner_radius=0.15, color=DERIV), M(r"f(u) = u^3", 32, DERIV))
            row = VGroup(M("x", 44), mf, mg, M(r"f(g(x))", 44)).arrange(RIGHT, buff=0.8).shift(UP * 1.8)
            arr = VGroup(*[Arrow(row[i].get_right(), row[i + 1].get_left(), buff=0.1, color=DIM) for i in range(3)])
            self.play(FadeIn(row), FadeIn(arr), run_time=1.2)
            b.line(1)
            rule = M(r"\frac{d}{dx}f\big(g(x)\big) = f'\big(", r"g(x)", r"\big)\cdot g'(x)", 60).shift(UP * 0.1)
            self.play(Write(rule), run_time=1.4)
            b.line(2)
            self.play(Indicate(rule[1], color=SECANT, scale_factor=1.3), run_time=1.2)
            b.line(3)
            words = T(r"derivative of the outside, evaluated at the inside, \\ times the derivative of the inside", 36, DIM).next_to(rule, DOWN, buff=0.6)
            self.play(FadeIn(words), run_time=0.8)
            b.line(4)
            uform = formula_box(M(r"u = g(x):\qquad \big[f(u)\big]' = f'(u)\cdot u'", 48), DERIV).next_to(words, DOWN, buff=0.4)
            self.play(FadeIn(uform), run_time=1)
        self.clear()
        # the chain rule stays in the corner through the worked examples (Adder, 3.1 note AO)
        self.example_ref = r"\frac{d}{dx}f(u) = f'(u)\cdot u'"
        self.example("Trig and exponential", r"Find (a) $\dfrac{d}{dx}\sin(3x)$ and (b) $\dfrac{d}{dx}e^{x^2}$.",
                     [r"\text{(a) } \sin(\underbrace{3x}_{u})", r"u = 3x", r"u' = 3", r"\cos u\cdot u' = \cos(3x)\cdot 3 = 3\cos(3x)",
                      r"\text{(b) } e^{\overbrace{x^2}^{u}}", r"u = x^2", r"u' = 2x", r"e^u\cdot u' = e^{x^2}\cdot 2x = 2xe^{x^2}"],
                     at=[1, 2, 2, 3, 4, 5, 5, 6])
        self.example("A root", r"Find $\dfrac{d}{dx}\sqrt{1 + \cos x}$.",
                     [r"\sqrt{\underbrace{1 + \cos x}_{u}}", r"u = 1 + \cos x", r"u' = -\sin x", r"\frac{d}{dx}\sqrt{u} = \frac{1}{2\sqrt{u}}\cdot u'",
                      r"= \frac{1}{2\sqrt{1 + \cos x}}\cdot(-\sin x) = -\frac{\sin x}{2\sqrt{1 + \cos x}}"], at=[1, 2, 2, 3, 4])

        with self.beat("Close") as b:
            dials, arrows = self.bakery()
            grp = VGroup(dials, arrows).scale(0.8).shift(UP * 1.4)
            card = formula_box(M(r"\big[f(u)\big]' = f'(u)\cdot u'", 54), DERIV).shift(DOWN * 1.6)
            self.play(FadeIn(grp), FadeIn(card), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A fixed-rate chain", r"A car uses $\frac{1}{30}$ gallon per mile and drives 60 miles per hour. How fast is it using gas?",
                     [r"\frac{1}{30}\,\frac{\text{gal}}{\text{mile}} \times 60\,\frac{\text{miles}}{\text{hr}}", r"= 2\ \frac{\text{gal}}{\text{hr}}"], at=[1, 2],
                     ref=r"\frac{dy}{dx} = \frac{dy}{du}\cdot\frac{du}{dx}")
        self.example("Example 2: Outside and inside", r"Find the derivative of $(2x^2 + 3)^4$.",
                     [r"(\underbrace{2x^2 + 3}_{u})^4", r"u = 2x^2 + 3", r"u' = 4x", r"\frac{d}{dx}u^4 = 4u^3\cdot u'",
                      r"= 4(2x^2 + 3)^3 \cdot 4x = 16x(2x^2 + 3)^3"], at=[1, 2, 2, 3, 4])
        self.example("Example 3: Trig and exponential layers", r"Find each derivative.",
                     [r"PART:(a) $\dfrac{d}{dx}\sin(x^3)$", r"\sin(\underbrace{x^3}_{u})", r"u = x^3", r"u' = 3x^2", r"\cos u\cdot u' = \cos(x^3)\cdot 3x^2",
                      r"PART:(b) $\dfrac{d}{dx}e^{5x}$", r"e^{\overbrace{5x}^{u}}", r"u = 5x", r"u' = 5", r"e^u\cdot u' = e^{5x}\cdot 5 = 5e^{5x}"],
                     at=[1, 2, 2, 2, 3, 4, 5, 5, 5, 6],
                     text=r"Find (a) $\dfrac{d}{dx}\sin(x^3)$ and (b) $\dfrac{d}{dx}e^{5x}$.")
        tb = table(["x", "f", "f'", "g", "g'"], [["1", "3", "-2", "4", "5"], ["4", "0", "7", "1", "-1"]], size=36)
        self.example("Example 4: From a table", VGroup(T(r"$h(x) = f(g(x))$. Find $h'(1)$.", 42), tb).arrange(DOWN, buff=0.3),
                     [r"h'(1) = f'\big(g(1)\big)\cdot g'(1)", r"g(1) = 4, \ \text{so } f'\big(g(1)\big) = f'(4) = 7", r"h'(1) = 7 \cdot 5 = 35", r"TEXT:We never used $f'(1) = -2$."], at=[1, 2, 3, 4],
                     ref=r"\frac{d}{dx}f\big(g(x)\big) = f'\big(g(x)\big)\cdot g'(x)",
                     text=r"$h(x) = f(g(x))$. Find $h'(1)$. \[ \begin{array}{c|cccc} x & f & f' & g & g' \\ \hline 1 & 3 & -2 & 4 & 5 \\ 4 & 0 & 7 & 1 & -1 \end{array} \]")
        self.finish()
