"""Topic 5.3: Increasing and decreasing intervals. Narration comes from transcripts/5_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "5.3"

    def construct(self):
        ax, al = plot_axes([0, 6, 1], [-2, 3, 1], w=10, h=4.6, coords=False)
        VGroup(ax, al).shift(UP * 0.3)
        f = lambda s: np.sin(1.2 * s) + 0.25 * s
        df = lambda s: 1.2 * np.cos(1.2 * s) + 0.25
        with self.beat("Uphill and downhill") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(ax.plot(f, x_range=[0, 6], color=FUNC, stroke_width=5)), run_time=1.2)
            S = ValueTracker(0.1)
            tan = always_redraw(lambda: tangent_line(ax, f, S.get_value(), df(S.get_value()), [S.get_value() - 0.5, S.get_value() + 0.5],
                                                     color=DERIV if df(S.get_value()) > 0 else TANGENT).set_stroke(width=6))
            self.add(tan)
            self.play(S.animate.set_value(5.9), run_time=5, rate_func=linear)
            b.line(1)
            roots = [r for r in np.linspace(0, 6, 6001) if abs(df(r)) < 2e-3]
            cuts = [0] + sorted({round(r, 1) for r in roots}) + [6]
            bars = VGroup()
            for lo, hi in zip(cuts, cuts[1:]):
                up = df((lo + hi) / 2) > 0
                seg = Line(ax.c2p(lo, -2) + DOWN * 0.5, ax.c2p(hi, -2) + DOWN * 0.5, color=DERIV if up else TANGENT, stroke_width=8)
                bars.add(VGroup(seg, T("increasing" if up else "decreasing", 26, DERIV if up else TANGENT).next_to(seg, DOWN, buff=0.15)))
            self.play(FadeIn(bars), run_time=1)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The rule") as b:
            r1 = M(r"f'(x) > 0 \text{ on an interval} \ \Rightarrow\ f \text{ is increasing there}", 46, DERIV)
            r2 = M(r"f'(x) < 0 \text{ on an interval} \ \Rightarrow\ f \text{ is decreasing there}", 46, TANGENT)
            VGroup(r1, r2).arrange(DOWN, buff=0.8)
            self.play(Write(r1), run_time=1.2)
            b.line(1)
            self.play(Write(r2), run_time=1.2)
        self.clear()

        with self.beat("A sign chart") as b:
            fp = M(r"f'(x) = 3x^2 - 12 = 3(x - 2)(x + 2)", 50).to_edge(UP, buff=0.7)
            self.play(Write(fp), run_time=1.2)
            b.line(1)
            ch = sign_chart([-2, 2], ["+", "-", "+"], words=["inc", "dec", "inc"]).shift(DOWN * 0.4)
            self.play(Create(ch[0]), FadeIn(ch[1]), FadeIn(ch[2]), FadeIn(ch[5]), run_time=1)
            b.line(2)
            tests = [r"f'(-3) = 15", r"f'(0) = -12", r"f'(3) = 15"]
            for k, tx in enumerate(tests):
                tm = M(tx, 32, DIM).next_to(ch[3][k], UP, buff=0.3)
                self.play(FadeIn(tm), FadeIn(ch[3][k]), run_time=0.7)
            b.line(3)
            self.play(FadeIn(ch[4]), run_time=0.8)
        self.clear()
        self.example("Increasing from a sign chart", r"Where is $f(x) = x^3 - 3x^2 + 4$ increasing?",
                     [r"f'(x) = 3x^2 - 6x = 3x(x - 2)", r"f'(-1) = 9 > 0, \quad f'(1) = -3 < 0, \quad f'(3) = 9 > 0", r"\text{increasing on } (-\infty, 0) \text{ and } (2, \infty)"], at=[1, 2, 3])

        with self.beat("Justify with the derivative") as b:
            s = T(r"$f$ is decreasing on $(-2, 2)$ \textbf{because} $f'(x) < 0$ there.", 46)
            self.play(Write(s), run_time=1.4)
            self.play(Circumscribe(s, color=SECANT), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            ch = sign_chart([-2, 2], ["+", "-", "+"], words=["inc", "dec", "inc"]).shift(UP * 0.4)
            self.play(FadeIn(ch), run_time=0.8)
            self.play(FadeIn(T(r"the sign of $f'$ is the direction of $f$", 42, SECANT).next_to(ch, DOWN, buff=0.7)), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: A cubic", r"On what intervals is $f(x) = x^3 - 12x + 1$ increasing? Decreasing?",
                     [r"f'(x) = 3x^2 - 12 = 3(x - 2)(x + 2)", r"\text{critical points: } x = -2,\ x = 2", r"\text{signs of } f' \text{: } +,\ -,\ +",
                      r"\text{increasing on } (-\infty, -2),\ (2, \infty);\ \ \text{decreasing on } (-2, 2)"], at=[1, 2, 3, 4])
        self.example("Example 2: An exponential", r"On what intervals is $f(x) = xe^{-x}$ increasing? Decreasing?",
                     [r"f'(x) = e^{-x} - xe^{-x} = (1 - x)e^{-x}", r"e^{-x} > 0, \text{ so the sign of } f' \text{ is the sign of } 1 - x",
                      r"\text{increasing on } (-\infty, 1);\ \ \text{decreasing on } (1, \infty)"], at=[1, 2, 3])
        self.example("Example 3: A repeated factor", r"$f'(x) = (x + 1)(x - 3)^2$. On what intervals is $f$ increasing?",
                     [r"\text{critical points: } x = -1,\ x = 3", r"\text{signs of } f' \text{: } -,\ +,\ +", r"\text{increasing on } (-1, 3) \text{ and } (3, \infty)"], at=[1, 2, 3])
        self.finish()
