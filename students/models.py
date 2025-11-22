from django.db import models

from users.models import CustomUser


class Student(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="student_user"
    )
    current_location = models.ForeignKey(
        "rooms.Room",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="student_location",
    )
    active_request = models.ForeignKey(
        "rooms.Request",
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="student_request",
    )
    flex_room = models.ForeignKey(
        "rooms.Room",
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        related_name="student_flex",
    )
    flex_active = models.BooleanField(default=False)
    event_log = models.ManyToManyField(
        "rooms.Request", blank=True, related_name="student_log"
    )

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"
