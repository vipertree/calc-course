"""Teacher slide decks: one per topic, built from the topic's content source (content/topic_X_Y.py, the same blocks
the notes and the site use), so a deck can't drift from the notes.

    ~/opt/mamba/envs/calc/bin/python tools/build_slides.py 1.2 1.3
    ~/opt/mamba/envs/calc/bin/python tools/build_slides.py all --no-pptx
    ... --media-root /workspace/repos/calc-course     # read stills from another checkout

Each topic gets two versions. "solutions" reveals every worked example step by step; "blank" shows each problem with
nothing worked, and the teacher works it on the board or over the slide. Both show every formula and definition in
full: no fill-in blanks and no "work it out here" boxes (Adder 2026-10-14).
    build/slides/<num>/deck-solutions.html, deck-blank.html     the decks the site shows to teacher accounts
    build/slides/<num>/<num>-slides-solutions.pptx, ...-blank.pptx   for PowerPoint and Google Slides
    build/slides/<num>/stills/*.png                              pictures from the lesson's animation
    build/slides/<num>/manifest.json                              what was built, and which stills were missing and why

Stills (Adder 2026-10-15: no video in the slides, stills rendered by manim): anim/stills.sh <num> runs the lesson
scene without animating and saves, per transcript beat, its fullest frame on a transparent background, plus each worked
example's figure as posed and as solved (build/stills/<slug>/{light,dark}/, stills.json). A notes section's slide gets
the still of its matching beat; an example gets its figure. A topic with no stills yet builds without pictures (logged).

Output stays off git (build/ is ignored): the site serves it only to teachers (web/course/views.py, slides_*).
"""
import argparse
import contextlib
import hashlib
import html as H
import importlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from calclib import (BigIdea, Check, Definition, Desmos, Example, Figure, FigureRow, Formula,  # noqa: E402
                     Meanings, Section, Table, Text, Video)
from calclib import web as W  # noqa: E402
from calclib import label  # noqa: E402  ("2.1", or "T3" for a trig module lesson)
from calclib.videx import problem_tex, video_examples  # noqa: E402
from transcripts import parse  # noqa: E402

OUT = ROOT / "build" / "slides"
HERE = ROOT / "tools" / "slides"
VERSIONS = ("solutions", "blank")
LOOKS = ("light", "dark")
CHROME_LIBS = Path.home() / "chromium-libs" / "root" / "usr" / "lib" / "x86_64-linux-gnu"
PAPER_BG = (0xF7, 0xF2, 0xE8)          # the site's light look (app.css [data-theme="paper"] --bg)
PAPER_INK = (0x22, 0x1D, 0x16)


def load_topic(num):
    with contextlib.redirect_stdout(io.StringIO()):
        return importlib.import_module("content.topic_" + num.replace(".", "_")).TOPIC


def all_topics():
    key = lambda n: tuple(int(k) for k in n.split("."))
    return sorted((p.stem[6:].replace("_", ".") for p in (ROOT / "content").glob("topic_*_*.py")), key=key)


# ------------------------------------------------------------------ text -> slide HTML
_BLANK_SPAN = re.compile(r'<span class="blank(?: pick)?" data-blank="([^"]+)"([^>]*)></span>')


def rich(s, version):
    """The course's LaTeX subset as HTML (math stays for KaTeX, as on the site). The notes' blanks are always filled in:
    the teacher presents everything in full and the students fill in their own notes (Adder 2026-10-14)."""
    if not s:
        return ""
    blanks = W.Blanks("s")
    out = W.html(s, blanks)
    answers = dict(blanks.items)

    def sub(m):
        bid, attrs = m.group(1), m.group(2)
        a = answers[bid]
        if a.startswith("pick:"):
            right = a[5:].strip()
            opts = json.loads(H.unescape(re.search(r'data-options="([^"]*)"', attrs).group(1)))
            return "<span class='pick'>" + "".join(
                f"<span class='{'yes' if o == right else 'opt'}'><span class='box'></span>{W.html(o)}</span>"
                for o in opts) + "</span>"
        return W.html(a)
    return _BLANK_SPAN.sub(sub, out)


