from django.contrib import admin
from backend.models import Game, Player, Card


# Register your models here.
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'password', 'maxPlayers')


class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'function', 'show_image', 'minPlayerInGame', 'maxCardInColoda')


admin.site.register(Game, GameAdmin)
admin.site.register(Card, CardAdmin)
