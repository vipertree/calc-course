"""The worked examples solved on screen in each lesson video, read straight from the manim scene (anim/sN_M.py).

Every video example also appears in the guided notes, so students can work it on paper. Reading the scene's own
`self.example(...)` calls keeps the two from drifting apart: change a problem in the video and the notes follow.

A call's problem is its second argument when that is a string. When the scene shows a mobject instead (a table,
say), the call must also pass `text=` with the problem as LaTeX for the page. A problem that needs its graph passes
`notes_graph={...}`: a literal dict of calclib.figs.graph arguments, drawn above the example in the notes. Steps are the scene's board lines:
math by default, "TEXT:..." for a sentence, "PART:..." for the next part of a multi-part question.
"""
import ast
from pathlib import Path

ANIM = Path(__file__).resolve().parent.parent / "anim"


def _const(node):
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def video_examples(number, lesson=False):
    """[(title, problem_tex, [step, ...], graph_spec_or_None), ...] for the worked examples in topic `number`'s video.
    graph_spec: keyword arguments for calclib.figs.graph, for problems that can't be stated without their graph.
    lesson=True returns the examples solved inside the lesson body instead (any title not starting "Example"):
    the notes place those where they belong with VideoExample("<title>")."""
    path = ANIM / f"s{number.replace('.', '_')}.py"
    if not path.exists():
        return []
    out = []
    for n in ast.walk(ast.parse(path.read_text())):
        if not (isinstance(n, ast.Call) and getattr(n.func, "attr", "") == "example" and n.args):
            continue
        title = _const(n.args[0])
        if not title or title.startswith("Example") == lesson:
            continue
        kw = {k.arg: k.value for k in n.keywords}
        problem = _const(kw["text"]) if "text" in kw else _const(n.args[1])
        steps_node = n.args[2] if len(n.args) > 2 else kw.get("steps")
        if problem is None or not isinstance(steps_node, ast.List):
            raise ValueError(f"{path.name}: {title!r} needs a literal problem (or text=...) and a literal list of steps")
        # non-string steps are tables or pictures drawn on the board; the notes version states them in text= instead
        steps = [s for s in (_const(e) for e in steps_node.elts) if s is not None]
        g = kw.get("notes_graph")
        if isinstance(g, ast.Call):                     # dict(fns=..., xr=...) written as a call
            graph = {k.arg: ast.literal_eval(k.value) for k in g.keywords}
        else:
            graph = ast.literal_eval(g) if g is not None else None
        out.append((title, problem, steps, graph))
    order = lambda e: int(e[0].split(":")[0].split()[-1]) if e[0].split(":")[0].split()[-1].isdigit() else 99
    return sorted(out, key=order)


def problem_tex(problem):
    """The notes version of a problem: limits and big fractions on their own line instead of squeezed inline."""
    def lift(m):
        tex = m.group(1)
        if r"\displaystyle" in tex or r"\dfrac" in tex:
            return r"\[ " + tex.replace(r"\displaystyle", "").replace(r"\dfrac", r"\frac").strip() + r" \]"
        return m.group(0)
    import re
    return re.sub(r"(?<![\\$])\$(?!\$)([^$]+?)(?<!\\)\$", lift, problem)


def solution_tex(steps):
    """Board lines as notes LaTeX: each math line on its own display line, sentences and part labels as text."""
    parts = []
    for s in steps:
        if s.startswith("TEXT:"):
            parts.append(s[5:])
        elif s.startswith("POWER:"):
            f = s[6:].split("|")
            coef = f[3] if len(f) > 3 else f[1]
            parts.append(rf"\[ \frac{{d}}{{dx}}\left[{f[0]}^{{{f[1]}}}\right] = {coef}{f[0]}^{{{f[2]}}} \]")
        elif s.startswith("PART:"):
            # the notes problem already lists the parts; the solution only needs the label, e.g. "(a)"
            label = s[5:].split(")", 1)[0] + ")" if s[5:].startswith("(") else s[5:]
            parts.append(r"\textbf{" + label + "}")
        else:
            parts.append(r"\[ " + s + r" \]")
    return " ".join(parts)
