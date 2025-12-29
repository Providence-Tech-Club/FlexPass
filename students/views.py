from django.shortcuts import render


def student_menu(request):
    return render(request, "student_menu.html")


def request_history(request):
    return render(request, "request_history.html")
