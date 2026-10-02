"""Which versions of a quiz or unit test someone gets, and whether they may see results yet.

Every quiz slot (and unit-test MCQ and FRQ slot) can have several versions. Two kinds of taker:

* individual users get a fresh random draw per slot for each attempt, and instant results;
* students in a class all get the same paper form (chosen per class and topic, so the teacher can print the
  matching PDF), submit once, and see scores and solutions only after the teacher releases them.

Only the served versions ever reach the page.
"""
import hashlib
import random

from accounts.models import class_for

from .models import QuizAttempt, Release

LETTERS = "ABCDEF"


def _rows(pub):
    rows = pub.get("quiz_variants") or [[q] for q in pub.get("quiz", [])]
    frows = pub.get("frq_variants") or []          # unit tests only; topic FRQs are practice
    return rows, frows


def n_forms(pub):
    rows, frows = _rows(pub)
    return max([len(r) for r in rows + frows] or [1])


def class_form(classroom, num, n):
    h = int(hashlib.sha256(f"{classroom.code}:{num}".encode()).hexdigest(), 16)
    return h % n


def strip(pub):
    """The public lesson without the unserved versions."""
    return {k: v for k, v in pub.items() if not k.endswith("_variants")}


def draw(request, num, pub):
    """-> (public lesson with quiz/frq set to the served versions, info)."""
    rows, frows = _rows(pub)
    cls = class_for(request.user)
    if cls is not None:
        k = class_form(cls, num, n_forms(pub))
        ids = [r[k % len(r)]["id"] for r in rows + frows]
        info = {"mode": "class", "form": LETTERS[k] if n_forms(pub) > 1 else "", "classroom": cls}
    else:
        key = f"draw:{num}"
        ids = request.session.get(key)
        ok = (isinstance(ids, list) and len(ids) == len(rows) + len(frows)
              and all(any(v["id"] == i for v in r) for i, r in zip(ids, rows + frows)))
        if not ok:
            ids = [random.choice(r)["id"] for r in rows + frows]
            request.session[key] = ids
        info = {"mode": "individual", "form": "", "classroom": None}
    pick = {v["id"]: v for r in rows + frows for v in r}
    out = strip(pub)
    out["quiz"] = [pick[i] for i in ids[:len(rows)]]
    if frows:
        out["frq"] = [pick[i] for i in ids[len(rows):]]
    return out, info


def new_draw(request, num):
    request.session.pop(f"draw:{num}", None)


def released(classroom, num):
    return Release.objects.filter(classroom=classroom, topic=num).exists()


def result_payload(attempt, priv):
    detail = {}
    for iid in attempt.served or list(attempt.detail):
        d = attempt.detail.get(iid, {"given": "", "correct": False})
        spec = priv["items"][iid]
        detail[iid] = {**d, "solution": spec["solution"], "display": spec["answer"].get("display", "")}
    return {"score": attempt.score, "total": attempt.total, "detail": detail}


def state(request, num, info, priv):
    """What the page needs to know about this taker's quiz or test."""
    if info["mode"] != "class":
        return {"mode": "individual"}
    cls = info["classroom"]
    a = QuizAttempt.objects.filter(user=request.user, topic=num, classroom=cls).order_by("-at").first()
    rel = released(cls, num)
    st = {"mode": "class", "form": info["form"], "class_name": cls.name, "submitted": a is not None, "released": rel}
    if a is not None and rel:
        st["result"] = result_payload(a, priv)
    return st


def withheld(request, num):
    """True when this user's results for num must stay hidden (class student, not yet released)."""
    cls = class_for(request.user)
    return cls is not None and not released(cls, num)
