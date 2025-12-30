import random
import string
from typing import Optional

from django.db import models
from moderators.models import Moderator

from students.models import Student


def generate_unique_join_code():
    """Generates a unique 6-character alphanumeric join code."""
    length = 6
    characters = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choice(characters) for _ in range(length))
        if not Room.objects.filter(join_code=code).exists():
            return code


class Request(models.Model):
    # Defined by Program
    time_of_request = models.TimeField(auto_now=True, editable=False)
    requesting_student = models.ForeignKey(
        "students.Student", default=None, null=True, on_delete=models.SET_NULL
    )

    # Defined by Student
    destination = models.ForeignKey(
        "rooms.Room", default=None, null=True, on_delete=models.SET_NULL
    )
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

    def send(
        student: Student,
        destination: "Room",
        reason: str,
        round_trip: bool,
    ) -> Optional["Request"]:
        """Checks if a request can be sent, then creates a request"""
        if (
            destination.current_students.count() - destination.active_requests.count()
            >= destination.max_students
        ):
            return

        if destination.current_students.filter(id=student.id).exists():
            return

        current_room = student.current_location

        request = Request.objects.create(
            requesting_student=student,
            destination=destination,
            reason=reason,
            round_trip=round_trip,
        )

        current_room.active_requests.add(request)
        student.active_request = request
        student.save()

        return request

    def approve(self) -> None:
        self.approved = True
        self.save()
        self.requesting_student.active_request = None
        self.requesting_student.save()
        self.destination.active_requests.remove(self)
        self.requesting_student.set_room(self.destination)
        self.requesting_student.event_log.add(self)

    def deny(self) -> None:
        self.requesting_student.active_request = None
        self.requesting_student.save()
        self.destination.active_requests.remove(self)


class Room(models.Model):
    # Generated Values
    join_code = models.CharField(
        max_length=6,
        unique=True,
        default=generate_unique_join_code,
        # editable=False,
    )

    # Defined by Moderator
    moderator = models.ForeignKey(
        "moderators.Moderator",
        null=True,
        on_delete=models.SET_NULL,
        related_name="room_moderator",
    )
    name = models.CharField(max_length=100)
    isFlexOne = models.BooleanField(help_text="Is this a flex room during flex 1.")
    description = models.CharField(
        max_length=200, help_text="Description of room for flex time.", blank=True
    )
    max_students = models.IntegerField(default=20)
    open_room = models.BooleanField(
        default=False, help_text="Is the room availible to all students?"
    )
    allowed_students = models.ManyToManyField(
        "students.Student", blank=True, related_name="room_allowed"
    )

    # Constantly Changing Values
    current_students = models.ManyToManyField("students.Student", blank=True)
    active_requests = models.ManyToManyField(Request, blank=True)

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.pk and not self.join_code:
            self.join_code = generate_unique_join_code()
        super().save(*args, **kwargs)

    def set_moderator(self, moderator: Moderator) -> None:
        if self.moderator:
            self.moderator.moderated_rooms.remove(self)

        self.moderator = moderator
        moderator.moderated_rooms.add(self)
