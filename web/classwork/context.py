from django.urls import reverse


def tabs(request):
    """The class tabs, for any page that has a class `c` (templates/classwork/_nav.html)."""
    m = getattr(request, "resolver_match", None)
    pk = m and m.kwargs.get("pk")
    if not pk or not (m.url_name or "").startswith("cw_"):
        return {}
    return {"cw_tabs": [(k, label, reverse(name, args=[pk])) for k, label, name in (
        ("home", "Home", "cw_home"), ("progress", "Progress", "cw_progress"), ("quizzes", "Quizzes and tests", "cw_quizzes"),
        ("calendar", "Calendar", "cw_calendar"), ("students", "Students", "cw_students"), ("setup", "Setup", "cw_setup"))]}
