from django.db import models

# default=None: hack to enforce NOT NULL
# http://stackoverflow.com/questions/12879256/


class FixedItem(models.Model):
    """ concrete parent class for anything the player can interact with """

    # name the player uses to refer to the item, e.g. "painting"
    name = models.CharField(max_length=30, default=None)
    # a few words displayed when listing the items in the room, e.g. "an oil painting"
    shortdesc = models.CharField(max_length=30, default=None)
    # longer text displayed when the player types "examine <name>"
    examine = models.TextField()
    # whether the item is initially hidden
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Item(FixedItem):
    """ items that can be picked up and used """

    pass


class AbstractUseItem(models.Model):
    """ describes how an item can be used """
    
    # comma-separated list of keywords, e.g. "use,move"
    keywords = models.CharField(max_length=200)
    # longer text describing the result of performing the action
    desc = models.TextField()
    
    script = models.CharField(max_length=200, blank=True)

    class Meta:
        abstract = True

class UseInventoryItem(AbstractUseItem):
    """ use an item from player inventory, which will be consumed """
    item = models.ForeignKey('Item', related_name='use_cases')
    on_item = models.ForeignKey('FixedItem', blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.keywords, self.item)

class UseDecoration(AbstractUseItem):
    item = models.ForeignKey('FixedItem')

    def __unicode__(self):
        return u'%s %s' % (self.keywords, self.item)


class Door(FixedItem):
    """ Door object """

    locked = models.BooleanField(default=False)
    room_a = models.ForeignKey('Room', related_name='doors_a')
    room_b = models.ForeignKey('Room', related_name='doors_b')

    def leads_to(self, this_room):
        """ Returns a string hinting at the next room """

        success = 'The door seems to lead to the'
        failure = 'The door doesn\'t seem to lead anywhere.'
        if this_room == self.room_a:
            return '%s %s.' % (success, self.room_b.title)
        elif this_room == self.room_b:
            return '%s %s.' % (success, self.room_a.title)
        else:
            return failure

    def __unicode__(self):
        return u'%s--%s' % (self.room_a, self.room_b)


class Room(models.Model):
    """ Room object """

    name = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=50, blank=True)  # optional - displayed above terminal
    desc_header = models.TextField(default=None)
    desc_footer = models.TextField()
    illuminated = models.BooleanField(default=True)
    default_items = models.ManyToManyField('FixedItem', related_name="found_in")
    door_north = models.ForeignKey('Door', null=True, blank=True, related_name='north')
    door_east = models.ForeignKey('Door', null=True, blank=True, related_name='east')
    door_south = models.ForeignKey('Door', null=True, blank=True, related_name='south')
    door_west = models.ForeignKey('Door', null=True, blank=True, related_name='west')


    def get_door(self, direction):
        """
        Returns the Door object for the direction specified
        """

        return {
            'east': self.door_east,
            'north': self.door_north,
            'west': self.door_west,
            'south': self.door_south
        }.get(direction)


    def set_door(self, direction, Door):
        """
        Given a direction and a Door object, set that Door object
        to the correct door attribute
        """

        {
            'east': lambda x: setattr(self, 'door_east', x),
            'north': lambda x: setattr(self, 'door_north', x),
            'west': lambda x: setattr(self, 'door_west', x),
            'south': lambda x: setattr(self, 'door_south', x),
        }.get(direction)(Door)


    def __unicode__(self):
        return self.name
