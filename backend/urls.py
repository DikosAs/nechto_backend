from django.urls import path
from .views import *

app_name = 'backend'

servers = ['1', '2', '3', '4', '5']

urlpatterns = [
    path('game-list/', games_list),
    path('<int:game_id>/data-load/<str:username>', load_data),
    path('<int:game_id>/add-player/<str:username>', add_player),
    path('<int:game_id>/del-player/<str:username>', del_player)
]