def plain(s):
    """Rough plain text of a LaTeX-subset string, for speaker notes: math stays as LaTeX between $ signs."""
    s = W.fill_blanks(s or "")
    s = re.sub(r"\\(textbf|emph|text)\{([^{}]*)\}", r"\2", s)
    s = s.replace(r"\par", "\n").replace("``", '"').replace("''", '"')
    return re.sub(r"[ \t]+", " ", s).strip()


def step_html(s):
    """One board line of a worked example: math by default, TEXT: a sentence, PART: the next part of the question."""
    if s.startswith("TEXT:"):
        return f"<div class='st text'>{W.html(s[5:])}</div>"
    if s.startswith("PART:"):
        return f"<div class='st part'>{W.html(s[5:])}</div>"
    if s.startswith("POWER:"):
        f = s[6:].split("|")
        coef = f[3] if len(f) > 3 else f[1]
        s = rf"\frac{{d}}{{dx}}\left[{f[0]}^{{{f[1]}}}\right] = {coef}{f[0]}^{{{f[2]}}}"
    return f"<div class='st math'>\\[ \\displaystyle {s} \\]</div>"


def step_plain(s):
    for tag in ("TEXT:", "PART:"):
        if s.startswith(tag):
            return plain(s[len(tag):])
    return s[6:].replace("|", ", ") if s.startswith("POWER:") else s


_FIG_CACHE = OUT / "_figures"


def fig_html(fig, extra_class="block"):
    """A notes figure as inline SVG (black ink is currentColor, so it follows the light and dark looks)."""
    figs = fig.figures if isinstance(fig, FigureRow) else [fig]
    parts = []
    for f in figs:
        tag = hashlib.sha1(f.tikz.encode()).hexdigest()[:10]
        cached = _FIG_CACHE / f"{f.name}-{tag}.svg"
        if not cached.exists():
            _FIG_CACHE.mkdir(parents=True, exist_ok=True)
            tmp = _FIG_CACHE / "tmp"
            name = W.figure_svg(f, str(tmp))
            shutil.move(str(tmp / name), cached)
        svg = re.sub(r"<\?xml[^>]*\?>\s*", "", cached.read_text())
        cap = f"<figcaption>{W.html(f.caption)}</figcaption>" if f.caption else ""
        parts.append(f"<figure><div class='svg'>{svg}</div>{cap}</figure>")
    if len(parts) > 1:
        return f"<div class='figrow {extra_class}'>{''.join(parts)}</div>"
    return parts[0].replace("<figure>", f"<figure class='{extra_class}'>", 1)


# ------------------------------------------------------------------ stills
def still_slug(beat):
    """The file-name form of a beat name; must match kit.py _save_still."""
    return re.sub(r"[^a-z0-9]+", "-", beat.lower()).strip("-")[:60] or "beat"


