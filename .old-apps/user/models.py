import uuid

from django.contrib.auth.models import User
from django.db import models

from classroom.models import Request


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_location = models.UUIDField(default=None, null=True, blank=True)
    active_request = models.ForeignKey(
        Request,
        default=None,
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING,
        related_name="active_student_request",
    )
    flex_room = models.UUIDField(default=None, null=True)
    flex_active = models.BooleanField(default=False)
    event_log = models.ManyToManyField(
        Request, blank=True, related_name="event_log")

    def __str__(self):
        return f"{self.user.username} - {self.id}"
