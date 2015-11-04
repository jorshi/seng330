from django.db import models

class FixedItem(models.Model):
    created_in = models.ForeignKey('Room')
    name = models.CharField(max_length=30, default='')
    examine = models.TextField(default='')
    hidden = models.BooleanField(default=False)

class Door(FixedItem):
    
    locked = models.BooleanField(default=False)
    room_a = models.ForeignKey('Room', related_name='room_a')
    room_b = models.ForeignKey('Room', related_name='room_b')

class Room(models.Model):

    title = models.CharField(max_length=30)
    desc_header = models.TextField()
    desc_footer = models.TextField()
    illuminated = models.BooleanField(default=True)
    
    doors = {
        'north': models.ForeignKey('Door', null=True, blank=True, related_name='north'),
        'east': models.ForeignKey('Door', null=True, blank=True, related_name='east'),
        'south': models.ForeignKey('Door', null=True, blank=True, related_name='south'),
        'west': models.ForeignKey('Door', null=True, blank=True, related_name='west'),
    }
