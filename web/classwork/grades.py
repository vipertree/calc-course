"""The class gradebook: categories with weights, the items in each, every student's score on each, curves,
class-wide changes, and the final grade.

What counts as an item:
* quizzes and unit tests: every one past its due date (a missing one scores 0 unless excused) and every one taken;
* practice: every lesson whose practice is past due (done or not, never right or wrong; late work can count less),
  or, in a class with no practice due dates, every lesson the student has started;
* practice exams: every one a student in the class finished (best or most recent attempt);
* the teacher's own items: whatever the teacher entered.
A category with no items yet for a student is left out of that student's grade and the weights are shared among the
rest, so a new class doesn't start at 0.
"""
import math

from course import content, exams
from course.models import ExamAttempt

from . import calendar as cal
from . import setup as S
from .models import Adjustment, Category, Curve, TeacherItem, TeacherScore
from .progress import DONE_SHARE, ClassData

DEFAULT_SCALE = [["A", 90], ["B", 80], ["C", 70], ["D", 60]]
DEFAULTS = [("Unit tests", "unittest", 45, {}), ("Quizzes", "quiz", 30, {"drop_lowest": 0}),
            ("Practice", "practice", 15, {"late_factor": 1.0}), ("Practice exams", "exam", 10, {"best": True})]
RULES = {"quiz": [("drop_lowest", "Drop the lowest", [(0, "No drops"), (1, "Drop the lowest 1"), (2, "Drop the lowest 2"), (3, "Drop the lowest 3")])],
         "unittest": [("drop_lowest", "Drop the lowest", [(0, "No drops"), (1, "Drop the lowest 1")])],
         "practice": [("late_factor", "Late work", [(1.0, "Counts in full"), (0.5, "Counts half"), (0.0, "Counts nothing")])],
         "exam": [("best", "Which attempt", [(True, "The best"), (False, "The most recent")])],
         "own": [("drop_lowest", "Drop the lowest", [(0, "No drops"), (1, "Drop the lowest 1"), (2, "Drop the lowest 2")])]}


def categories(c):
    """The class's categories, creating the defaults (for the kinds the class uses) the first time."""
    cats = list(Category.objects.filter(classroom=c).prefetch_related("items"))
    if not cats:
        for i, (name, src, w, rules) in enumerate(DEFAULTS):
            if S.used(c, src):
                cats.append(Category.objects.create(classroom=c, name=name, source=src, weight=w, rules=rules, order=i))
    return cats


def scale(c):
    return S.class_setup(c).grading.get("scale") or DEFAULT_SCALE


def letter(pct, sc):
    for name, lo in sc:
        if pct is not None and pct >= lo:
            return name
    return "F"


# ------------------------------------------------------------------ curves
def curve_fn(curve, raw):
    """The curve as a function on a score fraction, given the class's raw fractions. Never lowers a score."""
    p = curve.params or {}
    vals = [v for v in raw if v is not None]
    if curve.method == "mean":
        mean = sum(vals) / len(vals) if vals else 0
        shift = max(0.0, float(p.get("target", 80)) / 100 - mean)
        f = lambda x: x + shift
    elif curve.method == "add":
        f = lambda x: x + float(p.get("points", 5)) / 100
    elif curve.method == "top":
        top = max(vals) if vals else 1
        f = (lambda x: x / top) if top > 0 else (lambda x: x)
    elif curve.method == "sqrt":
        f = lambda x: math.sqrt(max(0.0, x))
    else:
        f = lambda x: x
    cap = (lambda x: x) if curve.allow_over else (lambda x: min(1.0, x))
    return lambda x: x if x is None else cap(max(x, f(x)))


