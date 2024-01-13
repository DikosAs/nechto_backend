import django.db.models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.handlers.wsgi import WSGIRequest
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from backend.models import Player, Card, Deck, Game, CardOfPlayer, CardOfDeck
from random import shuffle
from time import sleep


def generate_deck(game_id: int) -> list[Card]:
    if not Deck.objects.filter(game_id=game_id).exists():
        all_card: list[Card] = []
        card_from_db = Card.objects.filter(minPlayerInGame__lte=Game.objects.get(id=game_id).maxPlayers)

        for card in card_from_db:
            if card.minPlayerInGame <= Game.objects.get(id=game_id).maxPlayers:
                for i in range(card.maxCardInColoda):
                    all_card.append(card)
        else:
            shuffle(all_card)

            # добавляю колоду в базу данных
            Deck.objects.create(
                game_id=game_id
            )

            deck = Deck.objects.get(game_id=game_id)
            for cardID in all_card:
                CardOfDeck.objects.create(
                    deck=deck,
                    card=cardID
                )
            else:
                print('Колода сгенерирована и записана в базу данных')

    else:
        all_card = list(CardOfDeck.objects.filter(deck__game_id=game_id))

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
                'playerInGame': Player.objects.filter(game=game).count()
            }

        return JsonResponse(return_data, safe=False)


def add_player(request: WSGIRequest, game_id: int = 0, username: str = ''):
    if request.method == 'GET':
        players_in_game = Player.objects.filter(game_id=game_id)
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
                            game_id=game_id,
                            username=username,
                            position=empty_place[0]
                        )
                    else:
                        Player.objects.create(
                            game_id=game_id,
                            username=username,
                            position=players_in_game_count + 1
                        )
                    status: int = 200

                try:
                    # sleep(2)
                    players_in_game: django.db.models.QuerySet[Player] = Player.objects.filter(game_id=game_id)
                    players_in_game_count: int = players_in_game.count()
                    if players_in_game_count >= Game.objects.get(id=game_id).maxPlayers:
                        all_card: list[Card] = generate_deck(game_id)

                        cards_per_player = 4

                        for player in players_in_game:
                            for i in range(cards_per_player):
                                CardOfPlayer.objects.create(
                                    player=player,
                                    card=all_card.pop()
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
                game_id=game_id,
                username=username
            ).delete()
            status = 200
        except:
            status = 501

        players = Player.objects.filter(game_id=game_id)
        if not players.exists():
            Deck.objects.filter(game_id=game_id).delete()

            for player in players:
                CardFromPlayer.objects.filter(
                    player=player
                )


        return JsonResponse({}, safe=False, status=status)
