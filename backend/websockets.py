import django.db.models
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from backend.models import CardForPlayer, Player
from backend.views import *
import json


def str_to_list(string: str) -> list[int]:
    out = []
    for char in string:
        try:
            out.append(int(char))
        except ValueError:
            pass
    return out


@database_sync_to_async
def get_cards(username: str) -> list[int]:
    return str_to_list(CardForPlayer.objects.get(playerID__username=username).cards)


@database_sync_to_async
def get_players(game_id: int) -> list[Player]:
    return Player.objects.filter(gameID_id=game_id)


# Django WebSocket for game client
class GameWSClient(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.username = self.scope['url_route']['kwargs']['username']

        # Обновляю игроков в игре
        #          карты у игрока
        cards = await get_cards(self.username)
        players = await get_players(self.game_id)
        data = {
            'func': 'data',
            'cards': cards,
            'players': players
        }
        print(data)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            data = text_data
        if data.isinstance(dict):
            if data['func'] == 'data':
                pass

    async def send_data(self, data: dict):
        await self.send(text_data=json.dumps(data))
