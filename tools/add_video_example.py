"""Move a guided-notes example into the lesson video, so the notes and the video solve the same problem.

For each spec it
  * adds a transcript beat "## <title>" (with its On screen line and narration) right after the beat named `after`,
  * adds a matching self.example("<title>", problem, steps, ...) call to anim/sN_M.py, after that beat's self.clear(),
  * replaces the notes' Example("<title>", ...) block in content/topic_N_M.py with VideoExample("<title>", work=...).

A spec is a dict:
    num, title, after, problem (LaTeX for the screen and the notes), steps (board lines), at (narration line per step),
    lines (narration, line 0 states the problem and should end with [try it]), screen (the On screen description),
    optional: work (notes answer space), pre (scene code run just before the call, e.g. building a figure), extra (more
              keyword source for self.example: figure=..., text=..., notes_graph=...), checks (sympy check lines for the
              transcript), notes_title (the notes' old title, when the video renames it).

    from tools.add_video_example import apply
    apply([{...}, {...}])
"""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _slug(num):
    return num.replace(".", "_")


def _lit(x):
    """A Python raw-string literal for LaTeX text x (no escaping needed inside)."""
    if '"' not in x:
        return 'r"' + x + '"'
    if "'" not in x:
        return "r'" + x + "'"
    return repr(x)


def _call_end(s, i):
    """Index just past the self.example(...) call (and its line) starting at i."""
    depth, k = 0, s.index("(", i)
    for q in range(k, len(s)):
        depth += {"(": 1, ")": -1}.get(s[q], 0)
        if depth == 0:
            return s.index("\n", q) + 1


def _insertion_point(spec, s, placed):
    """Where the new call goes in the scene source: just after the clear() that ends the beat (or example) named `after`,
    and after any examples this tool already placed at that same spot, so they stay in spec order."""
    for key in (f'self.beat("{spec["after"]}")', f"self.beat({spec['after']!r})"):
        i = s.find(key)
        if i >= 0:
            j = s.index("\n        self.clear()\n", i) + len("\n        self.clear()\n")
            if s[j:].startswith("        self.title()\n"):
                j += len("        self.title()\n")
            break
    else:
        if spec["after"] == "Title":
            i = s.find("self.title()")
            j = s.index("\n", i) + 1
        else:
            for key in (f'self.example("{spec["after"]}"', f"self.example({spec['after']!r}"):
                i = s.find(key)
                if i >= 0:
                    break
            if i < 0:
                raise ValueError(f"{spec['num']}: no beat or example {spec['after']!r} in the scene")
            j = _call_end(s, i)
    while True:                                    # skip past calls (and their pre lines) placed earlier at this spot
        nxt = s[j:]
        hit = None
        for t, pre in placed:
            block = "".join(f"        {l}\n" for l in pre.splitlines() if l.strip())
            if nxt.startswith(block + f'        self.example("{t}"') or nxt.startswith(block + f"        self.example({t!r}"):
                hit = j + len(block)
                break
        if hit is None:
            return j
        j = _call_end(s, hit)


def _beat_before(s, j):
    """Name of the last beat or example that starts before index j in the scene source."""
    best, name = -1, None
    for m in re.finditer(r'self\.(?:beat|example)\((["\'])(.+?)\1', s[:j]):
        if m.start() > best:
            best, name = m.start(), m.group(2)
    if "self.title()" in s[:j] and s[:j].rfind("self.title()") > best:
        name = "Title"
    return name


def _scene(spec, placed):
    p = ROOT / "anim" / f"s{_slug(spec['num'])}.py"
    s = p.read_text()
    if f'self.example("{spec["title"]}"' in s or f"self.example({spec['title']!r}" in s:
        return _beat_before(s, s.find(spec["title"]))
    j = _insertion_point(spec, s, placed)
    anchor = _beat_before(s, j)
    steps = "[" + ", ".join(_lit(x) for x in spec["steps"]) + "]"
    extra = (", " + spec["extra"]) if spec.get("extra") else ""
    pre = "".join(f"        {l}\n" for l in spec.get("pre", "").splitlines() if l.strip())
    title = '"' + spec["title"] + '"' if '"' not in spec["title"] else repr(spec["title"])
    call = pre + f"        self.example({title}, {_lit(spec['problem'])},\n                     {steps}, at={spec['at']}{extra})\n"
    s = s[:j] + call + s[j:]
    p.write_text(s)
    placed.append((spec["title"], spec.get("pre", "")))
    return anchor


def _transcript(spec, anchor):
    """Add the beat right after `anchor` (the beat the scene plays just before the new example), keeping the
    transcript in the same order as the video."""
    p = ROOT / "transcripts" / f"{_slug(spec['num'])}.md"
    s = p.read_text()
    head = f"## {spec['title']}\n"
    if head not in s:
        m = re.search(rf"^## {re.escape(anchor)}\n", s, re.M)
        if not m:
            raise ValueError(f"{spec['num']}: no transcript beat {anchor!r}")
        nxt = re.search(r"^(## |# )", s[m.end():], re.M)
        at = m.end() + (nxt.start() if nxt else len(s) - m.end())
        body = head + f"**On screen:** {spec['screen']}\n" + "".join(f"> {l}\n" for l in spec["lines"]) + "\n"
        s = s[:at] + body + s[at:]
    for c in spec.get("checks", []):
        line = f"<!-- check: {c} -->"
        if line not in s:
            s = s.rstrip("\n") + "\n" + line + "\n"
    p.write_text(s)


def _notes(spec):
    p = ROOT / "content" / f"topic_{_slug(spec['num'])}.py"
    s = p.read_text()
    if f"VideoExample({spec['title']!r}" in s or f'VideoExample("{spec["title"]}"' in s:
        return
    tree = ast.parse(s)
    lines = s.splitlines(keepends=True)
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "Example" and n.args:
            t = n.args[0]
            title = t.value if isinstance(t, ast.Constant) else None
            if title == spec.get("notes_title", spec["title"]):
                indent = re.match(r"\s*", lines[n.lineno - 1]).group(0)
                tail = lines[n.end_lineno - 1][n.end_col_offset:]
                new = f'{indent}VideoExample({spec["title"]!r}, work="{spec.get("work", "2.6cm")}"){tail}'
                lines[n.lineno - 1:n.end_lineno] = [new]
                s = "".join(lines)
                if "VideoExample" not in s.split("NOTES")[0]:
                    s = re.sub(r"(from calclib import \()", r"\1VideoExample, ", s, count=1)
                p.write_text(s)
                return
    raise ValueError(f"{spec['num']}: no notes Example titled {spec.get('notes_title', spec['title'])!r}")


def apply(specs):
    placed = []
    for spec in specs:
        anchor = _scene(spec, placed)
        _transcript(spec, anchor)
        _notes(spec)
        print("moved", spec["num"], spec["title"], "after", anchor)
