from django.db import models

class FixedItem(models.Model):
    """ concrete parent class for anything the player can interact with """
    name = models.CharField(max_length=30)
    examine = models.TextField()
    hidden = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class Item(FixedItem):
    """ items that can be picked up and used """
    pass

class ItemUse(models.Model):
    """ describes how the item is used, consuming it """
    item = models.ForeignKey('Item', related_name='use_cases')
    use_on = models.ForeignKey('FixedItem', blank=True)
    keywords = models.CharField(max_length=200, default='use')
    use_message = models.TextField()
    use_script = models.CharField(max_length=200, blank=True)
    
    def __unicode__(self):
        return '%s %s' % (self.keywords, self.item)
    
class Door(FixedItem):
    """ Door object """
    locked = models.BooleanField(default=False)
    room_a = models.ForeignKey('Room', related_name='doors_a')
    room_b = models.ForeignKey('Room', related_name='doors_b')
    
    def __unicode__(self):
        return '%s--%s' % (self.room_a, self.room_b)

class Room(models.Model):
    """ Room object """
    title = models.CharField(max_length=30)
    desc_header = models.TextField()
    desc_footer = models.TextField()
    illuminated = models.BooleanField(default=True)
    default_items = models.ManyToManyField('FixedItem')
    door_north = models.ForeignKey('Door', null=True, blank=True, related_name='north')
    door_east = models.ForeignKey('Door', null=True, blank=True, related_name='east')
    door_south = models.ForeignKey('Door', null=True, blank=True, related_name='south')
    door_west = models.ForeignKey('Door', null=True, blank=True, related_name='west')
    doors = {
        'north': door_north,
        'east': door_east,
        'south': door_south,
        'west': door_west,
    }
    
    def __unicode__(self):
        return self.title
