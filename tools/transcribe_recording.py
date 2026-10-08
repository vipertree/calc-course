#!/usr/bin/env python3
"""Transcribe one of Adder's cleaned lesson recordings with word timestamps (faster-whisper, CPU).

    python tools/transcribe_recording.py 01-01      ->  voice/aligned/01-01.words.json

Output: {"duration": s, "words": [{"w": "word", "s": start, "e": end}, ...]}, the input the aligner needs.
"""
import json
import sys
from pathlib import Path

from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parents[1]
slug = sys.argv[1]
src = ROOT / "voice" / "adder-lesson-recordings" / "cleaned" / f"{slug}.wav"
out = ROOT / "voice" / "aligned" / f"{slug}.words.json"
model = WhisperModel("small.en", device="cpu", compute_type="int8")
segments, info = model.transcribe(str(src), word_timestamps=True, vad_filter=True, beam_size=5,
                                  initial_prompt="A calculus lesson: limits, average velocity, secant lines, Zeno's arrow.")
words = []
for seg in segments:
    for w in seg.words:
        words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)})
out.parent.mkdir(parents=True, exist_ok=True)
json.dump({"duration": info.duration, "words": words}, open(out, "w"), indent=0)
print(out, len(words), "words")
