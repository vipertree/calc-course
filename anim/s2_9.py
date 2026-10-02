"""Topic 2.9: The quotient rule, from a rectangle with area f, width g and height Q = f/g. Narration comes from transcripts/2_9.md."""
import numpy as np
from manim import *

from kit import *
from style import *

G0, Q0 = 4.6, 2.8          # drawn width g (across) and height Q (up)
RG, RQ = 1.1, 0.8          # dg/dx and dQ/dx


def rect(dx, corner, g=G0, q=Q0):
    dg, dq = RG * dx, RQ * dx
    main = Rectangle(width=g, height=q, color=FUNC, fill_color=FUNC, fill_opacity=0.3).move_to(corner + RIGHT * g / 2 + UP * q / 2)
    side = Rectangle(width=max(dg, 1e-3), height=q, color=SECANT, fill_color=SECANT, fill_opacity=0.7, stroke_width=1).move_to(corner + RIGHT * (g + dg / 2) + UP * q / 2)
    top = Rectangle(width=g, height=max(dq, 1e-3), color=DERIV, fill_color=DERIV, fill_opacity=0.7, stroke_width=1).move_to(corner + RIGHT * g / 2 + UP * (q + dq / 2))
    tiny = Rectangle(width=max(dg, 1e-3), height=max(dq, 1e-3), color=TANGENT, fill_color=TANGENT, fill_opacity=0.9, stroke_width=1).move_to(corner + RIGHT * (g + dg / 2) + UP * (q + dq / 2))
    return VGroup(main, side, top, tiny)


QR = r"\frac{d}{dx}\left[\frac{f(x)}{g(x)}\right] = \frac{g(x)\,f'(x) - f(x)\,g'(x)}{\big[g(x)\big]^2}"


