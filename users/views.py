from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import RegistrationForm, AuthenticationForm


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


def email_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")  # change this to your desired success URL
    else:
        form = AuthenticationForm(request)

    return render(request, "registration/login.html", {"form": form})
