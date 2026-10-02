"""Render every lesson tab in chromium and report visible text outside KaTeX that looks like LaTeX, plus KaTeX errors.

    LD_LIBRARY_PATH=$HOME/chromium-libs/root/usr/lib/x86_64-linux-gnu python3 tools/page_scan.py <user> <password>

Needs the dev server on :8018. Lone dollar signs (prices) and the practice typing hint are expected and skipped."""
import json, re, sys, glob, os
from playwright.sync_api import sync_playwright
BASE = "http://localhost:8018"
nums = sorted({os.path.basename(f)[:-5].replace("_", ".") for f in glob.glob(os.path.join(os.path.dirname(__file__), "..", "web", "course", "content", "*.json"))
               if not os.path.basename(f).startswith("U")}, key=lambda s: [int(x) for x in s.split(".")])
pages = [f"/topic/{n}/{a}" for n in nums for a in ("", "practice/", "testprep/", "quiz/")] + [f"/unit/U{u}/test/" for u in range(1, 6)]
JS = r"""() => {
  const out = [];
  const bad = /\\[A-Za-z]+|[{}^]|\$|\\\[|\\\]|\\\(|\\\)/;
  const w = document.createTreeWalker(document.querySelector('main') || document.body, NodeFilter.SHOW_TEXT, {
    acceptNode(n) {
      const p = n.parentElement;
      if (!p || p.closest('.katex, script, style, textarea, .desmos-box, svg, math-field, .ML__container')) return NodeFilter.FILTER_REJECT;
      return bad.test(n.nodeValue) ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
    }});
  let n; while ((n = w.nextNode())) out.push(n.nodeValue.trim().slice(0, 160));
  document.querySelectorAll('.katex-error').forEach(e => out.push('KATEX-ERROR: ' + (e.getAttribute('title') || '') + ' :: ' + e.textContent.slice(0, 100)));
  return out;
}"""
res = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 900})
    pg.goto(BASE + "/login/"); pg.fill("#id_username", sys.argv[1]); pg.fill("#id_password", sys.argv[2]); pg.click("button.primary")
    pg.wait_for_load_state("networkidle")
    for u in pages:
        pg.goto(BASE + u); pg.wait_for_timeout(1200)
        found = [t for t in pg.evaluate(JS) if t != "$" and not t.startswith("Enter your final answer")]
        if found: res[u] = found
    b.close()
print(sum(len(v) for v in res.values()), "hits on", len(res), "of", len(pages), "pages")
json.dump(res, open(os.path.join(os.path.dirname(__file__), "..", "build", "page_scan.json"), "w"), indent=1)
for u, v in res.items():
    for t in v[:4]: print(u, "|", t)
