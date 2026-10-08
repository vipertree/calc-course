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

UNIT_NAMES = {0: "Trig Review", 1: "Limits and Continuity", 2: "Differentiation: Definition and Fundamental Properties",
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
        if getattr(self, "_voice_beats", None):
            vm = [dict(m, **self._voice_beats[m["beat"]]) for m in self._voice_map if m["beat"] in self._voice_beats]
            with open(os.path.join(config.media_dir, f"voicemap_{self.NUM.replace('.', '_')}.json"), "w") as f:
                json.dump(vm, f, indent=1)
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
        if name in self.used:
            raise KeyError(f"{self.NUM}: beat {name!r} is narrated twice")
        lines = self.beats[name]["say"]
        self._beat_now = name
        with self.voiceover(text=self._text(lines, think)) as tr:
            # where this beat's narration starts in the video (the caption builder maps Adder's words with it)
            self._voice_map.append({"beat": name, "video_start": round(self.renderer.time, 3)})
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

    example_ref = None    # a formula (MathTex string) kept in the corner during worked examples, e.g. the chain rule

    def example(self, beat_name, problem, steps, figure=None, at=None, text=None, notes_graph=None, figure_at=None,
                follow=False, ref=None, cues=None):
        """A worked example: the problem across the top, then each step written in as its narration line starts.

        steps: list of MathTex/Tex strings or mobjects. at: narration line index for each step (default 1, 2, 3...).
        figure: optional mobject shown on the right, with the problem, or from narration line `figure_at` on (so a
        warning's picture arrives with the words that explain it). follow: a first-of-its-kind problem students watch
        rather than try, so no "Pause and try it" cue and no think pause (Adder, 2026-10-02).
        cues: {step index: function(scene)} run just before that step is written, e.g. to light up a table cell as the
        narration points at it.
        text: the problem as LaTeX for the notes, when `problem` is a mobject
        (calclib/videx.py copies every worked example into the guided notes)."""
        ref = ref if ref is not None else self.example_ref
        with self.beat(beat_name, think=not follow) as b:
            if isinstance(problem, Mobject):
                head = problem
            elif len(re.sub(r"\$[^$]*\$", "xxxx", problem)) > 80:
                # long word problems wrap onto lines instead of shrinking to fit one
                head = T(wrap_tex(problem, 62), 40, tex_environment="flushleft")
            else:
                head = T(problem, 42)
            card = None
            if ref:
                # the rule being practiced stays up in the top-right corner (Adder: 2.1's definition, 3.1's chain rule)
                card = formula_box(M(ref, 30), DERIV).set_max_width(3.9).to_corner(UR, buff=0.3)
                head.set_max_width(12.5 - card.width - 0.4).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.5)
                self.play(FadeIn(card), FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            else:
                head.set_max_width(12.5).to_edge(UP, buff=0.5)
                self.play(FadeIn(head, shift=DOWN * 0.2), run_time=0.8)
            if figure is not None:
                # below the problem, never on it: shrink to the room that's left
                room = min(head.get_bottom()[1], card.get_bottom()[1] if card else 9) - 0.35 - (-3.7)
                figure.set_max_height(min(5.2, room)).set_max_width(6.2)
                figure.next_to(head, DOWN, buff=0.35).to_edge(RIGHT, buff=0.4)
                if card is not None:
                    figure.next_to(card, DOWN, buff=0.3).to_edge(RIGHT, buff=0.4)
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
                if cues and k in cues:
                    cues[k](self)
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


def car_prop(width=1.1):
    """Amara's car: a painted side-view sprite (assets/car.png, generated art), facing right."""
    return ImageMobject(os.path.join(ASSETS, "car.png")).set_width(width)


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
    # each zero gets a bold tick, a dot, and a dashed divider up through the sign row, so it's obvious which section
    # each sign belongs to (Adder, 4.2)
    ticks = VGroup(*[VGroup(Line(p + UP * 0.3, p + DOWN * 0.3, color=INK, stroke_width=5), Dot(p, radius=0.08, color=INK),
                            DashedLine(p + UP * 0.3, p + UP * 1.0, color=DIM, stroke_width=2, dash_length=0.08)) for p in xs])
    labels = VGroup(*[M(str(c), 36).next_to(p, DOWN, buff=0.35) for c, p in zip(crit, xs)])
    mids = [line.point_from_proportion((k + 0.5) / (n + 1)) for k in range(n + 1)]
    sg = VGroup(*[M(s, size, DERIV if s == "+" else (TANGENT if s == "-" else DIM)).next_to(p, UP, buff=0.25) for s, p in zip(signs, mids)])
    wd = VGroup(*[T(w, 32, DIM).next_to(p, DOWN, buff=0.75) for w, p in zip(words or [], mids)])
    nm = M(name, 36, DIM).next_to(line, LEFT, buff=0.3)
    return VGroup(line, ticks, labels, sg, wd, nm)


def staged_chart(crit, signs, words=None, name="f'", width=10):
    """A sign chart for a worked example's figure (Adder, unit 5: a number line for every sign problem). The line,
    ticks and critical points show with the figure; each sign and the words stay hidden until reveal_sign/reveal_words
    run as cues, so the chart fills in as each test value is worked on the board."""
    ch = sign_chart(crit, signs, name=name, width=width, words=words)
    ch[3].set_opacity(0)
    ch[4].set_opacity(0)
    return ch


def reveal_sign(ch, *ks):
    """A cue for Scene.example: light up the signs of pieces ks (0 = leftmost)."""
    return lambda scene: scene.play(*[ch[3][k].animate.set_opacity(1) for k in ks], run_time=0.6)


def reveal_words(ch):
    """A cue for Scene.example: show the inc/dec (or max/min) words under the chart."""
    return lambda scene: scene.play(ch[4].animate.set_opacity(1), run_time=0.6)


def mark_point(ch, k, text, color=SECANT, size=30):
    """A cue for Scene.example: write a classification ("max", "min", "neither") above critical point k of a sign chart."""
    def cue(scene):
        lab = T(text, size, color).next_to(ch[1][k][2], UP, buff=0.12)
        ch.add(lab)
        scene.play(FadeIn(lab), run_time=0.5)
    return cue


# ---------------------------------------------------------------- scenery for word problems (Adder: real-life pictures should be pretty too)
WATER, WATER_HI, SAND = "#5B9BD5", "#BFDCF2", "#D9C291"
MEADOW, GRASS, GRASS_DK = "#A7C957", "#7FB069", "#55803F"
WOOD, WOOD_DK = "#9A6B43", "#6E4A2C"
CARD, CARD_DK, CARD_LT = "#C99A66", "#A57846", "#E2BE8F"
WOOL, MUZZLE = "#F6F2E9", "#3B3632"


def river_band(width, height=0.7, waves=3):
    """A river seen from above: water, pale ripple lines, and a sandy bank along the bottom edge."""
    water = Rectangle(width=width, height=height, stroke_width=0, fill_color=WATER, fill_opacity=1)
    rip = VGroup(*[FunctionGraph(lambda s, k=k: 0.04 * np.sin(5 * s + 1.7 * k), x_range=[-width / 2 + 0.2 + 0.3 * (k % 2), width / 2 - 0.2],
                                 color=WATER_HI, stroke_width=2).shift(UP * (height / 2 - (k + 1) * height / (waves + 1)))
                   for k in range(waves)])
    bank = Line(water.get_corner(DL), water.get_corner(DR), color=SAND, stroke_width=6)
    return VGroup(water, rip, bank)


def fence_path(points, post_gap=0.32):
    """A wooden fence seen from above along the polyline `points`: a rail with square posts at even spacing."""
    rail = VMobject(stroke_color=WOOD, stroke_width=6).set_points_as_corners(points)
    posts = VGroup()
    for p, q in zip(points, points[1:]):
        n = max(1, int(np.linalg.norm(q - p) / post_gap))
        for t in np.linspace(0, 1, n + 1):
            posts.add(Square(0.11, stroke_width=0, fill_color=WOOD_DK, fill_opacity=1).move_to(p + t * (q - p)))
    return VGroup(rail, posts)


def sheep(size=0.5):
    """A sheep seen from above: a lumpy wool body and a dark head."""
    r = size * 0.28
    body = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=WOOL, fill_opacity=1).move_to([dx * size, dy * size, 0])
                    for dx, dy in ((-0.22, 0.1), (0, 0.16), (0.2, 0.1), (-0.2, -0.12), (0.02, -0.16), (0.22, -0.1), (0, 0))])
    head = Ellipse(width=size * 0.34, height=size * 0.26, stroke_width=0, fill_color=MUZZLE, fill_opacity=1).move_to([size * 0.5, 0, 0])
    ears = VGroup(*[Ellipse(width=size * 0.14, height=size * 0.07, stroke_width=0, fill_color=MUZZLE, fill_opacity=1).move_to([size * 0.44, s * size * 0.17, 0])
                    for s in (1, -1)])
    return VGroup(body, ears, head)


