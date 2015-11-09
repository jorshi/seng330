from django.contrib import admin
import gamestate.models

@admin.register(gamestate.models.GameState)
class GameStateAdmin(admin.ModelAdmin):
    pass

@admin.register(gamestate.models.RoomState)
class RoomStateAdmin(admin.ModelAdmin):
    pass
