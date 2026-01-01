import logging
import random
import string
from typing import Optional

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Defined by Student
    requesting_student = models.ForeignKey(
        "students.Student", null=True, on_delete=models.SET_NULL
    )
    origin = models.ForeignKey(
        "rooms.Room", null=True, on_delete=models.SET_NULL, related_name="orgin"
    )
    destination = models.ForeignKey(
        "rooms.Room", null=True, on_delete=models.SET_NULL, related_name="destination"
    )
    reason = models.CharField(max_length=100, null=True)
    round_trip = models.BooleanField(
        help_text="Will the student come back to the flex room they left?",
    )
    returned = models.BooleanField(default=False, help_text="Has the student returned?")

    # Defined by Moderator
    approved = models.BooleanField(
        default=False, help_text="Has the request been approved?"
    )
    reviewed_by = models.ForeignKey(
        "moderators.Moderator", default=None, null=True, on_delete=models.SET_NULL
    )
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{str(self.updated_at)} - {self.reason}"

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
            origin=current_room,
            destination=destination,
            reason=reason,
            round_trip=round_trip,
        )

        current_room.active_requests.add(request)
        student.active_request = request
        student.save()

        # Send update to moderator
        channel_layer = get_channel_layer()
        group_name = f"request_{current_room.moderator.user.id}"
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "status_update",
                "action": "new",
                "status": "info",
                "message": "New Request",
            },
        )

        return request

    def approve(self, moderator: Moderator) -> None:
        self.approved = True
        self.reviewed_by = moderator
        self.save()

        self.requesting_student.active_request = None
        self.requesting_student.save()

        self.requesting_student.set_room(self.destination)
        self.requesting_student.event_log.add(self)
        self.origin.active_requests.remove(self)

        # Send update to student
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"request_{self.requesting_student.user.id}",
            {
                "type": "status_update",
                "action": "update",
                "status": "success",
                "message": "Request Approved",
            },
        )

    def deny(self, moderator: Moderator) -> None:
        self.approved = False
        self.reviewed_by = moderator
        self.save()

        self.requesting_student.active_request = None
        self.requesting_student.save()

        self.requesting_student.event_log.add(self)
        self.origin.active_requests.remove(self)

        # Send update to student
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"request_{self.requesting_student.user.id}",
            {
                "type": "status_update",
                "action": "update",
                "status": "error",
                "message": "Request Denied",
            },
        )


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
    description = models.CharField(
        max_length=200, help_text="Description of room for flex time.", blank=True
    )
    isFlexOne = models.BooleanField(help_text="Is this a flex room during flex 1.")
    max_students = models.IntegerField(default=20)
    open_room = models.BooleanField(
        default=False, help_text="Is the room availible to all students?"
    )
    allowed_students = models.ManyToManyField(
        "students.Student", blank=True, related_name="room_allowed"
    )
    is_archived = models.BooleanField(default=False)

    # Constantly Changing Values
    current_students = models.ManyToManyField("students.Student", blank=True)
    active_requests = models.ManyToManyField(Request, blank=True)
    flex_active = models.BooleanField(default=False)

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
        self.save()

        moderator.moderated_rooms.add(self)
