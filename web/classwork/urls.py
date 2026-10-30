from django.urls import path

from . import views as v

urlpatterns = [
    path("<int:pk>/setup/", v.setup_page, name="cw_setup"),
    path("<int:pk>/calendar/", v.calendar_page, name="cw_calendar"),
]
