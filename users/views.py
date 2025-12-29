import logging

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_not_required
from django.shortcuts import redirect, render

from .forms import AuthenticationForm, RegistrationForm

logger = logging.getLogger(__name__)


@login_not_required
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


@login_not_required
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


def logout_view(request):
    logout(request)

    return redirect("/")


def account(request):
    return render(request, "account.html")
