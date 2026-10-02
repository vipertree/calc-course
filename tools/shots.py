"""Screenshot the site in every theme: python3 tools/shots.py [outdir] [--base http://localhost:8018]"""
import os
import sys

LIBS = os.path.expanduser("~/chromium-libs/root/usr/lib/x86_64-linux-gnu")
os.environ["LD_LIBRARY_PATH"] = LIBS + ":" + os.environ.get("LD_LIBRARY_PATH", "")
from playwright.sync_api import sync_playwright  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "shots"
BASE = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "http://localhost:8018"
CODE = os.environ.get("JOIN_CODE", "")
os.makedirs(OUT, exist_ok=True)


def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
        page = ctx.new_page()
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("dialog", lambda d: errors.append("DIALOG " + d.message))
        page.goto(BASE + "/login/")
        page.fill("#id_username", os.environ.get("SHOT_USER", "demo-student"))
        page.fill("#id_password", os.environ.get("SHOT_PASS", "demo-student-pw"))
        page.click("button.primary")
        page.wait_for_load_state("networkidle")
        for theme in ["slate", "paper", "studio"]:
            page.goto(f"{BASE}/theme/{theme}/?next=/course/")
            for name, path in [("map", "/course/"), ("notes", "/topic/2.1/"), ("practice", "/topic/2.1/practice/"),
                               ("quiz", "/topic/2.1/quiz/"), ("testprep", "/topic/2.1/testprep/")]:
                page.goto(BASE + path)
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(1500)
                page.screenshot(path=f"{OUT}/{theme}-{name}.png", full_page=True)
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto(BASE + "/topic/2.1/")
        page.wait_for_timeout(1500)
        page.screenshot(path=f"{OUT}/mobile-notes.png", full_page=False)
        print("errors:", errors or "none")
        b.close()


main()
