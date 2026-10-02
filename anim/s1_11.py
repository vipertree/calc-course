"""Topic 1.11: Defining continuity at a point. Narration comes from transcripts/1_11.md."""
import numpy as np
from manim import *

from kit import *
from style import *

CONDS = [r"1. \ $f(c)$ is defined", r"2. \ $\displaystyle\lim_{x\to c} f(x)$ exists", r"3. \ $\displaystyle\lim_{x\to c} f(x) = f(c)$"]


def checklist(size=40):
    rows = VGroup()
    for c in CONDS:
        boxm = Square(side_length=0.45, color=INK, stroke_width=3)
        rows.add(VGroup(boxm, T(c, size)).arrange(RIGHT, buff=0.3))
    return rows.arrange(DOWN, buff=0.45, aligned_edge=LEFT)


def tick(boxm, ok=True):
    if ok:
        return Text("✓", color=DERIV, font_size=40).move_to(boxm)
    return Text("✗", color=TANGENT, font_size=40).move_to(boxm)


class Lesson(TranscriptScene):
    NUM = "1.11"

    def construct(self):
        with self.beat("From pencils to precision") as b:
            # three graphs, drawn faint: one continuous, one with a hole, one with a jump (Adder: show the test, then
            # say plainly that it is a quick check, not the definition)
            kinds = ["continuous", "hole", "jump"]
            panels, paths = VGroup(), []
            for kind in kinds:
                a_, _ = plot_axes([0, 2, 1], [0, 3, 1], w=3.4, h=2.5, coords=False)
                if kind == "continuous":
                    segs = [a_.plot(lambda x: 1.2 + 0.6 * np.sin(2.2 * x), x_range=[0, 2])]
                    extra = VGroup()
                elif kind == "hole":
                    segs = [a_.plot(lambda x: 0.6 + 0.9 * x, x_range=[0, 0.96]), a_.plot(lambda x: 0.6 + 0.9 * x, x_range=[1.04, 2])]
                    extra = VGroup(open_dot(a_, 1, 1.5))
                else:
                    segs = [a_.plot(lambda x: 0.7 + 0.2 * x, x_range=[0, 1]), a_.plot(lambda x: 2.0 + 0.3 * (x - 1), x_range=[1, 2])]
                    extra = VGroup(open_dot(a_, 1, 0.9), closed_dot(a_, 1, 2.0, FUNC))
                faint = VGroup(*[sg.copy().set_stroke(DIM, width=3, opacity=0.6) for sg in segs])
                panels.add(VGroup(a_, faint, extra))
                paths.append(list(faint))          # trace the copies that are on the panels (they move with them)
            panels.arrange(RIGHT, buff=0.7).shift(UP * 0.4)
            heads = VGroup(*[T(k, 30, DIM).next_to(pn, UP, buff=0.2) for k, pn in zip(kinds, panels)])
            q = T("Can you trace it without lifting your pencil?", 38).to_edge(UP, buff=0.4)
            self.play(FadeIn(q), FadeIn(panels), FadeIn(heads), run_time=1.4)
            pen = pencil_prop(1.4)
            b.line(1)
            trace_with_pencil(self, pen, paths[0][0], run_time=2)
            ok = T(r"no lift: continuous", 30, DERIV).next_to(panels[0], DOWN, buff=0.3)
            self.play(FadeIn(ok), run_time=0.5)
            b.line(2)
            for k in (1, 2):
                first, second = paths[k]
                trace_with_pencil(self, pen, first, run_time=1.2)
                # the pencil has to come off the page to get past the break
                self.play(pen.animate.shift(UP * 0.45), run_time=0.35)
                self.play(pen.animate.shift(second.get_start() - pen.tip() + UP * 0.45), run_time=0.45)
                self.play(pen.animate.shift(DOWN * 0.45), run_time=0.3)
                trace_with_pencil(self, pen, second, run_time=1.0)
                self.play(FadeIn(T("lift!", 30, TANGENT).next_to(panels[k], DOWN, buff=0.3)), run_time=0.5)
            self.play(FadeOut(pen), run_time=0.4)
            b.line(3)
            note = T(r"a quick picture, \emph{not} a formal definition", 34, SECANT).to_edge(DOWN, buff=0.4)
            self.play(FadeIn(note), run_time=0.8)
            b.line(4)
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            boxes = VGroup(*[Square(side_length=0.6, color=INK, stroke_width=3) for _ in range(3)]).arrange(RIGHT, buff=0.8)
            self.play(LaggedStart(*[Create(bx) for bx in boxes], lag_ratio=0.3), run_time=1.4)
        self.clear()
        self.title()

        cl = checklist().to_edge(LEFT, buff=0.8).shift(UP * 1.2)
        with self.beat("The three conditions") as b:
            self.play(*[Create(r[0]) for r in cl], run_time=0.8)
            for i in range(3):
                b.line(i + 1)
                self.play(Write(cl[i][1]), run_time=1.2)
        with self.beat("Each discontinuity fails a condition") as b:
            minis = VGroup()
            for kind in ("hole", "moved", "jump", "asym"):
                a, _ = plot_axes([0, 2, 1], [0, 3, 1], w=2.4, h=1.8, coords=False)
                if kind in ("hole", "moved"):
                    g = VGroup(a.plot(lambda x: 1 + 0.5 * x, x_range=[0, 2], color=FUNC), open_dot(a, 1, 1.5))
                    if kind == "moved":
                        g.add(closed_dot(a, 1, 2.6, SECANT))
                elif kind == "jump":
                    g = VGroup(a.plot(lambda x: 0.8, x_range=[0, 1], color=FUNC), a.plot(lambda x: 2.2, x_range=[1, 2], color=FUNC), open_dot(a, 1, 0.8), closed_dot(a, 1, 2.2, FUNC))
                else:
                    g = VGroup(a.plot(lambda x: 1.5 + 0.2 / (1 - x), x_range=[0, 0.93], color=FUNC), a.plot(lambda x: 1.5 + 0.2 / (1 - x), x_range=[1.07, 2], color=FUNC), asymptote(a, 1, [0, 3]))
                minis.add(VGroup(a, g))
            minis.arrange(RIGHT, buff=0.4).to_edge(DOWN, buff=0.4)
            fails = ["fails 1", "fails 3", "fails 2", "fails 2"]
            self.play(FadeIn(minis), run_time=1)
            for i, k in enumerate([0, 1, 2, 3]):
                if i in (0, 2):
                    b.line(1 if i == 0 else 2)
                self.play(FadeIn(T(fails[k], 30, TANGENT).next_to(minis[k], UP, buff=0.1)), run_time=0.6)
        self.clear()

        with self.beat("A justification, written out") as b:
            pw = M(r"f(x) = \begin{cases} x^2 + 1, & x < 2 \\ 4x - 3, & x \ge 2 \end{cases}", 44).to_edge(UP, buff=0.5)
            self.play(Write(pw), run_time=1.2)
            bd = Board().next_to(pw, DOWN, buff=0.5)
            bd.write(self, r"1.\ \ f(2) = 4(2) - 3 = 5")
            b.line(1)
            bd.write(self, r"2.\ \ \lim_{x\to2^-}(x^2 + 1) = 5,\ \ \lim_{x\to2^+}(4x - 3) = 5,\ \text{so } \lim_{x\to2} f(x) = 5")
            b.line(2)
            bd.write(self, r"3.\ \ \lim_{x\to2} f(x) = 5 = f(2) \ \Rightarrow\ f \text{ is continuous at } x = 2", SECANT)
        self.clear()
        self.example("Justify continuity", r"Let $f(x) = \begin{cases} x^2 + 1, & x < 2 \\ 4x - 3, & x \ge 2 \end{cases}$. Is $f$ continuous at $x = 2$? Justify using the definition.",
                     [r"f(2) = 4(2) - 3 = 5", r"\lim_{x\to2^-}(x^2 + 1) = 5, \quad \lim_{x\to2^+}(4x - 3) = 5 \ \Rightarrow\ \lim_{x\to2} f(x) = 5", r"\lim_{x\to2} f(x) = f(2): \ f \text{ is continuous at } x = 2"], at=[1, 2, 3])
        self.example("Justify discontinuity", r"Let $g(x) = \begin{cases} \dfrac{x^2 - 9}{x - 3}, & x \ne 3 \\ 5, & x = 3 \end{cases}$. Is $g$ continuous at $x = 3$?",
                     [r"g(3) = 5", r"x \ne 3: \ g(x) = \frac{\cancel{(x - 3)}(x + 3)}{\cancel{x - 3}} = x + 3", r"\lim_{x\to3} g(x) = 6 \ne 5 = g(3)", r"g \text{ is not continuous at } x = 3"], at=[1, 2, 3, 3])

        a, al = plot_axes([-1, 4, 1], [-1, 3, 1], w=7, h=4.6)
        VGroup(a, al).shift(DOWN * 0.3)
        with self.beat("One-sided continuity") as b:
            self.play(FadeIn(a), FadeIn(al), Create(a.plot(np.sqrt, x_range=[0, 4], color=FUNC, stroke_width=5)), FadeIn(closed_dot(a, 0, 0, FUNC)), run_time=1.4)
            arr = Arrow(a.c2p(1.6, 0.4), a.c2p(0.15, 0.05), color=SECANT, buff=0)
            self.play(GrowArrow(arr), run_time=0.8)
            b.line(1)
            st = M(r"\lim_{x\to0^+}\sqrt x = 0 = \sqrt0", 46, SECANT).to_corner(UR, buff=0.6)
            self.play(Write(st), run_time=1.2)
        self.clear()

        with self.beat("Close") as b:
            cl2 = checklist(44).shift(UP * 0.6)
            self.play(FadeIn(cl2), run_time=1)
            self.play(Circumscribe(cl2[2], color=SECANT), run_time=1.4)
            phrase = T(r"the limit equals the function value", 44, SECANT).next_to(cl2, DOWN, buff=0.7)
            self.play(FadeIn(phrase, shift=UP * 0.2), run_time=0.8)
        self.clear()

        self.examples_card()
        self.example("Example 1: Is it continuous?", r"Is $f$ continuous at $x = 3$? \[ f(x) = \begin{cases} x^2 - 2, & x < 3 \\ 2x + 1, & x \ge 3 \end{cases} \]",
                     [r"1.\ \ f(3) = 2(3) + 1 = 7\ \checkmark",
                      r"2.\ \ \lim_{x\to3^-} f(x) = \lim_{x\to3^-}(x^2 - 2) = 7, \quad \lim_{x\to3^+} f(x) = \lim_{x\to3^+}(2x + 1) = 7\ \checkmark",
                      r"3.\ \ \lim_{x\to3} f(x) = 7 = f(3)\ \checkmark \ \Rightarrow\ \text{continuous}"],
                     at=[1, 2, 3])
        self.example("Example 2: Which condition fails?", r"Is $g$ continuous at $x = 4$? \[ g(x) = \begin{cases} \dfrac{x^2 - 16}{x - 4}, & x \ne 4 \\ 5, & x = 4 \end{cases} \]",
                     [r"1.\ \ g(4) = 5\ \checkmark", r"2.\ \ \lim_{x\to4} g(x) = \lim_{x\to4}\frac{(x - 4)(x + 4)}{x - 4} = \lim_{x\to4}(x + 4) = 8\ \checkmark",
                      r"3.\ \ 8 \ne 5\ \times \ \Rightarrow\ \text{not continuous (removable)}"],
                     at=[1, 2, 3])
        self.example("Example 3: Finding the constant", r"Find $k$ so that $h$ is continuous at $x = 2$. \[ h(x) = \begin{cases} kx - 1, & x < 2 \\ x^2 + k, & x \ge 2 \end{cases} \]",
                     [r"\lim_{x\to2^-} h(x) = \lim_{x\to2^-}(kx - 1) = 2k - 1, \qquad h(2) = \lim_{x\to2^+}(x^2 + k) = 4 + k", r"2k - 1 = 4 + k", r"k = 5"], at=[1, 2, 3])
        self.finish()
