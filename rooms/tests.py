from django.test import TestCase
from users.models import CustomUser
from moderators.models import Moderator
from students.models import Student
from rooms.models import Room, Request


class RoomTestCase(TestCase):
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

    def test_send_request(self):
        """Request is sent successfully"""

        request = Request.send(
            student=self.testStudent1,
            destination=self.testRoom2,
            reason="Tech Club",
            round_trip=False,
        )

        self.assertEqual(self.testStudent1.active_request, request)

        self.assertIsNotNone(request)
        self.assertEqual(request.requesting_student, self.testStudent1)
        self.assertEqual(request.destination, self.testRoom2)
        self.assertEqual(request.reason, "Tech Club")
        self.assertEqual(request.round_trip, False)

    def test_approve_request(self):
        """Request is approved"""

        request = Request.send(
            student=self.testStudent1,
            destination=self.testRoom2,
            reason="Tech Club",
            round_trip=False,
        )

        request.approve()

        self.assertEqual(self.testStudent1.current_location, self.testRoom2)
        self.assertIsNotNone(
            self.testRoom2.current_students.filter(pk=self.testStudent1.pk)
        )
        self.assertFalse(
            self.testRoom1.current_students.filter(pk=self.testStudent1.pk).exists()
        )

    def test_deny_request(self):
        """Request is Denyed"""

        request = Request.send(
            student=self.testStudent1,
            destination=self.testRoom2,
            reason="Tech Club",
            round_trip=False,
        )

        request.deny()

        self.assertEqual(self.testStudent1.current_location, self.testRoom1)
        self.assertIsNotNone(
            self.testRoom1.current_students.filter(pk=self.testStudent1.pk)
        )
        self.assertFalse(
            self.testRoom2.current_students.filter(pk=self.testStudent1.pk).exists()
        )
