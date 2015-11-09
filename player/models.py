from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

class Player(models.Model):
    """ Player Object """
    user = models.OneToOneField(User, primary_key=True)

    def __unicode__(self):
        return "%s" % self.user
