"""Topic 0.5: Trigonometric identities. Narration comes from transcripts/0_5.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def two_graphs(w=10, h=3.2):
    """sin^2 x solid and (1 - cos 2x)/2 dashed on top of it."""
    ax, labs = pi_axes(-1, 2, [-0.3, 1.3, 1], w=w, h=h, yticks=(1,))
    g1 = ax.plot(lambda v: np.sin(v) ** 2, x_range=[-PI, 2 * PI], color=FUNC, stroke_width=7)
    g2 = DashedVMobject(ax.plot(lambda v: (1 - np.cos(2 * v)) / 2, x_range=[-PI, 2 * PI], color=SECANT, stroke_width=4), num_dashes=70)
    return ax, labs, g1, g2


class Lesson(TranscriptScene):
    NUM = "0.5"

    def construct(self):
        with self.beat("Two formulas, one graph") as b:
            ax, labs, g1, g2 = two_graphs()
            VGroup(ax, labs).shift(DOWN * 0.8)
            f1 = M(r"y = \sin^2 x", 44, FUNC).to_corner(UL, buff=0.6)
            f2 = M(r"y = \frac{1 - \cos 2x}{2}", 44, SECANT).to_corner(UR, buff=0.6)
            self.play(FadeIn(ax), FadeIn(labs), Write(f1), run_time=0.8)
            self.play(Create(g1), run_time=1.6)
            self.play(Write(f2), run_time=0.8)
            b.line(1)
            self.play(Create(g2), run_time=1.8)
            self.play(FadeIn(T("different formulas, same function", 34).next_to(ax, DOWN, buff=0.5)), run_time=0.6)
            b.line(2)
            self.play(FadeIn(formula_box(T("identity: true for every input", 36, ACCUM), ACCUM).move_to(UP * 2.2)), run_time=0.8)
        self.clear()
        self.title()

        with self.beat("The Pythagorean identities") as b:
            uc = TrigCircle(r=1.6, center=LEFT * 4.6 + UP * 0.6)
            p = formula_box(M(r"\sin^2\theta + \cos^2\theta = 1", 50, ACCUM), ACCUM).move_to(RIGHT * 1.6 + UP * 2.4)
            self.play(Create(uc), FadeIn(uc.drop(0.8)), FadeIn(uc.ray(0.8)), FadeIn(p), run_time=1)
            b.line(1)
            d1 = VGroup(M(r"\frac{\sin^2\theta}{\cos^2\theta} + \frac{\cos^2\theta}{\cos^2\theta} = \frac{1}{\cos^2\theta}", 40), M(r"\tan^2\theta + 1 = \sec^2\theta", 46, TANGENT)).arrange(DOWN, buff=0.3)
            d1.next_to(p, DOWN, buff=0.5)
            self.play(FadeIn(M(r"\div \cos^2\theta", 32, DIM).next_to(d1[0], LEFT, buff=0.4)), Write(d1[0]), run_time=1.2)
            self.play(Write(d1[1]), run_time=0.8)
            b.line(2)
            d2 = M(r"1 + \cot^2\theta = \csc^2\theta", 46, DERIV).next_to(d1, DOWN, buff=0.5)
            self.play(FadeIn(M(r"\div \sin^2\theta", 32, DIM).next_to(d2, LEFT, buff=0.4)), Write(d2), run_time=1)
            b.line(3)
            self.play(Indicate(p), run_time=1)
        self.clear()

        self.example("Simplifying an expression", r"Simplify $\dfrac{1 - \cos^2 x}{\sin x\cos x}$.",
                     [r"1 - \cos^2 x = \sin^2 x", r"\frac{1 - \cos^2 x}{\sin x\cos x} = \frac{\sin^2 x}{\sin x\cos x}", r"= \frac{\sin x}{\cos x}", r"= \tan x"], at=[1, 2, 3, 4],
                     ref=r"\sin^2 x + \cos^2 x = 1", follow=True)

        with self.beat("Even and odd") as b:
            uc = TrigCircle(r=2.2, center=LEFT * 3.6 + DOWN * 0.2)
            t = 0.7
            self.play(Create(uc), run_time=0.6)
            self.play(Create(uc.ray(t, FUNC)), FadeIn(uc.dot(t)), FadeIn(uc.angle_arc(t, FUNC, label=r"\theta")), Create(uc.ray(-t, TANGENT)), FadeIn(uc.dot(-t, TANGENT)),
                      FadeIn(uc.angle_arc(-t, TANGENT, label=r"-\theta")), run_time=1)
            b.line(1)
            self.play(FadeIn(uc.coord(t, r"(\cos\theta, \sin\theta)", FUNC, 26)), FadeIn(uc.coord(-t, r"(\cos\theta, -\sin\theta)", TANGENT, 26)), run_time=0.8)
            eo = VGroup(M(r"\cos(-\theta) = \cos\theta \quad \text{(even)}", 38), M(r"\sin(-\theta) = -\sin\theta \quad \text{(odd)}", 38), M(r"\tan(-\theta) = -\tan\theta", 38)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            eo.to_edge(RIGHT, buff=0.5).shift(UP * 1.8)
            self.play(LaggedStart(*[Write(e) for e in eo], lag_ratio=0.4), run_time=1.6)
            b.line(2)
            tri = right_triangle(2.4, 1.6, angle=r"\theta", size=28).next_to(eo, DOWN, buff=0.6).shift(LEFT * 1.2)
            top = tri[0].get_vertices()[2]
            self.play(Create(tri[0]), FadeIn(tri[1:]), FadeIn(M(r"\tfrac{\pi}{2} - \theta", 26, DERIV).move_to(top + DOWN * 0.75 + LEFT * 0.4)), run_time=1)
            co = VGroup(M(r"\sin\left(\tfrac{\pi}{2} - \theta\right) = \cos\theta", 36, DERIV), M(r"\cos\left(\tfrac{\pi}{2} - \theta\right) = \sin\theta", 36, DERIV)).arrange(DOWN, buff=0.2).next_to(tri, RIGHT, buff=0.4)
            self.play(Write(co), run_time=1.2)
        self.clear()

        with self.beat("Sum and difference formulas") as b:
            warn = VGroup(M(r"\sin(a + b) \ne \sin a + \sin b", 44, TANGENT), M(r"a = b = \tfrac{\pi}{2}: \quad \sin\pi = 0, \quad \sin\tfrac{\pi}{2} + \sin\tfrac{\pi}{2} = 2", 36, DIM)).arrange(DOWN, buff=0.3).to_edge(UP, buff=0.6)
            self.play(Write(warn[0]), run_time=0.8)
            self.play(FadeIn(warn[1]), run_time=0.8)
            b.line(1)
            s = formula_box(M(r"\sin(a \pm b) = \sin a\cos b \pm \cos a\sin b", 44, ACCUM), ACCUM).next_to(warn, DOWN, buff=0.6)
            self.play(FadeIn(s), run_time=0.8)
            b.line(2)
            c = formula_box(M(r"\cos(a \pm b) = \cos a\cos b \mp \sin a\sin b", 44, ACCUM), ACCUM).next_to(s, DOWN, buff=0.4)
            self.play(FadeIn(c), run_time=0.8)
            self.play(Indicate(c, color=SECANT, scale_factor=1.05), run_time=0.8)
            b.line(3)
            self.play(FadeIn(M(r"\tfrac{\pi}{12} = \tfrac{\pi}{3} - \tfrac{\pi}{4}", 40, SECANT).next_to(c, DOWN, buff=0.5)), run_time=0.8)
        self.clear()

        with self.beat("Double-angle formulas") as b:
            bd = Board()
            bd.anchor = UP * 3.1
            bd.write(self, r"\text{set } b = a:")
            bd.write(self, r"\sin(a + a) = \sin a\cos a + \cos a\sin a")
            bd.write(self, r"\sin 2a = 2\sin a\cos a", ACCUM)
            b.line(1)
            bd.write(self, r"\cos 2a = \cos^2 a - \sin^2 a", ACCUM)
            b.line(2)
            bd.write(self, r"= \cos^2 a - (1 - \cos^2 a) = 2\cos^2 a - 1", ACCUM)
            bd.write(self, r"= (1 - \sin^2 a) - \sin^2 a = 1 - 2\sin^2 a", ACCUM)
        self.clear()

        with self.beat("Power-reducing formulas") as b:
            left = VGroup(M(r"\cos 2x = 2\cos^2 x - 1", 38), M(r"2\cos^2 x = 1 + \cos 2x", 38), M(r"\cos^2 x = \frac{1 + \cos 2x}{2}", 42, ACCUM)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            right = VGroup(M(r"\cos 2x = 1 - 2\sin^2 x", 38), M(r"2\sin^2 x = 1 - \cos 2x", 38), M(r"\sin^2 x = \frac{1 - \cos 2x}{2}", 42, ACCUM)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            VGroup(left, right).arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.5)
            for m in left:
                self.play(Write(m), run_time=0.8)
            b.line(1)
            for m in right:
                self.play(Write(m), run_time=0.7)
            b.line(2)
            ax, labs, g1, g2 = two_graphs(w=9, h=2.6)
            VGroup(ax, labs).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(ax), FadeIn(labs), Create(g1), run_time=1)
            self.play(Create(g2), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            card = VGroup(M(r"\sin^2\theta + \cos^2\theta = 1, \quad \tan^2\theta + 1 = \sec^2\theta, \quad 1 + \cot^2\theta = \csc^2\theta", 38, ACCUM),
                          M(r"\cos(-\theta) = \cos\theta, \quad \sin(-\theta) = -\sin\theta", 38),
                          M(r"\sin 2a = 2\sin a\cos a", 40, TANGENT), M(r"\cos 2a = \cos^2 a - \sin^2 a = 2\cos^2 a - 1 = 1 - 2\sin^2 a", 38, TANGENT),
                          M(r"\cos^2 x = \frac{1 + \cos 2x}{2}, \quad \sin^2 x = \frac{1 - \cos 2x}{2}", 40, SECANT)).arrange(DOWN, buff=0.4)
            self.play(LaggedStart(*[FadeIn(c) for c in card], lag_ratio=0.4), run_time=2.4)
        self.clear()

        self.examples_card()
        self.example("Example 1: An exact value", r"Find the exact value of $\cos\frac{\pi}{12}$.",
                     [r"\frac{\pi}{12} = \frac{\pi}{3} - \frac{\pi}{4}", r"\cos(a - b) = \cos a\cos b + \sin a\sin b", r"= \cos\tfrac{\pi}{3}\cos\tfrac{\pi}{4} + \sin\tfrac{\pi}{3}\sin\tfrac{\pi}{4}",
                      r"= \tfrac12 \cdot \tfrac{\sqrt2}{2} + \tfrac{\sqrt3}{2} \cdot \tfrac{\sqrt2}{2}", r"= \frac{\sqrt2}{4} + \frac{\sqrt6}{4} = \frac{\sqrt6 + \sqrt2}{4}"], at=[1, 2, 2, 3, 4])
        self.example("Example 2: Verifying an identity", r"Show that $\sec x - \cos x = \sin x\tan x$.",
                     [r"\sec x - \cos x = \frac{1}{\cos x} - \cos x", r"= \frac{1}{\cos x} - \frac{\cos^2 x}{\cos x} = \frac{1 - \cos^2 x}{\cos x}", r"= \frac{\sin^2 x}{\cos x}",
                      r"= \sin x \cdot \frac{\sin x}{\cos x} = \sin x\tan x"], at=[1, 2, 3, 4])
        self.example("Example 3: Double angles from one value", r"$\sin x = \frac35$ and $x$ is in quadrant II. Find $\sin 2x$ and $\cos 2x$.",
                     [r"\cos^2 x = 1 - \frac{9}{25} = \frac{16}{25}", r"\text{quadrant II: } \cos x = -\frac45", r"\sin 2x = 2\sin x\cos x = 2\left(\tfrac35\right)\left(-\tfrac45\right) = -\frac{24}{25}",
                      r"\cos 2x = 1 - 2\sin^2 x = 1 - \frac{18}{25}", r"= \frac{7}{25}"], at=[1, 1, 2, 3, 4])
        self.example("Example 4: Simplifying with double angles", r"Simplify $\dfrac{\sin 2x}{1 + \cos 2x}$.",
                     [r"\sin 2x = 2\sin x\cos x", r"1 + \cos 2x = 1 + (2\cos^2 x - 1) = 2\cos^2 x", r"\frac{\sin 2x}{1 + \cos 2x} = \frac{2\sin x\cos x}{2\cos^2 x}", r"= \frac{\sin x}{\cos x} = \tan x"],
                     at=[1, 2, 3, 4])
        self.finish()
