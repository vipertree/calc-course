"""Review guided notes the way a student sees them, and flag what Adder keeps catching by eye.

    python tools/notes_review.py 1.1 1.2 ...      # or "all"
        [--shots DIR]   save full-page screenshots of each lesson's notes there (needs the dev server on :8018)
        [--no-browser]  static checks only

Static checks (web/course/content/<n>.json, as built by `build.py --web`):
  - raw TeX that escaped rendering (\\hfill, \\small, $$, stray backslash commands outside math)
  - long or tall inline math that should be a centered display line
  - blanks inside tables (tables are for data; blanks are for big ideas)
  - every worked example from the video has made it into the notes
Browser checks (headless Chromium, logged in as the demo student):
  - KaTeX errors on the page, blocks wider than the column (horizontal overflow)
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
CONTENT = ROOT / "web" / "course" / "content"
BASE = "http://localhost:8018"

INLINE = re.compile(r"(?<![\\$])\$(?!\$)(.+?)(?<!\\)\$")
TALL = re.compile(r"\\(dfrac|displaystyle|lim|sum|int|begin\{cases\}|begin\{array\})")
RAW = re.compile(r"\\(hfill|small|footnotesize|par|vspace|hspace|newline|noindent)\b|\$\$")


def text_outside_math(html):
    return re.sub(r"\\\[.*?\\\]|\\\(.*?\\\)|\$[^$]*\$", " ", html, flags=re.S)


def static(num):
    data = json.loads((CONTENT / f"{num.replace('.', '_')}.json").read_text())["public"]
    out = []
    for si, step in enumerate(data["steps"]):
        where = f"§{si + 1} {re.sub('<.*?>', '', step['title'])}"
        for b in step["blocks"]:
            html = b.get("html", "") or ""
            if b["type"] == "table" and "data-blank" in html:
                out.append((where, "blanks inside a table: fill the data in, keep blanks for big ideas"))
            outside = text_outside_math(re.sub(r"<[^>]+>", " ", html))
            m = RAW.search(outside)
            if m:
                out.append((where, f"raw TeX shows as text: {m.group(0)!r}"))
            # display lines that hold blanks are rendered as centered display-style pieces: not inline math
            for m in INLINE.finditer(re.sub(r"<span class='dline'>.*?</span>", " ", html, flags=re.S)):
                tex = m.group(1)
                if b["type"] in ("table", "figure") or "<span" in tex:
                    continue                                  # tables, and math wrapped around a blank
                if len(tex) > 55:
                    out.append((where, f"long inline math, put it on its own line: ${tex[:60]}...$"))
                elif TALL.search(tex) and len(tex) > 25:
                    out.append((where, f"tall inline math (fractions/limits), consider a display line: ${tex}$"))
    from calclib.videx import video_examples
    vids = video_examples(num)
    titles = [re.sub("<.*?>", "", s["title"]) for s in data["steps"]]
    if vids and "Worked examples" not in titles:
        out.append(("notes", f"{len(vids)} video examples are missing from the notes (rebuild with build.py --web)"))
    return out


def browser(nums, shots):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        br = p.chromium.launch()
        ctx = br.new_context(viewport={"width": 1400, "height": 900})
        pg = ctx.new_page()
        pg.goto(BASE + "/login/")
        pg.fill("input[name=username]", "demo-student")
        pg.fill("input[name=password]", "demo-student-pw")
        pg.click("form button")
        pg.wait_for_load_state()
        for num in nums:
            pg.goto(f"{BASE}/topic/{num}/")
            pg.wait_for_selector(".step", timeout=15000)
            pg.wait_for_timeout(1500)                      # KaTeX, MathLive and figures settle
            found = pg.evaluate("""() => {
                const r = [];
                document.querySelectorAll('.katex-error').forEach(e => r.push('KaTeX error: ' + (e.title || e.textContent).slice(0, 120)));
                document.querySelectorAll('.step .block, .step .card').forEach(e => {
                    if (e.scrollWidth > e.clientWidth + 4) r.push('wider than the column: ' + e.textContent.trim().slice(0, 80));
                });
                return r; }""")
            out[num] = found
            if shots:
                Path(shots).mkdir(parents=True, exist_ok=True)
                pg.screenshot(path=str(Path(shots) / f"notes_{num.replace('.', '_')}.png"), full_page=True)
        br.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("topics", nargs="+")
    ap.add_argument("--shots")
    ap.add_argument("--no-browser", action="store_true")
    a = ap.parse_args()
    nums = a.topics
    if nums == ["all"]:
        nums = sorted((p.stem.replace("_", ".") for p in CONTENT.glob("[0-9]*.json")), key=lambda s: [int(x) for x in s.split(".")])
    live = {} if a.no_browser else browser(nums, a.shots)
    total = 0
    for num in nums:
        issues = static(num) + [("page", s) for s in live.get(num, [])]
        total += len(issues)
        print(f"{num}: {len(issues)} issue{'s' if len(issues) != 1 else ''}")
        for where, msg in issues:
            print(f"   {where}: {msg}")
    print(f"total {total}")


if __name__ == "__main__":
    main()
