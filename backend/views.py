import django.db.models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from backend.models import Player, Card, Deck, Game, CardForPlayer
from random import shuffle
from time import sleep


def str_to_list(string: str) -> list[int]:
    out: list[int] = []

    for char in string:
        try:
            out.append(int(char))
        except:
            pass

    return out


def generate_deck(game_id: int) -> list[int]:
    if not Deck.objects.filter(gameID_id=game_id).exists():
        all_card: list[int] = []
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
        all_card: list[int] = str_to_list(Deck.objects.get(gameID_id=game_id).cards)

    return all_card


# Create your views here.
def update_data_on_client(request: WSGIRequest) -> JsonResponse:
    if request.method == 'GET':
        try:
            cards: dict[int, dict] = {}
            for card in Card.objects.all():
                try:
                    image: str = str(card.image.url)
                except ValueError:
                    image: str = str(card.image)
                cards[card.id]: dict = {
                    'name': card.name,
                    'description': card.description,
                    'function': card.function,
                    'image': image,
                    'minPlayerInGame': card.minPlayerInGame,
                    'maxCardInColoda': card.maxCardInColoda
                }
            data: dict = {'cards': cards}
            status: int = 200
        except:
            data: dict = {}
            status: int = 500

        return JsonResponse(data, safe=False, status=status)


def games_list(request: WSGIRequest) -> JsonResponse:
    if request.method == 'GET':
        return_data: dict[
            int, dict[
                str, int
            ]
        ] = {}

        for game in Game.objects.all():
            return_data[game.id]: dict[str, int] = {
                'maxPlayers': game.maxPlayers,
                'playerInGame': Player.objects.filter(gameID=game).count()
            }

        return JsonResponse(return_data, safe=False)


def add_player(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        players_in_game = Player.objects.filter(gameID_id=game_id)
        players_in_game_count: int = players_in_game.count()

        try:
            if Player.objects.filter(username=username).exists():
                status: int = 501
            else:
                empty_place: list[int] = [pos for pos in range(1, players_in_game_count+1)]
                for player in players_in_game:
                    try:
                        empty_place.remove(player.position)
                    except ValueError:
                        pass
                else:
                    if empty_place:
                        Player.objects.create(
                            gameID_id=game_id,
                            username=username,
                            position=empty_place[0]
                        )
                    else:
                        Player.objects.create(
                            gameID_id=game_id,
                            username=username,
                            position=players_in_game_count + 1
                        )
                    status: int = 200

                try:
                    sleep(2)
                    players_in_game: django.db.models.QuerySet[Player] = Player.objects.filter(gameID_id=game_id)
                    players_in_game_count: int = players_in_game.count()
                    if players_in_game_count >= Game.objects.get(id=game_id).maxPlayers:
                        all_card: list[int] = generate_deck(game_id)

                        settings_data: dict[str, int or django.db.models.QuerySet[Player]] = {
                            'cardsPerPlayer': 4,
                            'playerCount': players_in_game_count,
                            'players': players_in_game
                        }
                        cards_for_player: dict[int, list[int]] = {}

                        cardsIDs: list[int] = [i for i in range(len(all_card))]
                        card_pont: list[int] = cardsIDs[::settings_data['playerCount']]
                        for playerID in range(settings_data['playerCount']):
                            try:
                                cards_for_player[settings_data['players'][playerID].id]: list[int] = [
                                    all_card[card_pont[0]+playerID-1],
                                    all_card[card_pont[1]+playerID-1],
                                    all_card[card_pont[2]+playerID-1],
                                    all_card[card_pont[3]+playerID-1]
                                ]
                            except IndexError:
                                pass
                        else:
                            for player_cards in cards_for_player:
                                if not CardForPlayer.objects.filter(playerID_id=player_cards).exists():
                                    CardForPlayer.objects.create(
                                        playerID_id=player_cards,
                                        cards=cards_for_player[player_cards]
                                    )
                except IndexError:
                    pass
        except:
            status: int = 500

        return JsonResponse({}, safe=False, status=status)


def del_player(request: WSGIRequest, game_id: int = 0, username: str = '') -> JsonResponse:
    if request.method == 'GET':
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

        cardsForPlayer = CardForPlayer.objects.filter(playerID__username=username)
        if cardsForPlayer.exists():
            cardsForPlayer.delete()

        return JsonResponse({}, safe=False, status=status)
