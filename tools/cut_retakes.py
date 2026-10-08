#!/usr/bin/env python3
"""Take out Adder's bad takes by reading what he said, so only the last take of each passage is left.

    python tools/cut_retakes.py 01-01        (needs voice/aligned/01-01.words.json from transcribe_recording.py)

When a take goes wrong he says so out loud ("Okay, Claude, scrap this. I'm just going back to the beginning of
the from the other side section."), then says the passage again. So:
  1. Find each cue: "Claude", "scrap/scratch this/that", "start over", "let me redo", "take two".
  2. Skip the cue's sentence and any instructions to me after it ("I'm going to replace just that last sentence").
  3. The next sentence is the restart. Look back (up to LOOKBACK seconds) for the sentence whose words best match
     the restart's opening: that is where the abandoned take began. Cut from there to the restart.
  4. If nothing matches well enough, cut only the cue and the instructions, and flag it for a listen.

Writes voice/aligned/01-01.edited.wav (cuts made with short crossfades), 01-01.edited.words.json (word times moved
to the edited clock; align_recording.py and voice_captions.py use it when it exists) and 01-01.cuts.md, listing
every cut and the words it removed. Hand fixes go in 01-01.cuts.json: {"add": [[start, end]], "skip": [cue_time]}
in the cleaned recording's seconds.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
ALIGNED = ROOT / "voice" / "aligned"
LOOKBACK = 120.0      # seconds before a cue to search for where the abandoned take began
MATCH_MIN = 0.45      # opening-word similarity needed to trust a match
OPENING = 10          # words of each sentence compared
XFADE = 0.02

CUE = re.compile(r"\b(claude|scrap (this|that|it)|scratch (this|that|it)|start\b[^.]{0,40}\bover|let me redo|"
                 r"redo (that|this)|redoing|take two|one more time)\b")
META = re.compile(r"\b(claude|scrap|scratch|going back|go back|replace|redo|redoing|start\b.{0,40}\bover|from the top|"
                  r"again from|the beginning of|(last|past|that|this|the) sentence|this section|that section|take two|"
                  r"cutting|cut out|restarting|let me redo|"
                  r"one more time)\b")


def norm(w):
    return re.sub(r"[^a-z0-9']", "", w.lower())


def units(words):
    """Clauses: split at Whisper's sentence ends and at commas, so a cue in mid-sentence ("We can slide towards x,
    scratch that, redoing that sentence, and we get...") is its own unit. Returns [(first, last_exclusive, starts
    a sentence)]."""
    out, start, sent = [], 0, True
    for i, w in enumerate(words):
        if w["w"].endswith((".", "?", "!", ",")):
            out.append((start, i + 1, sent))
            sent = not w["w"].endswith(",")
            start = i + 1
    if start < len(words):
        out.append((start, len(words), sent))
    return out


def text(words, a, b):
    return " ".join(w["w"] for w in words[a:b])


def opening(words, a, b=None):
    return [norm(w["w"]) for w in words[a:(b if b else a + OPENING)][:OPENING] if norm(w["w"])]


def similarity(x, y):
    # drop a leading filler so "So our function grew" lines up with "In other words, our function grew"
    filler = {"so", "okay", "ok", "now", "and", "well", "alright", "um", "uh"}
    while x and x[0] in filler:
        x = x[1:]
    while y and y[0] in filler:
        y = y[1:]
    return SequenceMatcher(None, x, y).ratio() if x and y else 0.0


SLATE = re.compile(r"\b(recording|take (one|1|two|2)|lesson \d|topic \d)\b")
FILLER = {"so", "okay", "ok", "oh", "sorry", "um", "uh", "now", "and", "well", "alright", "right", "hmm"}


def abandoned_sentence(words, us, k):
    """The unit where the sentence a cue throws away begins: the sentence the cue interrupts ("So, the limit of 3,
    scratch that"), or the one before it when the cue starts its own sentence ("...two units. Sorry, Claude scrap
    that"). Fillers in front of the cue don't count as an interrupted sentence."""
    j = k
    while j > 0 and not us[j][2]:
        j -= 1
    before = [norm(w["w"]) for w in words[us[j][0]:us[k][0]]]
    if (j == k or all(w in FILLER for w in before)) and j > 0:
        j -= 1
        while j > 0 and not us[j][2]:
            j -= 1
    return j


def find_cuts(words, skip=()):
    us = units(words)
    said = lambda u: " ".join(norm(w["w"]) for w in words[us[u][0]:us[u][1]])
    cuts, notes = [], []
    k = 0
    while k < len(us):
        a = us[k][0]
        if not CUE.search(said(k)) or any(abs(words[a]["s"] - t) < 1.0 for t in skip):
            k += 1
            continue
        # instructions to me before or after the cue ("restarting that sentence, scratch that", "I'm going to
        # replace just that last sentence") go too
        while k > 0 and not us[k][2] and META.search(said(k - 1)):
            k -= 1
        a = us[k][0]
        r = k + 1
        while r < len(us) and META.search(said(r)):
            r += 1
        if r >= len(us):
            cuts.append((words[a]["s"], words[-1]["e"], "cue at the end; cut to the end"))
            break
        ra = us[r][0]
        restart = opening(words, ra)
        said_meta = " ".join(said(u) for u in range(k, r))
        if "sentence" in said_meta and "section" not in said_meta:
            # he named the scope: just the sentence the cue interrupts, or else the one before it
            j = abandoned_sentence(words, us, k)
            cuts.append((words[us[j][0]]["s"], words[ra]["s"], "retake of one sentence"))
            k = r
            continue
        # where did the abandoned take begin? the best-matching sentence start in the lookback window, counting
        # the start of the cue's own sentence when the cue comes mid-sentence
        best, best_u = 0.0, None
        for j in range(k, -1, -1):
            ja, _, is_sent = us[j]
            if words[a]["s"] - words[ja]["s"] > LOOKBACK:
                break
            if not is_sent or (j == k and is_sent):
                continue
            sim = similarity(opening(words, ja), restart)
            if sim > best + 0.05:
                best, best_u = sim, j
        cut_end = words[ra]["s"]
        if best_u is not None and best >= MATCH_MIN:
            cuts.append((words[us[best_u][0]]["s"], cut_end, f"retake: restart matched {best:.0%}"))
        else:
            # no clear earlier take: drop the cue and the sentence it abandoned, which is the start of its own
            # sentence when it interrupts one ("So, the limit of 3, scratch that"), else the sentence before it
            j = abandoned_sentence(words, us, k)
            cuts.append((words[us[j][0]]["s"], cut_end, f"cue (best match {best:.0%}): CHECK BY EAR"))
            notes.append(round(words[a]["s"], 2))
        k = r
    return cuts, notes


PAUSE_MAX = 1.4      # a silence between words longer than this is cut down (Adder: long pauses dragged)
PAUSE_LEFT = (0.35, 0.25)   # what stays: after the last sound, before the next word


def word_end(audio, sr, e, limit=0.8, floor_db=-40):
    """Where speech really stops after a word Whisper says ends at e (it often ends long numbers early)."""
    win, t, quiet = int(0.05 * sr), e, 0
    while t - e < limit:
        seg = audio[int(t * sr):int(t * sr) + win]
        if len(seg) == 0:
            break
        quiet = quiet + 1 if 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9) < floor_db else 0
        if quiet >= 2:
            return t - 0.05
        t += 0.05
    return t


