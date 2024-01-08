from django.urls import path
from .views import games_list, load_data, add_player, del_player, update_data_on_client

app_name = 'backend'

servers = ['1', '2', '3', '4', '5']

urlpatterns = [
    path('game-list/', games_list),
    path('<int:game_id>/data-load/<str:username>', load_data),
    path('<int:game_id>/add-player/<str:username>', add_player),
    path('<int:game_id>/del-player/<str:username>', del_player),
    path('update-data/', update_data_on_client),
]
