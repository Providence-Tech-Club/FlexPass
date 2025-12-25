from .models import Request, Room


def send_request(
    student,
    current_room: Room,
    destination: Room,
    reason: str,
    round_trip: bool,
) -> str:
    if destination.current_students.count() >= destination.max_students:
        return "failed"

    if destination.current_students.filter(id=student.id).exists():
        return "failed"

    request = Request.objects.create(
        requesting_student=student,
        destination=destination,
        reason=reason,
        round_trip=round_trip,
    )

    current_room.active_requests.add(request)
    destination.current_students.add(student)
    destination.save()
    student.active_request = request
    student.save()

    return "success"


def approve_request():
    pass
