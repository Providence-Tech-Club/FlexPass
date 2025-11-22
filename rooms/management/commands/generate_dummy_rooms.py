from django.core.management.base import BaseCommand
from faker import Faker

from moderators.models import Moderator
from rooms.models import Room
from users.models import CustomUser

fake = Faker()


class Command(BaseCommand):
    help = "Generates dummy data for Room & Moderator"

    def handle(self, *args, **options):
        for i in range(10):  # Generate 10 instances
            new_user = CustomUser.objects.create_user(
                email=fake.free_email(),
                password=fake.password(length=12),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                is_moderator=True,
            )
            new_mod = Moderator.objects.create(
                user=new_user,
            )
            new_room = Room.objects.create(
                moderator=new_mod,
                name=fake.word(),
                isFlexOne=fake.boolean(),
                description=fake.sentence(),
                max_students=fake.pyint(min_value=2, max_value=40),
                open_room=fake.boolean(chance_of_getting_true=75),
            )
            new_mod.moderated_rooms.add(new_room)

        self.stdout.write(self.style.SUCCESS(
            "Successfully generated dummy data"))
