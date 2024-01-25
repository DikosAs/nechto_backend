from channels.generic.websocket import AsyncJsonWebsocketConsumer
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
class GameWSClient(AsyncJsonWebsocketConsumer):
    async def connect(self):
        try:
            self.game_id = self.scope['url_route']['kwargs']['game_id']
            self.username = str(self.scope['url_route']['kwargs']['username'])
            self.room_group_id = f'game_{self.game_id}'

            await self.channel_layer.group_add(
                self.room_group_id,
                self.channel_name
            )

            await self.accept()
            await self.send_data()
        except Exception as e:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_id,
            self.channel_name
        )
        await self.send_data()

    async def receive_json(self, content, **kwargs):
        print(content)
        await self.send_data()

    async def send_data(self, content: dict = None):
        if content is None:
            cards = await get_cards_of_players(self.game_id)
            players = await get_players(self.game_id)
            content = {
                'func': 'data',
                'cards': cards,
                'players': players
            }
        content = {
            'type': 'send',
            'data': content
        }
        print(content)
        await self.channel_layer.group_send(
            self.room_group_id,
            content
        )
