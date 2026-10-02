"""Review published lesson videos: a contact sheet per video, plus a still at every layout problem the render logged.

    python tools/video_review.py 1.1 1.2 ...  [--out DIR]      # or "all"

For each topic it writes to DIR (default /tmp/video_review):
  sheet_<slug>.png    24 evenly spaced frames, 6x4: scan for clutter, leftovers from earlier scenes, empty stretches
  issue_<slug>_NN.png the frame at each moment the render's layout audit flagged (text on text or on a picture,
                      or anything outside the visible frame), with what collided printed below
The audit itself runs inside every render (anim/kit.py, TranscriptScene._audit) and is saved next to the media as
anim/media/pub_<slug>/layout_<slug>.json. Overlaps inside one group (a table's own cells, a formula's own parts)
are not reported; overlaps between separately placed things are.
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VIDEO = ROOT / "web" / "static" / "video"
MEDIA = ROOT / "anim" / "media"
BIN = Path.home() / "opt" / "mamba" / "envs" / "calc" / "bin"


def duration(mp4):
    out = subprocess.run([str(BIN / "ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(mp4)],
                         capture_output=True, text=True).stdout.strip()
    return float(out or 0)


def frame(mp4, t, dest):
    subprocess.run([str(BIN / "ffmpeg"), "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", str(mp4), "-frames:v", "1", str(dest)], check=True)


def review(num, out):
    slug = num.replace(".", "_")
    mp4 = VIDEO / f"{slug}.mp4"
    if not mp4.exists():
        print(f"{num}: no published video")
        return
    d = duration(mp4)
    subprocess.run([str(BIN / "ffmpeg"), "-v", "error", "-y", "-i", str(mp4), "-vf", f"fps=24/{d},scale=320:-1,tile=6x4",
                    "-frames:v", "1", str(out / f"sheet_{slug}.png")], check=True)
    audit = MEDIA / f"pub_{slug}" / f"layout_{slug}.json"
    issues = json.loads(audit.read_text()) if audit.exists() else None
    if audit.exists() and audit.stat().st_mtime < mp4.stat().st_mtime - 600:
        print(f"{num}: warning, the layout audit is older than the video")
    print(f"{num}: {d / 60:.1f} min, sheet_{slug}.png, "
          + ("no layout audit (render predates it)" if issues is None else f"{len(issues)} layout issue(s)"))
    for k, it in enumerate(issues or [], 1):
        frame(mp4, min(it["t"] + 0.1, d - 0.1), out / f"issue_{slug}_{k:02d}.png")
        print(f"   {k:02d}  t={it['t']:6.1f}s  [{it['beat']}]  {it['kind']}: " + "  <->  ".join(it["what"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topics", nargs="+")
    ap.add_argument("--out", default="/tmp/video_review")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    nums = a.topics
    if nums == ["all"]:
        nums = sorted((p.stem.replace("_", ".") for p in VIDEO.glob("*.mp4") if not p.stem.endswith("-dark")), key=lambda s: [int(x) for x in s.split(".")])
    for num in nums:
        review(num, out)


if __name__ == "__main__":
    main()
