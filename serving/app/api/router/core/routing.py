from django.urls import include, path

from core.ws import ChatConsumer, GptResponseGenerator

websocket_urlpatterns = [
    path('talk/<str:username>/', GptResponseGenerator.as_asgi()),
    path('chat/<str:room_name>/', ChatConsumer.as_asgi()),
]
