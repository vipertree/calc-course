from django.contrib import admin
from django.contrib.auth import views as auth
from django.urls import path, re_path

from accounts import views as acc
from course import views as v

NUM = r"(?P<num>\d{1,2}\.\d{1,2}|U\d{1,2})"

urlpatterns = [
    path("", v.home, name="home"),
    path("login/", auth.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth.LogoutView.as_view(), name="logout"),
    path("join/", acc.join, name="join"),
    path("course/", v.course_map, name="map"),
    path("formulas/", v.formulas, name="formulas"),
    re_path(rf"^topic/{NUM}/$", v.lesson, name="lesson"),
    re_path(rf"^topic/{NUM}/(?P<area>practice|quiz|testprep)/$", v.lesson, name="lesson_area"),
    re_path(r"^topic/(?P<num>\d{1,2}\.\d{1,2})/packet/$", v.packet, name="packet"),
    re_path(rf"^api/{NUM}/check/$", v.api_check, name="api_check"),
    re_path(rf"^api/{NUM}/step/$", v.api_step, name="api_step"),
    re_path(rf"^api/{NUM}/draft/$", v.api_draft, name="api_draft"),
    re_path(rf"^api/{NUM}/quiz/$", v.api_quiz, name="api_quiz"),
    re_path(rf"^api/{NUM}/frq/$", v.api_frq_score, name="api_frq"),
    re_path(r"^unit/(?P<num>U\d{1,2})/test/$", v.unit_test, name="unit_test"),
    re_path(r"^unit/(?P<num>U\d{1,2})/test/print/(?P<form>[A-Z])/(?P<kind>test|key)/$", v.test_pdf, name="test_pdf"),
    path("teacher/", v.teacher, name="teacher"),
    path("teacher/transcripts/", v.transcripts, name="transcripts"),
    path("teacher/handouts/", v.handouts, name="handouts"),
    re_path(rf"^teacher/handouts/{NUM}/(?P<name>[\w.-]+\.pdf)$", v.handout_pdf, name="handout_pdf"),
    path("teacher/class/new/", v.new_class, name="new_class"),
    path("teacher/class/<int:pk>/toggle/", v.toggle_class, name="toggle_class"),
    re_path(rf"^teacher/class/(?P<pk>\d+)/release/{NUM}/$", v.release, name="release"),
    re_path(r"^video/(?P<name>[\w.-]+)$", v.video, name="video"),
    path("theme/<str:theme>/", v.set_theme, name="theme"),
    path("design/<str:design>/", v.set_design, name="design"),
    path("admin/", admin.site.urls),
]
