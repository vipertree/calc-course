#!/usr/bin/env python3
"""Mirror Adder's AP Calculus FRQ archive (https://adderoaks.com/calcfrq/) into build/frq/raw/.

The archive is a small custom file server (adderoaks repo, calcfrq-server.py). Its directory pages list only
PDFs and folders whose names do not start with "_", so the full exam sets in /_AB/<year>/ and /_BC/<year>/ never
show on the home page. They are still served, so we crawl them too. Names follow two schemes:

    <CATEGORY>/<year>-<AB|BC>-Q<n>.pdf     the seven question-type folders (Adder's sorting)
    _AB/<year>/Q<n>.pdf, _BC/<year>/Q<n>.pdf   the exam sets, by year (_BC holds only BC-only questions)

Each PDF is the College Board question followed by its scoring guidelines (tools/build_frq_archive.py splits
them). Crawling is sequential with a short pause and a clear User-Agent; a file already on disk with the size the
server reports is skipped, so a rerun only fetches what changed. Stdlib only.

    python3 tools/fetch_frq_archive.py              # crawl and download
    python3 tools/fetch_frq_archive.py --dry-run    # list what would be fetched
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "https://adderoaks.com/calcfrq/"
REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "build" / "frq" / "raw"
UA = "MrOaksMath-FRQ-mirror/1.0 (calc-course tools/fetch_frq_archive.py; owner: adderoaks.com)"
# Folders the listings hide (leading underscore) but the server serves.
HIDDEN_ROOTS = ["_AB/", "_BC/"]
DELAY = 0.4

HREF = re.compile(r'href="([^"]+)"')


def get(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.status, dict(r.headers), (r.read() if method == "GET" else b"")


def listing(rel):
    """Child folders and PDF files of the directory page at BASE + rel (rel ends with "/")."""
    _, _, body = get(BASE + rel)
    dirs, files = [], []
    for href in HREF.findall(body.decode("utf-8", "replace")):
        if href.startswith(("/", "http", "#", "?")) or ".." in href:
            continue   # absolute links are the brand, breadcrumbs, favicon and fonts
        name = urllib.parse.unquote(href)
        (dirs if name.endswith("/") else files).append(name)
    return dirs, files


def crawl():
    """Every file under the archive, as relative paths, breadth first."""
    queue, seen, found = [""] + HIDDEN_ROOTS, set(), []
    while queue:
        rel = queue.pop(0)
        if rel in seen:
            continue
        seen.add(rel)
        try:
            dirs, files = listing(rel)
        except urllib.error.HTTPError as e:
            print(f"  listing {rel or '/'}: HTTP {e.code}", file=sys.stderr)
            continue
        print(f"  {rel or '/'}: {len(dirs)} folders, {len(files)} files")
        queue += [rel + d for d in dirs]
        found += [rel + f for f in files]
        time.sleep(DELAY)
    return found


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args()

    print(f"Crawling {BASE}")
    files = crawl()
    print(f"{len(files)} files listed")
    if args.dry_run:
        print("\n".join(files))
        return
    fetched = skipped = failed = 0
    log = []
    for rel in files:
        dest = args.out / rel
        url = BASE + urllib.parse.quote(rel)
        try:
            if dest.exists():
                _, head, _ = get(url, "HEAD")
                if int(head.get("Content-Length", -1)) == dest.stat().st_size:
                    skipped += 1
                    continue
                time.sleep(DELAY)
            _, head, body = get(url)
        except urllib.error.HTTPError as e:
            print(f"  FAILED {rel}: HTTP {e.code}", file=sys.stderr)
            log.append({"path": rel, "error": e.code})
            failed += 1
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(dest.suffix + ".part")
        tmp.write_bytes(body)
        tmp.replace(dest)
        fetched += 1
        print(f"  {rel}  {len(body):,} bytes")
        time.sleep(DELAY)
    (args.out.parent / "fetch.json").write_text(json.dumps(
        {"source": BASE, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
         "files": files, "errors": log}, indent=1))
    print(f"done: {fetched} fetched, {skipped} unchanged, {failed} failed -> {args.out}")


if __name__ == "__main__":
    main()
