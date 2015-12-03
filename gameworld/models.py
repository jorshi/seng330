from django.db import models
from model_utils.managers import InheritanceManager

# default=None: hack to enforce NOT NULL
# http://stackoverflow.com/questions/12879256/

class FixedItem(models.Model):
    """ concrete parent class for anything the player can interact with """

    # name the player uses to refer to the item, e.g. "painting"
    name = models.CharField(max_length=30, default=None)	
    pickupable = models.BooleanField(default=False)
    default_state = models.IntegerField(default=0)

    def addState(self, num=0, hidden=False, shortdesc="", examine=""):
        existing = self.states.filter(state=num)
        for dup in existing:
            print("Warning: %s state %s already exists... overwriting"
            % (self, num))
            dup.delete()
            
        state = ItemUseState()
        state.state = num
        state.item = self
        state.examine = examine
        state.hidden = hidden
        if shortdesc:
            state.short_desc = shortdesc
        else:
            if self.name[0] in "aeio":
                state.short_desc = "an " + self.name
            else:
                state.short_desc = "a " + self.name
        state.save()
        return self
    
    def addItemUse(self, state, pickup, use_pattern, use_message, consumed=False, on_item=None, change_self=None, change_other=None):
        #  TODO this makes UseKey()s too?
    
        if pickup:
            itemUse = UsePickupableItem()
            itemUse.consumed = consumed
        else:
            itemUse = UseDecoration()
        itemUse.item = self  
        try:
            itemUse.item_use_state = self.states.get(state=state)
            if change_self:
                itemUse.item_change = self.states.get(state=change_self)
        except:
            print("Error trying to add item use: %s state %s doesn't exist" % (self, state))
            return
        
        itemUse.use_message = use_message
        #fpatt = use_pattern.replace("NAME", self.name)
        fpatt = use_pattern.replace("NAME", "(.+)")
        if on_item:
            try:
                other = FixedItem.objects.get(pk=on_item.pk)
                itemUse.on_item = other
                if change_other:
                    try:
                        itemUse.on_item_change = other.states.get(state=change_other)
                    except:
                        print("Error: change_other %s doesn't exist for %s" % (change_other, other))
                        return
            except:
                print("Error: on_item %s doesn't exist or is ambiguous" % (on_item,))
                return
            
            #fpatt = fpatt.replace("OTHER", on_item.name)
            fpatt = fpatt.replace("OTHER", "(.+)")
        itemUse.use_pattern = "^\s*" + "\s+".join(fpatt.split()) + "\s*$"
        
        itemUse.save()
    
    def addKeyUse(self, state, on_door, use_message="", use_pattern=""):
        """ Usage for keys """

        keyUse = UseKey()
        try:
            keyUse.item_use_state = self.states.get(state=state)
        except:
            print("Error trying to add key use: state %s doesn't exist" % (state,))
            return
        keyUse.on_door = on_door
        keyUse.use_message = use_message
        # TODO regex parsing
        keyUse.use_pattern = use_pattern
        keyUse.save()
        
    def __unicode__(self):
        return self.name


class ItemUseState(models.Model):
    """
    Describes items as they change over the course of game play. We need this
    to store the various text / descriptions that a particular item may have
    in it's various states throughout game play. ex) A fire could be lit or
    unlit. Depending on this we want to be able to return a different description
    status.
    """
    
    state = models.IntegerField()
    item = models.ForeignKey("FixedItem", related_name="states")
    examine = models.TextField()
    hidden = models.BooleanField(default=False)
    short_desc = models.CharField(max_length=30, default=None)

    def json(self):
        obj = {
            'name': self.item.name,
            'examineDescription': self.examine,
            'enterRoomDescription': self.short_desc
        }
        # todo quick-fix for frontend spec
        obj['type'] = "pickupableAndUsable" if self.item.pickupable else "fixedAndUsable"
        
        usecases1 = self.abstractuseitem_action.all() 
        obj['useCases'] = [
            {
                'ref': usecase.pk,
                'usePattern': usecase.use_pattern,
                'useMessage': usecase.use_message
            } for usecase in usecases1]
        if not obj['useCases'] and not self.item.pickupable:
            obj['type'] = 'decoration'
        
        return obj
        
    def __unicode__(self):
        return u'%s(%s)' % (self.item, self.state)


class AbstractUseItem(models.Model):
    """ Describes how an item can be used """

    objects = InheritanceManager()
    # longer text describing the result of performing the action
    use_message = models.TextField()
    # Regex for use in JavaScript
    use_pattern = models.CharField(max_length=200, blank=True)
    item_use_state = models.ForeignKey("ItemUseState", related_name='%(class)s_action')
    # State to change this item to after usage - ie, what is the affect
    # on this item after it has been used?
    item_change = models.ForeignKey('ItemUseState', null=True, related_name='%(class)s_cause')


class UsePickupableItem(AbstractUseItem):
    """ Describes usage patterns for a pickable item """

    on_item = models.ForeignKey('ItemUseState', null=True, related_name='action_on_self')

    # State to change the on_item to after usage - ie, what affect
    # does this action have on the item it is being used on?
    on_item_change = models.ForeignKey('ItemUseState', null=True, related_name='indirect_cause')

    # Does this item disappear from the users inventory after it has
    # been used?
    consumed = models.BooleanField(default=False)

    def __unicode__(self):
        return u'use %s on %s' % (self.item_use_state.item, self.on_item)


class UseDecoration(AbstractUseItem):
    """ Usage patterns for using a decoration """

    def __unicode__(self):
        return u'use %s' % (self.item_use_state.item)

class UseKey(AbstractUseItem):
    """ Usage pattern for a key """

    on_door = models.ForeignKey("Door")

    def __unicode__(self):
        return u"key: opens %s" % self.on_door


class Door(FixedItem):
    """ Door object """

    locked = models.BooleanField(default=False)
    room_a = models.ForeignKey('Room', related_name='doors_a')
    room_b = models.ForeignKey('Room', related_name='doors_b')

    def shortdesc(self, this_room):
        """ Returns a string describing the door's position """
        pass
        
    def examine(self, this_room):
        """ Returns a string hinting at the next room """

        success = 'The door seems to lead to the'
        failure = 'The door doesn\'t seem to lead anywhere.'
        if this_room == self.room_a:
            return '%s %s.' % (success, self.room_b.title)
        elif this_room == self.room_b:
            return '%s %s.' % (success, self.room_a.title)
        else:
            return failure

    def other_room(self, this_room):
        """ Returns name of the other room """
        if this_room == self.room_a:
            return self.room_b
        elif this_room == self.room_b:
            return self.room_a
        else:
            return None
        
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
