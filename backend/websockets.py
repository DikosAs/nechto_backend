import django.db.models
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from backend.models import CardOfPlayer, Player, Card
import json


@database_sync_to_async
def get_cards_of_players(game_id: int) -> dict[Player.username, list[Card.id]]:
    cards = {}
    for player in Player.objects.filter(game_id=game_id):
        cards_: list[Card.id] = []
        for cardOfPlayer in CardOfPlayer.objects.filter(player=player):
            cards_.append(cardOfPlayer.card.id)
        else:
            cards[player.username] = cards_
    return cards


@database_sync_to_async
def get_players(game_id: int) -> dict[int, str]:
    players: dict = {}
    for player in Player.objects.filter(game_id=game_id):
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
        self.room_group_id = f'game_{self.game_id}'

        self.channel_layer.group_add(
            self.room_group_id,
            self.channel_name
        )

        await self.send_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
        await self.send_data()

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data: dict = json.loads(text_data)
        except json.decoder.JSONDecodeError:
            data: str = text_data
        if isinstance(data, dict):
            if data['func'] == 'step':
                card = await get_card_data_for_card_id(data['cardID'])

    async def send_data(
            self,
            data: dict = None
    ):
        if data is None:
            cards = await get_cards_of_players(self.game_id)
            players = await get_players(self.game_id)
            data = {
                'func': 'data',
                'cards': cards,
                'players': players
            }

        await self.channel_layer.group_send(
            self.room_group_id,
            data
        )

    async def send_updates(self, event):
        await self.send(json.dumps(event))