def water_tank(width=2.2, height=3.0):
    """A glass tank with a faucet above its left edge. Returns (group, water(level)) where water(level) draws the water
    for a fill fraction in [0, 1]; use it inside always_redraw."""
    glass = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=INK, stroke_width=3, fill_color=WATER_HI, fill_opacity=0.12)
    spout = VGroup(Line(glass.get_corner(UL) + UP * 0.9 + RIGHT * 0.2, glass.get_corner(UL) + UP * 0.9 + RIGHT * 0.75, color=DIM, stroke_width=8),
                   Line(glass.get_corner(UL) + UP * 0.9 + RIGHT * 0.72, glass.get_corner(UL) + UP * 0.5 + RIGHT * 0.72, color=DIM, stroke_width=8))
    group = VGroup(glass, spout)

    def water(level):
        h = max(level, 0.002) * (height - 0.08)
        return Rectangle(width=width - 0.08, height=h, stroke_width=0, fill_color=WATER, fill_opacity=0.85).align_to(glass, DOWN).shift(UP * 0.04)
    return group, water


def riemann_boxes(ax, f, edges, kind="left", color=AREA, opacity=0.45):
    """Riemann rectangles (kind "left", "right" or "mid") or trapezoids (kind "trap") on the partition `edges`, which may
    be uneven. Heights may be negative; each shape is drawn between the curve sample and the axis."""
    out = VGroup()
    for a, b in zip(edges, edges[1:]):
        if kind == "trap":
            pts = [ax.c2p(a, 0), ax.c2p(b, 0), ax.c2p(b, f(b)), ax.c2p(a, f(a))]
        else:
            s = {"left": a, "right": b, "mid": (a + b) / 2}[kind]
            h = f(s)
            pts = [ax.c2p(a, 0), ax.c2p(b, 0), ax.c2p(b, h), ax.c2p(a, h)]
        out.add(Polygon(*pts, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity))
    return out


