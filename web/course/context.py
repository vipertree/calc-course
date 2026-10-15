from functools import lru_cache

from django.conf import settings

from accounts.models import has_full_access

THEMES = [("slate", "Dark"), ("paper", "Light")]
# The site design. Adder 2026-10-15: Safety card it is; the Design menu is gone and the other looks are mothballed
# (their stylesheets stay in static/css/designs/ and web/design/BRIEFS.md; add one back here to revive it).
DESIGN = "safety"
MOTHBALLED_DESIGNS = [("classic", "Classic"), ("transit", "Transit"), ("drafting", "Drafting"),
           ("textbook", "Textbook"), ("chalk", "Chalkboard"), ("safety", "Safety card"), ("board", "Chalkboard (new)")]
DESIGN_FONTS = {
    "transit": "family=Public+Sans:ital,wght@0,400..900;1,400..700",
    "drafting": "family=B612:ital,wght@0,400;0,700;1,400&family=Barlow:ital,wght@0,400;0,600;1,400&family=Barlow+Semi+Condensed:wght@500;600",
    "textbook": "",   # Computer Modern comes from the KaTeX stylesheet already on every page
    "chalk": "family=Kalam:wght@400;700&family=Lexend:wght@400;500;600",
    "safety": "family=Bitter:wght@500;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400",
    "board": "family=Young+Serif&family=Hanken+Grotesk:ital,wght@0,400;0,600;0,700;1,400&family=Kalam:wght@400;700",
}


# The top bar: Calculus, Trigonometry and Videos as three dropdowns (Adder 2026-10-15 settled on dropdowns over
# plain links). Entries are (label, url name).
NAV = [
    ("Calculus", [("AP Calc Course", "map"), ("Calc Formula Sheet", "formulas"), ("AP Calc Practice Exams", "exams"),
                  ("AP FRQ Archive", "frq")]),     # shown only when settings.FRQ_ARCHIVE is on
    ("Trigonometry", [("Trig Course", "trig"), ("Trig Formulas", "trig_formulas")]),
    ("Videos", [("All videos", "videos")]),
]


def _published_videos():
    """Lesson slugs with a published video, re-read only when the video folder changes."""
    d = settings.VIDEO_DIR
    return _video_slugs(str(d), d.stat().st_mtime) if d.exists() else frozenset()


@lru_cache(maxsize=4)
def _video_slugs(path, mtime):
    from pathlib import Path
    return frozenset(p.stem for p in Path(path).glob("*.mp4") if not p.stem.endswith("-dark"))


def _course_tree(module, full):
    """The flyout under AP Calc Course (units, each with its lessons and unit test) or Trig Course (its lessons).
    Adder 2026-10-15: hover a course, then a unit, to reach any lesson."""
    from django.urls import reverse
    from . import content
    have, tests = content.available(), content.unit_tests()
    base = reverse("trig" if module else "map")

    def lessons(u):
        out = [{"label": t["label"], "title": t["title"], "url": reverse("lesson", args=[t["n"]]) if t["n"] in have else ""}
               for t in u["topics"]]
        if u["n"] in tests:
            out.append({"label": "Test", "title": f"{u['short']} test", "url": reverse("unit_test", args=[f"U{u['n']}"])})
        return out

    units = [u for u in content.syllabus() if u["module"] == module]
    if module:
        return [l for u in units for l in lessons(u)]
    return [{"label": u["short"], "title": u["title"], "url": f"{base}#unit-{u['n']}", "bc": u["bc"],
             "locked": not u["free"] and not full, "children": lessons(u)} for u in units]


def _video_tree():
    """The Videos dropdown below All videos: the trig module, then Units 1-10, each with a flyout of its published
    lesson videos; a video opens on the Videos page (/videos/#2.1). Adder 2026-10-15."""
    from django.urls import reverse
    from . import content
    have, base = _published_videos(), reverse("videos")
    out = []
    for u in sorted(content.syllabus(), key=lambda u: (not u["module"], u["n"])):
        vids = [{"label": t["label"], "title": t["title"], "url": f"{base}#{t['n']}"}
                for t in u["topics"] if content.slug(t["n"]) in have]
        if vids:
            out.append({"label": u["short"], "url": vids[0]["url"], "on": False, "children": vids})
    return out


def _nav(request, profile, full=False):
    from django.urls import reverse
    here = getattr(getattr(request, "resolver_match", None), "url_name", "")
    trees = {"map": lambda: _course_tree(False, full), "trig": lambda: _course_tree(True, full)}
    groups = [{"name": g, "items": [{"label": l, "url": reverse(n), "on": n == here,
                                     "children": trees[n]() if n in trees else []} for l, n in items
                                    if n != "frq" or settings.FRQ_ARCHIVE]}
              for g, items in NAV]
    for g in groups:
        g["on"] = any(i["on"] for i in g["items"])
        if g["name"] == "Videos":            # All videos, then Trig Review and Units 1-10, each opening its videos
            g["items"] += _video_tree()
    dash = None
    if request.user.is_authenticated:
        if profile and profile.is_teacher:
            dash = {"label": "Teacher Dashboard", "url": reverse("teacher"), "on": here == "teacher"}
        else:
            dash = {"label": "Student Dashboard", "url": reverse("student_dashboard"), "on": here == "student_dashboard"}
    return groups, dash


def _asset_version():
    """Dev only: the newest CSS/JS mtime, appended as ?v= so the browser never keeps a stale stylesheet after an
    edit. Production needs none: the manifest storage puts a content hash in every static file name."""
    if not settings.DEBUG:
        return ""
    import glob, os
    files = glob.glob(str(settings.BASE_DIR / "static" / "css" / "**" / "*.css"), recursive=True) + \
        glob.glob(str(settings.BASE_DIR / "static" / "js" / "*.js"))
    return str(int(max((os.path.getmtime(f) for f in files), default=0)))


def site(request):
    theme = request.COOKIES.get("theme", "")
    if theme not in dict(THEMES):
        theme = ""          # empty: the page picks dark or light from the device setting
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None
    full = has_full_access(request.user)
    nav_groups, nav_dash = _nav(request, profile, full)
    return {"ASSET_V": _asset_version(), "THEME": theme, "THEMES": THEMES,
            "DESIGN": DESIGN, "NAV": nav_groups, "NAV_DASH": nav_dash,
            "FRQ_ARCHIVE": settings.FRQ_ARCHIVE, "DESIGN_FONTS": DESIGN_FONTS[DESIGN],
            "DESMOS_API_KEY": settings.DESMOS_API_KEY,
            "PROFILE": profile, "IS_TEACHER": bool(profile and profile.is_teacher),
            "FULL_ACCESS": full,
            "CSP_NONCE": getattr(request, "csp_nonce", ""),
            "LEGAL_REVIEWED": settings.LEGAL_PAGES_REVIEWED, "CONTACT_EMAIL": settings.CONTACT_EMAIL,
            "BACKUP_DAYS": settings.BACKUP_DAYS, "UNVERIFIED_DAYS": settings.UNVERIFIED_ACCOUNT_DAYS}
