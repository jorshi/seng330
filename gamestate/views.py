"""
View Class for gamestate. Handles interactions with gamestate models
related to game play
"""

from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from player.models import Player
from gamestate.models import ItemState
from gameworld.models import AbstractUseItem, ItemUseState
#from gameworld.models import Room, ItemUseState, UseDecoration, AbstractUseItem, UseKey

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
        item_name = request.POST['name']
        try:
            other_name = request.POST['name2']
            #print(other_name)
        except:
            other_name = ""
        
        # TODO: changed API call
        # name: item name ***
        # (optional) name2 (door or item)
        
        if other_name:
            door_match = other_name.split()
            if door_match[0] in ['east', 'west', 'north', 'south']:
                if door_match[1] == 'door':
                    print("looking for door in room")
                    try:
                        door = game.current_room.room.get_door(
                            door_match[0])
                    except:
                        print("Error: door not found")
                        return
                    else:
                        other_door = door
                        other_item = None
                else:
                    print("Error")
                    return
            else:
                try:
                    print("looking for other item in room")
                    other_item = game.current_room.itemstate_set.get(
                        item__item__name=other_name)
                except ItemState.DoesNotExist:
                    print("post_player_action Error: %s not found" % other_name)
                    return
                else:
                    other_item = other_item.item
        else:
            other_item = None
            
        # look in inventory and current room
        item = None
        try:
            print("looking for %s in inventory" % item_name)
            item = game.inventory.get(item__name=item_name)
        except ItemUseState.DoesNotExist:
            pass
        else:
            action = _lookup_action(item, other_item)
            if not action.execute(game):
                return
            return get_current_room(request)
        
        try:
            print("looking for %s in room" % item_name)
            item = game.current_room.itemstate_set.get(item__item__name=item_name)
        except ItemUseState.DoesNotExist:
            print("post_player_action Error: %s not found" % item_name)
            return
        else:
            item = item.item  # go from ItemState (gamestate) to ItemUseState (gameworld)
            action = _lookup_action(item, other_item)
            if not action.execute(game):
                return
            return get_current_room(request)
  
    return get_current_room(request)

def _lookup_action(item, other_item):
    # TODO look for other_item
    actions = AbstractUseItem.objects.select_subclasses()
    # ambiguity?
    try:
        print("looking for action")
        action = actions.get(item_use_state=item)
        
    except AbstractUseItem.DoesNotExist:
        print("post_player_action Error: item usecase not found")
        return False
    except AbstractUseItem.MultipleObjectsReturned:
        print("post_player_action Error: >1 item usecase found for item")
        return False
    else:
        return action

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
    
@login_required
def post_take_item(request):
    player = Player.objects.get(user=request.user)
    game = player.gamestate
    if request.method == 'POST':
        item_name = request.POST['name']
        try:
            theitem = game.current_room.itemstate_set.get(item__item__name=item_name)
        except ItemState.DoesNotExist:
            return get_current_room(request)  # add error response?
        # check if it can be picked up
        # FixedItem (wrapped in ItemUseState, wrapped in ItemState)
        if theitem.item.item.pickupable:  
            print("moving %s to inventory" % item_name)
            game.inventory.add(theitem.item)  # ItemUseState (wrapped in ItemState)
            # delete the wrapper ItemState
            theitem.delete()
            # add() and delete() autoupdate the database - no need to call save()
        
    return get_current_room(request)
