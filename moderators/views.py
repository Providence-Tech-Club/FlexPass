from django.shortcuts import render
from users.utils import moderator_required

from rooms.models import Request
import logging


@moderator_required
def moderator_menu(request):
    return render(request, "moderator_menu.html")


@moderator_required
def room_management(request):
    return render(request, "room_management.html")


@moderator_required
def pending_requests(request):
    total_requests = Request.objects.none()

    for room in request.user.moderator_user.moderated_rooms.all():
        total_requests |= room.active_requests.all()

    sorted_requests = total_requests.order_by("-created_at")
    reviewed_requests = request.user.moderator_user.reviewed_requests.order_by(
        "-updated_at"
    )
    context = {
        "pending_requests": sorted_requests,
        "reviewed_requests": reviewed_requests,
    }
    return render(request, "pending_requests.html", context)


@moderator_required
def student_lookup(request):
    return render(request, "student_lookup.html")
