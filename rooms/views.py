from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RequestForm
from .models import Room, Request

import logging


def index(request):
    return HttpResponse("Welcome to the classroom view.")


def request_list(request):
    return render(request, "request_list.html")


@login_required()
def request(request):
    destination_id = request.GET.get("destination")
    destination = Room.objects.get(pk=destination_id)

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            reason = form.get_reason()
            round_trip = form.clean()["round_trip"]

            flex_request = Request.send(
                request.user.student_user, destination, reason, round_trip
            )

            encoded_params = urlencode(
                {"status": "success" if flex_request else "failed"}
            )
            return redirect(f"/rooms?{encoded_params}")
    else:
        form = RequestForm()

    return render(request, "request.html", {"form": form, "room": destination})


@login_required()
def room_list(request):
    rooms = Room.objects.all()
    context = {"rooms": rooms}

    if request.method == "POST":
        destination_id = request.POST.get("room_id")

        encoded_params = urlencode(
            {
                "destination": destination_id,
            }
        )
        return redirect(f"/rooms/request?{encoded_params}")
    elif request.method == "GET":
        status = request.GET.get("status")
        context["status"] = status

    return render(request, "room_list.html", context)
