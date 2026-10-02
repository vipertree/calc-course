"""Check video transcripts: copy-review scan on the narration, spoken-math hygiene, runtime estimate.

    python3 tools/transcripts.py [1.1 1.2 ...]
"""
import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WPM = 150          # measured on the Seed Audio clone: 72 words in 27 s is about 160; keep margin


def parse(path):
    title, beats, cur, part = "", [], None, "lesson"
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("# "):
            if title:
                part = "examples"        # "# Worked examples": the solved-problem video after the lesson
            else:
                title = line[2:]
        elif line.startswith("## "):
            cur = {"name": line[3:], "screen": [], "say": [], "part": part}
            beats.append(cur)
        elif cur is not None and line.startswith("> "):
            cur["say"].append(line[2:])
        elif cur is not None and line.startswith("**On screen:**"):
            cur["screen"].append(line[len("**On screen:**"):].strip())
        elif cur is not None and line.strip() and cur["screen"] and not cur["say"]:
            cur["screen"].append(line.strip())
    return title, beats


CHECK = re.compile(r"<!--\s*check:\s*(.+?)\s*-->")


def math_checks(path):
    """Evaluate hidden <!-- check: lhs == rhs --> lines with sympy. Returns failures."""
    import sympy as sp
    ns = {n: getattr(sp, n) for n in ["limit", "sqrt", "sin", "cos", "tan", "exp", "log", "pi", "oo", "E",
                                       "Rational", "Abs", "diff", "integrate", "simplify", "Symbol", "S",
                                       "expand", "factor", "cancel", "solve", "nsimplify", "N", "Float", "cot", "sec", "csc", "asin", "acos", "atan"]}
    ns.update({v: sp.Symbol(v) for v in "xthnkua"})
    bad = []
    for expr in CHECK.findall(open(path).read()):
        try:
            lhs, rhs = expr.split("==")
            a, b = eval(lhs, ns), eval(rhs, ns)
            pairs = list(zip(a, b)) if isinstance(a, (list, tuple)) and len(a) == len(b) else [(a, b)]
            ok = not isinstance(a, (list, tuple)) or len(pairs) == len(a)
            for u, v in pairs:
                u, v = sp.sympify(u), sp.sympify(v)
                if u.is_infinite or v.is_infinite:
                    ok = ok and u == v
                else:
                    diff = sp.simplify(u - v)
                    ok = ok and (diff == 0 or (not diff.free_symbols and abs(complex(sp.N(diff))) < 1e-9))
        except Exception as exc:  # noqa: BLE001
            ok, a = False, exc
        if not ok:
            bad.append(f"math check failed: {expr}  (got {a})")
    return bad


PAUSE = re.compile(r"\[(long pause|pause|try it)\]")   # [try it]: the think pause before a worked example is solved


def narration(beats):
    """Spoken words only: pause markers removed."""
    return "\n".join(PAUSE.sub("", s).strip() for b in beats for s in b["say"])


def pause_seconds(beats):
    secs = {"pause": 0.7, "long pause": 1.4, "try it": 3.0}
    return sum(secs[m.group(1)] for b in beats for s in b["say"] for m in PAUSE.finditer(s))


def problems(text):
    out = []
    if "—" in text or " -- " in text:
        out.append("em dash in narration")
    if "$" in text or "\\" in text:
        out.append("LaTeX in narration (write math as spoken words)")
    for pat in [r"\blet's (dive|explore|take a look)", r"\bit's not \w+,? it's", r"\bdelve", r"\bhonestly\b",
                r"\bgenuinely\b", r"\bjourney\b", r"\bseamless", r"\bcrucial\b", r"\bpivotal\b"]:
        if re.search(pat, text, re.I):
            out.append("copy tell: " + pat)
    return out


def main(nums):
    files = sorted(glob.glob(os.path.join(ROOT, "transcripts", "[0-9]*_*.md")),
                   key=lambda p: [int(x) for x in os.path.basename(p)[:-3].split("_")])
    if nums:
        files = [f for f in files if os.path.basename(f)[:-3].replace("_", ".") in nums]
    scan = os.path.join(ROOT, ".claude", "skills", "copy-review", "scripts", "scan.py")
    total, bad = 0, 0
    for f in files:
        title, beats = parse(f)
        text = narration(beats)
        words = len(text.split())
        secs = words / WPM * 60 + 2.5 * len(beats) + pause_seconds(beats)   # beat gaps + marked pauses
        ex = [b for b in beats if b["part"] == "examples"]
        ex_secs = len(narration(ex).split()) / WPM * 60 + 2.5 * len(ex) + pause_seconds(ex) if ex else 0
        total += secs
        probs = problems(text) + math_checks(f)
        nchecks = len(CHECK.findall(open(f).read()))
        tmp = f + ".narration.txt"
        open(tmp, "w").write(text)
        r = subprocess.run([sys.executable, scan, tmp, "--ext", "txt", "--min-severity", "med"],
                           capture_output=True, text=True)
        os.remove(tmp)
        hits = [l for l in r.stdout.splitlines() if l.strip() and "0 hits" not in l]
        flag = " !!" if probs or hits else ""
        bad += bool(flag)
        print(f"{os.path.basename(f):10s} {len(beats):2d} beats {words:5d} words ~{secs / 60:4.1f} min "
              f"{nchecks:2d} checks  {len(set(b['name'] for b in ex)):d} ex ({ex_secs / 60:.1f} min)  {title}{flag}")
        for p in probs + hits:
            print("     ", p)
    print(f"total ~{total / 60:.0f} min of video in {len(files)} transcripts; {bad} with flags")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1:]) else 0)
