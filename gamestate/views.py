"""
View Class for gamestate. Handles interactions with gamestate models
related to game play
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
from player.models import Player
from gamestate.models import GameState, RoomState
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

    # Create a GameState object for this game
    gameState = GameState()
    gameState.player = player
    gameState.current_room = Room.objects.get(name=STARTING_ROOM)
    gameState.save()

    # Add room state for first room
    gameState.add_room(gameState.current_room)

    return HttpResponseRedirect('/play/', { 'user': request.user, 'gameState': gameState })


@login_required
def resume_game(request):
    """
    Resume an existing game for this player
    """
    player = Player.objects.get(user=request.user)
    gameState = player.gamestate
    return render(request, 'game_view.html', { 'user': request.user, 'gameState': gameState })


@login_required
def get_current_room(request):
    """
    Get the current room that the player is in

    Returns:
        HttpResponse with JSON serialized room object
    """

    player = Player.objects.get(user=request.user)
    gameState = player.gamestate
    room = RoomState.objects.all()
    print room
    
    jsonResponse = serializers.serialize('json', [gameState.current_room,])
    return HttpResponse(jsonResponse, content_type="application/json")


@login_required
def get_room_inventory(request):
    """
    Get the inventory of the requested room

    Args: room name

    Returns:
        JSON Response Object - list of items
    """

    return JsonResponse({'room_inventory': ['itemA', 'itemB']})
