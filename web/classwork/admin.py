from django.contrib import admin

from .models import GraderMiss


@admin.register(GraderMiss)
class GraderMissAdmin(admin.ModelAdmin):
    """Answers teachers marked right that the grader called wrong: fix the grader, then tick resolved."""
    list_display = ("topic", "item", "given", "reported_by", "at", "resolved")
    list_filter = ("resolved",)
    list_editable = ("resolved",)
