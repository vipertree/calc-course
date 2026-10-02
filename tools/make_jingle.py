"""Synthesize the course jingle: a short mallet motif for the title card and a resolving version for the outro.

Pure numpy, no samples or services, so it costs nothing and can be regenerated or retuned at will.
Writes anim/assets/jingle_intro.wav and anim/assets/jingle_outro.wav (44.1 kHz, 16-bit, stereo).

    ~/opt/mamba/envs/calc/bin/python tools/make_jingle.py
"""
import wave
from pathlib import Path

import numpy as np

SR = 44100
OUT = Path(__file__).resolve().parent.parent / "anim" / "assets"


def hz(note):
    """'C5' -> frequency; sharps as 'F#4'."""
    names = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
    return 440.0 * 2 ** ((names[note[:-1]] + 12 * (int(note[-1]) + 1) - 69) / 12)


def mallet(f, dur, amp=1.0):
    """A marimba-ish tone: fundamental plus the bar's inharmonic 4x partial, fast attack, exponential decay."""
    t = np.arange(int(dur * SR)) / SR
    env = (1 - np.exp(-t * 400)) * np.exp(-t * 3.2)
    tone = np.sin(2 * np.pi * f * t) + 0.35 * np.sin(2 * np.pi * 3.93 * f * t) * np.exp(-t * 9) + 0.15 * np.sin(2 * np.pi * 2 * f * t)
    return amp * env * tone


def pad(freqs, dur, amp=0.18):
    """A soft sustained chord under the motif."""
    t = np.arange(int(dur * SR)) / SR
    env = np.minimum(t / 0.25, 1) * np.exp(-t * 1.1)
    return amp * env * sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2.001 * f * t) for f in freqs) / len(freqs)


def render(events, length, chord=None, chord_at=0.0):
    out = np.zeros(int(length * SR))
    for at, note, amp in events:
        w = mallet(hz(note), length - at, amp)
        i = int(at * SR)
        out[i:i + len(w)] += w[: len(out) - i]
    if chord:
        w = pad([hz(n) for n in chord], length - chord_at)
        i = int(chord_at * SR)
        out[i:i + len(w)] += w
    fade = np.ones_like(out)
    fade[-int(0.3 * SR):] = np.linspace(1, 0, int(0.3 * SR))
    out *= fade
    return 0.6 * out / np.max(np.abs(out))


def write(path, mono):
    # a little width: the right channel lags 8 ms
    lag = int(0.008 * SR)
    right = np.concatenate([np.zeros(lag), mono[:-lag]])
    data = (np.stack([mono, right], axis=1) * 32767).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # intro: a rising question that lands on the fifth (the lesson is about to answer it)
    intro = render([(0.00, "C5", 0.9), (0.16, "E5", 0.8), (0.32, "G5", 0.85), (0.56, "D6", 0.7), (0.80, "G5", 0.6)],
                   2.4, chord=["C4", "G4", "D5"], chord_at=0.56)
    # outro: the same opening, resolved home to C
    outro = render([(0.00, "C5", 0.9), (0.16, "E5", 0.8), (0.32, "G5", 0.85), (0.56, "B5", 0.7), (0.80, "C6", 0.9)],
                   2.8, chord=["C4", "E4", "G4", "C5"], chord_at=0.80)
    write(OUT / "jingle_intro.wav", intro)
    write(OUT / "jingle_outro.wav", outro)
    print("wrote", OUT / "jingle_intro.wav", OUT / "jingle_outro.wav")


if __name__ == "__main__":
    main()