class Stills:
    """The topic's manim stills (anim/stills.sh), copied into the deck folder as they're used."""

    def __init__(self, num, media_root, outdir, log):
        self.num, self.outdir, self.log = num, outdir, log
        slug = num.replace(".", "_")
        self.src = {look: media_root / "build" / "stills" / slug / look for look in LOOKS}
        self.have = {}
        for look, d in self.src.items():
            j = d / "stills.json"
            self.have[look] = {(e["beat"], e["kind"]) for e in json.loads(j.read_text())["stills"]} if j.exists() else set()
        if not self.have["light"]:
            log(f"{num}: no stills yet (run anim/stills.sh {num}); the deck has no pictures")
        self.used = set()

    def _mask(self, beat):
        from PIL import Image
        import numpy as np
        f = self.src["light"] / f"{still_slug(beat)}-end.png"
        with Image.open(f) as im:
            return np.asarray(im.getchannel("A").resize((192, 108))) > 24

    def distinct(self, beats):
        """Drop a beat's still when the next one only adds to it (the same graph a step later): an animation builds
        up over several beats, and the slides need the built-up picture once, not every stage of it."""
        beats = [b for b in beats if (b, "end") in self.have["light"]]
        masks = [self._mask(b) for b in beats]
        keep = []
        for i, b in enumerate(beats):
            if i + 1 < len(beats):
                m, n = masks[i], masks[i + 1]
                if m.sum() and (m & n).sum() / m.sum() > 0.85:
                    continue
            keep.append(b)
        return keep

    def get(self, beat, kind):
        """{"light": "stills/x.png", "dark": "stills/x-dark.png"} for a beat's still, or None."""
        if not beat or (beat, kind) not in self.have["light"]:
            return None
        res = {}
        for look in LOOKS:
            if (beat, kind) not in self.have[look]:
                continue
            name = f"{still_slug(beat)}-{kind}{'' if look == 'light' else '-dark'}.png"
            dest = self.outdir / "stills" / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            srcf = self.src[look] / f"{still_slug(beat)}-{kind}.png"
            if not dest.exists() or dest.stat().st_mtime < srcf.stat().st_mtime:
                crop_to_drawing(srcf, dest)
            self.used.add(name)
            res[look] = f"stills/{name}"
            if look == "light":
                from PIL import Image
                with Image.open(dest) as im:
                    res["size"] = im.size      # so the slide lays out before the image has loaded
        res.setdefault("dark", res["light"])
        return res


def crop_to_drawing(src, dest, margin=36):
    """A still on a transparent background, cut down to what is drawn on it (plus a margin)."""
    from PIL import Image
    im = Image.open(src)
    box = im.getchannel("A").point(lambda v: 255 if v > 24 else 0).getbbox() if im.mode == "RGBA" else None
    if box:
        x0, y0, x1, y1 = box
        im = im.crop((max(0, x0 - margin), max(0, y0 - margin), min(im.width, x1 + margin), min(im.height, y1 + margin)))
    im.save(dest, optimize=True)


def img_html(still, cls):
    w, h = still.get("size", (1920, 1080))
    return (f"<img class='{cls}' src='{still['light']}' data-light='{still['light']}' data-dark='{still['dark']}' "
            f"width='{w}' height='{h}' alt=''>")


# ------------------------------------------------------------------ which beat animates which notes section
_STOP = set("the a an of and or to in on at for with is are as by from its it this that what when how why your you "
            "using use into than then".split())


def _words(s):
    return {w[:5] for w in re.findall(r"[a-z]+", re.sub(r"\$[^$]*\$", " ", s.lower())) if w not in _STOP and len(w) > 2}


def assign_beats(section_titles, beats):
    """{section title: [beat, ...]}: every animation beat placed in a notes section, keeping both in order. A beat goes
    to the best-matching section (by shared words) at or after the previous beat's section; a beat that matches
    nothing stays with the section before it."""
    out = {t: [] for t in section_titles}
    if not section_titles:
        return out
    cur = 0
    for name in beats:
        bw = _words(name)
        best, score = cur, 0.0
        for i in range(cur, len(section_titles)):
            tw = _words(section_titles[i])
            if tw and bw:
                sc = len(tw & bw) / (len(tw) * len(bw)) ** 0.5
                if sc > score + 1e-9:
                    best, score = i, sc
        if score >= 0.3:
            cur = best
        out[section_titles[cur]].append(name)
    return out


# ------------------------------------------------------------------ the deck
def slide(kind, kicker, title, body, clip=None, clip_cap="", notes="", math_title=False):
    return {"kind": kind, "kicker": kicker, "title": title, "body": body, "clip": clip, "clip_cap": clip_cap,
            "notes": notes, "plain_title": not math_title and "$" not in title}


