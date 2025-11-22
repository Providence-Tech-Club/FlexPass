from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required()
def student(request):
    if request.user.is_staff:
        raise PermissionDenied(
            "Staff users are not allowed to access the student page."
        )
    return render(request, "student.html")


@login_required()
@staff_member_required()
def staff(request):
    return render(request, "staff.html")
