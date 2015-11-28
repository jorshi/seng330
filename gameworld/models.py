from django.db import models

# default=None: hack to enforce NOT NULL
# http://stackoverflow.com/questions/12879256/

class FixedItem(models.Model):
    """ concrete parent class for anything the player can interact with """

    # name the player uses to refer to the item, e.g. "painting"
    name = models.CharField(max_length=30, default=None)
    # whether the item is initially hidden
    hidden = models.BooleanField(default=False)
    default_state = models.IntegerField()

    def __unicode__(self):
        return self.name


class Item(FixedItem):
    """ items that can be picked up and used """

    pass


class ItemUseState(models.Model):
    """
    Describes items as they change over the course of game play
    """

    item = models.ForeignKey("FixedItem")
    examine = models.TextField()
    short_desc = models.CharField(max_length=30, default=None)
    state = models.IntegerField()
    
    def __unicode__(self):
        return u'%s(%s)' % (self.item, self.state)


class AbstractUseItem(models.Model):
    """ describes how an item can be used """

    # longer text describing the result of performing the action
    use_message = models.TextField()
    # Regex for use in JavaScript
    use_pattern = models.CharField(max_length=200, blank=True)
    item_use_state = models.ForeignKey("ItemUseState")

    class Meta:
        abstract = True


class UsePickupableItem(AbstractUseItem):
    """ Describes usage patterns for a pickable item """

    on_item = models.ForeignKey('FixedItem', blank=True)

    # State to change the on_item to after usage
    on_item_change = models.IntegerField(null=True)

    # State to change this item to after usage
    item_change = models.IntegerField(null=True)
    consumed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'use %s on %s' % (self.item_use_state.item, self.on_item)


class UseDecoration(AbstractUseItem):

    def __unicode__(self):
        return u'use %s' % (self.item_use_state.item)


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

    def update_state(self, state):
        """
        Temporarily update the state of this room during game play
        """

        self.illuminated = state.illuminated

    def __unicode__(self):
        return self.name
