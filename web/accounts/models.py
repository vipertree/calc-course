import secrets

from django.conf import settings
from django.db import models

# No 0/O/1/I/L: a join code gets read off a projector and typed on a phone.
CODE_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def new_code():
    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(6))


class Profile(models.Model):
    TEACHER, STUDENT = "teacher", "student"
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=[(TEACHER, "Teacher"), (STUDENT, "Student")], default=STUDENT)
    display_name = models.CharField(max_length=80)
    full_access = models.BooleanField(default=False, help_text="Paid or granted access outside a class")

    def __str__(self):
        return f"{self.display_name} ({self.role})"

    @property
    def is_teacher(self):
        return self.role == self.TEACHER


class Classroom(models.Model):
    name = models.CharField(max_length=80)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="classrooms")
    code = models.CharField(max_length=6, unique=True, default=new_code)
    course = models.CharField(max_length=2, choices=[("AB", "AP Calculus AB"), ("BC", "AP Calculus BC")], default="AB")
    open = models.BooleanField(default=True, help_text="Students can join with the code")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} [{self.code}]"


class Enrollment(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name="enrollments")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="enrollments")
    joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [("classroom", "student")]


def has_full_access(user):
    """Notes, quizzes, test prep and unit tests. Teachers, students in a class, and anyone granted access."""
    if not user.is_authenticated:
        return False
    p = getattr(user, "profile", None)
    if p is None:
        return user.is_superuser
    return p.is_teacher or p.full_access or user.enrollments.exists()


def class_for(user):
    """The class a student takes quizzes and tests with, or None for individual (self-paced) users.
    Class students all get the same form and see results only after the teacher releases them."""
    if not user.is_authenticated:
        return None
    p = getattr(user, "profile", None)
    if p is not None and p.is_teacher:
        return None
    e = user.enrollments.select_related("classroom").order_by("-joined").first()
    return e.classroom if e else None
