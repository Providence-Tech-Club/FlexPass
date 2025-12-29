from django.shortcuts import render


def moderator_menu(request):
    return render(request, "moderator_menu.html")


def room_management(request):
    return render(request, "room_management.html")


def pending_requests(request):
    return render(request, "pending_requests.html")


def student_lookup(request):
    return render(request, "student_lookup.html")
