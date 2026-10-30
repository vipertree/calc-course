"""How a teacher runs a class, and what the teacher has added or changed on top of what the site records.

The site records what students do (course.models: StepDone, Response, QuizAttempt, FRQScore, ExamAttempt). This app
holds the teacher's side:

* Setup: for each kind of work, where it's done (on the site, on paper, not used), when it opens, whether it has due
  dates, what gets recorded and when students see results (classwork.setup has the choices and the defaults).
* Dated: the calendar. One row per piece of work that has an open date, a due date or its own settings.
* StudentException: one student's different due date, extra time, or an excused item.
* Mark: a score or "done" the teacher entered or changed by hand (paper work, an override, an excused cell).
* AnswerFix: one answer the teacher marked right (or gave partial credit) after the auto-grader got it wrong.
* Category, TeacherItem, TeacherScore: the gradebook's weights, and the teacher's own graded items.
* Curve, Adjustment: curves on one assessment, and class-wide changes (a bonus, a dropped question).
"""
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

KIND_CHOICES = [("notes", "Lesson notes"), ("practice", "Practice"), ("quiz", "Quizzes"), ("testprep", "Test prep"),
                ("unittest", "Unit tests"), ("exam", "Practice exams")]


class Setup(models.Model):
    classroom = models.OneToOneField("accounts.Classroom", on_delete=models.CASCADE, related_name="setup")
    kinds = models.JSONField(default=dict, help_text="kind -> its settings; missing keys fall back to the defaults")
    units = models.JSONField(default=dict, help_text='unit number (as text) -> {kind: settings} for a unit set apart')
    show = models.JSONField(default=dict, help_text="what students see: grade, due_dates, unopened, behind")
    watch = models.JSONField(default=dict, help_text="what the dashboard flags: missing, hard_questions, sliding, inactive_days")
    template = models.CharField(max_length=30, blank=True)
    days = models.JSONField(default=list, blank=True, help_text="weekdays the class meets, 0 = Monday; empty = Monday to Friday")
    tz = models.CharField(max_length=40, default="America/New_York", help_text="the class's time zone: due 11:59 pm means there")
    grading = models.JSONField(default=dict, blank=True, help_text='{"scale": [["A", 90], ["B", 80], ...]}')
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Setup for {self.classroom}"


class Dated(models.Model):
    """One piece of work on the class calendar: a lesson's notes, practice or quiz ("2.5"), a unit test ("U2"), a
    practice exam ("ab1"). Open and due times, plus any settings of its own that differ from the class setup."""
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="dated")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    ref = models.CharField(max_length=12)
    opens = models.DateTimeField(null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    late_until = models.DateTimeField(null=True, blank=True, help_text="late work accepted until; empty = the class rule")
    settings = models.JSONField(default=dict, blank=True, help_text="this item's own settings, over the class setup")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["classroom", "kind", "ref"], name="one_date_row_per_item")]
        ordering = ["due", "opens"]

    def __str__(self):
        return f"{self.classroom.name}: {self.kind} {self.ref}"


class NoSchool(models.Model):
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="no_school")
    day = models.DateField()
    note = models.CharField(max_length=60, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["classroom", "day"], name="one_no_school_per_day")]


class StudentException(models.Model):
    """One student's own terms for one piece of work: a later due date, extra time on a timed test, or excused."""
    dated = models.ForeignKey(Dated, on_delete=models.CASCADE, related_name="exceptions")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="work_exceptions")
    due = models.DateTimeField(null=True, blank=True)
    late_until = models.DateTimeField(null=True, blank=True)
    time_factor = models.FloatField(default=1.0)
    excused = models.BooleanField(default=False)
    reopened = models.BooleanField(default=False, help_text="a closed quiz or test reopened for this student")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["dated", "student"], name="one_exception_per_student")]


class Accommodation(models.Model):
    """Standing terms for one student in one class, applied to every timed test (1.5x time, for example)."""
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="accommodations")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accommodations")
    time_factor = models.FloatField(default=1.0)
    note = models.CharField(max_length=120, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["classroom", "student"], name="one_accommodation_per_student")]


