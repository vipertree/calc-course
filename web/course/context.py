from django.conf import settings

from accounts.models import has_full_access

THEMES = [("slate", "Dark"), ("paper", "Light")]
# Alternate front-end designs (see web/design/BRIEFS.md). "classic" is the original look.
DESIGNS = [("classic", "Classic"), ("transit", "Transit"), ("drafting", "Drafting"),
           ("textbook", "Textbook"), ("chalk", "Chalkboard"), ("safety", "Safety card"), ("board", "Chalkboard (new)")]
DESIGN_FONTS = {
    "transit": "family=Public+Sans:ital,wght@0,400..900;1,400..700",
    "drafting": "family=B612:ital,wght@0,400;0,700;1,400&family=Barlow:ital,wght@0,400;0,600;1,400&family=Barlow+Semi+Condensed:wght@500;600",
    "textbook": "",   # Computer Modern comes from the KaTeX stylesheet already on every page
    "chalk": "family=Kalam:wght@400;700&family=Lexend:wght@400;500;600",
    "safety": "family=Bitter:wght@500;700;800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400",
    "board": "family=Young+Serif&family=Hanken+Grotesk:ital,wght@0,400;0,600;0,700;1,400&family=Kalam:wght@400;700",
}


# The top bar (Adder 2026-10-12): Calculus, Trigonometry and Videos, shown either as plain links or as three
# dropdowns; the viewer picks with NAV_STYLES (cookie "nav"). Entries are (label, url name, url name args, anchor).
NAV_STYLES = [("links", "Links"), ("menus", "Dropdowns")]
NAV = [
    ("Calculus", [("AP Calc Course", "map"), ("Calc Formula Sheet", "formulas"), ("AP Calc Practice Exams", "exams")]),
    ("Trigonometry", [("Trig Course", "trig"), ("Trig Formulas", "trig_formulas")]),
    ("Videos", [("All videos", "videos")]),
]


def _nav(request, profile):
    from django.urls import reverse
    here = getattr(getattr(request, "resolver_match", None), "url_name", "")
    groups = [{"name": g, "items": [{"label": l, "url": reverse(n), "on": n == here} for l, n in items]}
              for g, items in NAV]
    for g in groups:
        g["on"] = any(i["on"] for i in g["items"])
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
    design = request.COOKIES.get("design", "classic")
    if design not in dict(DESIGNS):
        design = "classic"
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None
    nav_style = request.COOKIES.get("nav", "links")
    if nav_style not in dict(NAV_STYLES):
        nav_style = "links"
    nav_groups, nav_dash = _nav(request, profile)
    return {"ASSET_V": _asset_version(), "THEME": theme, "THEMES": THEMES,
            "DESIGN": design, "DESIGNS": DESIGNS, "NAV": nav_groups, "NAV_DASH": nav_dash,
            "NAV_STYLE": nav_style, "NAV_STYLES": NAV_STYLES, "DESIGN_FONTS": DESIGN_FONTS.get(design, ""),
            "DESMOS_API_KEY": settings.DESMOS_API_KEY,
            "PROFILE": profile, "IS_TEACHER": bool(profile and profile.is_teacher),
            "FULL_ACCESS": has_full_access(request.user),
            "CSP_NONCE": getattr(request, "csp_nonce", ""),
            "LEGAL_REVIEWED": settings.LEGAL_PAGES_REVIEWED, "CONTACT_EMAIL": settings.CONTACT_EMAIL,
            "BACKUP_DAYS": settings.BACKUP_DAYS, "UNVERIFIED_DAYS": settings.UNVERIFIED_ACCOUNT_DAYS}
