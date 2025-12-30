from django.test import TestCase
from users.models import CustomUser
from moderators.models import Moderator
from students.models import Student
from rooms.models import Room, Request


class StudentTestCase(TestCase):
    def setUp(self):
        self.testUser1 = CustomUser.objects.create_user(
            email="testuser@example.com",
            password="oT7J6tH4K3wrWh",
            first_name="Test",
            last_name="User",
            is_moderator=True,
        )
        self.testUser2 = CustomUser.objects.create_user(
            email="anothermiscuser@example.com",
            password="McvIR43ifQf9eu",
            first_name="Bob",
            last_name="Smith",
            is_moderator=False,
        )
        self.testModerator1 = Moderator.objects.create(
            user=self.testUser1,
        )
        self.testStudent1 = Student.objects.create(
            user=self.testUser2,
        )
        self.testRoom1 = Room.objects.create(
            name="Flex 1",
            description="Testing flex room",
            isFlexOne=True,
            max_students=10,
            open_room=False,
        )
        self.testRoom2 = Room.objects.create(
            name="Flex 2",
            description="Another testing flex room",
            isFlexOne=True,
            max_students=5,
            open_room=True,
        )
        self.testRoom1.set_moderator(self.testModerator1)
        self.testRoom2.set_moderator(self.testModerator1)
        self.testStudent1.set_room(self.testRoom1)

    def test_set_room(self):
        """Set Room"""

        self.testStudent1.set_room(self.testRoom2)

        self.assertEqual(self.testStudent1.current_location, self.testRoom2)
