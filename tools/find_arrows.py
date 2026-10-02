"""List solution text that uses a bare '\\to' (an arrow outside \\lim_{...}), per topic.

Adder's rule: keep limit notation on every line, e.g. lim_{x->3} (x^2-9)/(x-3) = lim_{x->3} (x+3) = 6,
never "(x^2-9)/(x-3) = x+3 -> 6".   python3 tools/find_arrows.py [1.6 ...]
"""
import importlib, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import calclib

BARE = re.compile(r"(?<!_\{)(?<![a-z]\\to)(?:[^_{]|^)\\to\s*[-0-9\\\w]")


def texts(t):
    for b in t.notes:
        for f in ("solution", "body"):
            v = getattr(b, f, None)
            if isinstance(v, str):
                yield f"notes:{type(b).__name__}", v
    for area in ("practice", "quiz", "mcq"):
        for i, it in enumerate(getattr(t, area)):
            yield f"{area}{i + 1}", it.solution
    for f in t.frq:
        for p in f.parts:
            yield f"frq {p.label}", p.solution


def bare(s):
    s = re.sub(r"\\lim_\{[^{}]*\}", "LIM", s)
    return [m.start() for m in re.finditer(r"\\to", s)], s


for num in sys.argv[1:] or sorted(n[6:-3].replace("_", ".") for n in os.listdir("content") if n.startswith("topic_")):
    t = importlib.import_module("content.topic_" + num.replace(".", "_")).TOPIC
    for where, s in texts(t):
        hits, s2 = bare(s)
        if hits:
            print(f"{num} {where}: ...{s2[max(0, hits[0] - 70):hits[0] + 20]}...")
