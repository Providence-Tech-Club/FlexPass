from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import AuthenticationForm

urlpatterns = [
    # path("", views.room_list, name="room_list"),
    path(
        "login/",
        views.email_login,
        # auth_views.LoginView.as_view(
        #     template_name="registration/login.html",
        #     # authentication_form=AuthenticationForm,
        # ),
        name="login",
    ),
    path("register/", views.register, name="register"),
    # path("request_list", views.request_list, name="request_list"),
]
