"""Topic 9.6 (BC): Motion problems with parametric and vector-valued functions. Narration comes from transcripts/9_6.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.6"

    def construct(self):
        with self.beat("Everything at once") as b:
            field = Rectangle(width=7.5, height=5, stroke_width=0, fill_color=MEADOW, fill_opacity=0.35).shift(LEFT * 2)
            ax, _ = plot_axes([-3, 3, 1], [-2, 2, 1], w=7, h=4.4, coords=False)
            ax.move_to(field)
            px = lambda s: -2.6 + 1.7 * s
            py = lambda s: 1.4 * np.sin(1.6 * s)
            path = param_curve(ax, px, py, 0, 3.1)
            d = drone(0.7).move_to(ax.c2p(px(0), py(0)))
            self.play(FadeIn(field), FadeIn(ax), FadeIn(d), run_time=0.8)
            self.play(Create(path), MoveAlongPath(d, path), run_time=2.4, rate_func=linear)
            labels = VGroup(M(r"\text{position } (x(t), y(t))", 30), M(r"\text{velocity } \langle x', y'\rangle", 30, DERIV), M(r"\text{speed } \sqrt{(x')^2 + (y')^2}", 30), M(r"\text{distance } \int \text{speed}\,dt", 30, ACCUM),
                            M(r"\text{slope } \tfrac{dy}{dx} = \tfrac{y'}{x'}", 30, SECANT)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
            b.line(1)
            self.play(LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.3), run_time=2)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("The toolkit") as b:
            tab = table([r"\text{want}", r"\text{tool}"], [[r"\text{position at } b", r"x(b) = x(a) + \int_a^b x'(t)\,dt"], [r"\text{velocity vector}", r"\langle x'(t),\ y'(t)\rangle"],
                        [r"\text{speed}", r"\sqrt{(x')^2 + (y')^2}"], [r"\text{distance traveled}", r"\int_a^b \sqrt{(x')^2 + (y')^2}\,dt"], [r"\text{slope of the path}", r"y'/x'"],
                        [r"\text{left/right, up/down}", r"\text{signs of } x', y'"], [r"\text{at rest}", r"x' = 0 \text{ and } y' = 0"]], size=30)
            rows = tab[0]
            self.play(FadeIn(rows[0]), FadeIn(tab[1]), FadeIn(rows[1]), run_time=1)
            b.line(1)
            self.play(FadeIn(rows[2]), FadeIn(rows[3]), run_time=1)
            b.line(2)
            self.play(FadeIn(rows[4]), run_time=0.8)
            b.line(3)
            self.play(FadeIn(rows[5]), FadeIn(rows[6]), FadeIn(rows[7]), run_time=1.2)
        self.clear()

        self.example("A full motion problem", r"A particle has $x'(t) = 2t - 4$, $y'(t) = 3t^2$, and is at $(1, 0)$ at $t = 0$. (a) Speed at $t = 1$? (b) For which $t > 0$ is it moving left? (c) Position at $t = 2$? (d) Distance traveled, $0 \le t \le 2$?",
                     [r"\text{(a) } x'(1) = -2, \ y'(1) = 3", r"\text{speed} = \sqrt{(-2)^2 + 3^2} = \sqrt{13} \approx 3.61", r"\text{(b) } 2t - 4 < 0: \ 0 < t < 2",
                      r"\text{(c) } x(2) = 1 + \int_0^2 (2t - 4)\,dt = 1 + (4 - 8) = -3", r"y(2) = 0 + \int_0^2 3t^2\,dt = 8", r"\text{position } (-3, 8)",
                      r"\text{(d) } \int_0^2 \sqrt{(2t - 4)^2 + 9t^4}\,dt \approx 10.468"], at=[1, 1, 2, 3, 4, 4, 5], follow=True)

        with self.beat("Close") as b:
            card = VGroup(T("position: start $+ \\int$ velocity (each component)", 34), M(r"\text{speed: } \sqrt{(x')^2 + (y')^2}", 38), M(r"\text{distance: } \int \text{speed}\,dt", 38, ACCUM),
                          M(r"\text{slope: } y'/x'", 38, SECANT), T("direction: signs of $x'$ and $y'$", 34, DERIV)).arrange(DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: A calculator problem", r"A drone has $x'(t) = \cos(t^2)$, $y'(t) = e^{t/2}$, and is at $(3, 1)$ at $t = 0$. Find (a) its position at $t = 2$, (b) its speed at $t = 2$, (c) the distance traveled for $0 \le t \le 2$.",
                     [r"\text{(a) } x(2) = 3 + \int_0^2 \cos(t^2)\,dt \approx 3.461", r"y(2) = 1 + \int_0^2 e^{t/2}\,dt \approx 4.437", r"\text{(b) } \sqrt{\cos^2 4 + e^2} \approx 2.796",
                      r"\text{(c) } \int_0^2 \sqrt{\cos^2(t^2) + e^t}\,dt \approx 3.828"], at=[1, 1, 2, 3])
        self.example("Example 2: Slope and tangent line", r"A particle has $x'(t) = t + 1$, $y'(t) = t^2 - 2$, and is at $(4, 5)$ at $t = 1$. Find the slope of its path and the tangent line there.",
                     [r"\frac{dy}{dx} = \frac{y'}{x'} = \frac{1 - 2}{1 + 1} = -\tfrac12", r"y - 5 = -\tfrac12(x - 4)"], at=[1, 2])
        self.example("Example 3: At rest?", r"A particle has $x'(t) = t^2 - 4$ and $y'(t) = t - 2$ for $t \ge 0$. When is it at rest? When is it moving straight up or down?",
                     [r"\text{at rest: } t^2 - 4 = 0 \text{ and } t - 2 = 0: \ t = 2", r"TEXT:Vertical motion needs $x' = 0$ with $y' \ne 0$; $x' = 0$ only at $t = 2$, where $y' = 0$ too: never."],
                     at=[1, 2])
        self.finish()
