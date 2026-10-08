"""Teacher slide decks: one per topic, built from the topic's content source (content/topic_X_Y.py, the same blocks
the notes and the site use), so a deck can't drift from the notes.

    ~/opt/mamba/envs/calc/bin/python tools/build_slides.py 1.2 1.3
    ~/opt/mamba/envs/calc/bin/python tools/build_slides.py all --no-pptx
    ... --media-root /workspace/repos/calc-course     # read videos and voicemaps from another checkout

Each topic gets two versions, "solutions" (every worked example revealed step by step, blanks filled in) and
"blank" (problems only, with room to work them live):
    build/slides/<num>/deck-solutions.html, deck-blank.html     the decks the site shows to teacher accounts
    build/slides/<num>/<num>-slides-solutions.pptx, ...-blank.pptx   for PowerPoint and Google Slides
    build/slides/<num>/clips/*.mp4, *.jpg                         silent clips cut from the lesson video, and posters
    build/slides/<num>/manifest.json                              what was built, and which clips were skipped and why

Clips: every worked example (and, where a notes section matches a transcript beat, that beat's animation) is cut out
of web/static/video/<slug>.mp4 and <slug>-dark.mp4 with the audio removed. The cut points come from the render's
anim/media/pub_<slug>_<look>/voicemap_<slug>.json. A topic with no voicemap, or one older than its video, gets no clips
(logged); re-run this after the renders finish and the clips appear. The blank version's clip stops where the
solving starts (the end of the example's think pause); the solutions version plays the whole example.
Clips already cut from the same video at the same times are kept, so a re-run is quick.

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
from calclib.videx import problem_tex, video_examples  # noqa: E402
from transcripts import parse  # noqa: E402

OUT = ROOT / "build" / "slides"
HERE = ROOT / "tools" / "slides"
VERSIONS = ("solutions", "blank")
LOOKS = ("light", "dark")
FFMPEG = shutil.which("ffmpeg") or str(Path(sys.executable).parent / "ffmpeg")
FFPROBE = shutil.which("ffprobe") or str(Path(sys.executable).parent / "ffprobe")
CHROME_LIBS = Path.home() / "chromium-libs" / "root" / "usr" / "lib" / "x86_64-linux-gnu"
PAPER_BG = (0xF7, 0xF2, 0xE8)          # the site's light look (app.css [data-theme="paper"] --bg)
PAPER_INK = (0x22, 0x1D, 0x16)


def load_topic(num):
    with contextlib.redirect_stdout(io.StringIO()):
        return importlib.import_module("content.topic_" + num.replace(".", "_")).TOPIC


def all_topics():
    key = lambda n: tuple(int(k) for k in n.split("."))
    return sorted((p.stem[6:].replace("_", ".") for p in (ROOT / "content").glob("topic_*_*.py")), key=key)


def clock(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


# ------------------------------------------------------------------ text -> slide HTML
_BLANK_SPAN = re.compile(r'<span class="blank(?: pick)?" data-blank="([^"]+)"([^>]*)></span>')


def rich(s, version):
    """The course's LaTeX subset as HTML (math stays for KaTeX, as on the site). Notes blanks are filled in and
    underlined in the solutions version, and left as open lines in the blank version."""
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
                f"<span class='{'yes' if version == 'solutions' and o == right else 'opt'}'><span class='box'></span>{W.html(o)}</span>"
                for o in opts) + "</span>"
        if version == "solutions":
            return f"<span class='fill'>{W.html(a)}</span>"
        w = re.search(r"--w:(\d+)ch", attrs)
        return f"<span class='gap' style='--w:{w.group(1) if w else 6}ch'></span>"
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


# ------------------------------------------------------------------ clip timing
def probe_duration(path):
    r = subprocess.run([FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    return float(r.stdout.strip())


def video_path(media_root, slug, look):
    return media_root / "web" / "static" / "video" / f"{slug}{'' if look == 'light' else '-dark'}.mp4"


def load_timing(num, look, media_root, log):
    """{beat: {"start", "end", "next", "think", "solve"}} in seconds of the published video, or None."""
    slug = num.replace(".", "_")
    video = video_path(media_root, slug, look)
    vm = media_root / "anim" / "media" / f"pub_{slug}_{look}" / f"voicemap_{slug}.json"
    if not video.exists():
        log(f"{num} {look}: no video at {video}; no {look} clips")
        return None
    if not vm.exists():
        log(f"{num} {look}: no voicemap ({vm.relative_to(media_root)}); no {look} clips until the topic is re-rendered")
        return None
    if video.stat().st_mtime - vm.stat().st_mtime > 900:
        log(f"{num} {look}: the voicemap is older than the video (a later render wrote none); no {look} clips")
        return None
    u, t = num.split(".")
    aligned_path = media_root / "voice" / "aligned" / f"{int(u):02d}-{int(t):02d}.beats.json"
    aligned = json.loads(aligned_path.read_text()) if aligned_path.exists() else {"beats": {}}
    entries = json.loads(vm.read_text())
    dur = probe_duration(video)
    out = {}
    for i, e in enumerate(entries):
        s = e["video_start"]
        nxt = entries[i + 1]["video_start"] if i + 1 < len(entries) else dur - 9.5      # the outro card is ~9 s
        end = e.get("video_end")
        if end is None and "rec_start" in e:
            # Adder's recording: his slice of audio plus the think pauses inserted into it
            end = s + (e["rec_end"] - e["rec_start"]) + e.get("think", 5.0) * len(e.get("inserts", []))
        if end is None:
            end = nxt - 2.0
        end = min(end, nxt)
        think, solve = e.get("think_at"), e.get("solve_at")
        if solve is None and e.get("inserts"):
            think = s + e["inserts"][0]
            solve = think + e.get("think", 5.0)
        if solve is None and "rec_start" in e:
            lines = aligned["beats"].get(e["beat"], {}).get("lines", [])
            if len(lines) > 1:
                solve = s + lines[1] - e["rec_start"]           # a follow-along example: the first solving line
        out[e["beat"]] = {"start": s, "end": end, "next": nxt, "think": think, "solve": solve}
    return {"video": video, "beats": out, "duration": dur}


def span_times(b, span):
    """(start, stop, poster time) of a clip, or None when the timing can't place it."""
    if span == "full":
        stop = min(b["end"] + 1.2, b["next"])
        poster = b["solve"] - 0.3 if b["solve"] else b["start"] + 3.0
        return b["start"], stop, min(max(poster, b["start"] + 0.5), stop - 0.1)
    if span == "blank":
        if not b["solve"]:
            return None
        stop = b["solve"] - 0.1
        return b["start"], stop, max(stop - 0.3, b["start"] + 0.2)
    stop = min(b["end"] + 0.5, b["next"])                        # "anim": a lesson beat's animation
    return b["start"], stop, max(stop - 0.4, b["start"] + 0.2)


