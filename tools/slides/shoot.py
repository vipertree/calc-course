"""Screenshots of a built slide deck for the PowerPoint export (tools/build_slides.py runs this).

Runs under the system python3, which has playwright:
    LD_LIBRARY_PATH=$HOME/chromium-libs/root/usr/lib/x86_64-linux-gnu python3 tools/slides/shoot.py deck.html outdir [--theme paper]

Each slide is shot at 1920 x 1080 (times --scale) on a transparent page with its plain-text title and its video hidden:
PowerPoint gets the title as editable text and the clip as a real movie, placed where the page put them.
Writes outdir/slide-NN.png and outdir/shots.json ([{"png", "title", "titleText", "video", "errors"}, ...]).
"""
import argparse
import json
import os
import sys

from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("outdir")
    ap.add_argument("--theme", default="paper")
    ap.add_argument("--scale", type=float, default=1.5)
    ap.add_argument("--transparent", action="store_true", help="PowerPoint export: transparent page, title and video hidden")
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    url = "file://" + os.path.abspath(a.deck) + f"?theme={a.theme}" + ("&shot=1" if a.transparent else "")
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=a.scale)
        pg.on("pageerror", lambda e: print("page error:", e, file=sys.stderr))
        pg.goto(url)
        pg.wait_for_function("document.body.dataset.ready === '1'", timeout=60000)
        n = pg.evaluate("window.deckGo(0)")
        for i in range(n):
            pg.evaluate(f"window.deckGo({i})")
            pg.wait_for_timeout(60)
            info = pg.evaluate("window.deckInfo()")
            png = os.path.join(a.outdir, f"slide-{i + 1:02d}.png")
            pg.screenshot(path=png, omit_background=a.transparent)
            out.append(dict(info, png=png))
        b.close()
    with open(os.path.join(a.outdir, "shots.json"), "w") as f:
        json.dump(out, f, indent=1)
    bad = [i + 1 for i, s in enumerate(out) if s["errors"]]
    if bad:
        print(f"KaTeX errors on slides {bad}", file=sys.stderr)


if __name__ == "__main__":
    main()
