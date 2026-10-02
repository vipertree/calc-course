"""Answer checking. Students type in MathLive; the page sends its ASCII-math output.

Numbers match within the item's tolerance (exact items allow float noise only).
Expressions match if sympy proves the difference is 0, or, failing that, if they
agree at several random points. Word blanks match after normalising case,
punctuation and articles.
"""
import random
import re

import sympy as sp
from sympy.parsing.sympy_parser import (convert_xor, implicit_multiplication_application,
                                        parse_expr, standard_transformations)

TRANSFORMS = standard_transformations + (implicit_multiplication_application, convert_xor)
FUNCS = {"sqrt": sp.sqrt, "sin": sp.sin, "cos": sp.cos, "tan": sp.tan, "sec": sp.sec, "csc": sp.csc,
         "cot": sp.cot, "ln": sp.log, "log": sp.log, "exp": sp.exp, "arcsin": sp.asin, "arccos": sp.acos,
         "arctan": sp.atan, "asin": sp.asin, "acos": sp.acos, "atan": sp.atan, "abs": sp.Abs}
NAMES = {"pi": sp.pi, "e": sp.E, "E": sp.E, **FUNCS}
ALLOWED = re.compile(r"^[0-9A-Za-z+\-*/^().,\s|π√·×−=']*$")


class Unreadable(ValueError):
    pass


def latex_to_ascii(s):
    """Our own answer strings are LaTeX ($-\\tfrac{9}{4}$). Turn that subset into ASCII math."""
    s = s.strip().strip("$").strip()
    s = s.replace(r"\left", "").replace(r"\right", "").replace(r"\,", "").replace(r"\ ", " ")
    s = re.sub(r"\\[dt]?frac", r"\\frac", s)
    s = re.sub(r"\\frac\s*(\d)\s*(\d)", r"\\frac{\1}{\2}", s)       # \frac12 -> \frac{1}{2}
    for _ in range(6):
        s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
        s = re.sub(r"\\sqrt\{([^{}]*)\}", r"sqrt(\1)", s)
        s = re.sub(r"\^\{([^{}]*)\}", r"^(\1)", s)
    s = s.replace(r"\pi", "pi").replace(r"\cdot", "*").replace(r"\times", "*")
    s = re.sub(r"\\(sin|cos|tan|sec|csc|cot|ln|log)", r"\1", s)
    s = s.replace("{", "(").replace("}", ")")
    return s


FN = r"(?:arcsin|arccos|arctan|asin|acos|atan|sin|cos|tan|sec|csc|cot|ln|log|exp|sqrt)"
UNIT_TEX = re.compile(r"(?:\\(?:text|mathrm|operatorname)\{[^{}]*\}(?:\^\{?\d+\}?)?)+|\^?\\circ|°")


def tidy(text):
    """Forgive the small things: unicode look-alikes, stray punctuation, thousands commas, Sin, sinx."""
    t = (text or "").strip().replace("\u00a0", " ")
    for a, b in (("²", "^2"), ("³", "^3"), ("⁻¹", "^(-1)"), ("–", "-"), ("—", "-"), ("−", "-"), ("÷", "/"),
                 ("∗", "*"), ("≈", ""), ("\\approx", "")):
        t = t.replace(a, b)
    t = t.strip().rstrip(".;,").strip()
    t = re.sub(r"(?i)\b(sin|cos|tan)\s*\^\s*\(?\s*-\s*1\s*\)?", r"arc\1", t)      # sin^(-1) x -> arcsin x
    t = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "", t)                 # 1,200 -> 1200
    t = re.sub(r"(?i)" + FN, lambda m: m.group(0).lower(), t)       # Sin, LN -> sin, ln
    t = re.sub(r"(?i)\bpi\b", "pi", t)
    t = re.sub(r"(?<![a-z\\])" + "(" + FN[3:-1] + r")(\d*\.?\d*[a-z]|\d+(?:\.\d+)?)(?![a-z(\d])", r"\1(\2)", t)   # sinx -> sin(x)
    return t


