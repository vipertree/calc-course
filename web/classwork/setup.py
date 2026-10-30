"""The choices a teacher makes for each kind of work, the defaults, the starting templates, and how a class's
settings for one piece of work are worked out.

Settings for one item come from, last one winning:
  DEFAULTS[kind]  <  the class setup (Setup.kinds)  <  a unit set apart (Setup.units)  <  the item's own (Dated.settings)

The defaults are how the site behaved before any of this existed, so a class nobody has set up works the same.
"""
from accounts.models import unit_of

KINDS = ["notes", "practice", "quiz", "testprep", "unittest", "exam"]
NAMES = {"notes": "Lesson notes", "practice": "Practice", "quiz": "Quizzes", "testprep": "Test prep",
         "unittest": "Unit tests", "exam": "Practice exams"}
BLURBS = {"notes": "guided notes, video, checks", "practice": "the homework sets", "quiz": "5 questions a lesson",
          "testprep": "AP-style MCQ and FRQ", "unittest": "two forms per unit", "exam": "full-length AP"}

# field -> [(value, label)] per kind. A field a kind doesn't list is fixed for it (see FIXED).
WHERE = [("site", "On the site"), ("paper", "On paper (you enter it)"), ("off", "Not used")]
OPENS = [("all", "All at once"), ("schedule", "On your schedule"), ("lesson", "With its lesson")]
DATES = [("none", "None"), ("dated", "Dated")]
RESULTS = [("now", "Right away"), ("due", "At the due date"), ("release", "When I release them")]
TIMERS = [("0", "Untimed"), ("10", "10 minutes"), ("15", "15 minutes"), ("20", "20 minutes"), ("30", "30 minutes"),
          ("45", "45 minutes"), ("50", "50 minutes"), ("60", "60 minutes"), ("90", "90 minutes")]

CHOICES = {
    "notes": {"where": [("paper", "On paper, in class"), ("site", "On the site"), ("off", "Not used")],
              "opens": [("all", "All at once"), ("schedule", "On your schedule")],
              "dates": DATES,
              "record": [("auto", "Done, automatically"), ("mark", "You mark done"), ("nothing", "Nothing")]},
    "practice": {"where": [("site", "On the site"), ("paper", "On paper (you mark done)"), ("off", "Not used")],
                 "opens": [("lesson", "With its lesson"), ("all", "All at once"), ("schedule", "On your schedule")],
                 "dates": DATES,
                 "results": [("now", "Right away, with retries"), ("due", "After the due date")],
                 "done_when": [("all", "Every item is tried"), ("most", "Most items are tried (80%)"), ("self", "The student says it's done")],
                 "late": [("marked", "Accepted, marked late"), ("quiet", "Accepted, no mark"), ("lock", "Locked at the due date")],
                 "solutions": [("each", "Shown after each try"), ("due", "Shown after the due date"), ("never", "Never shown")]},
    "quiz": {"where": WHERE, "opens": OPENS, "dates": DATES,
             "record": [("score", "Score"), ("done", "Done or not")],
             "results": RESULTS,
             "attempts": [("one", "One (class form)"), ("best", "Best of unlimited")],
             "timer": TIMERS,
             "late": [("marked", "Accepted, marked late"), ("lock", "Locked at the due date")]},
    "testprep": {"where": [("site", "On the site"), ("paper", "On paper"), ("off", "Not used")],
                 "opens": [("lesson", "With its lesson"), ("all", "All at once")],
                 "record": [("nothing", "Nothing (study only)"), ("done", "Done or not"), ("score", "Score")]},
    "unittest": {"where": [("site", "On the site"), ("paper", "On paper (you enter scores)"), ("off", "Not used")],
                 "opens": [("all", "All at once"), ("schedule", "On test day")],
                 "dates": DATES,
                 "record": [("parts", "Score, by part"), ("total", "Total score only")],
                 "results": [("release", "When I release them"), ("now", "Right away")],
                 "timer": TIMERS,
                 "late": [("lock", "Locked at the due date"), ("marked", "Accepted, marked late")]},
    "exam": {"where": [("site", "On the site"), ("paper", "On paper (you enter scores)"), ("off", "Not used")],
             "opens": [("all", "All at once"), ("schedule", "On your schedule")],
             "dates": DATES,
             "record": [("score", "Score and AP estimate (1 to 5)"), ("done", "Done or not")],
             "results": [("now", "Right away"), ("release", "When I release them")]},
}
FIXED = {"practice": {"record": "done"}, "testprep": {"dates": "none", "results": "now"}}