def build_deck(t, version, stills, log):
    slug = t.number.replace(".", "_")
    num = label(t.number)                  # what students and teachers see on the slides
    tpath = ROOT / "transcripts" / f"{slug}.md"
    beat_names = [b["name"] for b in parse(str(tpath))[1]] if tpath.exists() else []
    end_examples = {(ti.split(":", 1)[1].strip() if ":" in ti else ti): ti for ti, *_ in video_examples(t.number)}
    body_examples = {ti for ti, *_ in video_examples(t.number, lesson=True)}
    raw_steps = {ti: (p, st) for ti, p, st, _ in video_examples(t.number) + video_examples(t.number, lesson=True)}
    unit_line = t.unit
    S = [slide("title", "", t.title, f"<span class='chip'>{num}</span><div class='unit'>{W.html(unit_line)}</div>"
               f"<h1>{W.html(t.title)}</h1><div class='goals'>{W.html(t.goals)}</div><div class='ver'>"
               + ("Teacher slides, solutions shown" if version == "solutions" else "Teacher slides, problems only")
               + "</div>", notes=plain(t.goals))]

    # group the notes into sections
    sections, cur = [], {"title": "", "blocks": []}
    for b in t.notes:
        if isinstance(b, Section):
            cur = {"title": b.title, "blocks": []}
            sections.append(cur)
        elif not sections:
            if not isinstance(b, Video):
                cur["blocks"].append(b)
                sections.append(cur)
        else:
            cur["blocks"].append(b)

    example_beats = set(end_examples.values()) | body_examples | {b.beat for b in t.notes if isinstance(b, Example) and b.beat}
    anim_beats = [n for n in beat_names if n not in example_beats and n not in ("Title", "Close")]
    sec_beats = assign_beats([s["title"] for s in sections if s["title"] and s["title"] != "Worked examples"], anim_beats)

    n_ex = n_chk = 0
    recap = []
    for sec in sections:
        title = sec["title"] or t.title
        blocks = sec["blocks"]
        in_worked = sec["title"] == "Worked examples"
        # graphs that belong to an example ride along on its slides
        attach = {}
        for i, b in enumerate(blocks):
            if not isinstance(b, Figure):
                continue
            for j in (i + 1, i - 1):
                if 0 <= j < len(blocks) and isinstance(blocks[j], Example) and j not in attach.values():
                    near = blocks[j]
                    if re.search(r"_[bv]ex\d+$", b.name) and j == i + 1 or re.search(r"graph", near.body, re.I):
                        attach[i] = j
                        break
        fig_for = {j: blocks[i] for i, j in attach.items()}
        pending = []
        # the section's animation stills, in video order: one beside each notes slide, the rest on slides of their own
        queue = [x for x in (stills.get(bt, "end") for bt in stills.distinct(sec_beats.get(sec["title"], []))) if x]

        slots = []          # this section's slides that can carry a picture: notes text or a formula box, no graph

        def take_clip():
            return None, ""     # pictures are placed once the section's slides are known (below)

        def flush():
            if not pending:
                return
            chunks, size, cur_chunk = [], 0, []
            for b in pending:
                w = 450 if isinstance(b, (Figure, FigureRow)) else 300 if isinstance(b, Table) else len(plain(getattr(b, "body", "") or ""))
                if cur_chunk and size + w > 950:
                    chunks.append(cur_chunk)
                    cur_chunk, size = [], 0
                cur_chunk.append(b)
                size += w
            if cur_chunk:
                chunks.append(cur_chunk)
            for chunk in chunks:
                figs = [b for b in chunk if isinstance(b, Figure)]
                # a slide that already has the notes' graph gets no second picture
                clip, cap = (None, "") if any(isinstance(b, (Figure, FigureRow)) for b in chunk) else take_clip()
                rest = [b for b in chunk if not isinstance(b, Figure)]
                if len(figs) == 1 and rest and clip is None:
                    body = f"<div class='with-fig'><div class='problem' style='font-size:inherit'>{''.join(block_html(b, version) for b in rest)}</div>{fig_html(figs[0], 'side')}</div>"
                else:
                    body = "".join(block_html(b, version) for b in chunk)
                if not any(isinstance(b, (Figure, FigureRow)) for b in chunk):
                    slots.append(len(S))
                S.append(slide("notes", f"{num} · Notes", title, body, clip, cap,
                               notes="\n\n".join(plain(getattr(b, "body", "") or getattr(b, "caption", "") or "") for b in chunk)))
            pending.clear()

        for i, b in enumerate(blocks):
            if i in attach:
                continue
            if isinstance(b, (Formula, Definition, BigIdea)):
                flush()
                clip, cap = take_clip()
                kicker = {Formula: "Key formula", Definition: "Definition", BigIdea: "Big idea"}[type(b)]
                slots.append(len(S))
                S.append(slide("idea", f"{num} · {kicker}", title, block_html(b, version), clip, cap,
                               notes=plain(b.body)))
                recap.append(b)
            elif isinstance(b, Example):
                flush()
                n_ex += 1
                beat = b.beat or (b.title if b.title in body_examples else end_examples.get(b.title) if in_worked else None)
                steps = raw_steps.get(beat, (None, None))[1] if beat else None
                S.extend(example_slides(num, n_ex, b, steps, fig_for.get(i), beat, version, stills, take_clip))
            elif isinstance(b, Check):
                flush()
                n_chk += 1
                S.extend(check_slides(num, n_chk, b, version))
            elif isinstance(b, (Video, Desmos)):
                continue                       # the video plays on the lesson page; Desmos graphs are interactive there
            elif isinstance(b, Meanings):
                if b.caption:
                    pending.append(Text(b.caption))
            else:
                pending.append(b)
        flush()
        place_stills(S, slots, queue, num, title)

    # close: what to remember, and what's next
    items = []
    for b in recap:
        if isinstance(b, BigIdea):
            items.append(f"<li>{rich(b.body, 'solutions')}</li>")
        else:
            items.append(f"<li><strong>{W.html(b.title)}</strong></li>")
    nxt = next_topic(t.number)
    body = (f"<ul class='recap'>{''.join(items)}</ul>" if items else f"<div class='prose'>{W.html(t.goals)}</div>") + \
        (f"<div class='upnext'>Up next: {label(nxt[0])} {W.html(nxt[1])}</div>" if nxt else "")
    S.append(slide("close", f"{num} · Close", "What to remember", body, notes=plain(t.goals)))
    return S


