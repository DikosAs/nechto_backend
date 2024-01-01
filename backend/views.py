from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from backend.models import *
from random import shuffle, choice


def generate_deck(game_id: int) -> list[int]:
    all_card = []
    for card in Card.objects.all():
        if card.minPlayerInGame <= Game.objects.get(id=game_id).maxPlayers or card.minPlayerInGame == 0:
            for i in range(card.maxCardInColoda):
                all_card.append(card.id)
    shuffle(all_card)
    Deck.objects.create(
        gameID=Game.objects.get(id=game_id),
        cards=all_card
    )

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
        return_data = {}
        try:
            if len(Player.objects.filter(username=username)) != 0:
                return_data['status'] = 501
            else:
                Player.objects.create(
                    gameID=Game.objects.get(id=game_id),
                    username=username,
                    position=len(Player.objects.filter(gameID=game_id))+1
                )
                return_data['status'] = 200
        except:
            return_data['status'] = 500

        # если игроков достаточно, то генерирую колоду
        if len(Player.objects.filter(gameID=Game.objects.get(id=game_id))) == Game.objects.get(id=game_id).maxPlayers:
            all_card = []
            for card in Card.objects.all():
                if card.minPlayerInGame <= Game.objects.get(id=game_id).maxPlayers or card.minPlayerInGame == 0:
                    for i in range(card.maxCardInColoda):
                        all_card.append(card.id)
            shuffle(all_card)
            Deck.objects.create(
                gameID=Game.objects.get(id=game_id),
                cards=all_card
            )
            # после генерации колоды раздаю карты (4 штуки)
            cards_for_player = {}
            cards_col = 4
            for i in all_card:
                card = all_card[0]
                if cards_col > 0:
                    for player in Player.objects.filter(gameID=Game.objects.get(id=game_id)):
                        cards_for_player[player.position] = card
                        all_card.remove(card)
                        all_card.append(card)
            else:
                print(cards_for_player)

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
        return_data = {}
        players = {}
        try:
            return_data['cards'] = CardForPlayer.objects.get(player_id=Player.objects.get(username=username).id)
            for player in list(Player.objects.filter(gameID=Game.objects.get(id=game_id))):
                players[player.position] = {
                    'id': player.id,
                    'gameID': player.gameID.id,
                    'username': player.username,
                }
            else: return_data['players'] = players
            return_data['status'] = 200
        except:
            for player in list(Player.objects.filter(gameID=Game.objects.get(id=game_id))):
                players[player.position] = {
                    'id': player.id,
                    'gameID': player.gameID.id,
                    'username': player.username,
                }
            else: return_data['players'] = players
            return_data['status'] = 503

        return JsonResponse(return_data, safe=False)


# all_cards = range(1, 20)
# users = [1, 2]
# c = 4
#
# out = {}
#
# cards_per_user = 4  # количество карт для каждого пользователя
# remaining_cards = len(all_cards) - len(users)*4  # количество оставшихся карт
#
# for cardNUM in cards_per_user:
#     out[users] = [
#         all_cards[],
#         all_cards[],
#         all_cards[],
#         all_cards[]
#     ]