# ------------------------------------------------------------------ items and scores
class Book:
    def __init__(self, c, data=None):
        self.c = c
        self.data = data or ClassData(c)
        self.cats = categories(c)
        self.curves = {(cv.kind, cv.ref): cv for cv in Curve.objects.filter(classroom=c)}
        self.bonus = sum(float(a.params.get("points", 0)) for a in Adjustment.objects.filter(classroom=c, kind="bonus"))
        self.scale = scale(c)
        self._exam = None
        self._curved = {}

    # items per category ------------------------------------------------
    def items(self, cat):
        d = self.data
        if cat.source in ("quiz", "unittest"):
            refs = {ref for (_, ref) in d.attempts if ref.startswith("U") == (cat.source == "unittest")}
            refs |= {ref for (k, ref), x in d.dated.items() if k == cat.source and x.due and x.due < d.now}
            refs |= {ref for (_, k, ref, _), m in d.marks.items() if k == cat.source and m.points is not None}
            return [(ref, cal.label(cat.source, ref)) for ref in sorted(refs, key=_numkey)]
        if cat.source == "practice":
            dated = [ref for (k, ref), x in d.dated.items() if k == "practice" and x.due and x.due < d.now]
            refs = set(dated) if dated else {ref for (_, ref) in d.tried}
            return [(ref, cal.label("practice", ref)) for ref in sorted(refs, key=_numkey)]
        if cat.source == "notes":
            refs = {ref for (k, ref), x in d.dated.items() if k == "notes" and x.due and x.due < d.now}
            refs |= {ref for (_, k, ref, _) in d.marks if k == "notes"}
            return [(ref, cal.label("notes", ref)) for ref in sorted(refs, key=_numkey)]
        if cat.source == "exam":
            return [(slug, f"Practice exam {slug.upper()}") for slug in sorted({a.exam for a in self.exam_attempts()})]
        return [(f"own{i.pk}", i.name) for i in cat.items.all()]

    def exam_attempts(self):
        if self._exam is None:
            self._exam = list(ExamAttempt.objects.filter(user__in=self.data.ids, finished__isnull=False).order_by("finished"))
        return self._exam

    def raw(self, cat, uid, key):
        """A score fraction (0 to 1), or None when the item doesn't count for this student (not due, excused)."""
        d = self.data
        if cat.source in ("quiz", "unittest"):
            m = d.marks.get((uid, cat.source, key, ""))
            if m is not None and (m.excused or m.absent):
                return None
            q = d.quiz(uid, key)
            due = d.due(cat.source, key, uid)
            dated = d.dated.get((cat.source, key))
            exc = d.exceptions.get((dated.pk, uid)) if dated else None
            if exc and exc.excused:
                return None
            if q is None:
                return 0.0 if due and due < d.now else None
            return q[0] / q[1] if q[1] else None
        if cat.source == "practice":
            m = d.marks.get((uid, "practice", key, ""))
            if m is not None and m.excused:
                return None
            due = d.due("practice", key, uid)
            dated = d.dated.get(("practice", key))
            exc = d.exceptions.get((dated.pk, uid)) if dated else None
            if exc and exc.excused:
                return None
            if m is not None and m.done:
                return 1.0
            total = d.counts(key).get("practice") or 0
            need = DONE_SHARE.get(d.sets["practice"].get("done_when"), 1.0)
            share = min(1.0, d.tried.get((uid, key), 0) / (total * need)) if total else 1.0
            if due and share >= 1.0 and (d.practice_last.get((uid, key)) or d.now) > due:
                share *= float(cat.rules.get("late_factor", 1.0))
            if not due and not d.tried.get((uid, key)):
                return None
            return share
        if cat.source == "notes":
            m = d.marks.get((uid, "notes", key, ""))
            if m is not None and m.excused:
                return None
            if m is not None and m.done:
                return 1.0
            total = d.counts(key).get("steps") or 0
            return min(1.0, d.steps.get((uid, key), 0) / total) if total else None
        if cat.source == "exam":
            tries = [a for a in self.exam_attempts() if a.user_id == uid and a.exam == key]
            if not tries:
                return None
            pub = exams.public(key)
            scores = [s["composite"] / s["composite_total"] for s in (exams.summary(a, pub) for a in tries) if s["composite_total"]]
            if not scores:
                return None
            return max(scores) if cat.rules.get("best", True) else scores[-1]
        item = next((i for i in cat.items.all() if f"own{i.pk}" == key), None)
        if item is None:
            return None
        sc = next((s for s in item.scores.all() if s.student_id == uid), None)
        if sc is None or sc.excused or sc.points is None:
            return None
        return min(1.0, sc.points / item.points) if item.points else None

    def score(self, cat, uid, key):
        """The score fraction after any curve on that assessment."""
        r = self.raw(cat, uid, key)
        kind = cat.source
        cv = self.curves.get((kind, key))
        if cv is None or r is None:
            return r
        if (kind, key) not in self._curved:
            self._curved[(kind, key)] = curve_fn(cv, [self.raw(cat, u, key) for u in self.data.ids])
        return self._curved[(kind, key)](r)

    def category(self, cat, uid):
        vals = [v for v in (self.score(cat, uid, k) for k, _ in self.items(cat)) if v is not None]
        drop = int(cat.rules.get("drop_lowest", 0) or 0)
        if drop and len(vals) > drop:
            vals = sorted(vals)[drop:]
        return sum(vals) / len(vals) if vals else None

    def final(self, uid):
        parts = [(cat.weight, self.category(cat, uid)) for cat in self.cats if cat.weight > 0]
        parts = [(w, v) for w, v in parts if v is not None]
        if not parts:
            return None
        pct = 100 * sum(w * v for w, v in parts) / sum(w for w, _ in parts) + self.bonus
        return round(pct, 1)

    def rows(self):
        out = []
        for s in self.data.students:
            cats = [self.category(cat, s.id) for cat in self.cats]
            f = self.final(s.id)
            out.append({"s": s, "name": s.profile.display_name, "cats": [None if v is None else round(100 * v, 1) for v in cats],
                        "final": f, "letter": letter(f, self.scale) if f is not None else ""})
        return out


def _numkey(ref):
    r = ref.lstrip("U").replace("BC", "")
    return (ref.startswith("U"), [int(x) if x.isdigit() else 0 for x in r.split(".")], ref)


def own_item_choices(c):
    return [(i.pk, i.name, i.category.name) for i in TeacherItem.objects.filter(category__classroom=c).select_related("category")]


def save_own_score(item, student, value):
    """value: a number, "" (clear), "ex" (excused) or a done checkbox ("on")."""
    v = (value or "").strip().lower()
    if v == "":
        TeacherScore.objects.filter(item=item, student=student).delete()
        return
    if v in ("ex", "excused"):
        TeacherScore.objects.update_or_create(item=item, student=student, defaults={"points": None, "excused": True})
        return
    if v == "on":
        v = str(item.points)
    try:
        pts = float(v)
    except ValueError:
        return
    TeacherScore.objects.update_or_create(item=item, student=student, defaults={"points": max(0.0, pts), "excused": False})


def test_parts(ref):
    """A unit test's scoreable parts for paper entry: the multiple choice, then each free-response question."""
    pub = content.public(ref) or {}
    mc = len(pub.get("quiz", []))
    frqs = pub.get("frq", [])
    return [("mc", f"MC (of {mc})", mc)] + [(f"frq{i}", f"FRQ {i} ({f['points']})", f["points"]) for i, f in enumerate(frqs, 1)]
