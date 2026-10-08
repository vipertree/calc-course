"""Shared look for every lesson animation.

The visual vocabulary is fixed course-wide: a student who has seen one video
knows that yellow is always a secant, orange-red is always a tangent, teal fill
is always area, and so on. Keep these constants the single source of truth.
"""
import os
import re

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN, Axes, Create, FadeIn, Line, MathTex,
    MovingCameraScene, RoundedRectangle, Tex, VGroup, VMobject, config,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService, initialize_speech_service
from manim_voiceover.tracker import AUDIO_OFFSET_RESOLUTION

# ---------------------------------------------------------------- palette
# The roles are fixed course-wide (see the module docstring); the inks come from the theme (themes.py, env CALC_THEME).
import themes as _themes  # noqa: E402

THEME = _themes.current()
_P = _themes.palette(THEME)
BG = _P["BG"]
INK = _P["INK"]          # body text
DIM = _P["DIM"]          # axes, secondary text
PANEL = _P["PANEL"]      # card fill

FUNC = _P["FUNC"]        # f, s(t), the function itself
SECANT = _P["SECANT"]    # average rate / secant line
TANGENT = _P["TANGENT"]  # instantaneous rate / tangent line
AREA = _P["AREA"]        # area under the curve
ACCUM = _P["ACCUM"]      # accumulation function A(x), F(x)
DERIV = _P["DERIV"]      # f'

config.background_color = BG
# \cancel{...} strikes out canceled terms in worked algebra (drawn in the tangent red)
config.tex_template.add_to_preamble(r"\usepackage{xcolor}\usepackage{cancel}\renewcommand{\CancelColor}{\color[HTML]{" + TANGENT.lstrip("#") + "}}")
if THEME != "dark":
    # on paper, anything drawn without an explicit color (plain Lines, Dots, Arrows) should be ink, not white
    from manim import Dot, Arrow, Line as _Line, VMobject as _VM  # noqa: E402
    for _cls in (_VM, _Line, Dot, Arrow):
        _cls.set_default(color=INK)

TEX_PREAMBLE_COLOR = INK


def _fit(dim):
    def fit(self, limit, **kw):
        """Shrink (never grow) so this dimension is at most `limit`. Manim 0.20's own set_max_* no longer scale."""
        size = getattr(self, dim)
        if size > limit > 0:
            self.scale(limit / size, **kw)
        return self
    return fit


from manim import Mobject  # noqa: E402
Mobject.set_max_width = _fit("width")
Mobject.set_max_height = _fit("height")


def T(text, size=36, color=INK, **kw):
    """Body text, typeset by LaTeX so text and math share one typeface."""
    return Tex(text, font_size=size, color=color, **kw)


def M(*args, **kw):
    """MathTex. Leading string args are TeX pieces (submobjects, for coloring/matching); then optional size and color."""
    parts = []
    rest = list(args)
    while rest and isinstance(rest[0], str) and not (parts and rest[0].startswith("#")):
        parts.append(rest.pop(0))
    size = rest.pop(0) if rest else kw.pop("size", 40)
    color = rest.pop(0) if rest else kw.pop("color", INK)
    return MathTex(*parts, font_size=size, color=color, **kw)


def course_axes(x_range, y_range, x_length=7.5, y_length=4.6, x_label="x", y_label="y"):
    ax = Axes(
        x_range=x_range, y_range=y_range, x_length=x_length, y_length=y_length,
        tips=False,
        axis_config={"color": DIM, "stroke_width": 2, "include_ticks": True,
                     "tick_size": 0.05},
    )
    labels = ax.get_axis_labels(M(x_label, 32, DIM), M(y_label, 32, DIM))
    return ax, labels


# ------------------------------------------------------- four-meaning panel
MEANINGS = {
    ("d", "a"): ("Instantaneous rate of change", "How fast is it changing right now?"),
    ("d", "g"): ("Slope of the tangent line", "How steep is the graph at a point?"),
    ("i", "a"): ("Accumulation", "How much has built up?"),
    ("i", "g"): ("Area under the curve", "What region does it fill?"),
}


def _icon(kind):
    """Tiny glyphs: a curve with a tangent, or a curve with shaded area."""
    ax = Axes(x_range=[0, 2], y_range=[0, 2], x_length=0.9, y_length=0.6, tips=False,
              axis_config={"stroke_width": 1.5, "color": DIM, "include_ticks": False})
    f = lambda x: 0.25 * x * x + 0.4
    g = ax.plot(f, color=FUNC, stroke_width=3)
    if kind == "slope":
        extra = ax.plot(lambda x: 0.5 * (x - 1) + f(1), x_range=[0.2, 1.8], color=TANGENT, stroke_width=3)
    elif kind == "area":
        extra = ax.get_area(g, x_range=[0.3, 1.7], color=AREA, opacity=0.7)
    elif kind == "rate":
        extra = M(r"\tfrac{d}{dt}", 26, TANGENT).move_to(ax.c2p(1, 1.4))
    else:
        extra = M(r"\textstyle\int", 30, AREA).move_to(ax.c2p(1, 1.3))
    return VGroup(ax, extra, g)


