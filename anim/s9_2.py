"""Topic 9.2 (BC): Second derivatives of parametric equations. Narration comes from transcripts/9_2.md."""
import numpy as np
from manim import *

from kit import *
from style import *


class Lesson(TranscriptScene):
    NUM = "9.2"

    def construct(self):
        X = lambda s: s * s - 1
        Y = lambda s: s**3 - 3 * s
        with self.beat("Bowl or hill?") as b:
            ax, al = plot_axes([-1.6, 3.6, 1], [-2.8, 2.8, 1], w=5.4, h=5.2, coords=False)
            VGroup(ax, al).shift(LEFT * 1.5)
            up = param_curve(ax, X, Y, 0.02, 2.1, color=DERIV)
            dn = param_curve(ax, X, Y, -2.1, -0.02, color=TANGENT)
            self.play(FadeIn(ax), FadeIn(al), Create(dn), Create(up), run_time=1.4)
            dot = Dot(ax.c2p(X(-2), Y(-2)), color=INK)
            self.play(MoveAlongPath(dot, param_curve(ax, X, Y, -2, 2)), run_time=2.4)
            b.line(1)
            self.play(FadeIn(VGroup(T("bowl: concave up", 32, DERIV), T("hill: concave down", 32, TANGENT), M(r"\frac{d^2y}{dx^2}", 48)).arrange(DOWN, buff=0.4).to_edge(RIGHT, buff=0.8)), run_time=1)
            b.line(2)
        self.clear()
        self.title()

        with self.beat("Differentiate the slope, then divide again") as b:
            r0 = M(r"\frac{d^2y}{dx^2} = \frac{d}{dx}\left(\frac{dy}{dx}\right)", 46).to_edge(UP, buff=0.7)
            self.play(Write(r0), run_time=1)
            b.line(1)
            r1 = M(r"\frac{d}{dx}(\text{anything}) = \frac{\frac{d}{dt}(\text{anything})}{dx/dt}", 42).next_to(r0, DOWN, buff=0.5)
            self.play(Write(r1), run_time=1)
            b.line(2)
            box = formula_box(M(r"\frac{d^2y}{dx^2} = \frac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{dx/dt}", 50, ACCUM), ACCUM).next_to(r1, DOWN, buff=0.5)
            self.play(FadeIn(box), run_time=1)
            b.line(3)
            wrong = M(r"\text{not } \frac{d^2y/dt^2}{d^2x/dt^2}", 40, TANGENT).next_to(box, DOWN, buff=0.4)
            self.play(FadeIn(wrong), run_time=0.6)
            self.play(Create(Cross(wrong, stroke_color=TANGENT, scale_factor=0.8)), run_time=0.6)
        self.clear()

        self.example("Concavity at a point", r"For $x = t^2 - 1$, $y = t^3 - 3t$, find $\frac{d^2y}{dx^2}$ and decide the concavity at $t = 2$.",
                     [r"\frac{dy}{dx} = \frac{3t^2 - 3}{2t} = \tfrac32 t - \tfrac32 t^{-1}", r"\frac{d}{dt}\left(\frac{dy}{dx}\right) = \tfrac32 + \tfrac32 t^{-2}", r"\frac{d^2y}{dx^2} = \frac{\tfrac32 + \frac{3}{2t^2}}{2t}",
                      r"= \frac{3t^2 + 3}{4t^3}", r"t = 2: \ \frac{12 + 3}{32} = \frac{15}{32} > 0: \ \text{concave up}", r"TEXT:The wrong shortcut gives $\frac{6t}{2} = 3t = 6$."],
                     at=[1, 2, 3, 4, 5, 6])

        with self.beat("Where is it concave up?") as b:
            f1 = M(r"\frac{d^2y}{dx^2} = \frac{3t^2 + 3}{4t^3}", 46).to_edge(UP, buff=0.6)
            self.play(Write(f1), FadeIn(T("top always positive: the sign follows $t^3$", 30, DIM).next_to(f1, DOWN, buff=0.3)), run_time=1.2)
            ch = sign_chart(["0"], ["-", "+"], name=r"\tfrac{d^2y}{dx^2}", width=6, words=["hill", "bowl"]).shift(DOWN * 0.2)
            self.play(FadeIn(ch), run_time=1)
            b.line(1)
            ax, _ = plot_axes([-1.6, 3.6, 1], [-2.8, 2.8, 1], w=3, h=2.8, coords=False)
            ax.to_edge(DOWN, buff=0.2)
            self.play(FadeIn(ax), Create(param_curve(ax, X, Y, -2.1, -0.02, color=TANGENT)), Create(param_curve(ax, X, Y, 0.02, 2.1, color=DERIV)), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(formula_box(M(r"\frac{d^2y}{dx^2} = \frac{\frac{d}{dt}\left(\frac{dy}{dx}\right)}{dx/dt}", 48, ACCUM), ACCUM), M(r"\text{not } \frac{d^2y}{dt^2} \div \frac{d^2x}{dt^2}", 38, TANGENT),
                          T("sign of $\\frac{d^2y}{dx^2}$: concavity", 36)).arrange(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2)
        self.clear()

        self.examples_card()
        self.example("Example 1: The circle again", r"For $x = \cos t$, $y = \sin t$, find $\frac{d^2y}{dx^2}$ at $t = \frac\pi4$.",
                     [r"\frac{dy}{dx} = -\cot t", r"\frac{d}{dt}(-\cot t) = \csc^2 t", r"\frac{d^2y}{dx^2} = \frac{\csc^2 t}{-\sin t} = -\csc^3 t", r"t = \tfrac\pi4: \ -\left(\sqrt2\right)^3 = -2\sqrt2 < 0: \ \text{concave down}"],
                     at=[1, 1, 2, 3])
        self.example("Example 2: Always concave up", r"For $x = e^t$, $y = e^{-t}$, find $\frac{d^2y}{dx^2}$.",
                     [r"\frac{dy}{dx} = \frac{-e^{-t}}{e^t} = -e^{-2t}", r"\frac{d}{dt}\left(-e^{-2t}\right) = 2e^{-2t}", r"\frac{d^2y}{dx^2} = \frac{2e^{-2t}}{e^t} = 2e^{-3t} > 0", r"TEXT:Concave up everywhere (this is $y = \frac1x$, $x > 0$)."],
                     at=[1, 2, 2, 3])
        ch3 = staged_chart(["1"], ["-", "+"], name=r"\tfrac{d^2y}{dx^2}", width=5, words=["hill", "bowl"])
        self.example("Example 3: An interval of concavity", r"For $x = t + 1$, $y = t^3 - 3t^2$, for which $t$ is the curve concave up?",
                     [r"\frac{dy}{dx} = \frac{3t^2 - 6t}{1} = 3t^2 - 6t", r"\frac{d}{dt}\left(\frac{dy}{dx}\right) = 6t - 6", r"\frac{d^2y}{dx^2} = \frac{6t - 6}{1} = 6t - 6", r"\text{concave up for } t > 1"],
                     at=[1, 2, 2, 3], figure=ch3, figure_at=3, cues={3: lambda sc: (reveal_sign(ch3, 0, 1)(sc), reveal_words(ch3)(sc))})
        self.finish()
