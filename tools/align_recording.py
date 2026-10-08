#!/usr/bin/env python3
"""Line up one of Adder's lesson recordings with the lesson's transcript, so the video can follow his voice.

    python tools/align_recording.py 01-01        (needs voice/aligned/01-01.words.json from transcribe_recording.py)

Adder speaks freely from the transcript rather than reading it word for word, so this is a global sequence
alignment (Needleman-Wunsch) of the transcript's words against the words Whisper heard, with fuzzy word matching.
Each narration line starts at the first of its words that matched; a line with no matches is placed between its
neighbours. Each beat runs from its first line's start to the next beat's start.

Writes voice/aligned/01-01.beats.json:
  {"source": "...wav", "duration": s, "beats": {name: {"start": s, "end": s, "lines": [s, ...], "matched": 0..1,
                                                       "heard": "his words in this beat"}}}
and voice/aligned/01-01.review.md, a table to check by ear. Manual fixes go in voice/aligned/01-01.overrides.json
({"Beat name": {"start": 12.3}} or {"Beat name": {"lines": [12.3, 15.0, ...]}}) and are applied last.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from transcripts import parse  # noqa: E402

NUMS = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven",
        "8": "eight", "9": "nine", "10": "ten", "12": "twelve", "16": "sixteen", "20": "twenty", "24": "twenty four",
        "36": "thirty six", "48": "forty eight", "60": "sixty", "72": "seventy two"}


PICKUP = 0.35     # a beat matching less than this was most likely skipped or ad-libbed away


def norm(w):
    w = w.lower().replace("’", "'")
    w = re.sub(r"[^a-z0-9']", "", w)
    return NUMS.get(w, w)


def words_of(text):
    text = re.sub(r"\[(long )?pause\]|\[try it\]", " ", text)
    out = []
    for w in text.split():
        n = norm(w)
        if n:
            out.extend(n.split())
    return out


def similar(a, b):
    if a == b:
        return 2.0
    if len(a) > 3 and len(b) > 3 and SequenceMatcher(None, a, b).ratio() > 0.8:
        return 1.0
    return -1.0


def sentence_start(spoken, j, reach=3):
    """A line whose first matched word is a few words into a spoken sentence ("Now, that's an | average")
    should start where that sentence starts. Walk back at most `reach` words to a sentence end or a pause."""
    for k in range(j, max(0, j - reach) - 1, -1):
        if k == 0:
            return 0
        prev = spoken[k - 1]
        if prev["w"].endswith((".", "?", "!")) or spoken[k]["s"] - prev["e"] > 0.35:
            return k
    return j


def align(T, W):
    """Global alignment score matrix with traceback; returns the list of (i, j) matched pairs."""
    n, m = len(T), len(W)
    gap = -0.6
    # band the DP around the diagonal (the two sequences progress together); generous band for detours
    band = max(300, abs(n - m) + 300)
    NEG = -1e9
    score = [[NEG] * (m + 1) for _ in range(n + 1)]
    back = [[0] * (m + 1) for _ in range(n + 1)]
    score[0][0] = 0.0
    for j in range(1, m + 1):
        score[0][j] = j * gap * 0.3          # spoken words before the transcript starts are cheap
        back[0][j] = 2
    for i in range(1, n + 1):
        center = int(i * m / n)
        lo, hi = max(0, center - band), min(m, center + band)
        if lo == 0:
            score[i][0] = i * gap
            back[i][0] = 1
        for j in range(max(1, lo), hi + 1):
            best, arg = score[i - 1][j - 1] + similar(T[i - 1], W[j - 1]), 0
            s = score[i - 1][j] + gap
            if s > best:
                best, arg = s, 1
            s = score[i][j - 1] + gap * 0.5    # extra spoken words (asides, restarts) are cheaper than missing ones
            if s > best:
                best, arg = s, 2
            score[i][j], back[i][j] = best, arg
    i, j, pairs = n, m, []
    while i > 0 or j > 0:
        a = back[i][j]
        if i > 0 and j > 0 and a == 0:
            if similar(T[i - 1], W[j - 1]) > 0:
                pairs.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and (a == 1 or j == 0):
            i -= 1
        else:
            j -= 1
    return pairs[::-1]


def main(slug):
    topic = f"{int(slug[:2])}.{int(slug[3:])}"
    _, blist = parse(ROOT / "transcripts" / f"{topic.replace('.', '_')}.md")
    beats = {b["name"]: b for b in blist}
    order = [b["name"] for b in blist]
    rec = json.load(open(ROOT / "voice" / "aligned" / f"{slug}.words.json"))
    spoken = rec["words"]
    W = [norm(w["w"]) for w in spoken]

    # transcript tokens, each tagged with its (beat, line)
    T, tag = [], []
    for name in order:
        for k, line in enumerate(beats[name]["say"]):
            for w in words_of(line):
                T.append(w)
                tag.append((name, k))
    pairs = align(T, [w or "_" for w in W])

    first = {}      # (beat, line) -> earliest spoken time of a matched word
    count = {}
    for i, j in pairs:
        key = tag[i]
        count[key] = count.get(key, 0) + 1
        if key not in first:
            first[key] = spoken[sentence_start(spoken, j)]["s"]
    keys = [(name, k) for name in order for k in range(len(beats[name]["say"]))]
    times = [first.get(key) for key in keys]
    # fill unmatched lines by interpolating between matched neighbours, keeping times increasing
    known = [(idx, t) for idx, t in enumerate(times) if t is not None]
    for idx in range(len(times)):
        if times[idx] is None:
            before = [p for p in known if p[0] < idx]
            after = [p for p in known if p[0] > idx]
            if before and after:
                (a, ta), (b, tb) = before[-1], after[0]
                times[idx] = ta + (tb - ta) * (idx - a) / (b - a)
            elif before:
                times[idx] = before[-1][1] + 1.0 * (idx - before[-1][0])
            else:
                times[idx] = 0.0
    for idx in range(1, len(times)):
        times[idx] = max(times[idx], times[idx - 1] + 0.3)
    # start each line a little before its first matched word, but never before the previous word ends
    out, pos = {}, 0
    for name in order:
        n = len(beats[name]["say"])
        if n == 0:
            continue
        lines = [round(max(0.0, t - 0.15), 3) for t in times[pos:pos + n]]
        words_in = sum(len(words_of(l)) for l in beats[name]["say"])
        matched = sum(count.get((name, k), 0) for k in range(n))
        out[name] = {"start": lines[0], "lines": lines, "matched": round(matched / max(1, words_in), 2)}
        pos += n
    names = [nm for nm in order if nm in out]
    for a, b in zip(names, names[1:]):
        out[a]["end"] = out[b]["start"]
    out[names[-1]]["end"] = round(rec["duration"], 3)
    # overrides last
    ov_path = ROOT / "voice" / "aligned" / f"{slug}.overrides.json"
    if ov_path.exists():
        for name, ov in json.load(open(ov_path)).items():
            out[name].update(ov)
            if "start" in ov and "lines" not in ov:
                out[name]["lines"][0] = ov["start"]
        for a, b in zip(names, names[1:]):
            out[a]["end"] = out[b]["start"]
    for name in names:
        s, e = out[name]["start"], out[name]["end"]
        out[name]["heard"] = " ".join(w["w"] for w in spoken if s <= w["s"] < e)
    src = f"voice/adder-lesson-recordings/cleaned/{slug}.wav"
    json.dump({"source": src, "duration": rec["duration"], "beats": out},
              open(ROOT / "voice" / "aligned" / f"{slug}.beats.json", "w"), indent=1)
    with open(ROOT / "voice" / "aligned" / f"{slug}.review.md", "w") as fh:
        fh.write(f"# {topic}: alignment of Adder's recording\n\n| beat | start | length | matched | first words heard |\n|---|---|---|---|---|\n")
        for name in names:
            b = out[name]
            mmss = f"{int(b['start'] // 60)}:{b['start'] % 60:04.1f}"
            flag = " **pickup?**" if b["matched"] < PICKUP else ""
            fh.write(f"| {name}{flag} | {mmss} | {b['end'] - b['start']:.1f}s | {b['matched']:.0%} | {' '.join(b['heard'].split()[:14])} |\n")
    pickups = [n for n in names if out[n]["matched"] < PICKUP]
    if pickups:
        print(f"{topic}: probably not in the recording (record a pickup, or override): {pickups}")
    print(f"{topic}: {len(names)} beats aligned; weakest: " +
          ", ".join(f"{n} {out[n]['matched']:.0%}" for n in sorted(names, key=lambda n: out[n]['matched'])[:4]))


if __name__ == "__main__":
    main(sys.argv[1])