def long_pauses(words, audio, sr, cuts):
    """Cuts that shorten every long silence between words to about PAUSE_LEFT."""
    out = []
    for a, b in zip(words, words[1:]):
        if any(s0 <= a["s"] < s1 or s0 <= b["s"] < s1 for s0, s1, _ in cuts):
            continue
        end = word_end(audio, sr, a["e"])
        c0, c1 = end + PAUSE_LEFT[0], b["s"] - PAUSE_LEFT[1]
        if b["s"] - end > PAUSE_MAX and c1 - c0 > 0.2:
            out.append((round(c0, 3), round(c1, 3), "long pause"))
    return out


def apply_cuts(audio, sr, cuts, words):
    """Edited audio and word list. Cuts sit in the gap before a word, so a short crossfade hides each splice."""
    keep, cursor = [], 0.0
    for s0, s1, _ in sorted(cuts):
        keep.append((cursor, s0))
        cursor = s1
    keep.append((cursor, len(audio) / sr))
    n = int(XFADE * sr)
    ramp = np.linspace(0, 1, n, dtype=np.float32)
    out = np.zeros(0, dtype=np.float32)
    for a, b in keep:
        seg = audio[int(a * sr):int(b * sr)].copy()
        if len(out) >= n and len(seg) >= n:
            seg[:n] = seg[:n] * ramp + out[-n:] * ramp[::-1]
            out = out[:-n]
        out = np.concatenate([out, seg])
    # move word times to the edited clock; drop words inside cuts
    new_words = []
    for w in words:
        removed, inside = 0.0, False
        for s0, s1, _ in cuts:
            if s0 <= w["s"] < s1:
                inside = True
            elif s1 <= w["s"]:
                removed += (s1 - s0) + XFADE      # the crossfade overlaps the two sides
        if not inside:
            new_words.append({**w, "s": round(w["s"] - removed, 3), "e": round(w["e"] - removed, 3)})
    return out, new_words


