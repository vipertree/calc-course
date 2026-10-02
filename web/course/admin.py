from django.contrib import admin

from .models import FRQScore, QuizAttempt, Response, StepDone

for m in (StepDone, Response, QuizAttempt, FRQScore):
    admin.site.register(m)
