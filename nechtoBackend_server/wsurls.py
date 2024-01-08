from django.urls import path
from backend.websockets import GameWSClient

websocket_urlpatterns = [
    path('ws/<str:username>@<int:game_id>/', GameWSClient.as_asgi()),
]
