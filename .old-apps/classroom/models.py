import random
import string
import uuid

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models


def generate_unique_join_code():
    """Generates a unique 6-character alphanumeric join code."""
    length = 6
    characters = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choice(characters) for _ in range(length))
        if not Classroom.objects.filter(join_code=code).exists():
            return code


class Request(models.Model):
    # Defined by Program
    time_of_request = models.TimeField(auto_now=True, editable=False)
    requesting_student = models.UUIDField(default=None, null=True)

    # Defined by Student
    destination = models.UUIDField(default=None, null=True)
    reason = models.CharField(max_length=100, null=True)
    round_trip = models.BooleanField(
        default=False,
        help_text="Will the student come back to the flex room they left?",
    )

    # Defined by Moderator
    approved = models.BooleanField(
        default=False, help_text="Has the request been approved?"
    )

    def __str__(self):
        return f"{str(self.time_of_request)} - {self.reason}"


class Classroom(models.Model):
    # Generated Values
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    join_code = models.CharField(
        max_length=6,
        unique=True,
        default=generate_unique_join_code,
        editable=False,
    )

    # Defined by Moderator
    moderator = models.ForeignKey(
        get_user_model(), on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100)
    isFlexOne = models.BooleanField(
        help_text="Is this a flex room during flex 1.")
    description = models.CharField(
        max_length=200, help_text="Description of room for flex time.", blank=True
    )
    max_students = models.IntegerField(default=20)
    open_room = models.BooleanField(
        default=False, help_text="Is the room availible to all students?"
    )
    allowed_students = ArrayField(
        models.UUIDField(default=None, null=True), default=list, blank=True
    )

    # Constantly Changing Values
    current_students = ArrayField(
        models.UUIDField(default=None, null=True), default=list, blank=True
    )
    active_requests = models.ManyToManyField(Request, blank=True)

    def __str__(self):
        return f"{self.name} - {self.id}"

    def save(self, *args, **kwargs):
        if (
            not self.pk and not self.join_code
        ):  # Only generate on first save if not already set
            self.join_code = generate_unique_join_code()
        super().save(*args, **kwargs)
