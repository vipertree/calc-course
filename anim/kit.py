"""Transcript-driven lesson scenes and reusable visuals.

A scene never types its own narration. It says

    with self.beat("Shrinking the interval") as b:
        ...animations...
        b.line(2)          # wait until narration line 2 of that beat starts

and the words come from transcripts/<topic>.md, so editing a transcript changes the video's audio with no code change.
[pause] and [long pause] become silences in the narration track. At the end, `self.finish()` fails the render if any
transcript beat was never used, so script and video can't drift apart.
"""
import os
import re
import sys
from contextlib import contextmanager

import numpy as np
from manim import *

from style import (AREA, BG, DERIV, DIM, FUNC, INK, PANEL, SECANT, TANGENT, ACCUM, LessonScene, M, T, formula_box,
                   title_card, SAFE_SCALE)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from transcripts import parse  # noqa: E402

UNIT_NAMES = {1: "Limits and Continuity", 2: "Differentiation: Definition and Fundamental Properties",
              3: "Differentiation: Composite, Implicit, and Inverse Functions", 4: "Contextual Applications of Differentiation",
              5: "Analytical Applications of Differentiation", 6: "Integration and Accumulation of Change", 7: "Differential Equations",
              8: "Applications of Integration", 9: "Parametric Equations, Polar Coordinates, and Vector-Valued Functions",
              10: "Infinite Sequences and Series"}


class Beat:
    def __init__(self, scene, tracker, n_lines):
        self.scene, self.tr, self.n = scene, tracker, n_lines

    def line(self, i):
        """Wait until narration line i (0-based) of this beat begins."""
        if 0 < i < self.n:
            self.scene.wait_until_bookmark(f"L{i}")

    def rest(self):
        """Seconds of narration left in this beat."""
        return max(self.tr.get_remaining_duration(), 0.0)


