"""
View Class for gamestate. Handles interactions with gamestate models
related to game play
"""

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from player.models import Player
from gamestate.models import GameState, RoomState, ItemState, DoorState
from gameworld.models import Room, ItemUseState, UseDecoration, AbstractUseItem, UseKey

@login_required
def get_current_room(request):
    """
    Get the current room that the player is in

    Returns:
        HttpResponse with JSON serialized room object

    """

    player = Player.objects.get(user=request.user)
    game = player.gamestate

    response = game.json()
    
    return JsonResponse(response)

@login_required
def post_player_action(request):

    player = Player.objects.get(user=request.user)
    game = player.gamestate
    if request.method == 'POST':
        print(request.POST)
        # TODO lookup the action performed & update the gamestate db

    return JsonResponse({})

@login_required
def post_change_room(request):

    player = Player.objects.get(user=request.user)
    game = player.gamestate
    if request.method == 'POST':
        room_name = request.POST['room']
        room_state = game.add_room(room_name)
        game.current_room = room_state
        game.save()
        
    return get_current_room(request)
