"""Topic 2.8: The product rule, from a w-by-l rectangle growing by dw and dl. Narration comes from transcripts/2_8.md."""
import numpy as np
from manim import *

from kit import *
from style import *

L0, W0 = 4.6, 2.8          # drawn length (across) and width (up)
RW, RL = 0.9, 1.1          # dw/dx and dl/dx, so a nudge dx grows w by RW*dx and l by RL*dx


def rect(dx, corner, l=L0, w=W0):
    dw, dl = RW * dx, RL * dx
    main = Rectangle(width=l, height=w, color=FUNC, fill_color=FUNC, fill_opacity=0.3).move_to(corner + RIGHT * l / 2 + UP * w / 2)
    top = Rectangle(width=l, height=max(dw, 1e-3), color=SECANT, fill_color=SECANT, fill_opacity=0.7, stroke_width=1).move_to(corner + RIGHT * l / 2 + UP * (w + dw / 2))
    side = Rectangle(width=max(dl, 1e-3), height=w, color=DERIV, fill_color=DERIV, fill_opacity=0.7, stroke_width=1).move_to(corner + RIGHT * (l + dl / 2) + UP * w / 2)
    tiny = Rectangle(width=max(dl, 1e-3), height=max(dw, 1e-3), color=TANGENT, fill_color=TANGENT, fill_opacity=0.9, stroke_width=1).move_to(corner + RIGHT * (l + dl / 2) + UP * (w + dw / 2))
    return VGroup(main, top, side, tiny)


