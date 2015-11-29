"""
View Class for gamestate. Handles interactions with gamestate models
related to game play
"""

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.core import serializers
from player.models import Player
from gamestate.models import GameState, RoomState, ItemState, DoorState
from gameworld.models import Room, ItemUseState, UseDecoration, AbstractUseItem, UseKey


def player_current_room(player):
    """
    Returns the current room object for a player
    """

    # Get the room state for the players current room
    room_state = RoomState.objects.filter(
        game_state=player.gamestate
    ).filter(
        room=player.gamestate.current_room
    )[0]

    return room_state.get_room()


@login_required
def get_current_room(request):
    """
    Get the current room that the player is in

    Returns:
        HttpResponse with JSON serialized room object
    """

    player = Player.objects.get(user=request.user)
    jsonResponse = serializers.serialize('json', [player_current_room(player),])
    return HttpResponse(jsonResponse, content_type="application/json")


@login_required
def get_doors(request):
    """
    Returns JSON list containing the doors for a particular room. The
    dictionary for each door contains the id of the door, the current
    locked status of the door, the room that door leads to, and the wall
    that door belongs to in the requested room
    """

    player = Player.objects.get(user=request.user)
    room = Room.objects.get(pk=request.GET.get('room'))
    doors = []

    for direction in ['north', 'south', 'east', 'west']:
        door = room.get_door(direction)
        if door:
            doorState = DoorState.objects.get(door=door)
            doors.append({
                'id': door.pk,
                'locked': doorState.locked,
                'roomLinkedTo': doorState.room_a.title if
                    doorState.room_b == room else doorState.room_b.title,
                'wall': direction,
            })

    return JsonResponse(doors, safe=False)


@login_required
def get_inventory(request):
    """
    Get the inventory of the requested room

    Args: room name

    Returns:
        JSON Response Object - list of items
    """

    player = Player.objects.get(user=request.user)
    room = request.GET.get('room')
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

            # Special Case for Keys
            itemType = "key" if all(type(use) == UseKey for use in itemUses) else None

            # Put it all into a dictionary based on front end requirements
            items.append({
                'type': itemType or type_map.get((thisItem.pickupable, not all(i == None for i in itemUses))),
                'name': thisItem.name,
                'hidden': useStates[itemState.state].hidden,
                'examineDescription': [useState.examine for useState in useStates],
                'enterRoomDescription': [useState.short_desc for useState in useStates],
                'state': itemState.state,
                'usePattern': [use.use_pattern if use else None for use in itemUses],
                'useMessage': [use.use_message if use else None for use in itemUses],
                'doorToUnlock': itemUses[itemState.state].on_door.pk if itemType == "key" else None,
            })

    return JsonResponse(items, safe=False)


@login_required
def use_door(request):

    player = Player.objects.get(user=request.user)
    gameState = player.gamestate
    currentRoom = player_current_room(player)
    door = DoorState.objects.get(door=request.GET.get('id'))

    # Check for a couple error cases
    if door.locked:
        raise Exception("Door is locked!")

    if currentRoom not in [door.room_a, door.room_b]:
        raise Exception("This is not is this room!")

    # Get next room, add to game state and set as player's current room
    nextRoom = door.room_a if currentRoom == door.room_b else door.room_b
    gameState.add_room(nextRoom)
    gameState.current_room = nextRoom
    gameState.save()

    print gameState
    # Return this room to the front end
    jsonResponse = serializers.serialize('json', [player_current_room(player),])
    return HttpResponse(jsonResponse, content_type="application/json")
