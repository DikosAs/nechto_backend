from django.contrib import admin
from backend.models import *


# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'password', 'maxPlayers')


class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'gameID', 'username', 'position')


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'descriptin', 'function', 'image', 'minPlayerInGame', 'maxCardInColoda')


class CardFunctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'function')


admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CardFunction, CardFunctionAdmin)
