from .models import Request, Room


def send_request(
    student,
    current_room: Room,
    destination: Room,
    reason: str,
    round_trip: bool,
) -> str:
    if len(destination.current_students) >= destination.max_students:
        return "failed"

    if student.id in destination.current_students:
        return "failed"

    request = Request.objects.create(
        requesting_student=student.id,
        destination=destination,
        reason=reason,
        round_trip=round_trip,
    )

    current_room.active_requests.add(request)
    destination.current_students.append(student.id)
    destination.save()
    student.active_request = request
    student.save()

    return "success"


def approve_request():
    pass