def coffee_mug(height=1.6):
    """A mug of coffee with a handle and three wisps of steam (vector art)."""
    w = height * 0.8
    body = RoundedRectangle(width=w, height=height, corner_radius=0.12, stroke_color=INK, stroke_width=3, fill_color="#E8E1D5", fill_opacity=1)
    coffee = Ellipse(width=w * 0.86, height=height * 0.12, stroke_width=0, fill_color="#6B4226", fill_opacity=1).move_to(body.get_top() + DOWN * height * 0.08)
    handle = Arc(radius=height * 0.28, start_angle=-PI / 2, angle=PI, stroke_color=INK, stroke_width=6).next_to(body, RIGHT, buff=-0.05)
    steam = VGroup(*[FunctionGraph(lambda s, k=k: 0.08 * np.sin(6 * s + k), x_range=[0, 0.7], color=DIM, stroke_width=3).rotate(PI / 2)
                     .next_to(body, UP, buff=0.1).shift(RIGHT * (k - 1) * w * 0.28) for k in range(3)])
    return VGroup(steam, handle, body, coffee)


def slope_field(ax, f, xs, ys, length=0.36, color=None, width=3):
    """Short segments of slope f(x, y) centred at each grid point (screen-length `length`), drawn in axis coordinates
    so the slopes are true to the axes' scales."""
    color = color or DIM
    sx = (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0])
    sy = (ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1])
    segs = VGroup()
    for x in xs:
        for y in ys:
            m = f(x, y)
            d = np.array([sx, m * sy, 0.0])
            d = d / np.linalg.norm(d) * length / 2
            p = ax.c2p(x, y)
            segs.add(Line(p - d, p + d, color=color, stroke_width=width))
    return segs


