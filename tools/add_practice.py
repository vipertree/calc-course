"""Insert a block of extra practice items before the '# --- quiz' marker of a topic file.
    python3 tools/add_practice.py 1.2 extra.py      (extra.py holds Python code that does PRACTICE += [...])"""
import sys
num, extra = sys.argv[1], open(sys.argv[2]).read()
p = f"content/topic_{num.replace('.', '_')}.py"
s = open(p).read()
marker = "# ---------------------------------------------------------------- quiz"
assert marker in s and "# extra practice (round 1)" not in s, "marker missing or already added"
s = s.replace(marker, "# extra practice (round 1)\n" + extra.strip() + "\n\n" + marker, 1)
open(p, "w").write(s)
print("added to", p)
