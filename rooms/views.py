from urllib.parse import urlencode

# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RequestForm
from .models import Room
from .utils import send_request


def index(request):
    return HttpResponse("Welcome to the classroom view.")


def request_list(request):
    return render(request, "request_list.html")


@login_required()
def request(request):
    destination_id = request.GET.get("destination")
    destination = Room.objects.get(pk=destination_id)

    # print(request.user.Student)

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            reason = form.get_reason()
            round_trip = form.clean()["round_trip"]

            current_room = request.user.student.current_location
            print(current_room)
            # return

            # current_room = Room.objects.get(pk=current_room_id)

            status = send_request(
                request.user.student, current_room, destination, reason, round_trip
            )

            # print(current_room)
            encoded_params = urlencode({"status": status})
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
        # destination = Classroom.objects.get(pk=room_id)

        # current_room_id = request.user.student.current_location
        # current_room = Classroom.objects.get(pk=current_room_id)

        encoded_params = urlencode(
            {
                # "current_room_id": current_room_id,
                "destination": destination_id,
            }
        )
        return redirect(f"/rooms/request?{encoded_params}")
    elif request.method == "GET":
        status = request.GET.get("status")
        context["status"] = status

    return render(request, "room_list.html", context)