def region(ax, top, bottom, a, b, var="x", color=AREA, opacity=0.45, n=80):
    """The region between two curves as a filled polygon. var="x": between y = bottom(x) and y = top(x), a <= x <= b.
    var="y": between x = bottom(y) (left) and x = top(y) (right), a <= y <= b."""
    s = np.linspace(a, b, n)
    pts = [(v, top(v)) for v in s] + [(v, bottom(v)) for v in s[::-1]]
    if var == "y":
        pts = [(q, p) for p, q in pts]
    return Polygon(*[ax.c2p(p, q) for p, q in pts], stroke_width=0, fill_color=color, fill_opacity=opacity)


def slice_rect(ax, top, bottom, at, d, var="x", color=SECANT, label=None):
    """A representative slice of width d at x = at (var="x", vertical) or y = at (var="y", horizontal), from bottom to
    top, with an optional nudge_arrow label ("dx" or "dy") on its thickness."""
    if var == "x":
        pts = [ax.c2p(at - d / 2, bottom(at)), ax.c2p(at + d / 2, bottom(at)), ax.c2p(at + d / 2, top(at)), ax.c2p(at - d / 2, top(at))]
    else:
        pts = [ax.c2p(bottom(at), at - d / 2), ax.c2p(top(at), at - d / 2), ax.c2p(top(at), at + d / 2), ax.c2p(bottom(at), at + d / 2)]
    rect = Polygon(*pts, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.55)
    if label is None:
        return rect
    if var == "x":
        arr = nudge_arrow(ax.c2p(at - d / 2, bottom(at)), ax.c2p(at + d / 2, bottom(at)), label=label, side=DOWN, color=color, size=26)
    else:
        arr = nudge_arrow(ax.c2p(top(at), at - d / 2), ax.c2p(top(at), at + d / 2), label=label, side=RIGHT, color=color, size=26)
    return VGroup(rect, arr)


