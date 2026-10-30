"""The teacher's class pages: setup, calendar, progress, students, quizzes and tests, gradebook."""
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from accounts.models import Classroom
from accounts.permissions import teacher_required

from . import setup as S
from .models import Setup


def own_class(request, pk):
    return get_object_or_404(Classroom, pk=pk, teacher=request.user)


def _row(kind, values):
    """One row of the setup table: each column's choices, with the current value marked."""
    cols = {}
    for field in ("where", "opens", "dates", "record", "results"):
        opts = S.CHOICES[kind].get(field)
        cur = values.get(field)
        if opts is None:
            cols[field] = {"fixed": dict(_FIXED_LABELS).get((kind, field), "")}
        else:
            cols[field] = {"name": f"{kind}.{field}", "options": [{"v": v, "label": l, "on": v == cur} for v, l in opts]}
    details = [{"label": S.DETAIL_LABELS[f], "name": f"{kind}.{f}",
                "options": [{"v": v, "label": l, "on": v == values.get(f)} for v, l in S.CHOICES[kind][f]]}
               for f in S.DETAIL.get(kind, [])]
    return {"kind": kind, "name": S.NAMES[kind], "blurb": S.BLURBS[kind], "off": values.get("where") == "off",
            "cols": [cols[f] for f in ("where", "opens", "dates", "record", "results")], "details": details}


_FIXED_LABELS = [(("practice", "record"), "Done or not, never right or wrong"), (("testprep", "dates"), "None"),
                 (("testprep", "results"), "Right away"), (("notes", "results"), "–")]

SHOW_LABELS = [("grade", "Their grade in the course, with your weights"), ("due_dates", "Due dates, on their course page"),
               ("unopened", "Lessons that haven't opened yet (titles only)"), ("behind", 'A "behind" note when they miss a due date')]
WATCH_LABELS = [("missing", "Missing and late work"), ("hard_questions", "Quiz questions half the class or more missed"),
                ("sliding", "Students whose last two quizzes are under 60%")]


@never_cache
@teacher_required
def setup_page(request, pk):
    c = own_class(request, pk)
    s = S.class_setup(c)
    if request.method == "POST":
        s = Setup.objects.filter(classroom=c).first() or Setup(classroom=c)
        tpl = request.POST.get("apply_template")
        if tpl in S.TEMPLATES:
            s.kinds, s.template = S.template_kinds(tpl), tpl
        else:
            s.kinds = {k: S.clean(k, {f.split(".", 1)[1]: v for f, v in request.POST.items() if f.startswith(k + ".")})
                       for k in S.KINDS}
            s.show = {k: f"show.{k}" in request.POST for k, _ in SHOW_LABELS}
            days = request.POST.get("watch.inactive_days", "").strip()
            s.watch = {**{k: f"watch.{k}" in request.POST for k, _ in WATCH_LABELS},
                       "inactive_days": int(days) if days.isdigit() and "watch.inactive" in request.POST else 0}
            s.template = ""
        s.save()
        return redirect("cw_setup", pk=c.pk)
    current = {k: S.settings_for(c, k) for k in S.KINDS}
    show, watch = S.show(c), S.watch(c)
    return render(request, "classwork/setup.html", {
        "c": c, "tab": "setup", "rows": [_row(k, current[k]) for k in S.KINDS],
        "templates": [(k, v[0]) for k, v in S.TEMPLATES.items()], "template": s.template,
        "show": [{"k": k, "label": l, "on": show[k]} for k, l in SHOW_LABELS],
        "watch": [{"k": k, "label": l, "on": watch[k]} for k, l in WATCH_LABELS],
        "inactive_days": watch["inactive_days"],
        "units_apart": sorted(s.units) if s.pk else [],
    })
