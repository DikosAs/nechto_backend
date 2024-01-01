from django.db import models
from django.contrib.auth.models import User
from django.db.models import BigAutoField


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
    gameID = models.ForeignKey(Game, models.CASCADE)
    username = models.CharField(max_length=50)
    position = models.SmallIntegerField()

    def __str__(self) -> str:
        return str(self.username)

    class Meta:
        verbose_name = "игрока"
        verbose_name_plural = "Игроки"


class Card(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField('Название', max_length=10)
    descriptin = models.TextField('Описание', null=True, blank=True)
    function = models.ForeignKey('CardFunction', models.CASCADE, verbose_name='Функция')
    image = models.ImageField('Изображение', null=True, blank=True)
    minPlayerInGame = models.IntegerField('Минимальное число игроков', default=0, null=True, blank=True)
    maxCardInColoda = models.IntegerField('Максимальное число карт в колоде', default=0, null=True, blank=True)

    def __str__(self) -> str:
        return str(self.id)

    class Meta:
        verbose_name = "карту"
        verbose_name_plural = "Карты"


class CardFunction(models.Model):
    id = models.BigAutoField(primary_key=True)
    function = models.CharField('Функция', max_length=100)

    def __str__(self) -> str:
        return self.function

    class Meta:
        verbose_name = "функцию карты"
        verbose_name_plural = "Функции карт"


class Deck(models.Model):
    id = models.BigAutoField(primary_key=True)
    gameID = models.ForeignKey(Game, models.CASCADE, to_field='id')
    cards = models.TextField(default=None, null=True, blank=True)


class CardForPlayer(models.Model):
    player_id = models.ForeignKey(Player, on_delete=models.CASCADE, to_field='id')
    cards = models.TextField(default=None, null=True, blank=True)
