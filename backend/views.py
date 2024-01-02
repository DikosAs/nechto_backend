from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from backend.models import *
from random import shuffle, choice


def str_to_list_int(string: str) -> list:
    out = []
    for char in string:
        try: out.append(int(char))
        except: pass
    return out


def generate_deck(game_id: Game) -> list:
    all_card = []
    if len(Deck.objects.filter(gameID=game_id)) == 0:
        for card in Card.objects.all():
            if card.minPlayerInGame <= game_id.maxPlayers or card.minPlayerInGame == 0:
                for i in range(card.maxCardInColoda):
                    all_card.append(card.id)
        shuffle(all_card)
        Deck.objects.create(
            gameID=game_id,
            cards=all_card
        )
    else:
        all_card = str_to_list(Deck.objects.get(gameID=game_id).cards)

    return all_card


# Create your views here.
def games_list(request: WSGIRequest):
    if request.method == 'GET':
        return_data = {}
        for game in Game.objects.all():
            return_data[game.id] = {
                'maxPlayers': game.maxPlayers,
                'minPlayerInGame': len(Player.objects.filter(gameID=game.id))
            }
        return JsonResponse(return_data, safe=False)


def add_player(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        GAME_ID = Game.objects.get(id=game_id)
        PLAYERS_IN_GAME = Player.objects.filter(gameID=GAME_ID)
        PLAYERS_IN_GAME_COUNT = PLAYERS_IN_GAME.count()

        return_data = {}
        try:
            if len(Player.objects.filter(username=username)) != 0:
                return_data['status'] = 501
            else:
                Player.objects.create(
                    gameID=GAME_ID,
                    username=username,
                    position=PLAYERS_IN_GAME_COUNT + 1
                )
                return_data['status'] = 200
        except:
            return_data['status'] = 500

        # если игроков достаточно, то генерирую колоду
        if PLAYERS_IN_GAME_COUNT >= GAME_ID.maxPlayers:
            all_card = generate_deck(GAME_ID)

            # после генерации колоды раздаю карты (4 штуки)
            settings_data = {
                'cardsPerPlayer': 4,
                'playerCount': PLAYERS_IN_GAME_COUNT,
                'players': PLAYERS_IN_GAME
            }
            cards_for_player = {}

            cardsIDs = [i for i in range(len(all_card))]
            card_pont = cardsIDs[::settings_data['playerCount']]
            for playerID in range(settings_data['playerCount']):
                try:
                    cards_for_player[settings_data['players'][playerID].id] = [
                        all_card[card_pont[0]+playerID-1],
                        all_card[card_pont[1]+playerID-1],
                        all_card[card_pont[2]+playerID-1],
                        all_card[card_pont[3]+playerID-1]
                    ]
                except IndexError:
                    pass
            else:
                for player_cards in cards_for_player:
                    CardForPlayer.objects.create(
                        playerID=Player.objects.get(id=player_cards),
                        cards=cards_for_player[player_cards]
                    )

        return JsonResponse(return_data, safe=False)


def del_player(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        return_data = {}
        try:
            Player.objects.filter(
                gameID=Game.objects.get(id=game_id),
                username=username
            ).delete()
            return_data['status'] = 200
        except:
            return_data['status'] = 501

        return JsonResponse(return_data, safe=False)


def load_data(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        PLAYERS_IN_GAME = Player.objects.filter(gameID=Game.objects.get(id=game_id))

        return_data = {}
        players = {}
        try:
            return_data['cards'] = CardForPlayer.objects.get(player_id=Player.objects.get(username=username).id)
            for player in PLAYERS_IN_GAME:
                players[player.position] = {
                    'id': player.id,
                    'gameID': player.gameID.id,
                    'username': player.username,
                }
            else:
                return_data['players'] = players
            return_data['status'] = 200
        except:
            for player in PLAYERS_IN_GAME:
                players[player.position] = {
                    'id': player.id,
                    'gameID': player.gameID.id,
                    'username': player.username,
                }
            else:
                return_data['players'] = players
            return_data['status'] = 503

        return JsonResponse(return_data, safe=False)