class Mark(models.Model):
    """A cell the teacher filled in or changed: a paper quiz score, a paper test part, notes marked done, a grade
    override, an excused item. part "" is the whole item; a unit test's parts are "mc", "frq1", "frq2", ..."""
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="marks")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_marks")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    ref = models.CharField(max_length=12)
    part = models.CharField(max_length=12, blank=True)
    points = models.FloatField(null=True, blank=True)
    possible = models.FloatField(null=True, blank=True)
    done = models.BooleanField(null=True, blank=True)
    excused = models.BooleanField(default=False)
    absent = models.BooleanField(default=False)
    by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["classroom", "student", "kind", "ref", "part"], name="one_mark_per_cell")]


class AnswerFix(models.Model):
    """The teacher's ruling on one answer the auto-grader judged: right, or partial credit (0 to 1).
    Kept per student; "the same answer for everyone" makes one row per student who typed it."""
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="answer_fixes")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answer_fixes")
    topic = models.CharField(max_length=12)
    item = models.CharField(max_length=40)
    credit = models.FloatField(default=1.0)
    by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["classroom", "student", "topic", "item"], name="one_fix_per_answer")]


class GraderMiss(models.Model):
    """An answer a teacher marked right that the grader called wrong: Adder's queue for fixing the grader."""
    topic = models.CharField(max_length=12)
    item = models.CharField(max_length=40)
    given = models.CharField(max_length=300)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="+")
    at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["resolved", "-at"]

    def __str__(self):
        return f"{self.topic} {self.item}: {self.given!r}"


class Category(models.Model):
    """One gradebook category. source is a kind of work (its items come from the site and from Marks), or "own" for
    the teacher's own items (participation, labs)."""
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=60)
    source = models.CharField(max_length=10, choices=KIND_CHOICES + [("own", "Your own items")])
    weight = models.FloatField(default=0)
    rules = models.JSONField(default=dict, blank=True, help_text="drop_lowest, late_factor, final_replaces_lowest, best_of")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "pk"]


class TeacherItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=80)
    points = models.FloatField(default=10)
    day = models.DateField(null=True, blank=True)
    done_only = models.BooleanField(default=False, help_text="scored as done or not")
    hidden = models.BooleanField(default=False, help_text="students don't see it")

    class Meta:
        ordering = ["day", "pk"]


class TeacherScore(models.Model):
    item = models.ForeignKey(TeacherItem, on_delete=models.CASCADE, related_name="scores")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_scores")
    points = models.FloatField(null=True, blank=True)
    excused = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["item", "student"], name="one_score_per_item")]


class Curve(models.Model):
    METHODS = [("mean", "Set the class average"), ("add", "Add points to everyone"), ("top", "Scale so the top score is 100%"),
               ("sqrt", "Square root"), ("ap", "From AP scores")]
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="curves")
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    ref = models.CharField(max_length=12)
    method = models.CharField(max_length=6, choices=METHODS)
    params = models.JSONField(default=dict, blank=True)
    allow_over = models.BooleanField(default=False, help_text="scores may go over 100%")
    at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["classroom", "kind", "ref"], name="one_curve_per_item")]


class Adjustment(models.Model):
    """A class-wide change: "bonus" adds points to every final grade; "drop_question" removes one question from one
    quiz or test for everyone."""
    KINDS = [("bonus", "Points on every final grade"), ("drop_question", "Drop one question for everyone")]
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="adjustments")
    kind = models.CharField(max_length=14, choices=KINDS)
    params = models.JSONField(default=dict)
    note = models.CharField(max_length=120, blank=True)
    at = models.DateTimeField(auto_now_add=True)


class TeacherNote(models.Model):
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="notes")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teacher_notes")
    text = models.TextField(blank=True)
    at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["classroom", "student"], name="one_note_per_student")]
