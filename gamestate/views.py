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
from gameworld.models import Room, ItemUseState, UseDecoration, AbstractUseItem


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


def get_room_doors(room):
    """
    Returns the door state objects for a room
    """
    pass


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

    # Map the type name based on whether the item is pickupable or not,
    # and usable or not
    type_map = {
        (True, True): "pickupableAndUsable",
        (True, False): "pickupableAndNonUsable",
        (False, True): "fixedAndUsable",
        (False, False): "fixedAndNonUsable",
    }

    if room:
        roomState = RoomState.objects.get(room=room, game_state=player.gamestate)
        itemStates = ItemState.objects.filter(room_state=roomState)

        # Update the item object and add it to a list of room items
        for itemState in itemStates:
            thisItem = itemState.item
            useStates = ItemUseState.objects.filter(item=thisItem)
            itemUses = []

            # Get item uses for the use states -- doing it in a loop because I want to make sure
            # the order matches the use states.
            for useState in useStates:
                itemUse = AbstractUseItem.objects.filter(item_use_state=useState).select_subclasses()
                itemUses.append(itemUse[0] if itemUse else None)

            # Put it all into a dictionary based on front end requirements
            items.append({
                'type': type_map.get((thisItem.pickupable, not all(i == None for i in itemUses))),
                'name': thisItem.name,
                'hidden': useStates[itemState.state].hidden,
                'examineDescription': [useState.examine for useState in useStates],
                'enterRoomDescription': [useState.short_desc for useState in useStates],
                'state': itemState.state,
                'usePattern': [use.use_pattern if use else None for use in itemUses],
                'useMessage': [use.use_message if use else None for use in itemUses],
            })

    return JsonResponse(items, safe=False)