class FourPanel(VGroup):
    """The 2x2 card: derivative/integral x analytical/graphical.

    panel.cells[("d","g")] etc.  highlight() returns a list of animations.
    """

    def __init__(self, width=11.6, height=4.4, **kw):
        super().__init__(**kw)
        cw, ch = width / 2 - 0.1, height / 2 - 0.35
        self.cells = {}
        icons = {("d", "a"): "rate", ("d", "g"): "slope", ("i", "a"): "int", ("i", "g"): "area"}
        for (row, col), (title, sub) in MEANINGS.items():
            box = RoundedRectangle(width=cw, height=ch, corner_radius=0.15,
                                   stroke_color=DIM, stroke_width=2, fill_color=PANEL, fill_opacity=1)
            t = T(title, 30)
            s = T(sub, 22, DIM)
            words = VGroup(t, s).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            icon = _icon(icons[(row, col)])
            words.set_max_width(cw - icon.width - 0.9)
            content = VGroup(icon, words).arrange(RIGHT, buff=0.3)
            content.move_to(box)
            cell = VGroup(box, content)
            x = -cw / 2 - 0.1 if col == "a" else cw / 2 + 0.1
            y = ch / 2 + 0.1 if row == "d" else -ch / 2 - 0.1
            cell.move_to([x, y - 0.25, 0])
            self.cells[(row, col)] = cell
            self.add(cell)
        top = max(c.get_top()[1] for c in self.cells.values())
        left = min(c.get_left()[0] for c in self.cells.values())
        self.col_heads = VGroup(
            T("Analytically", 26, DIM).move_to([self.cells[("d", "a")].get_center()[0], top + 0.28, 0]),
            T("Graphically", 26, DIM).move_to([self.cells[("d", "g")].get_center()[0], top + 0.28, 0]),
        )
        self.row_heads = VGroup(
            T("Derivative", 28, DERIV).rotate(np.pi / 2).move_to([left - 0.3, self.cells[("d", "a")].get_center()[1], 0]),
            T("Integral", 28, AREA).rotate(np.pi / 2).move_to([left - 0.3, self.cells[("i", "a")].get_center()[1], 0]),
        )
        self.add(self.col_heads, self.row_heads)

    def highlight(self, keys, color=TANGENT):
        anims = []
        for k, cell in self.cells.items():
            box, content = cell
            if k in keys:
                anims += [box.animate.set_stroke(color, width=5), content.animate.set_opacity(1)]
            else:
                anims += [box.animate.set_stroke(DIM, width=2), content.animate.set_opacity(0.3)]
        return anims


def formula_box(mob, color=INK, buff=0.25):
    box = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                           corner_radius=0.12, stroke_color=color, stroke_width=3,
                           fill_color=PANEL, fill_opacity=0.9).move_to(mob)
    return VGroup(box, mob)


def title_card(topic, title, unit):
    num = T(f"Topic {topic}", 30, DIM)
    ttl = T(title, 54).set_max_width(12)
    un = T(unit, 28, DIM)
    rule = Line(LEFT * 3, RIGHT * 3, color=FUNC, stroke_width=3)
    return VGroup(num, ttl, rule, un).arrange(DOWN, buff=0.3)


# ---------------------------------------------------------- narration (TTS)
KOKORO_DIR = os.path.expanduser("~/opt/kokoro")
PAUSE_SECONDS = {"P": 0.7, "Q": 1.4, "W": 5.0}     # [pause], [long pause], and W: the "pause and try it" think time (Adder: +2 s, 2026-10-02)
_BOOK = r"(<bookmark\s*mark\s*=[\'\"]\w*[\"\']\s*/>)"


