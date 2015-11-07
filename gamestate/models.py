from django.db import models
from player.models import Player
from gameworld.models import Room, Door, FixedItem, Item

class GameState(models.Model):
    """ Saves the state of player's current game """
    player = models.OneToOneField('player.Player', primary_key=True)
    current_room = models.ForeignKey('gameworld.Room')
    items = models.ManyToManyField('gameworld.Item')
    
    def __unicode__(self):
        return self.player

class UnlockedDoors(models.Model):
    """ Saves all the doors currently unlocked """
    game_state = models.ForeignKey('GameState')
    door = models.ForeignKey('gameworld.Door')
    room_a = models.ForeignKey('gameworld.Room', related_name='unlocked_a')
    room_b = models.ForeignKey('gameworld.Room', related_name='unlocked_b')
    
    def __unicode__(self):
        return '%s.%s' % (self.game_state, self.door)
        
class RoomState(models.Model):
    """ Saves all the rooms the player has entered """
    game_state = models.ForeignKey('GameState')
    room = models.ForeignKey('gameworld.Room')
    illuminated = models.BooleanField()
    
    def __unicode__(self):
        return '%s.%s' % (self.game_state, self.room)

class ItemState(models.Model):
    """ Saves all the items present in each saved room """
    room_state = models.ForeignKey('RoomState')
    item = models.ForeignKey('gameworld.FixedItem')
    hidden = models.BooleanField()
    
    def __unicode__(self):
        return '%s.%s' % (self.room_state, self.item)
        