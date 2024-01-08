from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from backend.models import Player, Card, Deck, Game, CardForPlayer
from random import shuffle


def str_to_list(string: str) -> list[int]:
    out = []

    for char in string:
        try:
            out.append(int(char))
        except:
            pass

    return out


def generate_deck(game_id: int) -> list:
    if not Deck.objects.filter(gameID_id=game_id).exists():
        all_card = []
        for card in Card.objects.all():
            if (card.minPlayerInGame <= Game.objects.get(id=game_id).maxPlayers
                    or card.minPlayerInGame == 0):
                for i in range(card.maxCardInColoda):
                    all_card.append(card.id)
        shuffle(all_card)
        Deck.objects.create(
            gameID_id=game_id,
            cards=all_card
        )
    else:
        all_card = str_to_list(Deck.objects.get(gameID_id=game_id).cards)

    return all_card


# Create your views here.
def update_data_on_client(request: WSGIRequest):
    if request.method == 'GET':
        try:
            cards = {}
            for card in Card.objects.all():
                try:
                    image = str(card.image.url)
                except ValueError:
                    image = str(card.image)
                cards[card.id] = {
                    'name': card.name,
                    'description': card.description,
                    'function': card.function,
                    'image': image,
                    'minPlayerInGame': card.minPlayerInGame,
                    'maxCardInColoda': card.maxCardInColoda
                }
            data = {'cards': cards}
            status = 200
        except:
            data = {}
            status = 500

        return JsonResponse(data, safe=False, status=status)


def games_list(request: WSGIRequest):
    if request.method == 'GET':
        return_data = {}

        for game in Game.objects.all():
            return_data[game.id] = {
                'maxPlayers': game.maxPlayers,
                'playerInGame': Player.objects.filter(gameID=game).count()
            }

        return JsonResponse(return_data, safe=False)


def add_player(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        players_in_game = Player.objects.filter(gameID_id=game_id)
        players_in_game_count = players_in_game.count()

        return_data = {}
        # try:
        if Player.objects.filter(username=username).exists():
            status = 501
        else:
            Player.objects.create(
                gameID_id=game_id,
                username=username,
                position=players_in_game_count + 1
            )
            status = 200

            # try:
        if players_in_game_count >= Game.objects.get(id=game_id).maxPlayers:
            all_card = generate_deck(game_id)

            settings_data = {
                'cardsPerPlayer': 4,
                'playerCount': players_in_game_count,
                'players': players_in_game
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
                print(cards_for_player)
                for player_cards in cards_for_player:
                    CardForPlayer.objects.create(
                        playerID=Player.objects.get(username=username),
                        cards=cards_for_player[player_cards]
                    )
                # except:
                #     pass
        # except:
        #     status = 500

        return JsonResponse(return_data, safe=False, status=status)


def del_player(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        return_data = {}
        try:
            Player.objects.filter(
                gameID_id=game_id,
                username=username
            ).delete()
            status = 200
        except:
            status = 501

        if not Player.objects.filter(gameID_id=game_id).exists():
            Deck.objects.filter(gameID_id=game_id).delete()

        return JsonResponse(return_data, safe=False, status=status)


def load_data(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        players_in_game = Player.objects.filter(gameID_id=game_id)

        return_data = {}
        players = {}

        # return_data['cards'] = CardForPlayer.objects.get(
        #     playerID=Player.objects.get(username=username)
        # ).cards

        try:
            for player in players_in_game:
                players[player.position] = {
                    'id': player.id,
                    'gameID': player.gameID.id,
                    'username': player.username,
                }
            return_data['players'] = players
        except:
            pass

        try:
            return_data['cards'] = CardForPlayer.objects.get(
                playerID=Player.objects.get(username=username)
            ).cards
            status = 200
        except:
            status = 503

        return JsonResponse(return_data, safe=False, status=status)