class KokoroService(SpeechService):
    """Local Kokoro TTS for manim-voiceover.

    Kokoro gives no word timestamps, so the text is synthesized in pieces split at
    each <bookmark/>, and exact word boundaries are written at every split. That
    makes wait_until_bookmark() land on the right word without Whisper.
    """

    def __init__(self, voice="am_michael", speed=1.0, **kwargs):
        initialize_speech_service(self, kwargs)
        self.voice, self.speed = voice, speed
        self._k = None

    def _kokoro(self):
        if self._k is None:
            from kokoro_onnx import Kokoro
            self._k = Kokoro(os.path.join(KOKORO_DIR, "kokoro-v1.0.onnx"),
                             os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
        return self._k

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        import soundfile as sf
        cache_dir = cache_dir or self.cache_dir
        input_data = {"input_text": text, "service": "kokoro", "voice": self.voice, "speed": self.speed}
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached
        audio_path = self.get_audio_basename(input_data) + ".wav"

        parts = re.split(_BOOK, text)
        chunks, offset, boundaries, t = [], 0, [], 0.0
        sr = 24000
        for p in parts:
            if re.match(_BOOK, p):
                # transcript pauses arrive as bookmarks named P<n> ([pause]) or Q<n> ([long pause]): insert silence
                mark = re.search(r"mark\s*=\s*['\"](\w+)", p).group(1)
                gap = PAUSE_SECONDS.get(mark[0]) if mark[:1] in PAUSE_SECONDS and mark[1:].isdigit() else None
                if gap:
                    chunks.append(np.zeros(int(gap * sr), dtype=np.float32))
                    t += int(gap * sr) / sr
                continue
            boundaries.append({"audio_offset": int(t * AUDIO_OFFSET_RESOLUTION), "text_offset": offset,
                               "word_length": len(p), "text": p, "boundary_type": "Word"})
            if p.strip():
                samples, sr = self._kokoro().create(p.strip(), voice=self.voice, speed=self.speed, lang="en-us")
                samples = _trim(samples, sr)
                chunks.append(samples)
                chunks.append(np.zeros(int(0.12 * sr), dtype=samples.dtype))
                t += (len(samples) + int(0.12 * sr)) / sr
            offset += len(p)
        boundaries.append({"audio_offset": int(t * AUDIO_OFFSET_RESOLUTION), "text_offset": offset,
                           "word_length": 1, "text": ".", "boundary_type": "Word"})
        sf.write(os.path.join(cache_dir, audio_path), np.concatenate(chunks), sr)
        assert offset == len(remove_bookmarks(text))
        return {"input_text": text, "input_data": input_data, "original_audio": audio_path,
                "word_boundaries": boundaries}


class RecordedService(SpeechService):
    """Adder's own narration (CALC_VOICE=adder): each beat plays its slice of his cleaned recording.

    tools/align_recording.py finds where each beat and each narration line starts in the recording
    (voice/aligned/<UU-TT>.beats.json). Here a beat's audio is that slice, and the bookmarks the scene waits on
    land where he starts the matching line, so animations follow his pacing. A [try it] think pause still gets its
    silence (PAUSE_SECONDS["W"]) inserted at that point; [pause] marks get nothing, since his own pauses are real.
    """

    def __init__(self, scene, beats_json, **kwargs):
        import json
        initialize_speech_service(self, kwargs)
        self.scene = scene
        self.align = json.load(open(beats_json))
        self.root = os.path.dirname(os.path.dirname(os.path.abspath(beats_json)))
        self._audio = None

    def _wav(self):
        if self._audio is None:
            import soundfile as sf
            self._audio = sf.read(os.path.join(os.path.dirname(self.root), self.align["source"]), dtype="float32")
        return self._audio

    def generate_from_text(self, text, cache_dir=None, path=None, **kwargs):
        import soundfile as sf
        cache_dir = cache_dir or self.cache_dir
        name = self.scene._beat_now
        b = self.align["beats"].get(name)
        if b is None:
            raise KeyError(f"{name!r} is not in the alignment for this recording; re-run tools/align_recording.py")
        input_data = {"input_text": text, "service": "adder", "beat": name, "start": b["start"], "end": b["end"],
                      "lines": b["lines"], "source": self.align["source"]}
        think = PAUSE_SECONDS["W"]
        lines_rel = [t - b["start"] for t in b["lines"]] + [b["end"] - b["start"]]
        w_ats = []
        li = 0
        for p in re.split(_BOOK, text):
            if re.match(_BOOK, p):
                mark = re.search(r"mark\s*=\s*['\"](\w+)", p).group(1)
                if mark.startswith("L") and mark[1:].isdigit():
                    li = int(mark[1:])
                elif mark.startswith("W") and mark[1:].isdigit():
                    w_ats.append(lines_rel[min(li + 1, len(lines_rel) - 1)])
        # remembered for the caption builder (also on a cache hit): where his words sit inside this beat's audio
        self.scene._voice_beats[name] = {"rec_start": b["start"], "rec_end": b["end"], "inserts": sorted(w_ats), "think": think}
        cached = self.get_cached_result(input_data, cache_dir)
        if cached is not None:
            return cached
        audio_path = self.get_audio_basename(input_data) + ".wav"
        data, sr = self._wav()
        if data.ndim > 1:
            data = data.mean(axis=1)
        lines = [t - b["start"] for t in b["lines"]] + [b["end"] - b["start"]]
        think = PAUSE_SECONDS["W"]

        # walk the text: each line's pieces get times interpolated inside that line's span of the recording
        parts = re.split(_BOOK, text)
        line_text = [""]
        for p in parts:
            if re.match(_BOOK, p):
                mark = re.search(r"mark\s*=\s*['\"](\w+)", p).group(1)
                if mark.startswith("L") and mark[1:].isdigit():
                    line_text.append("")
                continue
            line_text[-1] += p
        boundaries, offset, li, in_line, shift, inserts = [], 0, 0, 0, 0.0, []
        for p in parts:
            if re.match(_BOOK, p):
                mark = re.search(r"mark\s*=\s*['\"](\w+)", p).group(1)
                if mark.startswith("L") and mark[1:].isdigit():
                    li, in_line = int(mark[1:]), 0
                elif mark.startswith("W") and mark[1:].isdigit():
                    # think pause: silence at the end of this line (where the next one starts)
                    at = lines[min(li + 1, len(lines) - 1)]
                    inserts.append(at)
                    shift += think
                continue
            span = max(1, len(line_text[min(li, len(line_text) - 1)]))
            frac = min(1.0, in_line / span)
            src_t = lines[li] + (lines[min(li + 1, len(lines) - 1)] - lines[li]) * frac
            out_t = src_t + think * sum(1 for x in inserts if x <= src_t + 1e-6)
            boundaries.append({"audio_offset": int(out_t * AUDIO_OFFSET_RESOLUTION), "text_offset": offset,
                               "word_length": len(p), "text": p, "boundary_type": "Word"})
            offset += len(p)
            in_line += len(p)

        clip = data[int(b["start"] * sr):int(b["end"] * sr)]
        chunks, last = [], 0
        for at in sorted(inserts):
            cut = int(at * sr)
            chunks += [clip[last:cut], np.zeros(int(think * sr), dtype=clip.dtype)]
            last = cut
        chunks.append(clip[last:])
        total = sum(len(c) for c in chunks) / sr
        boundaries.append({"audio_offset": int(total * AUDIO_OFFSET_RESOLUTION), "text_offset": offset,
                           "word_length": 1, "text": ".", "boundary_type": "Word"})
        sf.write(os.path.join(cache_dir, audio_path), np.concatenate(chunks), sr)
        assert offset == len(remove_bookmarks(text))
        return {"input_text": text, "input_data": input_data, "original_audio": audio_path,
                "word_boundaries": boundaries}


def _trim(samples, sr, thresh=0.004):
    """Drop leading/trailing silence so stitched chunks don't leave gaps."""
    idx = np.where(np.abs(samples) > thresh)[0]
    if len(idx) == 0:
        return samples
    a = max(idx[0] - int(0.02 * sr), 0)
    b = min(idx[-1] + int(0.08 * sr), len(samples))
    return samples[a:b]


# Safe area. Scenes lay out in the usual 14.2 x 8 frame (to_edge etc. use it), but the camera shows a larger
# region, so everything sits inside margins on all sides, with a deeper band at the bottom where the
# player draws captions. Adder: captions were covering the bottom of the frame.
SAFE_SCALE = 1.22         # camera frame / layout frame: about 9% side margins, 13% caption band at the bottom
SAFE_TOP = 0.45           # extra room above the layout frame, in layout units (bottom gets the rest)


class LessonScene(VoiceoverScene, MovingCameraScene):
    """Base for lesson videos: narration service picked by env var CALC_VOICE, and a caption-safe frame."""

    def setup(self):
        super().setup()
        extra = config.frame_height * (SAFE_SCALE - 1)
        self.camera.frame.scale(SAFE_SCALE).shift(DOWN * (extra / 2 - SAFE_TOP))
        if THEME != "dark":
            # paper, border and logo are painted into the camera's background: behind everything, never faded or zoomed
            self.camera.background_image = _themes.background(THEME, self.camera.pixel_width, self.camera.pixel_height)
            self.camera.init_background()
        voice = os.environ.get("CALC_VOICE", "am_michael")
        self._voice_beats, self._voice_map = {}, []
        if voice == "adder":
            # Adder's recording, lined up by tools/align_recording.py (voice/aligned/<UU-TT>.beats.json)
            u, t = self.NUM.split(".")
            path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "voice", "aligned",
                                f"{int(u):02d}-{int(t):02d}.beats.json")
            self.set_speech_service(RecordedService(self, path))
        else:
            self.set_speech_service(KokoroService(voice=voice))
