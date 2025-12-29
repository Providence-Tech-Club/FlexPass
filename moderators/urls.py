from django.urls import path

from . import views

urlpatterns = [
    path("", views.moderator_menu, name="moderator_menu"),
    path("manage/", views.room_management, name="room_management"),
    path("requests/", views.pending_requests, name="pending_requests"),
    path("student-lookup/", views.student_lookup, name="student_lookup"),
]