class Lesson(TranscriptScene):
    NUM = "2.8"

    def construct(self):
        with self.beat("A tempting mistake") as b:
            bad = M(r"(f g)' \overset{?}{=} f' g'", 64).shift(UP * 1.6)
            self.play(Write(bad), run_time=1.2)
            b.line(1)
            # slowly: x^2 is x times x; the power rule says 2x; the shortcut says 1 times 1 (Adder)
            sq = M(r"x^2 = x \cdot x", 52).next_to(bad, DOWN, buff=0.7)
            self.play(Write(sq), run_time=1)
            b.line(2)
            right = VGroup(T("power rule:", 34, DIM), M(r"\frac{d}{dx}\,x^2 = 2x", 48, DERIV)).arrange(RIGHT, buff=0.3)
            right.next_to(sq, DOWN, buff=0.6).shift(LEFT * 3)
            self.play(FadeIn(right), run_time=1)
            b.line(3)
            short = VGroup(T("shortcut:", 34, DIM), M(r"(x)' \cdot (x)' = 1 \cdot 1 = 1", 48, SECANT)).arrange(RIGHT, buff=0.3)
            short.next_to(sq, DOWN, buff=0.6).shift(RIGHT * 3)
            self.play(FadeIn(short), run_time=1)
            b.line(4)
            ne = M(r"2x \ne 1", 60, TANGENT).next_to(VGroup(right, short), DOWN, buff=0.7)
            self.play(FadeIn(ne, scale=1.4), run_time=0.8)
        self.clear()
        self.title()

        corner = LEFT * 5.6 + DOWN * 2.3
        dx = ValueTracker(0.0)
        r = always_redraw(lambda: rect(dx.get_value(), corner))
        with self.beat("A rectangle that grows two ways") as b:
            base = rect(0, corner)[0]
            labs = VGroup(M("l", 40, DIM).next_to(base, DOWN, buff=0.15), M("w", 40, DIM).next_to(base, LEFT, buff=0.15), M(r"A = w \cdot l", 46).move_to(base))
            self.play(DrawBorderThenFill(base), FadeIn(labs), run_time=1.2)
            b.line(1)
            self.remove(base)
            self.add(r, labs[2])
            self.play(dx.animate.set_value(0.45), run_time=1.6)
            # each nudge gets a little double arrow, labeled where the labels were (Adder)
            dwl = nudge_arrow(corner + UP * W0, corner + UP * (W0 + RW * 0.45), "dw", LEFT, SECANT, 34)
            dll = nudge_arrow(corner + RIGHT * L0, corner + RIGHT * (L0 + RL * 0.45), "dl", DOWN, DERIV, 34)
            self.play(FadeIn(dwl), FadeIn(dll), run_time=0.6)
            b.line(2)
            tags = VGroup(M(r"l\,dw", 34, SECANT).move_to(corner + RIGHT * L0 / 2 + UP * (W0 + RW * 0.225)),
                          M(r"w\,dl", 34, DERIV).rotate(PI / 2).move_to(corner + RIGHT * (L0 + RL * 0.225) + UP * W0 / 2),
                          M(r"dw\,dl", 28, TANGENT).next_to(corner + RIGHT * (L0 + RL * 0.45) + UP * (W0 + RW * 0.45), UR, buff=0.08))
            for t in tags:
                self.play(FadeIn(t), run_time=0.6)
        with self.beat("From the nudge to the limit") as b:
            e1 = M(r"dA = l\,dw + w\,dl + dw\,dl", 42).set_max_width(6.4).to_edge(RIGHT, buff=0.4).shift(UP * 2.6)
            self.play(Write(e1), run_time=1.2)
            b.line(1)
            e2 = M(r"\frac{dA}{dx} = l\,\frac{dw}{dx} + w\,\frac{dl}{dx}", r"+ dw\,\frac{dl}{dx}", 42)
            e2.set_max_width(6.4).next_to(e1, DOWN, buff=0.45).align_to(e1, LEFT)
            self.play(Write(e2[0]), run_time=1.2)
            b.line(2)
            self.play(Write(e2[1]), run_time=0.8)
            b.line(3)
            self.play(FadeOut(tags), FadeOut(dwl), FadeOut(dll), run_time=0.4)
            self.play(dx.animate.set_value(0.08), run_time=3)
            b.line(4)
            self.play(Indicate(e2[1], color=TANGENT), run_time=1)
            note = M(r"dw \to 0", 38, TANGENT).next_to(e2[1], DOWN, buff=0.3)
            self.play(FadeIn(note), run_time=0.6)
            b.line(5)
            e3 = M(r"\frac{dA}{dx} = \frac{dw}{dx}\, l + w\,\frac{dl}{dx}", 48, INK).next_to(e2, DOWN, buff=1.0).align_to(e1, LEFT)
            self.play(Write(e3), run_time=1.4)
        with self.beat("Reading off the rule") as b:
            self.play(FadeOut(VGroup(e1, e2, note)), run_time=0.5)
            e4 = M(r"\frac{d}{dx}\big[f(x)\,g(x)\big] = f'(x)\,g(x) + f(x)\,g'(x)", 44).set_max_width(6.4).move_to(e3).to_edge(RIGHT, buff=0.4)
            self.play(e3.animate.shift(UP * 2.2), run_time=0.6)
            self.play(Write(e4), run_time=1.4)
            b.line(1)
            uv = formula_box(M(r"(uv)' = u'v + uv'", 64), DERIV).move_to(e4).shift(DOWN * 0.2)
            self.play(e4.animate.shift(UP * 1.2).set_opacity(0.5), FadeIn(uv), run_time=1.2)
        self.clear()
        self.remove(r)

        with self.beat("In words") as b:
            w = T(r"(derivative of the first) $\times$ (the second) \\ $+$ (the first) $\times$ (derivative of the second)", 44)
            self.play(FadeIn(w), run_time=1.2)
            b.line(1)
            self.play(Indicate(w, color=SECANT), run_time=1.2)
        self.clear()

        self.example("Two factors", r"Find $\dfrac{d}{dx}\left[x^2\sin x\right]$.",
                     [r"\underbrace{x^2}_{u}\,\underbrace{\sin x}_{v}", r"u' = 2x, \qquad v' = \cos x", r"u'v + uv' = 2x\sin x + x^2\cos x"], at=[1, 2, 3])
        self.example("Exponential times a polynomial", r"Find $\dfrac{d}{dx}\left[(x^3 - 1)e^x\right]$.",
                     [r"\underbrace{(x^3 - 1)}_{u}\,\underbrace{e^x}_{v}", r"u' = 3x^2, \qquad v' = e^x", r"u'v + uv' = 3x^2e^x + (x^3 - 1)e^x = e^x(x^3 + 3x^2 - 1)"], at=[1, 2, 3])
        self.example("At a point, no formula needed", r"$f(x) = (x^2 + 1)(x^3 - 2x)$. Find $f'(2)$.",
                     [r"\underbrace{(x^2 + 1)}_{u}\,\underbrace{(x^3 - 2x)}_{v}", r"u(2) = 5, \qquad v(2) = 8 - 4 = 4",
                      r"u' = 2x:\ u'(2) = 4, \qquad v' = 3x^2 - 2:\ v'(2) = 10", r"f'(2) = u'(2)v(2) + u(2)v'(2) = (4)(4) + (5)(10) = 66"], at=[1, 2, 3, 4])
        self.example("In context", r"Revenue is $R = pq$. At one moment the price $p = 40$ dollars and is rising at $2$ dollars per week, while sales $q = 300$ and are falling at $10$ per week. How fast is revenue changing?",
                     [r"u = p = 40,\ \ u' = 2, \qquad v = q = 300,\ \ v' = -10", r"R' = u'v + uv' = (2)(300) + (40)(-10)", r"= 600 - 400 = 200 \text{ dollars per week}"], at=[1, 2, 3])

        with self.beat("Close") as b:
            # the takeaway is the rule itself, not the picture (Adder)
            card = formula_box(M(r"(uv)' = u'v + uv'", 64), DERIV).shift(UP * 0.4)
            how = T("differentiate one factor at a time, then add", 34, DIM).next_to(card, DOWN, buff=0.5)
            self.play(FadeIn(card), run_time=1)
            self.play(FadeIn(how), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: A product of two familiar functions", r"Find $\dfrac{dy}{dx}$ for $y = x^3 e^x$.",
                     [r"\underbrace{x^3}_{u}\,\underbrace{e^x}_{v}", r"u' = 3x^2, \qquad v' = e^x", r"\frac{dy}{dx} = u'v + uv' = 3x^2 e^x + x^3 e^x", r"= x^2 e^x (3 + x)"], at=[1, 2, 3, 4])
        tb = table(["x", "f", "f'", "g", "g'"], [["2", "3", "-1", "5", "4"]], size=40)
        self.example("Example 2: Values from a table", VGroup(T(r"$h(x) = f(x)\,g(x)$. Find $h'(2)$.", 42), tb).arrange(DOWN, buff=0.3),
                     [r"h'(2) = f'(2)\,g(2) + f(2)\,g'(2)", r"= (-1)(5) + (3)(4)", r"= -5 + 12 = 7"], at=[1, 2, 3],
                     text=r"$h(x) = f(x)\,g(x)$. Find $h'(2)$. \[ \begin{array}{c|cccc} x & f & f' & g & g' \\ \hline 2 & 3 & -1 & 5 & 4 \end{array} \]")
        self.example("Example 3: Checking the rule on something we know", r"Differentiate $(2x + 1)(x^2 - 3)$ two ways.",
                     [r"\text{product rule: } 2(x^2 - 3) + (2x + 1)(2x) = 6x^2 + 2x - 6", r"\text{expand first: } 2x^3 + x^2 - 6x - 3 \ \to\ 6x^2 + 2x - 6",
                      r"\text{same answer } \checkmark"], at=[1, 2, 3])
        self.finish()