def to_sympy(text, var="x"):
    if text is None or not text.strip():
        raise Unreadable("empty")
    t = tidy(text)
    if "\\" in t:
        t = latex_to_ascii(t)
    t = t.replace("{", "(").replace("}", ")")
    # accept "y = ...", "f'(x) = ...", "dy/dx = ...", "k = 2" by keeping the right-hand side
    m = re.match(r"^\s*(dy/dx|[A-Za-z]\w*'*(?:\([^()=]*\))?)\s*=\s*(.+)$", t)
    if m:
        t = m.group(2)
    if len(t) > 200 or not ALLOWED.match(t):
        raise Unreadable(text)
    t = (t.replace("π", "pi").replace("√", "sqrt").replace("·", "*").replace("×", "*")
         .replace("−", "-"))
    t = re.sub(r"\|([^|]+)\|", r"abs(\1)", t)
    # decimals written with a leading dot: .5 -> 0.5
    t = re.sub(r"(?<![\d.])\.(\d)", r"0.\1", t)
    names = set(re.findall(r"[A-Za-z_]+", t))
    local = dict(NAMES)
    for n in names:
        if n not in local:
            if len(n) == 1:
                local[n] = sp.Symbol(n)
            elif n not in FUNCS:
                # allow implicit products of single letters like "xh"; parse_expr splits them
                for ch in n:
                    local.setdefault(ch, sp.Symbol(ch))
    try:
        return parse_expr(t, local_dict=local, transformations=TRANSFORMS, evaluate=True)
    except Exception as exc:  # noqa: BLE001  parse errors of every kind mean "couldn't read it"
        raise Unreadable(text) from exc


def _num(v):
    return complex(sp.N(v, 30))


DNE_WORDS = {"dne", "doesnotexist", "doesntexist", "nolimit", "none", "undefined"}
INF_WORDS = {"oo": sp.oo, "∞": sp.oo, "infinity": sp.oo, "inf": sp.oo, "+oo": sp.oo, "+∞": sp.oo, "+infinity": sp.oo,
             "-oo": -sp.oo, "-∞": -sp.oo, "-infinity": -sp.oo, "-inf": -sp.oo, "−∞": -sp.oo}


def _squash(s):
    return re.sub(r"[\s'’.]", "", (s or "").lower()).replace("\\infty", "∞").replace("\\mathrm", "")


def check_number(given, spec):
    g = _squash(given)
    if spec["value"] == "DNE":
        return g in DNE_WORDS
    if spec["value"] in ("oo", "-oo"):
        return INF_WORDS.get(g) == (sp.oo if spec["value"] == "oo" else -sp.oo)
    if g in DNE_WORDS or g in INF_WORDS:
        return False
    want = to_sympy(spec["value"])
    has_units = bool(UNIT_TEX.search(spec.get("display") or ""))
    if has_units:
        given = UNIT_TEX.sub(" ", given)
        # a plain-text unit after the number ("0.8 in/hr", "-1.5 gal/min^2"): keep the number
        m = re.match(r"^(.*?[\d)π])\s*([A-Za-z][A-Za-z/^()\d\s*·.\-]*)$", tidy(given))
        if m and not re.match(r"(?i)(" + FN[3:-1] + r"|pi|e\b|e\^)", m.group(2)):
            given = m.group(1)
    got = to_sympy(given)
    if got.free_symbols and has_units:
        # "40 m^2/hr" parses as 40*m**2/(h*r): keep the number, drop the unit letters
        num_part, unit_part = got.as_independent(*got.free_symbols, as_Add=False)
        if all(f.is_Symbol or (f.is_Pow and f.base.is_Symbol) for f in sp.Mul.make_args(unit_part)):
            got = num_part
    if got.free_symbols:
        return False
    tol = float(spec.get("tol") or 0)
    diff = abs(_num(got) - _num(want))
    if diff <= (tol if tol else 1e-9 * max(1, abs(_num(want)))):
        return True
    # an exact answer given as a decimal correct to three places (the AP standard) also counts
    decimals = re.search(r"\.(\d{3,})", tidy(given))
    return bool(decimals) and not want.is_integer and diff < 1e-3


