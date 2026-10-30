"""Where every student in a class stands, read in a few queries and judged by the class setup.

A lesson's progress counts only what the class tracks (Setup): notes steps when notes are recorded automatically,
the teacher's "done" mark when notes are marked by hand, practice items tried (never right or wrong) when practice
is on the site, the teacher's mark when it's on paper. A quiz score is the class attempt (first, or best for
best-of quizzes) with the teacher's answer fixes and dropped questions applied, or the score the teacher entered.
"""
import datetime as dt
from collections import defaultdict

from django.db.models import Count, Max

from accounts.models import unit_of
from course import content
from course.models import Draft, QuizAttempt, Response, StepDone

from . import calendar as cal
from . import setup as S
from .models import Adjustment, AnswerFix, Dated, Mark, StudentException

DONE_SHARE = {"all": 1.0, "most": 0.8, "self": 1.0}


class ClassData:
    def __init__(self, classroom):
        c = self.c = classroom
        self.students = sorted((e.student for e in c.enrollments.select_related("student__profile")),
                               key=lambda u: u.profile.display_name.lower())
        self.joined = {e.student_id: e.joined for e in c.enrollments.all()}
        ids = self.ids = [s.id for s in self.students]
        self.sets = {k: S.settings_for(c, k) for k in S.KINDS}
        self.steps = {(r["user"], r["topic"]): r["n"] for r in
                      StepDone.objects.filter(user__in=ids).values("user", "topic").annotate(n=Count("id"))}
        self.tried = {(r["user"], r["topic"]): r["n"] for r in
                      Response.objects.filter(user__in=ids, area="practice").values("user", "topic").annotate(n=Count("item", distinct=True))}
        self.attempts = defaultdict(list)
        for a in QuizAttempt.objects.filter(user__in=ids, classroom=c).order_by("at"):
            self.attempts[(a.user_id, a.topic)].append(a)
        self.marks = {(m.student_id, m.kind, m.ref, m.part): m for m in Mark.objects.filter(classroom=c)}
        self.fixes = {(f.student_id, f.topic, f.item): f.credit for f in AnswerFix.objects.filter(classroom=c)}
        self.dropped = defaultdict(set)
        for a in Adjustment.objects.filter(classroom=c, kind="drop_question"):
            self.dropped[a.params.get("ref", "")].add(a.params.get("item", ""))
        self.dated = {(d.kind, d.ref): d for d in Dated.objects.filter(classroom=c)}
        self.exceptions = {(e.dated_id, e.student_id): e for e in StudentException.objects.filter(dated__classroom=c)}
        last = defaultdict(lambda: None)
        for qs, f in ((StepDone.objects, "at"), (Response.objects, "at"), (Draft.objects, "updated")):
            for r in qs.filter(user__in=ids).values("user").annotate(t=Max(f)):
                if r["t"] and (last[r["user"]] is None or r["t"] > last[r["user"]]):
                    last[r["user"]] = r["t"]
        self.last_active = last
        self.now = dt.datetime.now(dt.timezone.utc)
        self._counts = {}

    # ------------------------------------------------------------------ pieces
    def counts(self, num):
        if num not in self._counts:
            self._counts[num] = content.counts(num) or {}
        return self._counts[num]

    def due(self, kind, ref, uid):
        d = self.dated.get((kind, ref))
        if d is None or self.sets[kind].get("dates") != "dated":
            return None
        e = self.exceptions.get((d.pk, uid))
        if e and e.excused:
            return None
        return e.due if e and e.due else d.due

    def quiz(self, uid, ref):
        """(points, possible) for this student's quiz or test, or None when there's nothing yet."""
        kind = "unittest" if ref.startswith("U") else "quiz"
        m = self.marks.get((uid, kind, ref, ""))
        if m is not None and (m.excused or m.absent):
            return None
        if m is not None and m.points is not None:
            return m.points, m.possible or self.counts(ref).get("quiz") or 5
        parts = [x for (u, k, r, p), x in self.marks.items() if u == uid and k == kind and r == ref and p and x.points is not None]
        if parts:
            return sum(x.points for x in parts), sum(x.possible or 0 for x in parts) or None
        tries = self.attempts.get((uid, ref))
        if not tries:
            return None
        scored = [self._score(uid, ref, a) for a in tries]
        return max(scored) if self.sets["quiz"].get("attempts") == "best" and kind == "quiz" else scored[0]

    def _score(self, uid, ref, a):
        drop = self.dropped.get(ref, set())
        items = [i for i in (a.served or list(a.detail)) if i not in drop]
        pts = 0.0
        for i in items:
            d = a.detail.get(i, {})
            pts += 1.0 if d.get("correct") else self.fixes.get((uid, ref, i), 0.0)
        return round(pts, 2), len(items)

    def lesson(self, uid, num):
        """A lesson's square on the progress map: how far along, done or not, quiz score, late, tracked at all."""
        n = self.counts(num)
        parts = []
        sn, sp = self.sets["notes"], self.sets["practice"]
        if sn["where"] != "off" and sn["record"] != "nothing":
            if sn["record"] == "mark" or sn["where"] == "paper":
                m = self.marks.get((uid, "notes", num, ""))
                parts.append(("notes", 1.0 if m and (m.done or m.excused) else 0.0))
            else:
                total = n.get("steps") or 0
                parts.append(("notes", min(1.0, self.steps.get((uid, num), 0) / total) if total else 1.0))
        if sp["where"] == "paper":
            m = self.marks.get((uid, "practice", num, ""))
            parts.append(("practice", 1.0 if m and (m.done or m.excused) else 0.0))
        elif sp["where"] == "site":
            total = n.get("practice") or 0
            need = DONE_SHARE.get(sp.get("done_when"), 1.0)
            m = self.marks.get((uid, "practice", num, ""))
            share = 1.0 if m and (m.done or m.excused) else (self.tried.get((uid, num), 0) / (total * need) if total else 1.0)
            parts.append(("practice", min(1.0, share)))
        progress = sum(p for _, p in parts) / len(parts) if parts else None
        done = bool(parts) and all(p >= 1.0 for _, p in parts)
        q = self.quiz(uid, num) if self.sets["quiz"]["where"] != "off" else None
        late = False
        for kind, share in parts:
            due = self.due(kind, num, uid)
            if due is not None and self.now > due and share < 1.0:
                late = True
        qdue = self.due("quiz", num, uid)
        if qdue is not None and self.now > qdue and q is None and self.sets["quiz"]["where"] != "off":
            late = True
        return {"progress": progress, "done": done, "quiz": q, "late": late, "tracked": bool(parts) or q is not None}

    def furthest(self, uid, unit):
        """The last lesson of the unit this student has finished, as an index into the unit's lessons (-1 = none)."""
        topics = cal.unit_topics(unit, self.c.course)
        best = -1
        for i, num in enumerate(topics):
            if self.lesson(uid, num)["done"]:
                best = i
        return best

    def scheduled_index(self, unit):
        """Where the schedule says the class should be in a unit today: the index of the last lesson opened or due."""
        topics = cal.unit_topics(unit, self.c.course)
        idx = -1
        for i, num in enumerate(topics):
            for kind in ("notes", "practice", "quiz"):
                d = self.dated.get((kind, num))
                when = d and (d.opens or d.due)
                if when and when <= self.now:
                    idx = max(idx, i)
        return idx

    def current_unit(self):
        """The unit the class is in: the one with the most recent opened or due date, else the one with the most
        recent student activity, else Unit 1."""
        dated = [(d.opens or d.due, d.ref) for d in self.dated.values() if (d.opens or d.due) and (d.opens or d.due) <= self.now + dt.timedelta(days=3)]
        if dated:
            return unit_of(max(dated)[1]) or 1
        recent = [(t, topic) for (u, topic), _ in self.steps.items() for t in [self.last_active.get(u)] if t]
        if recent:
            return unit_of(max(recent)[1]) or 1
        return 1

    def unit_summary(self, uid, unit):
        topics = cal.unit_topics(unit, self.c.course)
        cells = [self.lesson(uid, n) for n in topics]
        tracked = [c for c in cells if c["tracked"] or c["progress"] is not None]
        done = sum(1 for c in tracked if c["done"])
        qs = [c["quiz"] for c in cells if c["quiz"]]
        avg = round(100 * sum(p for p, _ in qs) / sum(t for _, t in qs)) if qs and sum(t for _, t in qs) else None
        share = done / len(tracked) if tracked else 0
        late = any(c["late"] for c in cells)
        return {"progress": share, "done": bool(tracked) and done == len(tracked), "avg": avg, "late": late}

    def quiz_average(self, uid):
        pts = tot = 0.0
        for (u, ref), _ in self.attempts.items():
            if u == uid and not ref.startswith("U"):
                q = self.quiz(uid, ref)
                if q and q[1]:
                    pts, tot = pts + q[0], tot + q[1]
        for (u, k, ref, part), m in self.marks.items():
            if u == uid and k == "quiz" and not part and m.points is not None and (uid, ref) not in self.attempts:
                pts, tot = pts + m.points, tot + (m.possible or 5)
        return round(100 * pts / tot) if tot else None

    def due_work(self, uid):
        """(done, due so far) for this student: the dated lessons, practice and quizzes whose due date has passed."""
        done = total = 0
        for (kind, ref), d in self.dated.items():
            if kind not in ("notes", "practice", "quiz") or self.sets[kind].get("dates") != "dated":
                continue
            due = self.due(kind, ref, uid)
            if due is None or due > self.now:
                continue
            total += 1
            if kind == "quiz":
                done += self.quiz(uid, ref) is not None
            else:
                cell = self.lesson(uid, ref)
                done += cell["done"]
        return done, total
