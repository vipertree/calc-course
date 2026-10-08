"""Topic 3.3: Differentiating inverse functions. Narration comes from transcripts/3_3.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def f(x):
    return x * x / 2 + x          # f(2) = 4, f'(2) = 3


class Lesson(TranscriptScene):
    NUM = "3.3"

    def mirror_axes(self):
        ax, al = plot_axes([0, 6, 1], [0, 6, 1], w=5.6, h=5.6)
        VGroup(ax, al).to_edge(LEFT, buff=1.2).shift(DOWN * 0.2)
        flip = lambda p: ax.c2p(*ax.p2c(p)[::-1])
        return ax, al, flip

    def find_x(self, tab, row):
        """'What x gives this g value?': light up the value in the g(x) column, then the x in its row, with an arrow between."""
        val, xc = tab.cells[row][1], tab.cells[row][0]
        self.play(Circumscribe(val, color=SECANT), val.animate.set_color(SECANT), run_time=1.0)
        self.play(GrowArrow(Arrow(val.get_left(), xc.get_right(), buff=0.08, color=SECANT, stroke_width=4, max_tip_length_to_length_ratio=0.3)),
                  xc.animate.set_color(SECANT), Circumscribe(xc, color=SECANT), run_time=1.0)

    def construct(self):
        with self.beat("Undoing a function") as b:
            box = lambda name, col: VGroup(RoundedRectangle(width=2, height=1.2, corner_radius=0.15, color=col), M(name, 44, col))
            r1 = VGroup(M("1", 48), box("f", FUNC), M("2", 48)).arrange(RIGHT, buff=0.8).shift(UP * 0.9)
            r2 = VGroup(M("2", 48), box(r"g = f^{-1}", DERIV), M("1", 48)).arrange(RIGHT, buff=0.8).shift(DOWN * 0.9)
            r2[1][0].stretch_to_fit_width(2.8)
            r2.arrange(RIGHT, buff=0.8).shift(DOWN * 0.9)
            for r in (r1, r2):
                r.add(Arrow(r[0].get_right(), r[1].get_left(), buff=0.1, color=DIM), Arrow(r[1].get_right(), r[2].get_left(), buff=0.1, color=DIM))
            self.play(FadeIn(r1), run_time=0.8)
            b.line(1)
            rev = T(r"algebraic reverse: undo each step, in the opposite order", 34, DIM).to_edge(UP, buff=0.5)
            self.play(FadeIn(rev), run_time=0.8)
            b.line(2)
            defn = formula_box(T(r"$g$ is the inverse of $f$: \quad $f(a) = b$ means $g(b) = a$", 40), DERIV).to_edge(UP, buff=0.4)
            self.play(FadeOut(rev), FadeIn(defn), run_time=1)
            b.line(3)
            io = T(r"inputs become outputs, outputs become inputs", 34, SECANT).next_to(defn, DOWN, buff=0.35)
            self.play(FadeIn(io), run_time=0.8)
            b.line(4)
            self.play(FadeIn(r2), run_time=0.8)
            b.line(5)
            pts = M(r"(1, 2) \ \longleftrightarrow\ (2, 1)", 50, SECANT).next_to(r2, DOWN, buff=0.7)
            self.play(Write(pts), run_time=1)
        self.clear()
        self.title()

        with self.beat("Three ways to say inverse") as b:
            head = T(r"How a problem tells you $g$ is the inverse of $f$", 44).to_edge(UP, buff=0.7)
            self.play(FadeIn(head), run_time=0.8)
            cues = VGroup(T(r"(a) It says so: ``$g$ is the inverse of $f$'' (or $g = f^{-1}$).", 38),
                          T(r"(b) For every $a$ and $b$, $f(a) = b$ means $g(b) = a$.", 38),
                          T(r"(c) $f\big(g(x)\big) = x$ for every $x$.", 38)).arrange(DOWN, buff=0.6, aligned_edge=LEFT).next_to(head, DOWN, buff=0.8)
            for k, c in enumerate(cues):
                b.line(k + 1)
                self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.8)
        self.clear()

        ax, al, flip = self.mirror_axes()
        cf = ax.plot(f, x_range=[0, 2.6], color=FUNC, stroke_width=5)
        ci = cf.copy().apply_function(flip).set_color(DERIV)
        diag = DashedLine(ax.c2p(0, 0), ax.c2p(6, 6), color=DIM)
        with self.beat("The mirror") as b:
            self.play(FadeIn(ax), FadeIn(al), Create(cf), Create(diag), FadeIn(M("y = x", 30, DIM).next_to(ax.c2p(6, 6), UR, buff=0.05)), run_time=1.4)
            p = closed_dot(ax, 2, 4, FUNC)
            self.play(FadeIn(p), FadeIn(M("(a, b)", 32, FUNC).next_to(p, LEFT, buff=0.15)), run_time=0.6)
            self.play(TransformFromCopy(cf, ci), TransformFromCopy(p, closed_dot(ax, 4, 2, DERIV)), run_time=1.6)
            self.play(FadeIn(M("(b, a)", 32, DERIV).next_to(ax.c2p(4, 2), DR, buff=0.1)), run_time=0.5)
            b.line(1)
            self.play(FadeIn(VGroup(M("f", 36, FUNC).next_to(ax.c2p(2.6, f(2.6)), RIGHT), M("f^{-1}", 36, DERIV).next_to(ax.c2p(6, 2.6), DOWN))), run_time=0.6)
        with self.beat("Rise and run trade places") as b:
            t1 = tangent_line(ax, f, 2, 3, [1.3, 2.6])
            tri = VGroup(Line(ax.c2p(2, 4), ax.c2p(2.5, 4), color=SECANT, stroke_width=5), Line(ax.c2p(2.5, 4), ax.c2p(2.5, 5.5), color=SECANT, stroke_width=5))
            self.play(Create(t1), run_time=0.8)
            b.line(1)
            l1 = VGroup(M("1", 30, SECANT).next_to(tri[0], DOWN, buff=0.08), M("3", 30, SECANT).next_to(tri[1], RIGHT, buff=0.08))
            self.play(Create(tri), FadeIn(l1), run_time=1)
            note = M(r"\text{slope } 3", 44, FUNC).to_edge(RIGHT, buff=1.2).shift(UP * 1.6)
            self.play(FadeIn(note), run_time=0.5)
            b.line(2)
            t2 = t1.copy().apply_function(flip).set_color(TANGENT)
            tri2 = tri.copy().apply_function(flip)
            self.play(TransformFromCopy(t1, t2), TransformFromCopy(tri, tri2), run_time=1.6)
            l2 = VGroup(M("3", 30, SECANT).next_to(tri2[0], RIGHT, buff=0.08), M("1", 30, SECANT).next_to(tri2[1], DOWN, buff=0.08))
            self.play(FadeIn(l2), run_time=0.6)
            b.line(3)
            note2 = M(r"\text{slope } \tfrac13", 44, DERIV).next_to(note, DOWN, buff=0.5)
            self.play(FadeIn(note2), run_time=0.6)
        with self.beat("The formula") as b:
            self.play(FadeOut(note), FadeOut(note2), run_time=0.4)
            rule = formula_box(M(r"\text{if } f(a) = b, \text{ then } \big(f^{-1}\big)'(b) = \frac{1}{f'(a)}", 40), DERIV).to_edge(RIGHT, buff=0.4).shift(UP * 1.4)
            self.play(FadeIn(rule), run_time=1)
            b.line(1)
            self.play(Flash(ax.c2p(2, 4), color=FUNC), Flash(ax.c2p(4, 2), color=DERIV), run_time=1)
        self.clear()

        with self.beat("An example without the inverse") as b:
            head = M(r"f(x) = x^3 + x, \qquad \big(f^{-1}\big)'(2) = \ ?", 52).to_edge(UP, buff=0.6)
            self.play(Write(head), run_time=1.2)
            board = Board()
            board.anchor = head.get_bottom() + DOWN * 0.5
            b.line(1)
            board.write(self, r"a^3 + a = 2")
            b.line(2)
            board.write(self, r"a = 1")
            b.line(3)
            board.write(self, r"f'(x) = 3x^2 + 1, \quad f'(1) = 4")
            board.write(self, r"\big(f^{-1}\big)'(2) = \frac{1}{f'(1)} = \frac14", color=DERIV)
        self.clear()

        with self.beat("The trap") as b:
            wrong = M(r"\frac{1}{f'(2)} = \frac{1}{13}", 56, TANGENT).shift(UP * 1.8)
            self.play(Write(wrong), run_time=1)
            self.play(Create(Cross(wrong, stroke_color=TANGENT, scale_factor=0.8)), run_time=0.6)
            b.line(1)
            lines = VGroup(NumberLine(x_range=[0, 3, 1], length=6, color=DIM, include_numbers=True, font_size=28),
                           NumberLine(x_range=[0, 3, 1], length=6, color=DIM, include_numbers=True, font_size=28)).arrange(DOWN, buff=1.4).shift(DOWN * 1.2)
            labs = VGroup(T(r"inputs of $f^{-1}$ (outputs of $f$)", 28, DIM).next_to(lines[0], UP, buff=0.2), T(r"inputs of $f$", 28, DIM).next_to(lines[1], DOWN, buff=0.4))
            self.play(FadeIn(lines), FadeIn(labs), run_time=0.8)
            self.play(GrowArrow(Arrow(lines[0].n2p(2), lines[1].n2p(1), color=DERIV, buff=0.1)), FadeIn(Dot(lines[0].n2p(2), color=DERIV)), FadeIn(Dot(lines[1].n2p(1), color=DERIV)), run_time=1)
        self.clear()
        self.example_ref = r"f(a) = b:\ \ \big(f^{-1}\big)'(b) = \frac{1}{f'(a)}"
        gtab = table(["x", "g(x)", "g'(x)"], [["1", "4", "3"], ["4", "6", r"\tfrac12"]], size=38)
        self.example("From a table", r"$g$ is invertible. Use the table to find $\left(g^{-1}\right)'(4)$.",
                     [r"TEXT:Cue: the problem names $g^{-1}$ outright.", r"TEXT:$\left(g^{-1}\right)'(4)$ needs $g^{-1}(4)$: what $x$ gives $g(x) = 4$?",
                      r"g(1) = 4, \ \text{so } g^{-1}(4) = 1", r"\left(g^{-1}\right)'(4) = \frac{1}{g'(1)} = \frac13",
                      r"TEXT:Not $\frac{1}{g'(4)}$: the $4$ is an output of $g$."], at=[1, 2, 3, 4, 5], figure=gtab,
                     cues={2: lambda sc: self.find_x(gtab, 1)}, follow=True)

        with self.beat("Implicit differentiation agrees") as b:
            board = Board()
            board.anchor = UP * 2.8
            board.write(self, r"y = f^{-1}(x), \ \text{so } f(y) = x")
            b.line(1)
            board.write(self, r"f'(y)\,\frac{dy}{dx} = 1")
            b.line(2)
            board.write(self, r"\frac{dy}{dx} = \frac{1}{f'(y)}", color=DERIV)
        self.clear()
        self.example("The natural log, again", r"Use $\ln x$ as the inverse of $e^x$ to find $\dfrac{d}{dx}\ln x$.",
                     [r"y = \ln x, \ \text{so } e^y = x", r"e^y\,\frac{dy}{dx} = 1", r"\frac{dy}{dx} = \frac{1}{e^y} = \frac{1}{x}"], at=[1, 2, 3], ref="")

        with self.beat("Close") as b:
            ax, al, flip = self.mirror_axes()
            cf = ax.plot(f, x_range=[0, 2.6], color=FUNC, stroke_width=5)
            t1 = tangent_line(ax, f, 2, 3, [1.3, 2.6])
            tri = VGroup(Line(ax.c2p(2, 4), ax.c2p(2.5, 4), color=SECANT, stroke_width=5), Line(ax.c2p(2.5, 4), ax.c2p(2.5, 5.5), color=SECANT, stroke_width=5))
            grp = VGroup(ax, cf, t1, tri, DashedLine(ax.c2p(0, 0), ax.c2p(6, 6), color=DIM))
            mir = VGroup(cf, t1, tri).copy().apply_function(flip).set_color(DERIV)
            self.play(FadeIn(grp), FadeIn(mir), run_time=1.4)
        self.clear()

        self.examples_card()
        self.example("Example 1: From given values", r"$f\big(g(x)\big) = x$ for every $x$. $f(2) = 5$ and $f'(2) = -4$. Find $g'(5)$.",
                     [r"TEXT:Cue: $f\big(g(x)\big) = x$, so $g$ is the inverse of $f$.", r"f(2) = 5, \ \text{so } g(5) = 2", r"g'(5) = \frac{1}{f'(2)} = -\frac14"], at=[1, 2, 3])
        tb = table(["x", "g(x)", "g'(x)"], [["1", "3", "4"], ["3", "7", "2"]], size=40)
        self.example("Example 2: A table with a distractor",
                     VGroup(T(r"For every $a$ and $b$, $g(a) = b$ means $h(b) = a$. Find $h'(3)$.", 40), tb).arrange(DOWN, buff=0.3),
                     [r"TEXT:Cue: $g(a) = b$ means $h(b) = a$, so $h$ is the inverse of $g$.", r"TEXT:$h'(3)$ needs $h(3)$: what $x$ gives $g(x) = 3$?",
                      r"g(1) = 3, \ \text{so } h(3) = 1", r"h'(3) = \frac{1}{g'(1)} = \frac14", r"TEXT:$g'(3)$ is a distractor: that $3$ is an input of $g$."],
                     at=[1, 2, 3, 4, 5], cues={2: lambda sc: self.find_x(tb, 1),
                                               4: lambda sc: sc.play(Indicate(tb.cells[2][2], color=TANGENT, scale_factor=1.4), run_time=0.8)},
                     text=r"For every $a$ and $b$, $g(a) = b$ means $h(b) = a$. Find $h'(3)$. \[ \begin{array}{c|cc} x & g(x) & g'(x) \\ \hline 1 & 3 & 4 \\ 3 & 7 & 2 \end{array} \]")
        a3, _ = plot_axes([0, 4, 1], [0, 2, 1], w=5.4, h=3.6)
        gs = np.linspace(-0.2, 1.3, 120)
        fig = VGroup(a3, VMobject(color=DERIV, stroke_width=4).set_points_smoothly([a3.c2p(t ** 3 + t + 1, t) for t in gs if 0 <= t ** 3 + t + 1 <= 4]),
                     a3.plot(lambda x: 1 + (x - 3) / 4, x_range=[0.5, 4], color=TANGENT, stroke_width=4), closed_dot(a3, 3, 1, INK))
        self.example("Example 3: A tangent line to an inverse", r"$g$ is the inverse of $f(x) = x^3 + x + 1$. Find the equation for the line tangent to $g$ at $x = 3$.",
                     [r"TEXT:Cue: it says $g$ is the inverse of $f$ outright.", r"f(1) = 3, \ \text{so } g(3) = 1", r"f'(1) = 4, \ \text{so } g'(3) = \frac14",
                      r"y - 1 = \frac14(x - 3)"], figure=fig, at=[1, 2, 3, 4])
        self.finish()
