from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from player.models import Player
from gameworld.models import Room, Door, FixedItem


class GameState(models.Model):
    """ Saves the state of player's current game """

    player = models.OneToOneField('player.Player', primary_key=True)

    current_room = models.ForeignKey('gamestate.RoomState', null=True)

    # list of items the player has taken from rooms
    inventory = models.ManyToManyField('gameworld.ItemUseState')

    def add_room(self, room_name):
        """
        Add a room state if this is the
        first time the player has entered this room.
        
        Returns the RoomState.
        """
        
        # TODO: error handling
        room = Room.objects.get(name=room_name)
        #print("adding %s for %s" % (room_name, self.player))
        
        try:
            roomState = self.roomstate_set.get(room=room)
            #print("%s already visited" % room_name)
        except RoomState.DoesNotExist:
            #print("%s not visited yet" % room_name)
            roomState = RoomState()
            roomState.game_state = self
            roomState.room = room
            roomState.illuminated = room.illuminated
            roomState.save()

            # Add all default room items as ItemStates for this room
            for item in room.default_items.all():
                itemState = ItemState()
                itemState.room_state = roomState
                itemState.item = item.states.get(state=item.default_state)
                itemState.save()

            # Add all doors as DoorStates for this room - unless they have already been added
            # by another room that has been visited
            for door in Door.objects.filter(models.Q(room_a=room) | models.Q(room_b=room)):
                if not self.doorstate_set.filter(door=door).exists():
                    doorState = DoorState()
                    doorState.game_state = self
                    doorState.door = door
                    doorState.locked = door.locked
                    doorState.room_a = door.room_a
                    doorState.room_b = door.room_b
                    doorState.save()
        return roomState

    def json(self):
        """
        Returns a serializable dictionary. 
        room - the current room state
        inventory - a list of the items in player's inventory
        """
        obj = {}
        obj["room"] = self.current_room.json()
        obj["inventory"] = [item.json() for item in self.inventory.all()]
        return obj
        
    
    def __unicode__(self):
        return "%s.GameState" % self.player



class DoorState(models.Model):
    """ Saves all the doors the player has seen """

    game_state = models.ForeignKey('GameState')

    # a door in a room the player has entered, whether unlocked or not
    door = models.ForeignKey('gameworld.Door')
    locked = models.BooleanField()
    room_a = models.ForeignKey('gameworld.Room', related_name='unlocked_a')
    room_b = models.ForeignKey('gameworld.Room', related_name='unlocked_b')

    def json(self, room):
        obj = { 
            'locked': self.locked,
            'next_room': self.door.other_room(room).name
        }
        return obj
        
    def __unicode__(self):
        return '%s.%s' % (self.game_state, self.door)


class RoomState(models.Model):
    """ Saves all the rooms the player has entered and any changes to that room """

    game_state = models.ForeignKey('GameState') # GameState reference
    room = models.ForeignKey('gameworld.Room')  # Room reference
    illuminated = models.BooleanField()         # Currently illuminated?

    def json(self):
        obj = { 
            'title': self.room.title,
            'desc_header': self.room.desc_header,
            'desc_footer': self.room.desc_footer,
            'illuminated': self.illuminated,
            }
        items = self.itemstate_set.all()
        obj['items'] = [item.json() for item in items if not item.item.hidden]
        
        dirs = ['north', 'south', 'east', 'west']
        
        obj['doors'] = {}
        for dir in dirs:
            try:
                door = self.game_state.doorstate_set.get(door=self.room.get_door(dir))
                obj['doors'][dir] = door.json(self.room)
            except DoorState.DoesNotExist:
                obj['doors'][dir] = None
            
        
        return obj

    def __unicode__(self):
        return u'%s.%s' % (self.game_state, self.room)


class ItemState(models.Model):
    """ Saves all the items present in each saved room """

    room_state = models.ForeignKey('RoomState')         # RoomState reference
    item = models.ForeignKey('gameworld.ItemUseState')     # Item reference
    
    def json(self):
        return self.item.json()

    def __unicode__(self):
        return u'%s.%s' % (self.room_state, self.item)


class Statistics(models.Model):
    """ Tracks statistics for the player's current game """

    game_state = models.OneToOneField('GameState', primary_key=True)
    rooms_unlocked = models.PositiveSmallIntegerField(default=0)
    items_taken = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return '%s.%s' % (self.room_state, self.item)
