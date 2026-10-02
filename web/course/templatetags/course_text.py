import re

from django import template

register = template.Library()


@register.filter
def plaintext(s):
    """A title with TeX in it, as plain text for places math can't render (the browser tab):
    "Derivatives of $\\cos x$ and $e^x$" -> "Derivatives of cos x and e^x"."""
    s = re.sub(r"\\([A-Za-z]+)", r"\1", str(s))
    return s.replace("$", "").replace("{", "").replace("}", "")