class Lesson(TranscriptScene):
    NUM = "2.9"

    def construct(self):
        with self.beat("Dividing changing quantities") as b:
            t = ValueTracker(0)
            miles = always_redraw(lambda: M(rf"\text{{miles}}: {120 + 31 * t.get_value():.0f}", 48).shift(LEFT * 3 + UP * 1))
            gal = always_redraw(lambda: M(rf"\text{{gallons}}: {4 + 1.1 * t.get_value() + 0.08 * t.get_value() ** 2:.1f}", 48).shift(RIGHT * 3 + UP * 1))
            mpg = always_redraw(lambda: M(rf"\frac{{\text{{miles}}}}{{\text{{gallons}}}} = {(120 + 31 * t.get_value()) / (4 + 1.1 * t.get_value() + 0.08 * t.get_value() ** 2):.2f}", 52, SECANT).shift(DOWN * 1.2))
            self.play(FadeIn(miles), FadeIn(gal), FadeIn(mpg), run_time=0.8)
            self.play(t.animate.set_value(6), run_time=4, rate_func=linear)
        self.clear()
        self.title()

        corner = LEFT * 5.6 + DOWN * 2.3
        dx = ValueTracker(0.0)
        r = always_redraw(lambda: rect(dx.get_value(), corner))
        with self.beat("The ratio as a rectangle") as b:
            base = rect(0, corner)[0]
            area = M(r"\text{area } f", 46).move_to(base)
            gl = M("g", 40, DIM).next_to(base, DOWN, buff=0.15)
            self.play(DrawBorderThenFill(base), FadeIn(area), FadeIn(gl), run_time=1.2)
            b.line(1)
            ql = M("Q", 40, DIM).next_to(base, LEFT, buff=0.15)
            cap = M(r"Q = \frac{f}{g}", 52).to_edge(RIGHT, buff=1).shift(UP * 1.6)
            self.play(FadeIn(ql), Write(cap), run_time=1)
            b.line(2)
            self.play(FadeIn(T(r"height $=$ area $\div$ width", 34, DIM).next_to(cap, DOWN, buff=0.4)), run_time=0.8)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (base, area, gl, ql) and not isinstance(m, ValueTracker)], run_time=0.4)

        with self.beat("Nudging the rectangle") as b:
            self.remove(base)
            self.add(r, area)
            self.play(dx.animate.set_value(0.45), run_time=1.6)
            tags = VGroup(M(r"Q\,dg", 32, SECANT).rotate(PI / 2).move_to(corner + RIGHT * (G0 + RG * 0.225) + UP * Q0 / 2),
                          M(r"g\,dQ", 32, DERIV).move_to(corner + RIGHT * G0 / 2 + UP * (Q0 + RQ * 0.225)),
                          M(r"dg\,dQ", 28, TANGENT).next_to(corner + RIGHT * (G0 + RG * 0.45) + UP * (Q0 + RQ * 0.45), UR, buff=0.08))
            b.line(1)
            for tg in tags:
                self.play(FadeIn(tg), run_time=0.5)
            b.line(2)
            e1 = M(r"df = Q\,dg + g\,dQ + dg\,dQ", 42).set_max_width(6.4).to_edge(RIGHT, buff=0.4).shift(UP * 2.8)
            self.play(Write(e1), run_time=1.2)
        with self.beat("Solving for the change in height") as b:
            e2 = M(r"\frac{df}{dx} = Q\,\frac{dg}{dx} + g\,\frac{dQ}{dx} + dg\,\frac{dQ}{dx}", 42).set_max_width(6.4)
            e2.next_to(e1, DOWN, buff=0.4).align_to(e1, LEFT)
            self.play(Write(e2), FadeOut(tags), run_time=1.2)
            self.play(dx.animate.set_value(0.06), run_time=2.4)
            b.line(1)
            board = VGroup(M(r"f' = Q\,g' + g\,Q'", 46))
            board[0].next_to(e2, DOWN, buff=0.5).align_to(e1, LEFT)
            self.play(Write(board[0]), run_time=1)
            b.line(2)
            steps = [r"Q' = \frac{f' - Q\,g'}{g}", r"= \frac{f' - \frac{f}{g}\,g'}{g}", r"= \frac{f'\,g - f\,g'}{g^2}"]
            for i, s in enumerate(steps):
                if i == 1:
                    b.line(3)
                if i == 2:
                    b.line(4)
                m = M(s, 46, DERIV if i == 2 else INK).next_to(board[-1], DOWN, buff=0.3).align_to(e1, LEFT)
                board.add(m)
                self.play(Write(m), run_time=1)
        self.clear()
        self.remove(r)

        with self.beat("The rule and a memory aid") as b:
            rule = M(r"\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}", 60)
            card = formula_box(rule, DERIV).shift(UP * 1.6)
            self.play(FadeIn(card), run_time=1.2)
            fg = M(QR, 36, DIM).next_to(card, DOWN, buff=0.4)
            self.play(FadeIn(fg), run_time=0.6)
            b.line(1)
            aid = T(r"``low d-high minus high d-low, over the square of what's below''", 36, SECANT).next_to(fg, DOWN, buff=0.4)
            self.play(FadeIn(aid), run_time=1)
            b.line(2)
            self.play(Indicate(rule, color=TANGENT, scale_factor=1.05), run_time=1)
        self.clear()

        UV = lambda top, bot: rf"\frac{{d}}{{dx}}\left[\frac{{\overbrace{{{top}}}^{{u}}}}{{\underbrace{{{bot}}}_{{v}}}}\right]"
        self.example("A rational function", r"Find $\dfrac{d}{dx}\left[\dfrac{x^2 + 1}{x - 3}\right]$.",
                     [UV("x^2 + 1", "x - 3"), r"u' = 2x, \qquad v' = 1", r"\frac{u'v - uv'}{v^2} = \frac{(2x)(x - 3) - (x^2 + 1)(1)}{(x - 3)^2}",
                      r"= \frac{x^2 - 6x - 1}{(x - 3)^2}"], at=[1, 1, 2, 3])
        self.example("With exponentials", r"Find $\dfrac{d}{dx}\left[\dfrac{e^x}{x}\right]$.",
                     [UV("e^x", "x"), r"u' = e^x, \qquad v' = 1", r"\frac{u'v - uv'}{v^2} = \frac{xe^x - e^x}{x^2}", r"= \frac{e^x(x - 1)}{x^2}"], at=[1, 1, 2, 3])
        self.example("At a point, no formula needed", r"$f(x) = \dfrac{x^2 + 3}{2x - 1}$. Find $f'(2)$.",
                     [r"u = x^2 + 3, \qquad v = 2x - 1", r"u(2) = 7, \quad v(2) = 3, \quad u'(2) = 4, \quad v'(2) = 2",
                      r"f'(2) = \frac{u'(2)v(2) - u(2)v'(2)}{v(2)^2} = \frac{(4)(3) - (7)(2)}{3^2}", r"= \frac{12 - 14}{9} = -\frac29"], at=[1, 2, 3, 4])
        self.example("Rewrite instead", r"Find the derivatives of (a) $\dfrac{x^3 + 4x}{x}$ and (b) $\dfrac{5}{x^2}$ without the quotient rule.",
                     [r"\text{(a) } \frac{x^3 + 4x}{x} = x^2 + 4 \ \to\ 2x", r"\text{(b) } \frac{5}{x^2} = 5x^{-2} \ \to\ -10x^{-3}"], at=[1, 2])
        ax, al = plot_axes([0, 400, 100], [0, 40, 10], w=5, h=3.8, xlabel="n", ylabel="A")
        avg = lambda n: 2000 / n + 5
        figc = VGroup(ax, al, ax.plot(avg, x_range=[60, 400], color=FUNC, stroke_width=4), tangent_line(ax, avg, 100, -0.2, [40, 160]), closed_dot(ax, 100, 25, INK))
        self.example("In context", r"Making $n$ lamps costs $C(n) = 2000 + 5n$ dollars, so the average cost per lamp is $A(n) = \dfrac{2000 + 5n}{n}$. Find $A'(100)$ and interpret it.",
                     [r"u = 2000 + 5n,\ u' = 5; \quad v = n,\ v' = 1", r"A'(n) = \frac{5n - (2000 + 5n)}{n^2}", r"= \frac{\cancel{5n} - 2000 - \cancel{5n}}{n^2} = -\frac{2000}{n^2}",
                      r"A'(100) = -\frac{2000}{10000} = -0.2", r"TEXT:At 100 lamps, average cost is falling by about 20 cents per additional lamp."], figure=figc, at=[1, 2, 2, 3, 4])

        with self.beat("Close") as b:
            card = formula_box(M(r"\left(\frac{u}{v}\right)' = \frac{u'v - uv'}{v^2}", 52), DERIV).shift(UP * 0.8)
            aid = T(r"low d-high minus high d-low, over the square of what's below", 34, SECANT).next_to(card, DOWN, buff=0.5)
            self.play(FadeIn(card), FadeIn(aid), run_time=1.2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A rational function", r"Find $f'(x)$ for $f(x) = \dfrac{3x - 2}{x + 4}$.",
                     [UV("3x - 2", "x + 4"), r"u' = 3, \qquad v' = 1", r"f'(x) = \frac{(3)(x + 4) - (3x - 2)(1)}{(x + 4)^2}",
                      r"= \frac{\cancel{3x} + 12 - \cancel{3x} + 2}{(x + 4)^2} = \frac{14}{(x + 4)^2}"], at=[1, 1, 2, 3])
        self.example("Example 2: A trig quotient", r"Find $\dfrac{dy}{dx}$ for $y = \dfrac{\sin x}{1 + \cos x}$.",
                     [r"u = \sin x,\ u' = \cos x; \quad v = 1 + \cos x,\ v' = -\sin x", r"\frac{dy}{dx} = \frac{(\cos x)(1 + \cos x) - (\sin x)(-\sin x)}{(1 + \cos x)^2}", r"= \frac{\cos x + \cos^2 x + \sin^2 x}{(1 + \cos x)^2}",
                      r"= \frac{1 + \cos x}{(1 + \cos x)^2}", r"= \frac{1}{1 + \cos x}"], at=[1, 1, 2, 3, 4])
        tb = table(["x", "f", "f'", "g", "g'"], [["1", "6", "2", "3", "-1"]], size=40)
        self.example("Example 3: Values at a point", VGroup(T(r"Find the derivative of $\dfrac{f}{g}$ at $x = 1$.", 42), tb).arrange(DOWN, buff=0.3),
                     [r"\frac{g(1)\,f'(1) - f(1)\,g'(1)}{g(1)^2} = \frac{(3)(2) - (6)(-1)}{3^2}", r"= \frac{12}{9}", r"= \frac43"], at=[1, 2, 3],
                     text=r"Find the derivative of $\dfrac{f}{g}$ at $x = 1$. \[ \begin{array}{c|cccc} x & f & f' & g & g' \\ \hline 1 & 6 & 2 & 3 & -1 \end{array} \]")
        self.finish()