class Clips:
    """Cuts and remembers the silent clips for one topic (both looks)."""

    def __init__(self, num, media_root, outdir, log, enabled=True):
        self.num, self.outdir, self.log = num, outdir, log
        self.timing = {look: load_timing(num, look, media_root, log) for look in LOOKS} if enabled else {}
        self.made = {}
        mpath = outdir / "manifest.json"
        self.previous = json.loads(mpath.read_text()).get("clips", {}) if mpath.exists() else {}
        self.used = set()

    def get(self, cid, beat, span):
        """{"light": {...}, "dark": {...}} for a clip of `beat`, cutting it if needed, or None."""
        res = {}
        for look in LOOKS:
            tm = self.timing.get(look)
            if not tm:
                continue
            b = tm["beats"].get(beat)
            if b is None:
                self.log(f"{self.num} {look}: beat {beat!r} is not in the voicemap; no clip")
                continue
            times = span_times(b, span)
            if times is None:
                self.log(f"{self.num} {look}: {beat!r} has no think-pause time, so the blank version gets no clip")
                continue
            a, z, poster_t = times
            if z - a < 1.0 or z > tm["duration"]:
                self.log(f"{self.num} {look}: {beat!r} clip {a:.1f}-{z:.1f} s doesn't fit the video; skipped")
                continue
            name = f"{cid}-{span}{'' if look == 'light' else '-dark'}"
            mp4, jpg = self.outdir / "clips" / f"{name}.mp4", self.outdir / "clips" / f"{name}.jpg"
            key = {"src": str(tm["video"]), "src_mtime": tm["video"].stat().st_mtime, "start": round(a, 3),
                   "stop": round(z, 3), "poster": round(poster_t, 3)}
            if self.previous.get(name) != key or not mp4.exists() or not jpg.exists():
                cut(tm["video"], a, z, mp4)
                poster(tm["video"], poster_t, jpg)
            self.made[name] = key
            res[look] = {"mp4": f"clips/{name}.mp4", "jpg": f"clips/{name}.jpg", "start": a, "stop": z}
        if not res:
            return None
        res.setdefault("light", res.get("dark"))
        return res


