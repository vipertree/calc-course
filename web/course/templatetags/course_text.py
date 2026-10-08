import re

from django import template

register = template.Library()


@register.filter
def plaintext(s):
    """A title with TeX in it, as plain text for places math can't render (the browser tab):
    "Derivatives of $\\cos x$ and $e^x$" -> "Derivatives of cos x and e^x"."""
    s = re.sub(r"\\([A-Za-z]+)", r"\1", str(s))
    return s.replace("$", "").replace("{", "").replace("}", "")


@register.filter
def lesson_label(num):
    """ "2.1" stays "2.1"; a module lesson "0.3" shows as "T3"."""
    from course import content
    return content.label(str(num))


@register.filter
def unit_name(n):
    """ "Unit 4", or a module's own name (the trig review is never "Unit 0")."""
    from course import content
    for u in content.syllabus():
        if str(u["n"]) == str(n):
            return u["short"]
    return f"Unit {n}"


@register.filter
def work_name(num):
    """What a quiz or test row is called: "Topic 2.1 quiz", "T3 quiz", "Unit 4 test", "Trig Review test"."""
    num = str(num)
    if num.startswith("U"):
        return f"{unit_name(num[1:])} test"
    lab = lesson_label(num)
    return f"Topic {lab} quiz" if lab == num else f"{lab} quiz"