class TranscriptScene(LessonScene):
    NUM = "0.0"

    def setup(self):
        super().setup()
        title, beats = parse(os.path.join(ROOT, "transcripts", self.NUM.replace(".", "_") + ".md"))
        self.topic_title = re.sub(r"^\S+\s+", "", title)
        self.beats = {b["name"]: b for b in beats}
        self.order = [b["name"] for b in beats]
        self.used = []
        self._marks = 0
        self._issues = {}
        self._beat_now = "start"

    # ------------------------------------------------------------ layout audit
    # After every animation, look for text colliding with other text or pictures, and anything leaving the
    # visible frame. Findings go to media/layout_<slug>.json for the video-review skill; nothing is fixed here.
    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)
        self._audit()

    @staticmethod
    def _leaves(mob):
        """Text and pictures inside a mobject (skipping text faded to nothing)."""
        out = []
        for m in mob.get_family():
            if isinstance(m, ImageMobject):
                out.append(m)
            elif isinstance(m, MathTex) and m.width > 0:
                glyphs = [g for g in m.family_members_with_points()]
                if glyphs and max(g.get_fill_opacity() for g in glyphs) > 0.05:
                    out.append(m)
        return out

    def _audit(self):
        def box(m):
            return m.get_left()[0], m.get_right()[0], m.get_bottom()[1], m.get_top()[1]
        fx0, fx1, fy0, fy1 = box(self.camera.frame)
        tops = [m for m in self.mobjects if not isinstance(m, ValueTracker)]
        leaves = [(i, leaf) for i, top in enumerate(tops) for leaf in self._leaves(top)]
        now = round(self.renderer.time, 1)
        zoomed = self.camera.frame.width < config.frame_width * SAFE_SCALE * 0.98
        for i, leaf in ([] if zoomed else leaves):      # a zoomed camera crops on purpose
            x0, x1, y0, y1 = box(leaf)
            if x0 < fx0 - 0.02 or x1 > fx1 + 0.02 or y0 < fy0 - 0.02 or y1 > fy1 + 0.02:
                self._note("off-frame", now, leaf)
        for a in range(len(leaves)):
            for c in range(a + 1, len(leaves)):
                (i, m), (j, n) = leaves[a], leaves[c]
                if i == j:
                    continue                      # parts of one group are laid out together on purpose
                ax0, ax1, ay0, ay1 = box(m)
                bx0, bx1, by0, by1 = box(n)
                if min(ax1, bx1) - max(ax0, bx0) > 0.08 and min(ay1, by1) - max(ay0, by0) > 0.08:
                    self._note("overlap", now, m, n)

    @staticmethod
    def _name(m):
        if isinstance(m, ImageMobject):
            return "<image>"
        return getattr(m, "tex_string", type(m).__name__)[:60]

    def _note(self, kind, now, *mobs):
        key = (kind,) + tuple(self._name(m) for m in mobs)
        if key not in self._issues:
            self._issues[key] = {"kind": kind, "t": now, "beat": self._beat_now, "what": [self._name(m) for m in mobs]}

    def _write_audit(self):
        import json
        out = os.path.join(config.media_dir, f"layout_{self.NUM.replace('.', '_')}.json")
        with open(out, "w") as f:
            json.dump(sorted(self._issues.values(), key=lambda d: d["t"]), f, indent=1)

    def _text(self, lines, think=False):
        out = []
        for i, ln in enumerate(lines):
            ln = ln.strip()
            if think and i == 0 and len(lines) > 1 and not any("[try it]" in x for x in lines):
                # worked examples: a few seconds of silence after the problem is read, before the solving starts.
                # A transcript can place it itself with [try it] (multi-part problems: one per part).
                ln = re.sub(r"\s*\[(long )?pause\]\s*$", "", ln) + " [try it]"

            def think_mark(m):
                self._marks += 1
                return f" <bookmark mark='W{self._marks}'/> "
            ln = re.sub(r"\s*\[try it\]", think_mark, ln)

            def pause(m):
                self._marks += 1
                return f" <bookmark mark='{'Q' if m.group(1) else 'P'}{self._marks}'/> "
            ln = re.sub(r"\[(long )?pause\]", pause, ln)
            out.append((f"<bookmark mark='L{i}'/>" if i else "") + ln)
        return re.sub(r"\s+", " ", " ".join(out)).strip()

    @contextmanager
    def beat(self, name, think=False):
        if name not in self.beats:
            raise KeyError(f"{self.NUM}: no beat named {name!r}. Beats: {self.order}")
        lines = self.beats[name]["say"]
        self._beat_now = name
        with self.voiceover(text=self._text(lines, think)) as tr:
            yield Beat(self, tr, len(lines))
        self.used.append(name)

    def finish(self):
        missing = [n for n in self.order if n not in self.used]
        if missing:
            raise RuntimeError(f"{self.NUM}: transcript beats not animated: {missing}")
        self.clear(0.8)
        self.outro()
        self._write_audit()

    def outro(self):
        """Closing card with the outro jingle: this topic, and what comes next."""
        here = T(f"Topic {self.NUM}", 34, DIM)
        name = T(re.sub(r"(\b\w)\^(\w+)", r"$\1^{\2}$", self.topic_title), 46).set_max_width(12)
        card = VGroup(here, name, Line(LEFT * 2.5, RIGHT * 2.5, color=FUNC, stroke_width=3)).arrange(DOWN, buff=0.3).shift(UP * 0.6)
        nxt = next_topic(self.NUM)
        if nxt:
            card.add(T(r"Up next: Topic " + nxt[0] + r" \textperiodcentered{} " + re.sub(r"(\b\w)\^(\w+)", r"$\1^{\2}$", nxt[1]), 32, SECANT)
                     .set_max_width(12).next_to(card, DOWN, buff=0.6))
        self.add_sound(os.path.join(ASSETS, "outro_guitar.wav"), gain=-4)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.0)
        self.wait(6.4)                       # the outro music runs about 8 s and ends on its own
        self.play(FadeOut(card), run_time=0.6)

    # ------------------------------------------------------------ common pieces
    def clear(self, run_time=0.6):
        """Fade out everything on screen: shapes, text, images and Groups of them (anything but trackers)."""
        mobs = [m for m in self.mobjects if not isinstance(m, ValueTracker)]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time)

    def title(self, beat_name="Title"):
        unit = int(self.NUM.split(".")[0])
        # titles are plain text; put bits of math like "e^x" into math mode so LaTeX accepts them
        title = re.sub(r"(\b\w)\^(\w+)", r"$\1^{\2}$", self.topic_title)
        card = title_card(self.NUM, title, f"Unit {unit} \\textperiodcentered{{}} {UNIT_NAMES[unit]}")
        # no narration on the title card: just the card and the intro music (Adder, 2026-10-01)
        self.add_sound(os.path.join(ASSETS, "intro_guitar.wav"), gain=-4)
        self.play(FadeIn(card, shift=UP * 0.2), run_time=1.2)
        self.wait(2.2)
        self.play(FadeOut(card), run_time=0.6)
        if beat_name in self.beats:
            self.used.append(beat_name)

    def examples_card(self):
        card = VGroup(T("Worked examples", 64), Line(LEFT * 2.5, RIGHT * 2.5, color=FUNC, stroke_width=3)).arrange(DOWN, buff=0.3)
        self.play(FadeIn(card), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(card), run_time=0.6)

    def example(self, beat_name, problem, steps, figure=None, at=None, text=None, notes_graph=None, figure_at=None,
                follow=False):
        """A worked example: the problem across the top, then each step written in as its narration line starts.

        steps: list of MathTex/Tex strings or mobjects. at: narration line index for each step (default 1, 2, 3...).
        figure: optional mobject shown on the right, with the problem, or from narration line `figure_at` on (so a
        warning's picture arrives with the words that explain it). follow: a first-of-its-kind problem students watch
        rather than try, so no "Pause and try it" cue and no think pause (Adder, 2026-10-02).
        text: the problem as LaTeX for the notes, when `problem` is a mobject
        (calclib/videx.py copies every worked example into the guided notes)."""
        with self.beat(beat_name, think=not follow) as b:
            head = problem if isinstance(problem, Mobject) else T(problem, 42)
            head.set_max_width(12.5).to_edge(UP, buff=0.5)
            self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            if figure is not None:
                # below the problem, never on it: shrink to the room that's left
                room = head.get_bottom()[1] - 0.35 - (-3.7)
                figure.set_max_height(min(5.2, room)).set_max_width(6.2)
                figure.next_to(head, DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
                if figure_at is None:
                    self.play(FadeIn(figure), run_time=0.8)
            # the think pause: a cue while the problem sits alone on screen, gone when the solving starts
            cue = None
            if not follow:
                cue = T(r"Pause and try it.", 32, DIM).next_to(head, DOWN, buff=0.6)
                if figure is not None:
                    cue.to_edge(LEFT, buff=0.8)
                self.play(FadeIn(cue), run_time=0.5)
            board = Board(left=figure is None).next_to(head, DOWN, buff=0.5)
            at = at or list(range(1, len(steps) + 1))
            for k, (s, i) in enumerate(zip(steps, at)):
                if figure_at is not None and i >= figure_at and figure not in self.mobjects:
                    b.line(figure_at)
                    self.play(FadeIn(figure), run_time=0.8)
                b.line(i)
                if cue is not None:
                    self.play(FadeOut(cue), run_time=0.3)
                    cue = None
                if isinstance(s, str) and s.startswith("PART:"):
                    # a multi-part question's next part, shown on its own (its [try it] pause follows) before its work
                    part = board.write(self, T(s[5:], 40, SECANT))
                    cue = T(r"Pause and try it.", 28, DIM).next_to(part, RIGHT, buff=0.5)
                    self.play(FadeIn(cue), run_time=0.4)
                else:
                    board.write(self, s)
            if cue is not None:
                self.play(FadeOut(cue), run_time=0.3)
        self.wait(1.2)
        self.clear()
        self.wait(1.0)                                         # a real break before the next example


def power_parts(step):
    """'POWER:x|7|6' or 'POWER:x|-3|-4|-3' (optional 4th field: how to write the new coefficient) -> (base, exp, new_exp, coef)."""
    f = step[6:].split("|")
    return f[0], f[1], f[2], (f[3] if len(f) > 3 else f[1])


def next_topic(num):
    """(number, title) of the lesson after `num`, from the transcripts folder, or None at the end."""
    key = lambda n: tuple(int(k) for k in n.split("."))
    nums = sorted((p.stem.replace("_", ".") for p in TRANSCRIPTS.glob("*_*.md")), key=key)
    later = [n for n in nums if key(n) > key(num)]
    if not later:
        return None
    first = (TRANSCRIPTS / f"{later[0].replace('.', '_')}.md").read_text().splitlines()[0]
    return later[0], first.lstrip("# ").split(" ", 1)[1]


def wrap_tex(text, width):
    """Break prose into lines of about `width` characters with LaTeX \\\\, never inside $...$ math."""
    words, lines, cur, in_math = text.split(" "), [], "", False
    for w in words:
        if cur and not in_math and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
        in_math ^= w.count("$") % 2 == 1
    lines.append(cur)
    return r" \\ ".join(lines)


class Board(VGroup):
    """A column of math lines that grows downward, left-aligned."""

    def __init__(self, left=True, width=12.5, **kw):
        super().__init__(**kw)
        self.left, self.maxw = left, (width if left else 6.8)
        self.anchor = None

    def next_to(self, mob, direction=DOWN, buff=0.4, **kw):
        self.anchor = mob.get_bottom() + DOWN * buff
        return self

    def place(self, mob):
        """Put the next line under the last one (or at the top), scrolling like write() does. Returns the shift used."""
        if len(self) == 0:
            top = self.anchor if self.anchor is not None else UP * 2
            mob.move_to(top + DOWN * mob.height / 2).to_edge(LEFT, buff=0.8)
            return None
        mob.next_to(self[-1], DOWN, buff=0.4, aligned_edge=LEFT)
        return -3.6 - mob.get_bottom()[1]

    def write_power(self, scene, s, size=48):
        """The power rule, drawn: write d/dx[x^n], circle the exponent, swing a copy of it out front, then lower the exponent by one."""
        base, e, ne, coef = power_parts(s)
        left = M(r"\frac{d}{dx}\left[", base, "^{" + e + "}", r"\right] =", size)
        right = M(coef, base, "^{" + ne + "}", size, DERIV)
        line = VGroup(left, right).arrange(RIGHT, buff=0.25)
        over = self.place(line)
        if over and over > 0:
            top = self.anchor[1] if self.anchor is not None else 3.0
            gone = [m for m in self if m.get_top()[1] + over > top + 0.05]
            scene.play(self.animate.shift(UP * over), *[FadeOut(m) for m in gone], run_time=0.6)
            for m in gone:
                self.remove(m)
            line.shift(UP * over)
        right[1].align_to(left[1], DOWN)
        scene.play(Write(left), run_time=1)
        ring = Circle(color=SECANT, stroke_width=3).surround(left[2], buffer_factor=1.6)
        scene.play(Create(ring), run_time=0.6)
        flying = left[2].copy().set_color(SECANT)
        scene.play(Transform(flying, right[0].copy().set_color(SECANT), path_arc=-PI * 0.7), run_time=1.2)
        scene.play(FadeIn(right[1]), run_time=0.4)
        minus = M(e + " - 1 = " + ne, 30, SECANT).next_to(right[2], UP, buff=0.25)
        scene.play(FadeIn(minus), run_time=0.6)
        scene.play(Write(right[2]), run_time=0.6)
        scene.wait(0.4)
        scene.play(FadeOut(minus), FadeOut(ring), FadeOut(flying), FadeIn(right[0]), right.animate.set_color(DERIV), run_time=0.6)
        self.add(line)
        return line

    def write(self, scene, s, color=INK, size=48):
        if isinstance(s, str) and s.startswith("POWER:"):
            return self.write_power(scene, s, size)
        if isinstance(s, Mobject):
            mob = s
        elif s.startswith("TEXT:"):
            # prose wraps to the board's width rather than shrinking to fit it (shrunk prose is unreadable at 480p)
            mob = T(wrap_tex(s[5:], int(self.maxw * 5.4)), 40, color, tex_environment="flushleft")
        else:
            mob = M(s, size, color)
        mob.set_max_width(self.maxw)
        if len(self) == 0:
            top = self.anchor if self.anchor is not None else UP * 2
            mob.move_to(top + DOWN * mob.height / 2).to_edge(LEFT, buff=0.8)
        else:
            mob.next_to(self[-1], DOWN, buff=0.4, aligned_edge=LEFT)
            over = -3.6 - mob.get_bottom()[1]
            if over > 0:
                # out of room: slide the board up, and let the oldest lines go rather than run over the problem above
                top = self.anchor[1] if self.anchor is not None else 3.0
                gone = [m for m in self if m.get_top()[1] + over > top + 0.05]
                scene.play(self.animate.shift(UP * over), *[FadeOut(m) for m in gone], run_time=0.6)
                for m in gone:
                    self.remove(m)
                mob.shift(UP * over)
        if isinstance(s, str) and r"\cancel" in s:
            # write the line clean first, then strike out the canceled terms so the cancellation is something you watch happen
            plain = M(re.sub(r"\\cancel\{", "{", s), size, color)
            plain.set_max_width(self.maxw).move_to(mob, aligned_edge=LEFT)
            scene.play(Write(plain), run_time=min(1.6, 0.6 + 0.04 * len(plain.family_members_with_points())))
            scene.wait(0.6)
            self.add(mob)
            scene.play(FadeIn(mob), FadeOut(plain), run_time=0.9)
            return mob
        self.add(mob)
        scene.play(Write(mob), run_time=min(1.6, 0.6 + 0.04 * len(mob.family_members_with_points())))
        return mob


# ---------------------------------------------------------------- graphs
def plot_axes(xr, yr, w=7.4, h=5.0, coords=True, xlabel="x", ylabel="y", font=26):
    ax = Axes(x_range=xr, y_range=yr, x_length=w, y_length=h, tips=False,
              axis_config={"color": DIM, "stroke_width": 2, "font_size": font})
    if coords:
        ax.add_coordinates()
    labs = VGroup(M(xlabel, 32, DIM).next_to(ax.x_axis, RIGHT, buff=0.15),
                  M(ylabel, 32, DIM).next_to(ax.y_axis, UP, buff=0.15))
    return ax, labs


def open_dot(ax, x, y, color=FUNC):
    return Circle(radius=0.08, color=color, stroke_width=3, fill_color=BG, fill_opacity=1).move_to(ax.c2p(x, y))


def closed_dot(ax, x, y, color=INK):
    return Dot(ax.c2p(x, y), radius=0.08, color=color)


def asymptote(ax, x, yr):
    return DashedLine(ax.c2p(x, yr[0]), ax.c2p(x, yr[1]), color=DIM, stroke_width=2, dash_length=0.12)


def secant_line(ax, f, a, b, xr, color=SECANT):
    m = (f(b) - f(a)) / (b - a)
    return ax.plot(lambda x: f(a) + m * (x - a), x_range=xr, color=color, stroke_width=4)


def tangent_line(ax, f, a, slope, xr, color=TANGENT):
    return ax.plot(lambda x: f(a) + slope * (x - a), x_range=xr, color=color, stroke_width=4)


def table(headers, rows, size=36, highlight_cols=(), color=INK):
    """headers: list of strings (LaTeX), rows: list of lists. Returns a VGroup grid with .cells[r][c]."""
    data = [headers] + rows
    cells = [[M(str(v), size, DIM if r == 0 else color) for v in row] for r, row in enumerate(data)]
    grid = VGroup(*[VGroup(*row) for row in cells])
    colw = [max(cells[r][c].width for r in range(len(cells))) + 0.5 for c in range(len(headers))]
    for r, row in enumerate(cells):
        x = 0
        for c, m in enumerate(row):
            m.move_to(RIGHT * (x + colw[c] / 2) + DOWN * r * 0.72)
            x += colw[c]
    rule = Line(grid[0].get_left() + DOWN * 0.36 + LEFT * 0.2, grid[0].get_right() + DOWN * 0.36 + RIGHT * 0.2, color=DIM, stroke_width=2)
    out = VGroup(grid, rule).move_to(ORIGIN)            # centered, like every other mobject
    out.cells = cells
    return out


def callout(text, color=SECANT, size=36):
    t = T(text, size, color)
    return formula_box(t, color)


# ---------------------------------------------------------------- small props
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
from pathlib import Path  # noqa: E402
TRANSCRIPTS = Path(__file__).resolve().parent.parent / "transcripts"


def arrow_prop(length=2.2, color=None, angle=0.0):
    """Zeno's arrow: a painted sprite (assets/arrow.png, generated art), `length` units long, pointing at `angle`
    (radians from the +x direction). An arrow in flight is always drawn along its path: use aim() to turn it."""
    a = ImageMobject(os.path.join(ASSETS, "arrow.png")).set_width(length)
    a.heading = 0.0
    return aim(a, angle)


def aim(arrow, angle):
    """Turn an arrow_prop to point at `angle` (absolute, radians), about its own center."""
    arrow.rotate(angle - getattr(arrow, "heading", 0.0))
    arrow.heading = angle
    return arrow


def path_angle(f, x, dx=1e-3):
    """The direction of travel along y = f(x) at x, moving right."""
    return float(np.arctan2(f(x + dx) - f(x - dx), 2 * dx))


FLIGHT_TILT = 0.2   # radians: a snapshot of the arrow early in its flight, still climbing


def pencil_prop(length=1.6):
    """A drawn pencil leaning up and to the right, its point at the origin. pencil.tip() is where it writes."""
    body = Rectangle(width=length, height=length * 0.16, color=INK, stroke_width=2, fill_color=SECANT, fill_opacity=1)
    cone = Polygon(body.get_corner(UL), body.get_corner(DL), body.get_left() + LEFT * length * 0.22, color=INK,
                   stroke_width=2, fill_color=PANEL, fill_opacity=1)
    lead = Polygon(cone.get_vertices()[2], cone.get_vertices()[2] + RIGHT * length * 0.07 + UP * length * 0.03,
                   cone.get_vertices()[2] + RIGHT * length * 0.07 + DOWN * length * 0.03, color=INK, fill_color=INK, fill_opacity=1)
    eraser = Rectangle(width=length * 0.14, height=length * 0.16, color=INK, stroke_width=2, fill_color=TANGENT,
                       fill_opacity=1).next_to(body, RIGHT, buff=0)
    p = VGroup(body, cone, lead, eraser)
    tip = cone.get_vertices()[2].copy()
    p.rotate(PI / 4, about_point=tip).shift(-tip)
    p.tip = lambda: p[1].get_vertices()[2]
    return p


def trace_with_pencil(scene, pencil, path, run_time=1.6, ink=None):
    """Move the pencil's point along `path`, drawing it as it goes. Returns the inked stroke."""
    stroke = path.copy().set_stroke(ink or FUNC, width=5, opacity=1)
    pencil.shift(path.get_start() - pencil.tip())
    dot = Dot(path.get_start(), radius=0.001)
    pencil.add_updater(lambda m: m.shift(dot.get_center() - m.tip()))
    scene.add(pencil)
    scene.play(MoveAlongPath(dot, path), Create(stroke), run_time=run_time, rate_func=linear)
    pencil.clear_updaters()
    return stroke


def nudge_arrow(p0, p1, label="dx", side=DOWN, color=INK, size=30, offset=0.18):
    """A nudge drawn as a small double-headed arrow from p0 to p1, set `offset` off the shape on `side` and
    labeled like a dimension (Adder: every dx, dl, dw in a picture gets its own little arrow)."""
    a = DoubleArrow(p0, p1, buff=0, color=color, stroke_width=3, tip_length=0.1,
                    max_tip_length_to_length_ratio=0.45).shift(side * offset)
    return VGroup(a, M(label, size, color).next_to(a, side, buff=0.08))


def zeno_bust(height=5.6):
    """Jan de Bisschop's etching of a bust of Zeno of Elea (c. 1670, Rijksmuseum, CC0); see assets/CREDITS.md."""
    return ImageMobject(os.path.join(ASSETS, "zeno.png")).set_height(height)


def number_line_pair(xmin, xmax, label_in="x", label_out="f(x)"):
    top = NumberLine(x_range=[xmin, xmax, 1], length=10, color=DIM, include_numbers=True, font_size=24).shift(UP * 1.2)
    bot = NumberLine(x_range=[xmin, xmax, 1], length=10, color=DIM, include_numbers=True, font_size=24).shift(DOWN * 1.2)
    labs = VGroup(M(label_in, 30, DIM).next_to(top, LEFT), M(label_out, 30, DIM).next_to(bot, LEFT))
    return top, bot, labs


def sign_chart(crit, signs, name="f'", width=10, words=None, size=44):
    """A sign chart: a line with the critical points ticked and labeled, a sign between each pair, and optional words
    (e.g. "inc", "dec") under each piece. Returns VGroup(line, ticks, labels, signs, words, name)."""
    line = Line(LEFT * width / 2, RIGHT * width / 2, color=DIM, stroke_width=3)
    n = len(crit)
    xs = [line.point_from_proportion((k + 1) / (n + 1)) for k in range(n)]
    ticks = VGroup(*[Line(p + UP * 0.15, p + DOWN * 0.15, color=INK, stroke_width=3) for p in xs])
    labels = VGroup(*[M(str(c), 34).next_to(p, DOWN, buff=0.25) for c, p in zip(crit, xs)])
    mids = [line.point_from_proportion((k + 0.5) / (n + 1)) for k in range(n + 1)]
    sg = VGroup(*[M(s, size, DERIV if s == "+" else (TANGENT if s == "-" else DIM)).next_to(p, UP, buff=0.25) for s, p in zip(signs, mids)])
    wd = VGroup(*[T(w, 32, DIM).next_to(p, DOWN, buff=0.75) for w, p in zip(words or [], mids)])
    nm = M(name, 36, DIM).next_to(line, LEFT, buff=0.3)
    return VGroup(line, ticks, labels, sg, wd, nm)