def place_stills(S, slots, queue, num, title):
    """Put a section's animation stills (in video order) beside its slides. They are shared out over the section's
    text slides in order; a slide that gets more than one is repeated, its text held still while the picture steps
    through the animation (Adder 2026-10-15). A section with no text slide shows them on picture slides."""
    if not queue:
        return
    if not slots:
        S.extend(slide("picture", f"{num} · From the lesson", title, img_html(q, "big still")) for q in queue)
        return
    n, m = len(slots), len(queue)
    share = [queue[i * m // n:(i + 1) * m // n] for i in range(n)] if m >= n else [[q] for q in queue] + [[]] * (n - m)
    for pos, pics in sorted(zip(slots, share), reverse=True):      # from the end, so earlier positions stay put
        if not pics:
            continue
        base = S[pos]
        copies = [dict(base, clip=q) for q in pics]
        if len(copies) > 1:
            for j, c in enumerate(copies, 1):
                c["kicker"] = f"{base['kicker']} · {j} of {len(copies)}"
        S[pos:pos + 1] = copies


def block_html(b, version):
    if isinstance(b, Text):
        return f"<div class='block prose'>{rich(b.body, version)}</div>"
    if isinstance(b, Formula):
        return f"<div class='block formula'><div class='tag'>{W.html(b.title)}</div><div class='prose'>{rich(b.body, version)}</div></div>"
    if isinstance(b, Definition):
        return f"<div class='block definition'><div class='tag'>{W.html(b.title)}</div><div class='prose'>{rich(b.body, version)}</div></div>"
    if isinstance(b, BigIdea):
        return f"<div class='block bigidea'><span class='tag'>BIG IDEA</span>{rich(b.body, version)}</div>"
    if isinstance(b, Table):
        head = "<tr>" + "".join(f"<th>{W.html(c.strip())}</th>" for c in b.header.split("&")) + "</tr>" if b.header else ""
        rows = [re.sub(r"^\s*\[[^\]]*\]", "", r).replace(r"\hline", "") for r in b.latex.split(r"\\")]
        rows = [r for r in rows if r.strip()]
        body = "".join("<tr>" + "".join(f"<td>{rich(c.strip(), version)}</td>" for c in r.split("&")) + "</tr>" for r in rows)
        vbar = " vbar" if "|" in b.spec else ""
        return f"<div class='block'><table class='data{vbar}'>{head}{body}</table></div>"
    if isinstance(b, (Figure, FigureRow)):
        return fig_html(b)
    raise TypeError(b)


def example_slides(num, k, ex, steps, fig, beat, version, stills, take_clip):
    """A worked example: the problem, then (solutions version) the solution one step at a time. The blank version is
    the problem alone; the teacher works it on the board or over the slide. The picture is the video's own figure
    (a manim still, as posed and then solved) when there is one, else the notes' figure."""
    kicker = f"{num} · Example {k}"
    problem = W.html(ex.body)
    # restated above the work, the problem stays compact: its displayed formulas go back inline
    compact = W.html(re.sub(r"\\\[(.+?)\\\]", lambda m: "$\\displaystyle " + m.group(1).strip() + "$", ex.body, flags=re.S))
    take_clip()                                    # an example never takes its section's picture
    posed, solved = stills.get(beat, "figure-problem"), stills.get(beat, "figure")
    if posed:
        fig_h = img_html(posed, "side still")
        fig_done = img_html(solved or posed, "side still")
    else:
        fig_h = fig_done = fig_html(fig, "side") if fig is not None else ""
    sol_lines = [step_plain(s) for s in steps] if steps else [plain(ex.solution)]
    notes = "Problem: " + plain(ex.body)
    if version == "solutions":
        notes += "\n\nSolution:\n" + "\n".join(sol_lines)
    main = f"<div class='problem'>{problem}</div>"
    if fig_h:
        main = f"<div class='with-fig'>{main}{fig_h}</div>"
    out = [slide("problem", kicker, W.html(ex.title), main, notes=notes)]
    if version == "blank":
        return out
    if steps:
        lines = [step_html(s) for s in steps]
        for j in range(1, len(lines) + 1):
            shown = [ln.replace("class='st ", "class='st now " if i == j - 1 else "class='st ", 1) if i < j
                     else ln.replace("class='st ", "class='st later ", 1) for i, ln in enumerate(lines)]
            body = f"<div class='problem small'>{compact}</div><div class='steps'>{''.join(shown)}</div>"
            f = fig_done if j == len(lines) else fig_h
            if f:
                body = f"<div class='with-fig'><div style='flex:1;min-width:0'>{body}</div>{f}</div>"
            out.append(slide("step", f"{kicker} · Step {j} of {len(lines)}", W.html(ex.title), body,
                             notes="\n".join(sol_lines[:j])))
    else:
        body = f"<div class='problem small'>{compact}</div><div class='answer'><div class='tag'>SOLUTION</div><div class='prose'>{W.html(ex.solution)}</div></div>"
        if fig_done:
            body = f"<div class='with-fig'><div style='flex:1;min-width:0'>{body}</div>{fig_done}</div>"
        out.append(slide("step", f"{kicker} · Solution", W.html(ex.title), body, notes=plain(ex.solution)))
    return out


def check_slides(num, k, c, version):
    kicker = f"{num} · Quick check {k}"
    prompt = f"<div class='problem'>{W.html(c.prompt)}</div>"
    out = [slide("check", kicker, "Quick check", prompt, notes="Prompt: " + plain(c.prompt)
                 + ("" if version == "blank" else f"\n\nAnswer: {c.answer.tex()}"))]
    if version == "solutions":
        ans = c.answer.tex()
        body = (f"<div class='problem small'>{W.html(c.prompt)}</div><div class='answer'><div class='tag'>ANSWER</div>"
                + (f"<div class='prose'>$\\displaystyle {ans}$</div>" if ans else "")
                + (f"<div class='prose'>{W.html(c.solution)}</div>" if c.solution else "") + "</div>")
        out.append(slide("answer", kicker, "Quick check: answer", body, notes=plain(c.solution)))
    return out


def next_topic(num):
    syl = json.loads((ROOT / "web" / "course" / "syllabus.json").read_text())
    # a topic taught in an AB and a BC version (docs/ab-bc-versions.md): neither version's deck points at the other
    twin = next((t.get("twin") for u in syl for t in u["topics"] if t["n"] == num), None)
    flat = [(t["n"], t["title"]) for u in syl for t in u["topics"] if t["n"] != twin]
    nums = [n for n, _ in flat]
    if num in nums and nums.index(num) + 1 < len(flat):
        return flat[nums.index(num) + 1]
    return None


# ------------------------------------------------------------------ HTML
def site_tokens():
    """The color and font tokens from the site's stylesheet (everything before its first layout rule)."""
    css = (ROOT / "web" / "static" / "css" / "app.css").read_text()
    return css[:css.index("\n* { box-sizing")]


FONTS = ("https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Source+Sans+3:"
         "wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap")
KATEX = "https://cdn.jsdelivr.net/npm/katex@0.16.22/dist"


def deck_html(t, version, slides):
    n = len(slides)
    parts = []
    for i, s in enumerate(slides, 1):
        if s["kind"] == "title":
            parts.append(f"<section class='slide k-title' id='s{i}'>{s['body']}</section>")
            continue
        head = (f"<header class='sh'><div class='kicker'>{s['kicker']}</div>"
                f"<h2 class='title{' plain' if s['plain_title'] else ''}'>{s['title']}</h2></header>")
        aside = f"<aside class='clip'>{img_html(s['clip'], 'still')}</aside>" if s["clip"] else ""
        parts.append(f"<section class='slide k-{s['kind']}' id='s{i}'>{head}<div class='sb'><div class='main mathy'><div class='fit'>"
                     f"{s['body']}</div></div>{aside}</div><footer class='sf'><span>{label(t.number)} {W.html(t.title)}</span>"
                     f"<span>{i} / {n}</span></footer></section>")
    kind = "solutions" if version == "solutions" else "blank"
    css = site_tokens() + "\n" + (HERE / "deck.css").read_text()
    js = (HERE / "deck.js").read_text()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{label(t.number)} slides ({kind})</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="{KATEX}/katex.min.css">
<style>
{css}
</style>
</head>
<body class="deck" data-version="{version}">
<div class="viewport"><div class="stage">
{chr(10).join(parts)}
</div></div>
<nav class="chrome" aria-label="Slide controls">
  <button type="button" data-act="prev" aria-label="Previous slide">&#9664;</button>
  <span class="count">1 / {n}</span>
  <button type="button" data-act="next" aria-label="Next slide">&#9654;</button>
  <button type="button" data-act="theme">Light / dark</button>
  <button type="button" data-act="full">Fullscreen</button>
  <button type="button" data-act="keys">Keys</button>
  <a href="./">Exit</a>
</nav>
<div class="keys" hidden><div class="card"><h2>Keys</h2><table>
  <tr><td><kbd>&rarr;</kbd> <kbd>Page Down</kbd> <kbd>Space</kbd></td><td>Next slide</td></tr>
  <tr><td><kbd>&larr;</kbd> <kbd>Page Up</kbd></td><td>Previous slide</td></tr>
  <tr><td><kbd>Home</kbd> <kbd>End</kbd></td><td>First or last slide</td></tr>
  <tr><td><kbd>F</kbd></td><td>Fullscreen</td></tr>
  <tr><td><kbd>T</kbd></td><td>Light or dark</td></tr>
  <tr><td><kbd>B</kbd></td><td>Black screen</td></tr>
</table></div></div>
<div class="blackout" hidden></div>
<script>
{js}
</script>
<script defer src="{KATEX}/katex.min.js"></script>
<script defer src="{KATEX}/contrib/auto-render.min.js" onload="window.deckTypeset()"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ PowerPoint
def build_pptx(t, version, slides, deck, outdir, log):
    """Each slide's picture (math and stills rendered at 1.5x of 1080p), its title as editable text, and the slide's
    text (and, in the solutions version, the solution) in the speaker notes."""
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Emu, Pt
    shots = outdir / "_shots" / version
    env = dict(os.environ, LD_LIBRARY_PATH=str(CHROME_LIBS))
    py = shutil.which("python3", path="/usr/bin:/bin") or "python3"
    r = subprocess.run([py, str(HERE / "shoot.py"), str(deck), str(shots), "--theme", "paper", "--transparent"],
                       env=env, capture_output=True, text=True)
    if r.returncode != 0:
        log(f"{t.number} {version}: screenshots failed, no PowerPoint\n{r.stderr[-2000:]}")
        return None
    if r.stderr.strip():
        log(f"{t.number} {version}: {r.stderr.strip()}")
    info = json.loads((shots / "shots.json").read_text())
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    px = lambda v: Emu(int(round(v * 6350)))           # 1920 px across a 13.33 in slide
    layout = prs.slide_layouts[6]
    for s, shot in zip(slides, info):
        sl = prs.slides.add_slide(layout)
        fill = sl.background.fill
        fill.solid()
        fill.fore_color.rgb = RGBColor(*PAPER_BG)
        sl.shapes.add_picture(shot["png"], 0, 0, width=prs.slide_width, height=prs.slide_height)
        if shot["title"]:
            r_ = shot["title"]
            tb = sl.shapes.add_textbox(px(r_["x"]), px(r_["y"]), px(r_["w"] + 40), px(r_["h"]))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
            run = tf.paragraphs[0].add_run()
            run.text = shot["titleText"]
            run.font.size, run.font.name, run.font.bold = Pt(31), "Georgia", True
            run.font.color.rgb = RGBColor(*PAPER_INK)
        if s["notes"]:
            sl.notes_slide.notes_text_frame.text = s["notes"]
    dest = outdir / f"{t.number}-slides-{version}.pptx"
    prs.save(dest)
    return dest


# ------------------------------------------------------------------ main
def build(num, media_root, pptx=True):
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print("  " + msg)

    t = load_topic(num)
    outdir = OUT / num
    outdir.mkdir(parents=True, exist_ok=True)
    stills = Stills(num, media_root, outdir, log)
    made = {"topic": num, "title": t.title, "versions": {}}
    for version in VERSIONS:
        slides = build_deck(t, version, stills, log)
        deck = outdir / f"deck-{version}.html"
        deck.write_text(deck_html(t, version, slides))
        entry = {"html": deck.name, "slides": len(slides), "stills": sum(1 for s in slides if s["clip"] or "class='side still'" in s["body"])}
        if pptx:
            p = build_pptx(t, version, slides, deck, outdir, log)
            if p:
                entry["pptx"] = p.name
        elif (outdir / f"{num}-slides-{version}.pptx").exists():
            entry["pptx"] = f"{num}-slides-{version}.pptx"          # kept from an earlier run
        made["versions"][version] = entry
        print(f"  {deck.relative_to(ROOT)}: {len(slides)} slides, {entry['stills']} with stills"
              + (f", {entry['pptx']}" if entry.get("pptx") else ""))
    # stills no deck uses any more, and the video clips of the older decks, are deleted
    for f in (outdir / "stills").glob("*") if (outdir / "stills").exists() else []:
        if f.name not in stills.used:
            f.unlink()
    shutil.rmtree(outdir / "clips", ignore_errors=True)
    shutil.rmtree(outdir / "_shots", ignore_errors=True)
    made["stills"] = sorted(stills.used)
    made["log"] = log_lines
    (outdir / "manifest.json").write_text(json.dumps(made, indent=1))
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("topics", nargs="+", help="topic numbers like 1.2, or 'all'")
    ap.add_argument("--media-root", default=str(ROOT), help="checkout whose anim/media and web/static/video to read")
    ap.add_argument("--no-pptx", action="store_true")
    a = ap.parse_args()
    nums = all_topics() if a.topics == ["all"] else a.topics
    for num in nums:
        print(num)
        build(num, Path(a.media_root).resolve(), pptx=not a.no_pptx)


if __name__ == "__main__":
    main()
