from django.contrib import admin

from .models import FRQScore, IssuedPacket, QuizAttempt, Response, StepDone

for m in (StepDone, Response, QuizAttempt, FRQScore):
    admin.site.register(m)


@admin.register(IssuedPacket)
class IssuedPacketAdmin(admin.ModelAdmin):
    """Look a packet ID up here to see who printed that copy."""
    list_display = ("code", "topic", "user", "created")
    search_fields = ("code", "user__username", "user__profile__display_name")
    list_filter = ("topic",)
    readonly_fields = ("user", "topic", "code", "created")
