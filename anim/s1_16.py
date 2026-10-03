"""Topic 1.16: Working with the Intermediate Value Theorem. Narration comes from transcripts/1_16.md."""
import numpy as np
from manim import *

from kit import *
from style import *


def trail(x):
    return 2000 + 3000 * (x / 10) ** 1.3 + 250 * np.sin(1.3 * x)


class Lesson(TranscriptScene):
    NUM = "1.16"

    def construct(self):
        ax, al = plot_axes([0, 10, 2], [1500, 5500, 1000], w=9.6, h=5, xlabel="t", ylabel="\\text{feet}")
        ax.shift(DOWN * 0.3)
        path = ax.plot(trail, x_range=[0, 10], color=FUNC, stroke_width=5)
        line35 = DashedLine(ax.c2p(0, 3500), ax.c2p(10, 3500), color=SECANT)
        with self.beat("A hike up a mountain") as b:
            self.play(FadeIn(ax), FadeIn(al), run_time=0.6)
            hiker = Dot(color=SECANT, radius=0.12)
            alt = always_redraw(lambda: M(f"{int(ax.p2c(hiker.get_center())[1]):,}".replace(",", r"{,}") + r"\text{ ft}", 40, SECANT).to_corner(UR, buff=0.6))
            self.add(alt)
            self.play(Create(path), MoveAlongPath(hiker, path), run_time=3)
            self.play(Create(line35), FadeIn(M(r"3500\text{ ft}", 34, SECANT).next_to(ax.c2p(10, 3500), RIGHT, buff=0.15)), run_time=0.8)
            b.line(1)
            cross = [x for x in np.linspace(0, 10, 2000) if abs(trail(x) - 3500) < 6][0]
            self.play(Flash(ax.c2p(cross, 3500), color=SECANT), run_time=1)
        self.clear()
        self.title()

        a2, al2 = plot_axes([0, 5, 1], [0, 6, 1], w=7.4, h=5, coords=False)
        VGroup(a2, al2).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        g = lambda x: 1 + 0.25 * x ** 2 + 0.6 * np.sin(2 * x)
        with self.beat("The theorem") as b:
            gc = a2.plot(g, x_range=[0.5, 4.5], color=FUNC, stroke_width=5)
            k = 3.2
            self.play(FadeIn(a2), Create(gc), FadeIn(closed_dot(a2, 0.5, g(0.5))), FadeIn(closed_dot(a2, 4.5, g(4.5))), run_time=1.6)
            kl = DashedLine(a2.c2p(0, k), a2.c2p(5, k), color=SECANT)
            self.play(Create(kl), FadeIn(M("k", 36, SECANT).next_to(kl, LEFT)), run_time=0.8)
            c = [x for x in np.linspace(0.5, 4.5, 4000) if abs(g(x) - k) < 0.005][0]
            self.play(FadeIn(Dot(a2.c2p(c, k), color=SECANT)), FadeIn(M("c", 36, SECANT).next_to(a2.c2p(c, 0), DOWN)), run_time=0.8)
            st = T(r"$f$ continuous on $[a, b]$, $k$ between $f(a)$ and $f(b)$ \\ $,\ \text{so}\ $ $f(c) = k$ for some $c$ in $(a, b)$", 34).to_edge(RIGHT, buff=0.5).shift(UP * 1.5)
            self.play(FadeIn(st), run_time=1)
            b.line(1)
            self.play(Indicate(st, color=SECANT, scale_factor=1.02), run_time=1)
            b.line(2)
            every = T(r"every condition matters", 34, TANGENT).next_to(st, DOWN, buff=0.5)
            self.play(FadeIn(every), run_time=0.8)
        self.clear()

        a3, al3 = plot_axes([0, 4, 1], [0, 6, 1], w=7.4, h=5, coords=False)
        a3.shift(DOWN * 0.3)
        with self.beat("Why continuity matters") as b:
            self.play(FadeIn(a3), Create(a3.plot(lambda x: 1 + 0.5 * x, x_range=[0, 2], color=FUNC, stroke_width=5)),
                      Create(a3.plot(lambda x: 4.2 + 0.4 * (x - 2), x_range=[2, 4], color=FUNC, stroke_width=5)), FadeIn(open_dot(a3, 2, 2)), FadeIn(closed_dot(a3, 2, 4.2, FUNC)), run_time=1.6)
            kl = DashedLine(a3.c2p(0, 3), a3.c2p(4, 3), color=SECANT)
            self.play(Create(kl), run_time=0.8)
            self.play(Flash(a3.c2p(2, 3), color=TANGENT), run_time=1)
        self.clear()

        a4, al4 = plot_axes([-0.5, 1.5, 0.5], [-1.5, 2, 0.5], w=7, h=5)
        VGroup(a4, al4).to_edge(LEFT, buff=0.7).shift(DOWN * 0.3)
        p = lambda x: x ** 3 + x - 1
        with self.beat("Finding a root") as b:
            e = M(r"x^3 + x - 1 = 0", 50, FUNC).to_edge(RIGHT, buff=0.7).shift(UP * 2)
            self.play(Write(e), run_time=1)
            b.line(1)
            self.play(FadeIn(a4), FadeIn(al4), Create(a4.plot(p, x_range=[-0.3, 1.3], color=FUNC, stroke_width=5)), run_time=1.4)
            vals = VGroup(M(r"f(0) = -1", 42, TANGENT), M(r"f(1) = 1", 42, DERIV)).arrange(DOWN, aligned_edge=LEFT).next_to(e, DOWN, buff=0.5)
            self.play(FadeIn(closed_dot(a4, 0, -1, TANGENT)), FadeIn(closed_dot(a4, 1, 1, DERIV)), Write(vals), run_time=1.2)
            b.line(2)
            root = 0.6823
            self.play(Flash(a4.c2p(root, 0), color=SECANT), FadeIn(T(r"a root in $(0, 1)$", 40, SECANT).next_to(vals, DOWN, buff=0.4)), run_time=1)
        self.clear()
        self.example("A root exists", r"Show that $x^3 + x - 1 = 0$ has a solution between $x = 0$ and $x = 1$.",
                     [r"f(x) = x^3 + x - 1 \text{ is a polynomial: continuous on } [0, 1]", r"f(0) = -1 < 0 < 1 = f(1)", r"\text{IVT: } f(c) = 0 \text{ for some } c \text{ in } (0, 1)"], at=[1, 2, 3])
        self.example("A given value", r"Show that $\cos x = x$ for some $x$ in $\left[0, \dfrac\pi2\right]$.",
                     [r"g(x) = \cos x - x \text{ is continuous on } \left[0, \tfrac\pi2\right]", r"g(0) = 1 > 0, \quad g\left(\tfrac\pi2\right) = -\tfrac\pi2 < 0", r"\text{IVT: } g(c) = 0, \text{ so } \cos c = c"], at=[1, 2, 3])

        with self.beat("Reading a table") as b:
            tb = table(["x", "1", "3", "4", "7"], [["g(x)", "5", "-2", "1", "6"]], size=48).shift(UP * 0.6)
            self.play(FadeIn(tb), run_time=1)
            b.line(1)
            for k, (c1, c2) in enumerate([(1, 2), (2, 3)]):
                br = Brace(VGroup(tb.cells[1][c1], tb.cells[1][c2]), DOWN, color=SECANT).shift(DOWN * 0.7 * k)   # staggered: the pairs share a column
                self.play(GrowFromCenter(br), FadeIn(T("sign change", 30, SECANT).next_to(br, DOWN)), run_time=0.8)
            res = T("at least two zeros", 44).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(res), run_time=0.8)
        self.clear()

        with self.beat("Writing the justification") as b:
            parts = VGroup(T(r"Since $g$ is \textbf{continuous on $[1, 3]$}", 40), T(r"and \textbf{$g(1) > 0 > g(3)$},", 40),
                           T(r"by the \textbf{Intermediate Value Theorem}", 40), T(r"there is a $c$ in $(1, 3)$ with $g(c) = 0$.", 40)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            for m in parts:
                self.play(FadeIn(m, shift=RIGHT * 0.2), run_time=0.9)
            b.line(1)
            banner = callout(r"On the AP exam: expect an IVT or MVT justification.", SECANT, 34).next_to(parts, DOWN, buff=0.6)
            self.play(FadeIn(banner, shift=UP * 0.2), run_time=0.9)
        self.clear()

        tbj = table(["x", "1", "3", "4", "7"], [["g(x)", "5", "-2", "1", "6"]], size=40)
        self.example("Justify with the IVT", VGroup(T(r"$g$ is continuous. Must there be a value $c$ in $(1, 3)$ with $g(c) = 0$? Justify your answer.", 38), tbj).arrange(DOWN, buff=0.35),
                     [r"TEXT:$g$ is continuous on $[1, 3]$.",
                      r"TEXT:$g(1) = 5 > 0$ and $g(3) = -2 < 0$, so $0$ is between $g(3)$ and $g(1)$.",
                      r"TEXT:Therefore, by the Intermediate Value Theorem, there is a value $c$ in $(1, 3)$ with $g(c) = 0$."], at=[1, 2, 3],
                     text=r"$g$ is continuous, with values in the table above. Must there be a value $c$ in $(1, 3)$ with $g(c) = 0$? Justify your answer.")

        with self.beat("Close") as b:
            ax, al = plot_axes([0, 10, 2], [1500, 5500, 1000], w=9.6, h=5, coords=False)
            ax.shift(DOWN * 0.3)
            self.play(FadeIn(ax), Create(ax.plot(trail, x_range=[0, 10], color=FUNC, stroke_width=5)), Create(DashedLine(ax.c2p(0, 3500), ax.c2p(10, 3500), color=SECANT)),
                      FadeIn(Dot(ax.c2p(10, trail(10)), color=SECANT, radius=0.12)), run_time=1.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: A root in an interval", r"Show that $x^4 - 2x - 5 = 0$ has a solution between $x = 1$ and $x = 2$.",
                     [r"f(x) = x^4 - 2x - 5 \text{ is continuous on } [1, 2]", r"f(1) = -6,\quad f(2) = 7", r"TEXT:Since $f$ is continuous on $[1, 2]$ and $-6 < 0 < 7$, by the Intermediate Value Theorem $f(c) = 0$ for some $c$ in $(1, 2)$."],
                     at=[1, 2, 3])
        tbh = table(["x", "0", "2", "5", "8"], [["h(x)", "3", "-1", "4", "2"]], size=40)
        self.example("Example 2: Counting from a table", VGroup(T(r"$h$ is continuous. Least number of solutions of $h(x) = 1$ on $[0, 8]$?", 40), tbh).arrange(DOWN, buff=0.35),
                     [r"[0, 2]:\ 3 \to -1 \ \checkmark", r"[2, 5]:\ -1 \to 4 \ \checkmark", r"[5, 8]:\ 4 \to 2 \ \text{(no promise)}", r"\text{at least } 2"], at=[1, 2, 3, 4],
                     text=r"$h$ is continuous. What is the least number of solutions of $h(x) = 1$ on $[0, 8]$? \[ \begin{array}{c|cccc} x & 0 & 2 & 5 & 8 \\ \hline h(x) & 3 & -1 & 4 & 2 \end{array} \]")
        a5, _ = plot_axes([0, 2, 1], [-4, 4, 2], w=4.6, h=4)
        fig5 = VGroup(a5, a5.plot(lambda x: 1 / (x - 1), x_range=[0, 0.78], color=FUNC), a5.plot(lambda x: 1 / (x - 1), x_range=[1.25, 2], color=FUNC), asymptote(a5, 1, [-4, 4]))
        self.example("Example 3: When the theorem doesn't apply", r"$f(x) = \dfrac{1}{x - 1}$: \ $f(0) = -1$, $f(2) = 1$. Must $f(c) = 0$ in $(0, 2)$?",
                     [r"\text{continuous on } [0, 2]?", r"\text{No: asymptote at } x = 1", r"\text{the IVT doesn't apply; } \frac{1}{x - 1} \ne 0"], figure=fig5, at=[1, 2, 3])
        self.finish()