def _solve_for_y(given, var):
    """'y - 8 = 12(x - 2)' -> 12x - 16. None if it isn't an equation we can solve for y."""
    t = tidy(given)
    if "\\" in t:
        t = latex_to_ascii(t)
    if t.count("=") != 1:
        return None
    lhs, rhs = t.split("=")
    if re.match(r"^\s*(dy/dx|[A-Za-z]\w*'*(?:\([^()=]*\))?)\s*$", lhs):
        return None          # "y = ...", "f'(x) = ...": to_sympy keeps the right side
    y = sp.Symbol("y")
    try:
        eq = to_sympy(lhs, var) - to_sympy(rhs, var)
    except Unreadable:
        return None
    if y not in eq.free_symbols:
        return None
    sols = sp.solve(eq, y)
    return sols[0] if len(sols) == 1 else None


def check_expr(given, spec):
    var = spec.get("var") or "x"
    want = to_sympy(spec["value"], var)
    solved = _solve_for_y(given, var)
    got = solved if solved is not None else to_sympy(given, var)
    if got.free_symbols - want.free_symbols:
        return False
    try:
        if sp.simplify(got - want) == 0:
            return True
    except Exception:  # noqa: BLE001
        pass
    syms = sorted(want.free_symbols | got.free_symbols, key=str)
    rng = random.Random(7)
    agree = 0
    for _ in range(12):
        pt = {s: sp.Rational(rng.randint(3, 97), 17) for s in syms}
        try:
            a, b = _num(want.subs(pt)), _num(got.subs(pt))
        except Exception:  # noqa: BLE001
            continue
        if abs(a - b) > 1e-7 * max(1, abs(a)):
            return False
        agree += 1
    return agree >= 5


_ART = re.compile(r"\b(the|a|an)\b")


def _norm(s):
    s = re.sub(r"\\[a-z]+\{([^{}]*)\}", r"\1", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
    s = _ART.sub(" ", s)
    return " ".join(s.split())


def check_words(given, answer):
    g, a = _norm(given), _norm(answer)
    if not g:
        return False
    if g == a:
        return True
    # singular/plural and small typos in long phrases
    if g.rstrip("s") == a.rstrip("s"):
        return True
    return len(a) > 12 and _close(g, a)


def _close(a, b):
    """Levenshtein distance <= 2."""
    if abs(len(a) - len(b)) > 2:
        return False
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1] <= 2


def _plain(s):
    """Normalized text for keys that aren't sympy expressions (0/0, intervals, f'(a))."""
    s = (s or "").lower().replace("$", "").replace("\\left", "").replace("\\right", "").replace(" ", "")
    s = re.sub(r"\\[dt]frac", r"\\frac", s)
    s = re.sub(r"\\frac\{?(\w)\}?\{?(\w)\}?", r"\1/\2", s)
    for inf in ("\\infty", "∞", "infinity", "inf"):
        s = s.replace(inf, "oo")
    return s.replace("{", "").replace("}", "").replace("(", "").replace(")", "").replace("−", "-")


DNE = {"does not exist", "doesnt exist", "doesn t exist", "dne", "does not exists", "nonexistent", "no limit"}


def check_blank(given, answer):
    """A notes blank: math if the key is in $...$, words otherwise. A check-box blank ("pick:") must match exactly;
    a "does not exist" blank also takes DNE."""
    if answer.startswith("pick:"):
        return (given or "").strip() == answer[5:]
    if _norm(answer) in DNE:
        return _norm(given) in DNE
    if answer.strip().startswith("$"):
        try:
            want = to_sympy(latex_to_ascii(answer))
            if want.has(sp.nan, sp.zoo) or want.free_symbols - {sp.Symbol("x")}:
                raise Unreadable(answer)
        except Exception:  # noqa: BLE001  not an ordinary expression: compare as text
            return _plain(given) == _plain(answer)
    a = answer.strip().strip("$").strip()
    if a in (r"\infty", r"+\infty", r"-\infty"):
        return check_number(given, {"value": "-oo" if a.startswith("-") else "oo"})
    if answer.strip().startswith("$"):
        try:
            return check_expr(given, {"value": latex_to_ascii(answer), "var": "x"})
        except Unreadable:
            return False
    return check_words(given, answer)


def check(given, spec):
    kind = spec["kind"]
    if kind == "choice":
        return (given or "").strip().upper() == spec["value"]
    if kind == "self":
        return None
    try:
        if kind == "number":
            return check_number(given, spec)
        return check_expr(given, spec)
    except Unreadable:
        return False
