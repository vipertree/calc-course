from django.urls import path, re_path

from . import views as v

urlpatterns = [
    path("<int:pk>/setup/", v.setup_page, name="cw_setup"),
    path("<int:pk>/calendar/", v.calendar_page, name="cw_calendar"),
    path("<int:pk>/progress/", v.progress_page, name="cw_progress"),
    path("<int:pk>/", v.class_home, name="cw_home"),
    path("<int:pk>/quizzes/", v.quizzes_page, name="cw_quizzes"),
    re_path(r"^(?P<pk>\d+)/quizzes/(?P<ref>\d{1,2}\.\d{1,2}|U\d{1,2}(?:BC)?)/$", v.quiz_page, name="cw_quiz"),
    path("<int:pk>/students/", v.students_page, name="cw_students"),
    path("<int:pk>/students/<int:uid>/", v.student_page, name="cw_student"),
]
