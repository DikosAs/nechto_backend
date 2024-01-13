import django.db.models
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from backend.models import CardForPlayer, Player
from backend.views import *
import json


def str_to_list(string: str) -> list[int]:
    out: list[int] = []
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
def get_players(game_id: int) -> dict[int, str]:
    players: dict = {}
    for player in Player.objects.filter(gameID_id=game_id):
        players[player.position] = player.username
    return players


@database_sync_to_async
def get_card_data_for_card_id(card_id: int) -> Card:
    return Card.objects.get(id=card_id)


# Django WebSocket for game client
class GameWSClient(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        self.game_id = self.scope['url_route']['kwargs']['game_id']
        self.username = self.scope['url_route']['kwargs']['username']

        self.channel_layer.group_add(
            self.game_id,
            self.channel_name
        )

        await self.send_data(base_data=True)

    async def disconnect(self, close_code):
        await self.send_data(base_data=True)

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data: dict = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            data: str = text_data
        if isinstance(data, dict):
            if data['func'] == 'step':
                card = await get_card_data_for_card_id(data['cardID'])
                if "flamethrower" in card.function:
                    await self.send_data(base_data=True)
                else:
                    await self.send_data(base_data=False)

    async def send_data(
            self,
            data: dict = None,
            base_data: bool = False
    ):
        if base_data:
            cards = await get_cards(self.username)
            players = await get_players(self.game_id)
            data = {
                'func': 'data',
                'cards': cards,
                'players': players
            }
        self.channel_layer.group_send(
            self.game_id,
            data
        )
        await self.send(text_data=json.dumps(data))

    async def chat_message(self, event):
        await self.send(
            text_data=json.dumps(
                event['message']
            )
        )