def main(slug):
    rec = json.load(open(ALIGNED / f"{slug}.words.json"))
    words = rec["words"]
    fix = json.load(open(ALIGNED / f"{slug}.cuts.json")) if (ALIGNED / f"{slug}.cuts.json").exists() else {}
    src = ROOT / "voice" / "adder-lesson-recordings" / "cleaned" / f"{slug}.wav"
    audio, sr = sf.read(str(src), dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    cuts, flagged = find_cuts(words, fix.get("skip", []))
    # the slate ("Okay, recording 1.1.") before the lesson starts
    us = units(words)
    for u in range(min(4, len(us))):
        if SLATE.search(" ".join(norm(w["w"]) for w in words[us[u][0]:us[u][1]])):
            nxt = next((v for v in range(u + 1, len(us)) if us[v][2]), None)
            if nxt is not None:
                cuts.append((0.0, words[us[nxt][0]]["s"] - 0.1, "slate"))
            break
    cuts += [(a, b, "added by hand") for a, b in fix.get("add", [])]
    cuts += long_pauses(words, audio, sr, cuts)
    merged = []
    for a, b, why in sorted(cuts):
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(b, merged[-1][1]), merged[-1][2] + " + " + why)
        else:
            merged.append((a, b, why))
    cuts = merged
    edited, new_words = apply_cuts(audio, sr, cuts, words)
    sf.write(str(ALIGNED / f"{slug}.edited.wav"), edited, sr)
    json.dump({"duration": round(len(edited) / sr, 3), "words": new_words, "source_words": f"{slug}.words.json",
               "cuts": [[round(a, 3), round(b, 3), why] for a, b, why in cuts]},
              open(ALIGNED / f"{slug}.edited.words.json", "w"), indent=0)
    with open(ALIGNED / f"{slug}.cuts.md", "w") as fh:
        fh.write(f"# {slug}: bad takes removed\n\nTimes are in the cleaned recording. Fixes go in `{slug}.cuts.json` "
                 "(`\"add\": [[start, end]]` for a missed cut, `\"skip\": [cue time]` to keep one).\n\n")
        pauses = [c for c in cuts if c[2] == "long pause"]
        if pauses:
            fh.write(f"{len(pauses)} long pauses shortened ({sum(b - a for a, b, _ in pauses):.1f}s removed; "
                     f"every silence over {PAUSE_MAX}s now leaves about {sum(PAUSE_LEFT):.1f}s).\n\n")
        for a, b, why in cuts:
            if why == "long pause":
                continue
            removed = text(words, *[i for i in [next(i for i, w in enumerate(words) if w["s"] >= a - 1e-6),
                                                 next((i for i, w in enumerate(words) if w["s"] >= b - 1e-6), len(words))]])
            fh.write(f"## {int(a // 60)}:{a % 60:04.1f} to {int(b // 60)}:{b % 60:04.1f} ({b - a:.1f}s), {why}\n\n"
                     f"> {removed}\n\n")
    total = sum(b - a for a, b, _ in cuts)
    print(f"{slug}: {len(cuts)} cuts, {total:.1f}s removed" + (f"; CHECK BY EAR at {flagged}" if flagged else ""))
    for a, b, why in cuts:
        if why != "long pause":
            print(f"  {a:7.2f}-{b:7.2f}  {why}")


if __name__ == "__main__":
    main(sys.argv[1])
