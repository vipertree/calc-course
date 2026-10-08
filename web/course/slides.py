"""Teacher slide decks, built by ../tools/build_slides.py into build/slides/<num>/ (off git, outside static/).

Only teacher accounts get them: the views check the role, and in production nginx serves the files from an internal
location after that check (settings.SLIDES_ACCEL, docs/teacher-slides.md). They are never under /static/.
"""
import json
import re

from django.conf import settings

VERSIONS = (("solutions", "Solutions shown"), ("blank", "Blank, to work live"))
# what a slide folder may hand out: the two decks, the PowerPoint files, and clips with their posters
FILE_RE = re.compile(r"^(deck-(solutions|blank)\.html|\d{1,2}\.\d{1,2}-slides-(solutions|blank)\.pptx|clips/[\w-]+\.(mp4|jpg))$")
TYPES = {".html": "text/html; charset=utf-8", ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
         ".mp4": "video/mp4", ".jpg": "image/jpeg"}


def folder(num):
    return settings.SLIDES_DIR / num


def manifest(num):
    """What tools/build_slides.py made for this topic, or None if it has no deck."""
    p = folder(num) / "manifest.json"
    if not p.is_file():
        return None
    try:
        m = json.loads(p.read_text())
    except ValueError:
        return None
    return m if m.get("versions") else None


def available():
    d = settings.SLIDES_DIR
    return {p.parent.name for p in d.glob("*/manifest.json")} if d.is_dir() else set()


def path_for(num, name):
    """The file for a request, or None if the name isn't one a deck folder hands out."""
    if not FILE_RE.fullmatch(name):
        return None
    base = folder(num).resolve()
    p = (base / name).resolve()
    if base not in p.parents or not p.is_file():
        return None
    return p
