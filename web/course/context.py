from django.conf import settings

from accounts.models import has_full_access

THEMES = [("slate", "Dark"), ("paper", "Light")]
# Alternate front-end designs (see web/design/BRIEFS.md). "classic" is the original look.
DESIGNS = [("classic", "Classic"), ("transit", "Transit"), ("drafting", "Drafting"),
           ("textbook", "Textbook"), ("chalk", "Chalkboard")]
# Transit course map: "rows" keeps the reading order across each row and bends the route line along it;
# "columns" lays the stations out down each column, so the vertical lines match the order.
MAP_LAYOUTS = [("rows", "Rows"), ("columns", "Columns")]
DESIGN_FONTS = {
    "transit": "family=Public+Sans:ital,wght@0,400..900;1,400..700",
    "drafting": "family=B612:ital,wght@0,400;0,700;1,400&family=Barlow:ital,wght@0,400;0,600;1,400&family=Barlow+Semi+Condensed:wght@500;600",
    "textbook": "",   # Computer Modern comes from the KaTeX stylesheet already on every page
    "chalk": "family=Kalam:wght@400;700&family=Lexend:wght@400;500;600",
}


def site(request):
    theme = request.COOKIES.get("theme", "")
    if theme not in dict(THEMES):
        theme = ""          # empty: the page picks dark or light from the device setting
    design = request.COOKIES.get("design", "classic")
    if design not in dict(DESIGNS):
        design = "classic"
    map_layout = request.COOKIES.get("maplayout", "rows")
    if map_layout not in dict(MAP_LAYOUTS):
        map_layout = "rows"
    profile = getattr(request.user, "profile", None) if request.user.is_authenticated else None
    return {"THEME": theme, "THEMES": THEMES,
            "DESIGN": design, "DESIGNS": DESIGNS, "DESIGN_FONTS": DESIGN_FONTS.get(design, ""),
            "MAP_LAYOUT": map_layout, "MAP_LAYOUTS": MAP_LAYOUTS, "DESMOS_API_KEY": settings.DESMOS_API_KEY,
            "PROFILE": profile, "IS_TEACHER": bool(profile and profile.is_teacher),
            "FULL_ACCESS": has_full_access(request.user)}
