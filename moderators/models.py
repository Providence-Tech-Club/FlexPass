from django.db import models

from users.models import CustomUser


class Moderator(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="moderator_user"
    )
    moderated_rooms = models.ManyToManyField(
        "rooms.Room", blank=True, related_name="moderator_rooms"
    )
    reviewed_requests = models.ManyToManyField("rooms.Request", blank=True)

    def __str__(self):
        return f"{self.user.last_name}, {self.user.first_name}"
