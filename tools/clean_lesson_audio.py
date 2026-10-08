#!/usr/bin/env python3
"""Create cleaned, de-noised audio masters and cut clear slate/retake segments."""

import subprocess
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORDINGS = ROOT / "voice" / "adder-lesson-recordings"
OUTPUT = RECORDINGS / "cleaned"

# Cleaning no longer cuts anything: retakes are found by reading the transcript (tools/cut_retakes.py), and
# one-off cuts (slates, an isolated "huh") live in voice/aligned/<slug>.cuts.json as "add" spans. Cleaning keeps the
# recording's clock, so those times are the same in the original and the cleaned master.
CUTS = {}


def make_master(slug, cuts):
    source = RECORDINGS / slug
    destination = OUTPUT / f"{slug}.wav"
    probe = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(source), "-f", "null", "-"],
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True, check=True,
    )
    stamps = re.findall(r"time=([0-9:.]+)", probe.stderr)
    if not stamps:
        raise RuntimeError(f"Could not read duration for {source}")
    hours, minutes, seconds = stamps[-1].split(":")
    duration = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

    spans = []
    cursor = 0.0
    for start, end in cuts:
        if start < cursor or end <= start or end > duration:
            raise ValueError(f"Invalid edit for {slug}: {start}-{end}")
        spans.append((cursor, start))
        cursor = end
    spans.append((cursor, duration))

    filters = []
    labels = []
    for index, (start, end) in enumerate(spans):
        label = f"a{index}"
        length = end - start
        filters.append(
            f"[0:a]atrim=start={start:.6f}:end={end:.6f},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d=0.008,afade=t=out:st={max(length - 0.008, 0):.6f}:d=0.008[{label}]"
        )
        labels.append(f"[{label}]")

    filters.append(
        f"{''.join(labels)}concat=n={len(spans)}:v=0:a=1[edited];"
        "[edited]highpass=f=75,lowpass=f=16000,afftdn=nr=8:nf=-50:tn=1,"
        "acompressor=threshold=-25dB:ratio=2.5:attack=15:release=250:makeup=6,"
        "loudnorm=I=-18:LRA=11:TP=-1.5,aresample=48000,aformat=channel_layouts=mono[out]"
    )
    subprocess.run([
        "ffmpeg", "-hide_banner", "-y", "-i", str(source),
        "-filter_complex", ";".join(filters), "-map", "[out]",
        "-c:a", "pcm_s24le", str(destination),
    ], check=True)
    removed = sum(end - start for start, end in cuts)
    print(f"{destination}: removed {removed:.2f}s from {duration:.2f}s source")


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    import sys
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    for source in sorted(p for p in RECORDINGS.iterdir() if p.is_file()):
        if only is None or source.name == only:
            make_master(source.name, CUTS.get(source.name, []))
