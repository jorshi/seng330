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


@login_required
def get_current_room(request):
    """
    Get the current room that the player is in

    Returns:
        HttpResponse with JSON serialized room object
    """

    player = Player.objects.get(user=request.user)

    # Get the room state for the players current room
    room_state = RoomState.objects.filter(
        game_state=player.gamestate
    ).filter(
        room=player.gamestate.current_room
    )[0]


    jsonResponse = serializers.serialize('json', [room_state.get_room(),])
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
