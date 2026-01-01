from django.shortcuts import render


def student_menu(request):
    return render(request, "student_menu.html")


def request_history(request):
    sorted_requests = request.user.student_user.event_log.all().order_by("-updated_at")
    context = {
        "request_history": sorted_requests,
    }
    return render(request, "request_history.html", context)
