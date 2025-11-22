from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("register/", views.register, name="register"),
    path("student/", views.student, name="student"),
    path("staff/", views.staff, name="staff"),
]