def cut(src, a, z, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".part.mp4")
    subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{a:.3f}", "-i", str(src), "-t", f"{z - a:.3f}", "-an",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(dest)


def poster(src, t, dest):
    subprocess.run([FFMPEG, "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(src), "-frames:v", "1", "-q:v", "3",
                    str(dest)], check=True)


# ------------------------------------------------------------------ which beat animates which notes section
_STOP = set("the a an of and or to in on at for with is are as by from its it this that what when how why your you "
            "using use into than then".split())


def _words(s):
    return {w[:5] for w in re.findall(r"[a-z]+", re.sub(r"\$[^$]*\$", " ", s.lower())) if w not in _STOP and len(w) > 2}


def match_sections(section_titles, beats):
    """{section title: beat name}: each notes section's best-matching transcript beat (by shared words, in order)."""
    out, last = {}, -1
    for title in section_titles:
        tw = _words(title)
        best, score = None, 0.0
        for i, name in enumerate(beats):
            if i <= last:
                continue
            bw = _words(name)
            if not tw or not bw:
                continue
            sc = len(tw & bw) / (len(tw) * len(bw)) ** 0.5
            if sc > score:
                best, score = i, sc
        if best is not None and score >= 0.3:
            out[title] = beats[best]
            last = best
    return out


# ------------------------------------------------------------------ the deck
def slide(kind, kicker, title, body, clip=None, clip_cap="", notes="", math_title=False):
    return {"kind": kind, "kicker": kicker, "title": title, "body": body, "clip": clip, "clip_cap": clip_cap,
            "notes": notes, "plain_title": not math_title and "$" not in title}


def build_deck(t, version, clips, log):
    num, slug = t.number, t.number.replace(".", "_")
    tpath = ROOT / "transcripts" / f"{slug}.md"
    beat_names = [b["name"] for b in parse(str(tpath))[1]] if tpath.exists() else []
    end_examples = {(ti.split(":", 1)[1].strip() if ":" in ti else ti): ti for ti, *_ in video_examples(num)}
    body_examples = {ti for ti, *_ in video_examples(num, lesson=True)}
    raw_steps = {ti: (p, st) for ti, p, st, _ in video_examples(num) + video_examples(num, lesson=True)}
    unit_line = t.unit
    S = [slide("title", "", t.title, f"<span class='chip'>{num}</span><div class='unit'>{W.html(unit_line)}</div>"
               f"<h1>{W.html(t.title)}</h1><div class='goals'>{W.html(t.goals)}</div><div class='ver'>"
               + ("Teacher slides, solutions shown" if version == "solutions" else "Teacher slides, blank for working live")
               + "<!--slides-for--></div>", notes=plain(t.goals))]

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
    sec_beat = match_sections([s["title"] for s in sections if s["title"] and s["title"] != "Worked examples"], anim_beats)

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
        sec_clip_beat = sec_beat.get(sec["title"])
        first = [True]

        def take_clip():
            """The section's lesson animation goes on the section's first slide."""
            if not first[0]:
                return None, ""
            first[0] = False
            if not sec_clip_beat:
                return None, ""
            c = clips.get(f"s{sections.index(sec) + 1}", sec_clip_beat, "anim")
            if c:
                return c, f"Silent clip from the lesson video ({clock(c['light']['start'])} to {clock(c['light']['stop'])})."
            return None, ""

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
                clip, cap = take_clip()
                figs = [b for b in chunk if isinstance(b, (Figure, FigureRow))]
                rest = [b for b in chunk if not isinstance(b, (Figure, FigureRow))]
                if len(figs) == 1 and rest and clip is None:
                    body = f"<div class='with-fig'><div class='problem' style='font-size:inherit'>{''.join(block_html(b, version) for b in rest)}</div>{fig_html(figs[0], 'side')}</div>"
                else:
                    body = "".join(block_html(b, version) for b in chunk)
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
                S.append(slide("idea", f"{num} · {kicker}", title, block_html(b, version), clip, cap,
                               notes=plain(b.body)))
                recap.append(b)
            elif isinstance(b, Example):
                flush()
                n_ex += 1
                beat = b.beat or (b.title if b.title in body_examples else end_examples.get(b.title) if in_worked else None)
                steps = raw_steps.get(beat, (None, None))[1] if beat else None
                S.extend(example_slides(num, n_ex, b, steps, fig_for.get(i), beat, version, clips, take_clip))
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

    # close: what to remember, and what's next
    items = []
    for b in recap:
        if isinstance(b, BigIdea):
            items.append(f"<li>{rich(b.body, 'solutions')}</li>")
        else:
            items.append(f"<li><strong>{W.html(b.title)}</strong></li>")
    nxt = next_topic(num)
    body = (f"<ul class='recap'>{''.join(items)}</ul>" if items else f"<div class='prose'>{W.html(t.goals)}</div>") + \
        (f"<div class='upnext'>Up next: {nxt[0]} {W.html(nxt[1])}</div>" if nxt else "")
    S.append(slide("close", f"{num} · Close", "What to remember", body, notes=plain(t.goals)))
    return S


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


