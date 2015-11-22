from django.db import models
from player.models import Player
from gameworld.models import Room, Door, FixedItem, Item


class GameState(models.Model):
    """ Saves the state of player's current game """

    player = models.OneToOneField('player.Player', primary_key=True)
    current_room = models.ForeignKey('gameworld.Room')

    # list of items the player has taken from rooms
    inventory = models.ManyToManyField('gameworld.Item')

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

    def __unicode__(self):
        return "%s.GameState" % self.player


class DoorState(models.Model):
    """ Saves all the doors the player has seen """

    game_state = models.ForeignKey('GameState')

    # a door in a room the player has entered, whether unlocked or not
    door = models.ForeignKey('gameworld.Door')

    # whether the door is currently locked
    locked = models.BooleanField()

    # room_a of the door
    room_a = models.ForeignKey('gameworld.Room', related_name='unlocked_a')

    # room_b of the door
    room_b = models.ForeignKey('gameworld.Room', related_name='unlocked_b')

    def __unicode__(self):
        return '%s.%s' % (self.game_state, self.door)

class RoomState(models.Model):
    """ Saves all the rooms the player has entered """

    game_state = models.ForeignKey('GameState')
    room = models.ForeignKey('gameworld.Room')
    # whether the room is currently lit
    illuminated = models.BooleanField()

    def get_room(self):
        self.room.update_state(self)
        return self.room

    def __unicode__(self):
        return u'%s.%s' % (self.game_state, self.room)

class ItemState(models.Model):
    """ Saves all the items present in each saved room """

    room_state = models.ForeignKey('RoomState')
    # the item
    item = models.ForeignKey('gameworld.FixedItem')
    # whether the item is currently hidden
    hidden = models.BooleanField()

    def __unicode__(self):
        return u'%s.%s' % (self.room_state, self.item)

class Statistics(models.Model):
    """ Tracks statistics for the player's current game """

    game_state = models.OneToOneField('GameState', primary_key=True)
    rooms_unlocked = models.PositiveSmallIntegerField(default=0)
    items_taken = models.PositiveSmallIntegerField(default=0)

    def __unicode__(self):
        return '%s.%s' % (self.room_state, self.item)
