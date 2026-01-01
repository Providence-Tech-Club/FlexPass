from django.contrib import messages
from django.shortcuts import render, redirect

from rooms.models import Request
from users.utils import moderator_required


@moderator_required
def moderator_menu(request):
    return render(request, "moderator_menu.html")


@moderator_required
def room_management(request):
    return render(request, "room_management.html")


@moderator_required
def pending_requests(request):
    if request.method == "POST":
        request_id = request.POST.get("request_id")
        action = request.POST.get("action")

        pending_request = Request.objects.get(pk=request_id)
        if action == "approve":
            pending_request.approve(request.user.moderator_user)
            messages.info(request, "Approved Request")
        else:
            pending_request.deny(request.user.moderator_user)
            messages.info(request, "Denied Request")

        return redirect("pending_requests")

    total_requests = Request.objects.none()

    for room in request.user.moderator_user.moderated_rooms.all():
        total_requests |= room.active_requests.all()

    sorted_requests = total_requests.order_by("-created_at")
    reviewed_requests = Request.objects.filter(
        reviewed_by=request.user.moderator_user
    ).order_by("-updated_at")
    context = {
        "pending_requests": sorted_requests,
        "reviewed_requests": reviewed_requests,
    }
    return render(request, "pending_requests.html", context)


@moderator_required
def student_lookup(request):
    return render(request, "student_lookup.html")
