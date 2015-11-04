from django.contrib import admin
from player.models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """ Admin view for Player """

    list_display = ('user',)
