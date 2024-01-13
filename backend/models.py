from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Game(models.Model):
    id = models.SmallIntegerField('Номер комнаты', primary_key=True)
    password = models.CharField('Пароль', max_length=1024, null=True, blank=True)
    maxPlayers = models.SmallIntegerField('Максимум игроков')

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = "игру"
        verbose_name_plural = "Игры"


class Player(models.Model):
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey(Game, models.CASCADE)
    username = models.CharField(max_length=50)
    position = models.SmallIntegerField()

    def __str__(self) -> str:
        return str(self.username)


class Card(models.Model):
    CARD_TYPES = [
        ("ACT", "Активная"),
        ("DEF", "Защитная"),
        ("PAN", "Паника"),
    ]
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('Название', max_length=32)
    type = models.CharField('Тип', max_length=3, choices=CARD_TYPES, default="ACT")
    description = models.TextField('Описание', null=True, blank=True)
    function = models.CharField('Функция', max_length=100)
    image = models.ImageField('Изображение', null=True, blank=True)
    minPlayerInGame = models.IntegerField('Минимальное число игроков', default=0, null=True, blank=True)
    maxCardInColoda = models.IntegerField('Максимальное число карт в колоде', default=0, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = "карту"
        verbose_name_plural = "Карты"

    @admin.display(description="Картинка")
    def show_image(self):
        from django.utils import html
        if self.image:
            return html.format_html("<img src='{}' style ='width:100px;'>", self.image.url)


class Deck(models.Model):
    id = models.BigAutoField(primary_key=True)
    game = models.ForeignKey(Game, models.CASCADE, to_field='id')


class CardOfDeck(models.Model):
    deck = models.ForeignKey(Deck, models.CASCADE, to_field='id')
    card = models.ForeignKey(Card, models.CASCADE, to_field='id')


class CardOfPlayer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, to_field='id')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, to_field='id')
