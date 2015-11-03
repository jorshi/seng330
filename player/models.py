from django.db import models
from django.contrib.auth.models import User
from gameworld.models import Room, Door
from django.contrib import admin

class Player(models.Model):
    """ Player Object """

    user = models.OneToOneField(User, primary_key=True)

class GameState(models.Model):

    player = models.OneToOneField('Player', primary_key=True)
    current_room = models.OneToOneField(Room)

class UnlockedDoors(models.Model):

    game_state = models.ForeignKey('GameState')
    door = models.OneToOneField(Door)
