"""
View Class for gamestate. Handles interactions with gamestate models
related to game play
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
from player.models import Player
from gamestate.models import GameState, RoomState, ItemState
from gameworld.models import Room, ItemUseState, UseDecoration


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
    ).get(
        room=player.gamestate.current_room
    )
    


    jsonResponse = room_state.json # TODO implement JSON in each gamestate.model
    return HttpResponse(jsonResponse, content_type="application/json")



@login_required
def get_room_inventory(request):
    """
    Get the inventory of the requested room

    Args: room name

    Returns:
        JSON Response Object - list of items
    """

    player = Player.objects.get(user=request.user)
    room = request.GET.get('room', None)
    items = []

    if room:
        roomState = RoomState.objects.get(room=room, game_state=player.gamestate)
        itemStates = ItemState.objects.filter(room_state=roomState)

        # Update the item object and add it to a list of room items
        for itemState in itemStates:
            thisItem = itemState.item
            useState = ItemUseState.objects.get(item=thisItem, state=itemState.state)
            itemUse = UseDecoration.objects.filter(item_use_state=useState)
            items.append({
                'name': thisItem.name,
                'hidden': itemState.hidden,
                'examine': useState.examine,
                'short_dec': useState.short_desc,
                'state': itemState.state,
                'usage': [use.use_pattern for use in itemUse],
            })
            
    return JsonResponse(items, safe=False)

