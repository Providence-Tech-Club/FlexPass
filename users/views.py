from .forms import AuthenticationForm, RegistrationForm
from django.contrib.auth import login
from django.shortcuts import redirect, render
import logging

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            if user:
                login(request, user)
                return redirect("/")
            else:
                form.add_error("join_code", "Invalid Join Code")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


def email_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm(request)

    return render(request, "login.html", {"form": form})
