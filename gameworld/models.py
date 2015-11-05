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
        return ' '.join([unicode(self.keywords), unicode(self.item)])
    
class Door(FixedItem):
    """ Door object """
    locked = models.BooleanField(default=False)
    room_a = models.ForeignKey('Room', related_name='doors_a')
    room_b = models.ForeignKey('Room', related_name='doors_b')
    
    def __unicode__(self):
        return "--".join([unicode(self.room_a), unicode(self.room_b)])

class Room(models.Model):
    """ Room object """
    title = models.CharField(max_length=30)
    desc_header = models.TextField()
    desc_footer = models.TextField()
    illuminated = models.BooleanField(default=True)
    default_items = models.ManyToManyField('FixedItem')
    doors = {
        'north': models.ForeignKey('Door', null=True, blank=True, related_name='north'),
        'east': models.ForeignKey('Door', null=True, blank=True, related_name='east'),
        'south': models.ForeignKey('Door', null=True, blank=True, related_name='south'),
        'west': models.ForeignKey('Door', null=True, blank=True, related_name='west'),
    }
    
    def __unicode__(self):
        return self.title
