from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/request-new/$", consumers.RequestNewConsumer.as_asgi()),
]
