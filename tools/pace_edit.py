"""Small helper for transcript revision passes.
    from pace_edit import T; t = T("1_5"); t.pause("phrase", long=False); t.examples(text); t.checks(lines); t.save()"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class T:
    def __init__(self, num):
        self.p = os.path.join(ROOT, "transcripts", num + ".md")
        self.s = open(self.p).read()

    def pause(self, phrase, long=False):
        """Add a [pause] right after `phrase` (which must occur once in the narration)."""
        assert self.s.count(phrase) == 1, (self.s.count(phrase), phrase)
        mark = " [long pause]" if long else " [pause]"
        self.s = self.s.replace(phrase, phrase + mark, 1)

    def sub(self, a, b):
        assert a in self.s, a
        self.s = self.s.replace(a, b, 1)

    def examples(self, text):
        assert "# Worked examples" not in self.s
        j = self.s.index("<!-- check:") if "<!-- check:" in self.s else len(self.s)
        self.s = self.s[:j] + "# Worked examples\n\n" + text.strip() + "\n\n" + self.s[j:]

    def checks(self, *lines):
        self.s = self.s.rstrip("\n") + "\n" + "".join(f"<!-- check: {c} -->\n" for c in lines)

    def save(self):
        open(self.p, "w").write(self.s)
