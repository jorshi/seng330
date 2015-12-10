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
from gameworld.models import AbstractUseItem
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
        try:
            action_pk = int(request.POST['ref'])
            action = AbstractUseItem.objects.filter(
                        pk=action_pk).select_subclasses()[0]
            if not action.execute(game):
                return
                
        except ValueError:
            print("POST data was not an int")
            return
        except IndexError:
            print("%s not found" % action_pk)
            return  # TODO error response
        
    return get_current_room(request)

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
