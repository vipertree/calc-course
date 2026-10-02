from django.contrib import admin

from .models import Classroom, Enrollment, Profile

admin.site.register(Profile)
admin.site.register(Classroom)
admin.site.register(Enrollment)
