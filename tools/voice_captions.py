#!/usr/bin/env python3
"""Captions for a video narrated by Adder: his actual words (from Whisper), timed on the video's clock.

    python tools/voice_captions.py <voicemap.json> <UU-TT> <out.vtt>

The render writes voicemap_<topic>.json: where each beat's narration starts in the video, which slice of the
recording it plays, and where think-pause silences were inserted. Each word Whisper heard in that slice lands at
  video_start + (word time - slice start) + think * (silences inserted before it).
Cues break at sentence ends, pauses over 0.6 s, or about 9 words; spoken math is then rewritten as notation by
tools/subtitle_math.py.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# words Whisper reliably mishears in these lessons (heard -> meant)
FIXES = {"Aaliyah": "Elea", "Elia": "Elea", "Ilya": "Elea"}


def stamp(t):
    h, rem = divmod(max(0.0, t), 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def main(vmap_path, slug, out):
    vmap = json.load(open(vmap_path))
    words = json.load(open(ROOT / "voice" / "aligned" / f"{slug}.words.json"))["words"]
    timed = []
    for b in vmap:
        s0, s1 = b["rec_start"], b["rec_end"]
        for w in words:
            if s0 <= w["s"] < s1:
                rel = w["s"] - s0
                rel_e = w["e"] - s0
                shift = b["think"] * sum(1 for x in b["inserts"] if x <= rel + 1e-6)
                word = FIXES.get(w["w"].strip(".,?!"), None)
                word = w["w"].replace(w["w"].strip(".,?!"), word) if word else w["w"]
                timed.append((b["video_start"] + rel + shift, b["video_start"] + rel_e + shift, word))
    cues, cur = [], []
    for i, (s, e, w) in enumerate(timed):
        cur.append((s, e, w))
        nxt = timed[i + 1] if i + 1 < len(timed) else None
        end_sentence = w.endswith((".", "?", "!"))
        gap = (nxt[0] - e) if nxt else 9
        if end_sentence or gap > 0.6 or len(cur) >= 9 or nxt is None:
            cues.append((cur[0][0], cur[-1][1], " ".join(x[2] for x in cur)))
            cur = []
    lines = ["WEBVTT", ""]
    for s, e, text in cues:
        lines += [f"{stamp(s)} --> {stamp(max(e, s + 0.8))}", text, ""]
    Path(out).write_text("\n".join(lines))
    subprocess.run([sys.executable, str(ROOT / "tools" / "subtitle_math.py"), out], check=True)
    print(out, len(cues), "cues")


if __name__ == "__main__":
    main(*sys.argv[1:4])