def solid_of_revolution(ax, r_out, a, b, r_in=None, axis_y=0.0, n=9, color=ACCUM, tilt=0.32):
    """A 2D sketch of a solid made by revolving about the horizontal line y = axis_y: the outline (curve and its mirror
    image), n elliptical cross sections (discs, or washers when r_in is given), all in axis coordinates.
    tilt is the ellipse's width-to-height ratio on screen."""
    sy = ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]
    def edge(r, sign):
        return ax.plot(lambda v: axis_y + sign * r(v), x_range=[a, b], color=color, stroke_width=3)
    out = VGroup(edge(r_out, 1), edge(r_out, -1))
    if r_in is not None:
        out.add(edge(r_in, 1).set_stroke(opacity=0.7), edge(r_in, -1).set_stroke(opacity=0.7))
    for v in np.linspace(a, b, n):
        R = abs(r_out(v)) * sy
        e = Ellipse(width=max(2 * R * tilt, 0.02), height=max(2 * R, 0.02), stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.18)
        e.move_to(ax.c2p(v, axis_y))
        out.add(e)
        if r_in is not None:
            r = abs(r_in(v)) * sy
            out.add(Ellipse(width=max(2 * r * tilt, 0.02), height=max(2 * r, 0.02), stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(ax.c2p(v, axis_y)))
    return out


def cross_section(kind, p0, p1, color=ACCUM, squash=1.0):
    """One cross section standing straight up (screen UP) on the base segment p0-p1 (screen points, e.g. the two ends
    of a slice of a base region drawn in an oblique view). kind: "square", "rectangle2" (height twice the base),
    "equilateral", "isosceles_right" (a leg on the base), "isosceles_hyp" (the hypotenuse on the base), or "semicircle" (diameter on the base).
    squash scales heights to suit the view."""
    p0, p1 = np.array(p0, dtype=float), np.array(p1, dtype=float)
    s = np.linalg.norm(p1 - p0)
    h = UP * s * squash
    if kind in ("square", "rectangle2"):
        k = 1 if kind == "square" else 2
        shape = Polygon(p0, p1, p1 + k * h, p0 + k * h)
    elif kind == "equilateral":
        shape = Polygon(p0, p1, (p0 + p1) / 2 + 0.866 * h)
    elif kind == "isosceles_right":
        shape = Polygon(p0, p1, p0 + h)
    elif kind == "isosceles_hyp":            # hypotenuse on the base, right angle on top
        shape = Polygon(p0, p1, (p0 + p1) / 2 + h / 2)
    else:
        c, u = (p0 + p1) / 2, (p1 - p0) / 2
        shape = Polygon(*[c + np.cos(t) * u + np.sin(t) * h / 2 for t in np.linspace(0, PI, 32)])
    return shape.set_stroke(color, 3).set_fill(color, 0.35)


def oblique(origin=ORIGIN, sx=1.0, sy=1.0, depth=(0.6, 0.42)):
    """A map (x, y) -> screen point for a base region lying flat, seen from above and in front: x runs to the right,
    y runs back into the page along the slanted `depth` direction. Cross sections then stand straight up (screen UP),
    e.g. cross_section("square", P(x, g(x)), P(x, f(x)))."""
    d = np.array([depth[0], depth[1], 0.0])
    o = np.array(origin, dtype=float)
    return lambda x, y: o + RIGHT * x * sx + d * y * sy


def base_curve(P, f, a, b, color=FUNC, var="x", width=4):
    """The curve y = f(x) (var="x") or x = f(y) (var="y") drawn flat in an oblique() view."""
    if var == "x":
        return ParametricFunction(lambda s: P(s, f(s)), t_range=[a, b, 0.01], color=color, stroke_width=width)
    return ParametricFunction(lambda s: P(f(s), s), t_range=[a, b, 0.01], color=color, stroke_width=width)


def oblique_axes(P, xr, yr, color=None):
    """Thin x and y axes in an oblique() view, with labels."""
    color = color or DIM
    xa = Arrow(P(xr[0], 0), P(xr[1], 0), buff=0, color=color, stroke_width=2, tip_length=0.18)
    ya = Arrow(P(0, yr[0]), P(0, yr[1]), buff=0, color=color, stroke_width=2, tip_length=0.18)
    return VGroup(xa, ya, M("x", 28, color).next_to(xa.get_end(), RIGHT, buff=0.08), M("y", 28, color).next_to(ya.get_end(), UR, buff=0.05))


def sections(P, top, bot, xs, kind, squash=1.0, color=ACCUM, var="x"):
    """Cross sections (cross_section kinds) standing on the base segments at each x in xs (or each y, for var="y")."""
    out = VGroup()
    for v in xs:
        if var == "x":
            p0, p1 = P(v, bot(v)), P(v, top(v))
        else:
            p0, p1 = P(bot(v), v), P(top(v), v)
        out.add(cross_section(kind, p0, p1, color=color, squash=squash))
    return out


def base_region(P, top, bot, a, b, var="x", color=AREA, opacity=0.35, n=60):
    s = np.linspace(a, b, n)
    if var == "x":
        pts = [P(v, top(v)) for v in s] + [P(v, bot(v)) for v in s[::-1]]
    else:
        pts = [P(top(v), v) for v in s] + [P(bot(v), v) for v in s[::-1]]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def rect_section(p0, p1, height, color=ACCUM):
    """A rectangle standing up on p0-p1 with the given screen height."""
    return Polygon(p0, p1, p1 + UP * height, p0 + UP * height).set_stroke(color, 3).set_fill(color, 0.35)


def solid_about_vertical(ax, r_out, c, d, r_in=None, axis_x=0.0, n=9, color=ACCUM, tilt=0.32):
    """solid_of_revolution's twin for a vertical axis x = axis_x: radii are functions of y on [c, d], cross sections are
    flat ellipses (discs or washers) stacked up the axis."""
    sx = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
    def edge(r, sign):
        return ax.plot_parametric_curve(lambda s: np.array([axis_x + sign * r(s), s, 0.0]), t_range=[c, d, 0.01], color=color, stroke_width=3)
    out = VGroup(edge(r_out, 1), edge(r_out, -1))
    if r_in is not None:
        out.add(edge(r_in, 1).set_stroke(opacity=0.7), edge(r_in, -1).set_stroke(opacity=0.7))
    for v in np.linspace(c, d, n):
        R = abs(r_out(v)) * sx
        out.add(Ellipse(width=max(2 * R, 0.02), height=max(2 * R * tilt, 0.02), stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.18).move_to(ax.c2p(axis_x, v)))
        if r_in is not None:
            r = abs(r_in(v)) * sx
            out.add(Ellipse(width=max(2 * r, 0.02), height=max(2 * r * tilt, 0.02), stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1).move_to(ax.c2p(axis_x, v)))
    return out


def ladybug(size=0.5):
    """A small ladybug (vector art), facing up; rotate to aim it along a path."""
    shell = Ellipse(width=size, height=size * 1.15, stroke_color=INK, stroke_width=2, fill_color="#D7263D", fill_opacity=1)
    head = Circle(radius=size * 0.22, stroke_width=0, fill_color=INK, fill_opacity=1).next_to(shell, UP, buff=-size * 0.12)
    seam = Line(shell.get_top(), shell.get_bottom(), color=INK, stroke_width=2)
    spots = VGroup(*[Dot(shell.get_center() + np.array([sx * size * 0.22, sy * size * 0.25, 0]), radius=size * 0.07, color=INK) for sx in (-1, 1) for sy in (-0.6, 0.5)])
    return VGroup(head, shell, seam, spots)


def param_curve(ax, xf, yf, t0, t1, color=FUNC, width=4):
    """The parametric curve (x(t), y(t)) for t0 <= t <= t1, in axis coordinates."""
    return ax.plot_parametric_curve(lambda s: np.array([xf(s), yf(s), 0.0]), t_range=[t0, t1, 0.01], color=color, stroke_width=width)


def drone(size=0.9):
    """A small quadcopter seen from above (vector art)."""
    body = RoundedRectangle(width=size * 0.45, height=size * 0.45, corner_radius=size * 0.1, stroke_color=INK, stroke_width=2, fill_color="#4A5568", fill_opacity=1)
    arms = VGroup(Line(LEFT * size / 2 + UP * size / 2, RIGHT * size / 2 + DOWN * size / 2, color=INK, stroke_width=4),
                  Line(LEFT * size / 2 + DOWN * size / 2, RIGHT * size / 2 + UP * size / 2, color=INK, stroke_width=4))
    rotors = VGroup(*[Circle(radius=size * 0.18, stroke_color=DIM, stroke_width=2, fill_color=WATER_HI, fill_opacity=0.6).move_to(np.array([sx * size / 2, sy * size / 2, 0]))
                      for sx in (-1, 1) for sy in (-1, 1)])
    return VGroup(arms, rotors, body)


def polar_curve(ax, f, t0, t1, color=FUNC, width=4):
    """The polar curve r = f(theta), t0 <= theta <= t1, drawn on Cartesian axes."""
    return ax.plot_parametric_curve(lambda s: np.array([f(s) * np.cos(s), f(s) * np.sin(s), 0.0]), t_range=[t0, t1, 0.01], color=color, stroke_width=width)


def lighthouse(height=1.6):
    """A striped lighthouse with a lamp (vector art)."""
    w = height * 0.3
    tower = Polygon([-w / 2, 0, 0], [w / 2, 0, 0], [w * 0.35, height, 0], [-w * 0.35, height, 0], stroke_color=INK, stroke_width=2, fill_color=PANEL, fill_opacity=1)
    stripes = VGroup(*[Polygon([-w / 2 + k * 0.03, k * height / 4, 0], [w / 2 - k * 0.03, k * height / 4, 0], [w / 2 - (k + 0.5) * 0.03, (k + 0.5) * height / 4, 0], [-w / 2 + (k + 0.5) * 0.03, (k + 0.5) * height / 4, 0],
                               stroke_width=0, fill_color=TANGENT, fill_opacity=1) for k in range(4)])
    lamp = Circle(radius=w * 0.3, stroke_width=0, fill_color="#F6C945", fill_opacity=1).move_to([0, height + w * 0.2, 0])
    return VGroup(tower, stripes, lamp)


def polar_region(ax, f, t0, t1, inner=None, color=AREA, opacity=0.45, n=120):
    """The region swept by r = f(theta) for t0 <= theta <= t1 (from the origin, or from r = inner(theta))."""
    s = np.linspace(t0, t1, n)
    outer = [ax.c2p(f(v) * np.cos(v), f(v) * np.sin(v)) for v in s]
    if inner is None:
        pts = [ax.c2p(0, 0)] + outer
    else:
        pts = outer + [ax.c2p(inner(v) * np.cos(v), inner(v) * np.sin(v)) for v in s[::-1]]
    return Polygon(*pts, stroke_width=0, fill_color=color, fill_opacity=opacity)


def polar_wedge(ax, f, t, dt, color=SECANT, opacity=0.7):
    """A thin sector from the origin at angle t, width dt, radius f(t)."""
    r = f(t)
    return Polygon(ax.c2p(0, 0), ax.c2p(r * np.cos(t), r * np.sin(t)), ax.c2p(r * np.cos(t + dt), r * np.sin(t + dt)), stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=opacity)


# ---------------------------------------------------------------- Unit 0: trig review
PI_NAMES = {k: t for k, t in ((-2, r"-2\pi"), (-1.5, r"-\tfrac{3\pi}{2}"), (-1, r"-\pi"), (-0.5, r"-\tfrac{\pi}{2}"), (0.5, r"\tfrac{\pi}{2}"), (1, r"\pi"),
                              (1.5, r"\tfrac{3\pi}{2}"), (2, r"2\pi"), (2.5, r"\tfrac{5\pi}{2}"), (3, r"3\pi"), (3.5, r"\tfrac{7\pi}{2}"), (4, r"4\pi"))}


def pi_axes(x0, x1, yr, w=9.0, h=3.6, step=0.5, ylabel="y", yticks=(1, -1), font=26):
    """Axes over [x0 pi, x1 pi] with tick labels at multiples of step*pi (pi/2 by default) and the y ticks given.
    Returns (axes, labels); plot with real radians, e.g. ax.plot(np.sin, x_range=[x0 * PI, x1 * PI])."""
    ax, labs = plot_axes([x0 * PI, x1 * PI, step * PI], yr, w=w, h=h, coords=False, ylabel=ylabel)
    k = np.ceil(x0 / step - 1e-9) * step
    while k <= x1 + 1e-9:
        if abs(k) > 1e-9 and k in PI_NAMES:
            labs.add(M(PI_NAMES[k], font, DIM).next_to(ax.c2p(k * PI, 0), DOWN, buff=0.12))
        k += step
    labs.add(*[M(f"{v:g}", font - 2, DIM).next_to(ax.c2p(0, v), LEFT, buff=0.12) for v in yticks])
    return ax, labs


class TrigCircle(VGroup):
    """A unit circle with axes, for the trig review. pt(t) is the point at angle t; ray, angle_arc, drop (the
    reference triangle under a point) and coord (its (cos t, sin t) label) build the usual unit-circle pictures."""

    def __init__(self, r=2.4, center=ORIGIN, ticks=True, **kw):
        super().__init__(**kw)
        self.r, self.c = r, np.array(center, dtype=float)
        self.add(Line(self.c + LEFT * (r + 0.45), self.c + RIGHT * (r + 0.45), color=DIM, stroke_width=2),
                 Line(self.c + DOWN * (r + 0.45), self.c + UP * (r + 0.45), color=DIM, stroke_width=2),
                 Circle(radius=r, color=INK, stroke_width=3).move_to(self.c))
        if ticks:
            self.add(*[M(s, 24, DIM).move_to(self.c + d * (r + 0.28) + o) for s, d, o in
                       (("1", RIGHT, DOWN * 0.22), ("-1", LEFT, DOWN * 0.22), ("1", UP, RIGHT * 0.2), ("-1", DOWN, RIGHT * 0.25))])

    def pt(self, t):
        return self.c + self.r * np.array([np.cos(t), np.sin(t), 0.0])

    def dot(self, t, color=FUNC):
        return Dot(self.pt(t), radius=0.1, color=color)

    def ray(self, t, color=INK):
        return Line(self.c, self.pt(t), color=color, stroke_width=4)

    def angle_arc(self, t, color=SECANT, radius=0.5, label=None, size=30):
        """The angle from the positive x-axis to t (negative t turns clockwise), with an optional label."""
        g = VGroup(Arc(radius=radius, start_angle=0, angle=t, arc_center=self.c, color=color, stroke_width=4))
        if abs(t) > 2 * PI - 0.3:
            g[0].add_tip(tip_length=0.15)
        if label:
            g.add(M(label, size, color).move_to(self.c + (radius + 0.32) * np.array([np.cos(t / 2), np.sin(t / 2), 0])))
        return g

    def drop(self, t, color=SECANT):
        """The reference triangle: ray to the point, a vertical leg down (or up) to the x-axis, the horizontal leg."""
        p = self.pt(t)
        foot = np.array([p[0], self.c[1], 0])
        return VGroup(Polygon(self.c, foot, p, stroke_color=color, stroke_width=3, fill_color=color, fill_opacity=0.18),
                      DashedLine(foot, p, color=color))

    def coord(self, t, tex, color=FUNC, size=30, out=0.55):
        d = np.array([np.cos(t), np.sin(t), 0.0])
        return M(tex, size, color).move_to(self.pt(t) + out * d + RIGHT * 0.35 * np.sign(np.cos(t)) * (abs(np.cos(t)) > 0.2))

    def arc(self, a, b, color=DERIV, width=9):
        return Arc(radius=self.r, start_angle=a, angle=b - a, arc_center=self.c, color=color, stroke_width=width)


def right_triangle(a, b, opp=None, adj=None, hyp=None, angle=None, color=INK, size=34):
    """A right triangle with legs a (horizontal) and b (vertical), the angle at the left corner, the right angle at the
    bottom right. opp, adj, hyp, angle: optional LaTeX labels. Returns a VGroup (triangle first)."""
    A, B, C = ORIGIN, RIGHT * a, RIGHT * a + UP * b
    g = VGroup(Polygon(A, B, C, color=color, stroke_width=4),
               Square(0.22, color=DIM, stroke_width=2).move_to(B + LEFT * 0.11 + UP * 0.11))
    th = np.arctan2(b, a)
    if angle:
        g.add(Arc(radius=0.55, start_angle=0, angle=th, arc_center=A, color=SECANT, stroke_width=4),
              M(angle, size - 2, SECANT).move_to(A + 0.9 * np.array([np.cos(th / 2), np.sin(th / 2), 0])))
    if opp:
        g.add(M(opp, size, FUNC).next_to(Line(B, C), RIGHT, buff=0.15))
    if adj:
        g.add(M(adj, size, DERIV).next_to(Line(A, B), DOWN, buff=0.15))
    if hyp:
        n = np.array([-np.sin(th), np.cos(th), 0])
        g.add(M(hyp, size, INK).move_to((A + C) / 2 + n * 0.42))
    return g


def ferris_wheel(radius=1.6, cars=8):
    """A Ferris wheel on an A-frame (vector art); the hub is at the group's [0] center."""
    hub = Dot(ORIGIN, radius=0.08, color=INK)
    rim = Circle(radius=radius, stroke_color=INK, stroke_width=4)
    spokes = VGroup(*[Line(ORIGIN, radius * np.array([np.cos(a), np.sin(a), 0]), color=DIM, stroke_width=2) for a in np.linspace(0, TAU, cars, endpoint=False)])
    pal = ["#D7263D", "#F6C945", "#5B9BD5", "#59A96A"]
    gondolas = VGroup(*[RoundedRectangle(width=0.3, height=0.24, corner_radius=0.06, stroke_color=INK, stroke_width=2, fill_color=pal[k % 4], fill_opacity=1)
                        .move_to(radius * np.array([np.cos(a), np.sin(a), 0]) + DOWN * 0.14) for k, a in enumerate(np.linspace(0, TAU, cars, endpoint=False))])
    legs = VGroup(Line(ORIGIN, DOWN * (radius + 0.5) + LEFT * radius * 0.6, color=INK, stroke_width=5),
                  Line(ORIGIN, DOWN * (radius + 0.5) + RIGHT * radius * 0.6, color=INK, stroke_width=5))
    ground = Line(DOWN * (radius + 0.5) + LEFT * radius * 1.1, DOWN * (radius + 0.5) + RIGHT * radius * 1.1, color=SAND, stroke_width=6)
    return VGroup(hub, legs, ground, spokes, rim, gondolas)


def clipped_plot(ax, f, x0, x1, ymax, color=FUNC, width=4, n=600):
    """Plot y = f(x) on [x0, x1], dropping the parts with |y| > ymax and breaking the curve there (tan, sec, csc near
    their asymptotes). Returns a VGroup of the separate branches."""
    xs = np.linspace(x0, x1, n)
    out, cur = VGroup(), []
    for xv in xs:
        with np.errstate(all="ignore"):
            yv = f(xv)
        if np.isfinite(yv) and abs(yv) <= ymax:
            cur.append(ax.c2p(xv, yv))
        else:
            if len(cur) > 1:
                out.add(VMobject(color=color, stroke_width=width).set_points_as_corners(cur))
            cur = []
    if len(cur) > 1:
        out.add(VMobject(color=color, stroke_width=width).set_points_as_corners(cur))
    return out
