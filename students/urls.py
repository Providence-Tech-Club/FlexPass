from django.urls import path

from . import views

urlpatterns = [
    path("", views.student_menu, name="student_menu"),
    path("requests/", views.request_history, name="request_history"),
]
