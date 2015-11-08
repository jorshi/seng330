"""
View Class for gamestate. Handles interactions with gamestate models
related to game play
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from player.models import Player
from gamestate.models import GameState
from gameworld.models import Room

# Hardcode the starting room for now
# TODO - Maybe have a map object that references the starting room for a map?
STARTING_ROOM = "Entrance Hall"

@login_required
def new_game(request):
    """
    Start a new game for this player
    """

    player = Player.objects.get(user=request.user)

    # Erase users current game state if they are starting a new game
    try:
        gameState = player.gamestate
        gameState.delete()
    except GameState.DoesNotExist:
        pass

    gameState = GameState()
    gameState.player = player
    gameState.current_room = Room.objects.get(name=STARTING_ROOM)
    gameState.save()

    return HttpResponseRedirect('/play/', { 'user': request.user, 'gameState': gameState })


@login_required
def resume_game(request):
    """
    Resume an existing game for this player
    """
    player = Player.objects.get(user=request.user)
    gameState = player.gamestate
    return render(request, 'game_view.html', { 'user': request.user, 'gameState': gameState })
