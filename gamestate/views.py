"""
View Class for gamestate. Handles interactions with gamestate models
related to game play
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from player.models import Player
from gamestate.models import GameState, RoomState, ItemState


@login_required
def get_current_room(request):
    """
    Get the current room that the player is in

    Returns:
        HttpResponse with JSON serialized room object

    """

    player = Player.objects.get(user=request.user)
    game = player.gamestate

    # Get the room state for the players current room
    room_state = game.roomstate_set.get(room=game.current_room)
    
    return JsonResponse(room_state.json())

@login_required
def post_player_action(request):

    player = Player.objects.get(user=request.user)
    game = player.gamestate
    if request.method == 'POST':
        print(request.POST)
        # TODO lookup the action performed & update the gamestate db
    return JsonResponse({})