DEFAULTS = {
    "notes": {"where": "site", "opens": "all", "dates": "none", "record": "auto"},
    "practice": {"where": "site", "opens": "lesson", "dates": "none", "record": "done", "results": "now",
                 "done_when": "all", "late": "marked", "solutions": "each"},
    "quiz": {"where": "site", "opens": "all", "dates": "none", "record": "score", "results": "release",
             "attempts": "one", "late": "marked", "timer": "0"},
    "testprep": {"where": "site", "opens": "lesson", "dates": "none", "record": "nothing", "results": "now"},
    "unittest": {"where": "site", "opens": "all", "dates": "none", "record": "parts", "results": "release",
                 "timer": "0", "late": "lock"},
    "exam": {"where": "site", "opens": "all", "dates": "none", "record": "score", "results": "now"},
}
# Fields that sit in a row's "More" panel rather than its main columns.
DETAIL = {"practice": ["done_when", "late", "solutions"], "quiz": ["timer", "attempts", "late"], "unittest": ["timer", "late"]}
DETAIL_LABELS = {"done_when": "Counts as done when", "late": "Late work", "solutions": "Answers and solutions",
                 "attempts": "Attempts", "timer": "Time limit (extra time is per student)"}

SHOW_DEFAULTS = {"grade": True, "due_dates": True, "unopened": False, "behind": True, "trig": False}
WATCH_DEFAULTS = {"missing": True, "hard_questions": True, "sliding": True, "inactive_days": 0}

TEMPLATES = {
    "self_paced": ("Self-paced, all online", {k: {"opens": "all" if k != "practice" else "lesson", "dates": "none"} for k in KINDS}
                   | {"quiz": {"opens": "all", "dates": "none", "results": "now", "attempts": "best"}}),
    "dated_tests": ("Online, dated quizzes and tests", {"quiz": {"opens": "schedule", "dates": "dated"},
                                                        "unittest": {"opens": "schedule", "dates": "dated"}}),
    "full_schedule": ("Online, full schedule", {"notes": {"opens": "schedule"}, "practice": {"opens": "lesson", "dates": "dated"},
                                                "quiz": {"opens": "schedule", "dates": "dated"},
                                                "unittest": {"opens": "schedule", "dates": "dated"},
                                                "exam": {"opens": "schedule", "dates": "dated"}}),
    "paper": ("Paper in class, site for videos and practice", {"notes": {"where": "paper", "opens": "schedule", "record": "mark"},
                                                                "practice": {"dates": "dated"},
                                                                "quiz": {"where": "paper", "dates": "dated", "opens": "schedule"},
                                                                "testprep": {"record": "nothing"},
                                                                "unittest": {"where": "paper", "dates": "dated", "opens": "schedule"},
                                                                "exam": {"where": "paper"}}),
}


def template_kinds(name):
    """A template's settings in full (every kind, every field), for filling the setup table."""
    over = TEMPLATES[name][1]
    return {k: {**DEFAULTS[k], **over.get(k, {})} for k in KINDS}


def clean(kind, values):
    """Keep only the fields this kind offers, and only values it allows."""
    out = {}
    for field, opts in CHOICES[kind].items():
        v = values.get(field)
        if v in {o[0] for o in opts}:
            out[field] = v
    out.update(FIXED.get(kind, {}))
    return out


def kind_of_ref(ref):
    """The kind a calendar ref names when the kind isn't given: "U2" a unit test, "ab1" an exam, else a lesson."""
    if ref.startswith("U"):
        return "unittest"
    return "lesson" if ref[:1].isdigit() else "exam"


def class_setup(classroom):
    from .models import Setup
    s = getattr(classroom, "_setup_cache", None)
    if s is None:
        s = Setup.objects.filter(classroom=classroom).first() or Setup(classroom=classroom)
        classroom._setup_cache = s
    return s


def settings_for(classroom, kind, ref=None, dated=None):
    """The settings that apply to one piece of work in a class."""
    s = class_setup(classroom)
    out = {**DEFAULTS[kind], **(s.kinds.get(kind) or {})}
    unit = unit_of(ref) if ref else None
    if unit is not None:
        out.update((s.units.get(str(unit)) or {}).get(kind) or {})
    if dated is not None:
        out.update(dated.settings or {})
    out.update(FIXED.get(kind, {}))
    return out


def show(classroom):
    return {**SHOW_DEFAULTS, **(class_setup(classroom).show or {})}


def watch(classroom):
    return {**WATCH_DEFAULTS, **(class_setup(classroom).watch or {})}


def used(classroom, kind):
    return settings_for(classroom, kind)["where"] != "off"


def includes_unit(classroom, unit):
    """Is this unit part of the class? Every calculus unit is; the Trig Review (unit 0) only when the teacher adds it."""
    return unit != 0 or bool(show(classroom).get("trig"))


def class_units(classroom):
    """The units this class covers, in order, as syllabus entries."""
    from classwork.calendar import unit_topics
    from course import content
    return [u for u in content.syllabus() if includes_unit(classroom, u["n"]) and unit_topics(u["n"], classroom.course)]
