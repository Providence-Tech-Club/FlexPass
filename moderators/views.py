from django.shortcuts import render
from users.utils import moderator_required


@moderator_required
def moderator_menu(request):
    return render(request, "moderator_menu.html")


@moderator_required
def room_management(request):
    return render(request, "room_management.html")


@moderator_required
def pending_requests(request):
    return render(request, "pending_requests.html")


@moderator_required
def student_lookup(request):
    return render(request, "student_lookup.html")
