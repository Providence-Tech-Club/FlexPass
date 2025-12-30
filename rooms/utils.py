from .models import Request, Room
from students.models import Student


def send_request(
    student: Student,
    # current_room: Room,
    destination: Room,
    reason: str,
    round_trip: bool,
) -> bool:
    if destination.current_students.count() >= destination.max_students:
        return False

    if destination.current_students.filter(id=student.id).exists():
        return False

    current_room = student.current_location

    request = Request.objects.create(
        requesting_student=student,
        destination=destination,
        reason=reason,
        round_trip=round_trip,
    )

    current_room.active_requests.add(request)
    # destination.current_students.add(student)
    student.active_request = request

    return True


def approve_request(
    request: Request,
):
    request.approved = True
    request.requesting_student.active_request = None
    request.destination.active_requests.remove(request)
    request.requesting_student.set_room(request.destination)


def deny_request(
    request: Request,
):
    request.requesting_student.active_request = None
    request.destination.active_requests.remove(request)