def example_slides(num, k, ex, steps, fig, beat, version, clips, take_clip):
    """A worked example: the problem (with its silent clip), then the solution one step at a time (solutions version)
    or a slide with room to work it (blank version)."""
    kicker = f"{num} · Example {k}"
    problem = W.html(ex.body)
    fig_h = fig_html(fig, "side") if fig is not None else ""
    take_clip()                                    # an example is never a section's animation slot
    clip = cap = None
    if beat:
        span = "full" if version == "solutions" else "blank"
        clip = clips.get(f"ex{k}", beat, span)
        if clip:
            a, z = clip["light"]["start"], clip["light"]["stop"]
            cap = (f"Silent clip from the lesson video ({clock(a)} to {clock(z)})." if span == "full" else
                   "Silent clip from the lesson video. It stops before the solving starts.")
    sol_lines = [step_plain(s) for s in steps] if steps else [plain(ex.solution)]
    notes = "Problem: " + plain(ex.body)
    if version == "solutions":
        notes += "\n\nSolution:\n" + "\n".join(sol_lines)
    if clip:
        notes += f"\n\nClip: {cap}"
    out = []
    main = f"<div class='problem'>{problem}</div>"
    if fig_h and not clip:
        main = f"<div class='with-fig'>{main}{fig_h}</div>"
    elif fig_h:
        main += fig_h
    out.append(slide("problem", kicker, W.html(ex.title), main, clip, cap or "", notes=notes))
    if version == "blank":
        body = f"<div class='problem small'>{problem}</div>"
        body = f"<div class='with-fig'><div style='flex:1;display:flex;flex-direction:column'>{body}<div class='workroom'>Work it out here</div></div>{fig_h}</div>" \
            if fig_h else body + "<div class='workroom'>Work it out here</div>"
        out.append(slide("work", kicker, W.html(ex.title), body, notes="Problem: " + plain(ex.body)))
        return out
    if steps:
        lines = [step_html(s) for s in steps]
        for j in range(1, len(lines) + 1):
            shown = [ln.replace("class='st ", "class='st now " if i == j - 1 else "class='st ", 1) if i < j
                     else ln.replace("class='st ", "class='st later ", 1) for i, ln in enumerate(lines)]
            body = f"<div class='problem small'>{problem}</div><div class='steps'>{''.join(shown)}</div>"
            if fig_h:
                body = f"<div class='with-fig'><div style='flex:1;min-width:0'>{body}</div>{fig_h}</div>"
            out.append(slide("step", f"{kicker} · Step {j} of {len(lines)}", W.html(ex.title), body,
                             notes="\n".join(sol_lines[:j])))
    else:
        body = f"<div class='problem small'>{problem}</div><div class='answer'><div class='tag'>SOLUTION</div><div class='prose'>{W.html(ex.solution)}</div></div>"
        if fig_h:
            body = f"<div class='with-fig'><div style='flex:1;min-width:0'>{body}</div>{fig_h}</div>"
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
    else:
        out[0]["body"] += "<div class='workroom'>Work it out here</div>"
    return out


