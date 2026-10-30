"""What a class student sees about their own class work on their page (/me/): what's due, their grade if the teacher
shows it, and quiz scores only once results are visible to them (with the teacher's fixes applied)."""
import datetime as dt

from course.models import QuizAttempt

from . import calendar as cal
from . import setup as S
from .access import results_visible


def extras(user, c):
    show = S.show(c)
    now = dt.datetime.now(dt.timezone.utc)
    tz = cal.zone(c)
    out = {"show_grade": show["grade"], "show_due": show["due_dates"]}
    from .progress import ClassData
    data = ClassData(c)
    if show["due_dates"]:
        due = []
        for (kind, ref), d in data.dated.items():
            when = data.due(kind, ref, user.id)
            if not when or kind not in ("notes", "practice", "quiz", "unittest") or when > now + dt.timedelta(days=14):
                continue
            done = data.quiz(user.id, ref) is not None if kind in ("quiz", "unittest") else data.lesson(user.id, ref)["done"]
            if done or (when < now - dt.timedelta(days=21)):
                continue
            due.append({"label": cal.label(kind, ref), "when": when.astimezone(tz), "late": when < now, "kind": kind, "ref": ref})
        out["due"] = sorted(due, key=lambda x: x["when"])
    if show["grade"]:
        from .grades import Book

        class Mine(Book):
            """The student's own view: a quiz or test whose results they can't see yet doesn't count in it."""
            def raw(self, cat, uid, key):
                if cat.source in ("quiz", "unittest") and not results_visible(user, cat.source, key):
                    return None
                return super().raw(cat, uid, key)
        b = Mine(c, data)
        f = b.final(user.id)
        out["grade"] = None if f is None else {"pct": f, "letter": __import__("classwork.grades", fromlist=["letter"]).letter(f, b.scale),
                                                "cats": [{"name": cat.name, "weight": cat.weight,
                                                          "pct": None if v is None else round(100 * v, 1)}
                                                         for cat in b.cats for v in [b.category(cat, user.id)]]}
    quizzes = []
    for a in QuizAttempt.objects.filter(user=user).order_by("-at")[:8]:
        kind = "unittest" if a.topic.startswith("U") else "quiz"
        if a.classroom_id == c.pk:
            visible = results_visible(user, kind, a.topic)
            q = data.quiz(user.id, a.topic) if visible else None
            quizzes.append({"a": a, "score": q and f"{q[0]:g}", "total": q and q[1], "waiting": not visible})
        else:
            quizzes.append({"a": a, "score": a.score, "total": a.total, "waiting": False})
    out["quizzes"] = quizzes
    return out
