from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from player.models import Player
from gameworld.models import Room, Door, FixedItem
import json


class GameState(models.Model):
    """ Saves the state of player's current game """

    player = models.OneToOneField('player.Player', primary_key=True)
    current_room = models.ForeignKey('gameworld.Room')

    # list of items the player has taken from rooms
    inventory = models.ManyToManyField('gameworld.FixedItem')

    def add_room(self, room):
        """
        Add a room state if this is the
        first time the player has entered this room.
        """

        roomState = RoomState.objects.filter(game_state=self)
        if not room in [rm.room for rm in roomState]:
            roomState = RoomState()
            roomState.game_state = self
            roomState.room = room
            roomState.illuminated = room.illuminated
            roomState.save()

            # Add all default room items as ItemStates for this room
            for item in room.default_items.all():
                itemState = ItemState()
                itemState.room_state = roomState
                itemState.item = item
                itemState.state = item.default_state
                itemState.save()

            # Add all doors as DoorStates for this room - unless they have already been added
            # by another room that has been visited
            for door in Door.objects.filter(models.Q(room_a=room) | models.Q(room_b=room)):
                if not DoorState.objects.filter(door=door).count():
                    doorState = DoorState()
                    doorState.game_state = self
                    doorState.door = door
                    doorState.locked = door.locked
                    doorState.room_a = door.room_a
                    doorState.room_b = door.room_b
                    doorState.save()

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
            'next_room': self.door.other_room(room),
            'shortdesc': None, # todo 'a door to the [dir]'
            'examine': self.door.desc(room)
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
        # TODO add items, doors to obj
        obj['items'] = []
        # this is awful please fix it
        obj['doors'] = { 
            'north': DoorState.objects.filter(
                game_state = self.game_state
                ).get(
                door = self.room.door_north
                ).json(self.room),
            # etc.
        }
        return json.dumps(obj)

    def __unicode__(self):
        return u'%s.%s' % (self.game_state, self.room)


class ItemState(models.Model):
    """ Saves all the items present in each saved room """

    room_state = models.ForeignKey('RoomState')         # RoomState reference
    item = models.ForeignKey('gameworld.FixedItem')     # Item reference
    state = models.IntegerField()                       # current state of item

    def __unicode__(self):
        return u'%s.%s' % (self.room_state, self.item)


class Statistics(models.Model):
    """ Tracks statistics for the player's current game """

    game_state = models.OneToOneField('GameState', primary_key=True)
    rooms_unlocked = models.PositiveSmallIntegerField(default=0)
    items_taken = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return '%s.%s' % (self.room_state, self.item)