def next_topic(num):
    syl = json.loads((ROOT / "web" / "course" / "syllabus.json").read_text())
    flat = [(t["n"], t["title"]) for u in syl for t in u["topics"]]
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
        aside = ""
        if s["clip"]:
            c = s["clip"]
            lt, dk = c["light"], c.get("dark") or c["light"]
            aside = (f"<aside class='clip'><video muted controls playsinline preload='metadata' poster='{lt['jpg']}' "
                     f"data-light='{lt['mp4']}' data-dark='{dk['mp4']}' data-poster-light='{lt['jpg']}' data-poster-dark='{dk['jpg']}'>"
                     f"</video><p class='cap'>{H.escape(s['clip_cap'])}</p></aside>")
        parts.append(f"<section class='slide k-{s['kind']}' id='s{i}'>{head}<div class='sb'><div class='main mathy'><div class='fit'>"
                     f"{s['body']}</div></div>{aside}</div><footer class='sf'><span>{t.number} {W.html(t.title)}</span>"
                     f"<span>{i} / {n}</span></footer></section>")
    label = "solutions" if version == "solutions" else "blank"
    css = site_tokens() + "\n" + (HERE / "deck.css").read_text()
    js = (HERE / "deck.js").read_text()
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t.number} slides ({label})</title>
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
  <tr><td><kbd>K</kbd></td><td>Play or pause the clip</td></tr>
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
    """Each slide's picture (math rendered by KaTeX at 1.5x of 1080p), its title as editable text, its clip as an
    embedded movie, and the slide's text (and, in the solutions version, the solution) in the speaker notes."""
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
        if shot["video"] and s["clip"]:
            v, c = shot["video"], s["clip"]["light"]
            sl.shapes.add_movie(str(outdir / c["mp4"]), px(v["x"]), px(v["y"]), px(v["w"]), px(v["h"]),
                                poster_frame_image=str(outdir / c["jpg"]), mime_type="video/mp4")
        if s["notes"]:
            sl.notes_slide.notes_text_frame.text = s["notes"]
    dest = outdir / f"{t.number}-slides-{version}.pptx"
    prs.save(dest)
    return dest


# ------------------------------------------------------------------ main
def build(num, media_root, pptx=True, clips_on=True):
    log_lines = []

    def log(msg):
        log_lines.append(msg)
        print("  " + msg)

    t = load_topic(num)
    outdir = OUT / num
    outdir.mkdir(parents=True, exist_ok=True)
    clips = Clips(num, media_root, outdir, log, enabled=clips_on)
    made = {"topic": num, "title": t.title, "versions": {}}
    for version in VERSIONS:
        slides = build_deck(t, version, clips, log)
        deck = outdir / f"deck-{version}.html"
        deck.write_text(deck_html(t, version, slides))
        entry = {"html": deck.name, "slides": len(slides), "clips": sum(1 for s in slides if s["clip"])}
        if pptx:
            p = build_pptx(t, version, slides, deck, outdir, log)
            if p:
                entry["pptx"] = p.name
        elif (outdir / f"{num}-slides-{version}.pptx").exists():
            entry["pptx"] = f"{num}-slides-{version}.pptx"          # kept from an earlier run
        made["versions"][version] = entry
        print(f"  {deck.relative_to(ROOT)}: {len(slides)} slides, {entry['clips']} with clips"
              + (f", {entry['pptx']}" if entry.get("pptx") else ""))
    # clips no deck uses any more (an example was removed) are deleted
    for f in (outdir / "clips").glob("*") if (outdir / "clips").exists() else []:
        if f.stem not in clips.made:
            f.unlink()
    shutil.rmtree(outdir / "_shots", ignore_errors=True)
    made["clips"] = clips.made
    made["log"] = log_lines
    (outdir / "manifest.json").write_text(json.dumps(made, indent=1))
    return made


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("topics", nargs="+", help="topic numbers like 1.2, or 'all'")
    ap.add_argument("--media-root", default=str(ROOT), help="checkout whose anim/media and web/static/video to read")
    ap.add_argument("--no-pptx", action="store_true")
    ap.add_argument("--no-clips", action="store_true")
    a = ap.parse_args()
    nums = all_topics() if a.topics == ["all"] else a.topics
    for num in nums:
        print(num)
        build(num, Path(a.media_root).resolve(), pptx=not a.no_pptx, clips_on=not a.no_clips)


if __name__ == "__main__":
    main()
