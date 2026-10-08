from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class StepDone(models.Model):
    """A student finished one step (section) of a lesson's notes."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="steps_done")
    topic = models.CharField(max_length=8)
    step = models.PositiveSmallIntegerField()
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("user", "topic", "step")]


class Response(models.Model):
    """One checked answer: a notes blank, a check, a practice item, a test-prep item or FRQ part."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="responses")
    topic = models.CharField(max_length=8)
    item = models.CharField(max_length=40)
    area = models.CharField(max_length=10)     # notes | practice | testprep | frq
    given = models.CharField(max_length=300)
    correct = models.BooleanField()
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=["user", "topic", "area"])]


class Draft(models.Model):
    """What a student has typed or picked in one answer box, saved as they go, so a reload or another device
    shows it again. Not graded: Response is the record of checked answers."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="drafts")
    topic = models.CharField(max_length=8)
    item = models.CharField(max_length=40)
    value = models.TextField(blank=True)
    revealed = models.BooleanField(default=False)     # a notes blank whose answer the student chose to show
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "topic", "item"], name="one_draft_per_box")]


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quiz_attempts")
    topic = models.CharField(max_length=8)
    score = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()
    detail = models.JSONField(default=dict)    # item id -> {"given":..., "correct":...}
    served = models.JSONField(default=list)    # the item ids this attempt was given, in order
    classroom = models.ForeignKey("accounts.Classroom", null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name="attempts", help_text="Set for class students: results wait for release")
    form = models.CharField(max_length=1, blank=True, help_text="Paper form letter for class attempts")
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-at"]


class FRQScore(models.Model):
    """A student's own rubric score for one FRQ part (AP-style self-assessment)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="frq_scores")
    topic = models.CharField(max_length=8)
    part = models.CharField(max_length=40)
    earned = models.PositiveSmallIntegerField()
    possible = models.PositiveSmallIntegerField()
    at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "part")]


class Release(models.Model):
    """A teacher has released a quiz or unit test's scores and solutions to one class."""
    classroom = models.ForeignKey("accounts.Classroom", on_delete=models.CASCADE, related_name="releases")
    topic = models.CharField(max_length=8)
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("classroom", "topic")]


class IssuedPacket(models.Model):
    """A personalized topic packet someone downloaded. The code is printed on every page of their copy,
    so a copy found elsewhere can be traced back to who printed it."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="packets")
    topic = models.CharField(max_length=8)
    code = models.CharField(max_length=9, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.code} ({self.topic}, {self.user})"


class ExamAttempt(models.Model):
    """One sitting of a full-length practice exam (content/exams/). The server owns the clock: a part starts when the
    server stamps part_started, its deadline is that stamp plus the part's minutes, and an answer that arrives after it
    (or for a part already over) is refused. Parts only move forward. See course/exams.py."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_attempts")
    exam = models.CharField(max_length=20)                        # the exam's slug, "ab1"
    started = models.DateTimeField(auto_now_add=True)
    part = models.PositiveSmallIntegerField(default=0)            # index of the current part; len(parts) = all done
    part_started = models.DateTimeField(null=True, blank=True)    # null: waiting on the "start this part" screen
    timing = models.JSONField(default=dict)                       # part key -> {"start", "end", "timed_out"}
    answers = models.JSONField(default=dict)                      # multiple-choice item id -> letter
    flags = models.JSONField(default=list)                        # item ids marked for review
    frq = models.JSONField(default=dict)                          # FRQ part id -> [bool per rubric line], self-scored
    finished = models.DateTimeField(null=True, blank=True)
    mc_score = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        ordering = ["-started"]
        indexes = [models.Index(fields=["user", "exam"])]

    def __str__(self):
        return f"{self.exam} #{self.pk} ({self.user})"
