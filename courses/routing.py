from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/get-mark/', consumers.GetMarkConsumer.as_asgi()),
]
