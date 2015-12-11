from django.db import models
from model_utils.managers import InheritanceManager

# default=None: hack to enforce NOT NULL
# http://stackoverflow.com/questions/12879256/

def usePatternFormat(patt):
    fpatt = patt.replace("NAME", "(.+)").replace("OTHER", "(.+)")
    return "^\s*" + "\s+".join(fpatt.split()) + "\s*$"

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
    
    def addItemUse(self, state, pickup, use_pattern, use_message, 
        consumed=False, on_item=None, change_self=None, change_other=None):
        """
        use_pattern: use the NAME and OTHER wildcards to replace the item and on_item names
        """
    
        if pickup or on_item is not None:
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
        
        if on_item:
            try:
                other = ItemUseState.objects.get(pk=on_item.pk)
                itemUse.on_item = other
                if change_other:
                    try:
                        itemUse.on_item_change = other.item.getState(change_other)
                    except:
                        print("Error: change_other %s doesn't exist for %s" % (change_other, other))
                        return
            except:
                print("Error: on_item %s doesn't exist or is ambiguous" % (on_item,))
                return
            
        itemUse.use_pattern = usePatternFormat(use_pattern)
        itemUse.save()
    
    def addKeyUse(self, state, on_door, use_message="", use_pattern=""):
        """ Usage for keys 
            use_pattern: use the DOOR wildcard to replace with appropriate door(s)
        """

        keyUse = UseKey()
        try:
            keyUse.item_use_state = self.states.get(state=state)
        except:
            print("Error trying to add key use: state %s doesn't exist" % (state,))
            return
        
        keyUse.on_door = on_door
        if use_message:
            keyUse.use_message = use_message
        else:
            keyUse.use_message = "You unlocked the door."
        
        if not use_pattern:
            use_pattern = "unlock|(use NAME on) DOOR"
        keyUse.use_pattern = usePatternFormat(use_pattern)
        keyUse.save()
        
    def getState(self, num):
        return self.states.get(state=num)
        
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

    def json(self, room_name):
        obj = {
            'name': self.item.name,
            'examineDescription': self.examine,
            'enterRoomDescription': self.short_desc
        }
        # quick-fix for frontend spec
        obj['type'] = "pickupableAndUsable" if self.item.pickupable else "fixedAndUsable"
        
        usecases = AbstractUseItem.objects.select_subclasses().filter(
            item_use_state=self)
        temp = [use.json(room_name) for use in usecases]
        obj['useCases'] = [x for x in temp if x is not None]
        
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
    
    def json(self, room_name):
        obj = {}
        obj['ref'] = self.pk
        obj['usePattern'] = self.use_pattern
        obj['useMessage'] = self.use_message
        return obj


class UsePickupableItem(AbstractUseItem):
    """ Describes usage patterns for a pickable item """

    on_item = models.ForeignKey('ItemUseState', null=True, related_name='action_on_self')

    # State to change the on_item to after usage - ie, what affect
    # does this action have on the item it is being used on?
    on_item_change = models.ForeignKey('ItemUseState', null=True, related_name='indirect_cause')

    # Does this item disappear from the users inventory after it has
    # been used?
    consumed = models.BooleanField(default=False)
    
    def execute(self, game_state):
        item = self.item_use_state
        if item.item.pickupable:
            # check if item is in inventory
            if not game_state.inventory.filter(pk=item.pk).exists():  # ItemUseState items
                print("UsePickupableItem error: %s is not in inventory" % item)
                return False
            if self.item_change:
                game_state.inventory.add(self.item_change)
                game_state.inventory.remove(item)
        else:
            # check if item is in current room
            if not game_state.current_room.itemstate_set.filter(item=item).exists():
                print("UsePickupableItem error: %s is not in the room" % item)
                return False
            if self.item_change:
                wrapper = game_state.current_room.itemstate_set.get(item=item)
                wrapper.item = self.item_change
                wrapper.save()
                
        if self.consumed:
            game_state.inventory.remove(item)
        
            
        if self.on_item is not None:
            # check if on_item is in inventory
            if game_state.inventory.filter(pk=self.on_item.pk).exists():
                if self.on_item_change is not None:
                    game_state.inventory.add(self.on_item_change)
                    game_state.inventory.remove(self.on_item)
            # check if on_item is in room
            elif game_state.current_room.itemstate_set.filter(item=self.on_item).exists():
                wrapper = game_state.current_room.itemstate_set.get(item=self.on_item)
                if self.on_item_change is not None:
                    wrapper.item = self.on_item_change
                    wrapper.save()
            else:
                print("UsePickupableItem error: on_item not found anywhere")
                return False
                
        return True

    def __unicode__(self):
        return u'use %s on %s' % (self.item_use_state.item, self.on_item.item)


class UseDecoration(AbstractUseItem):
    """ Usage patterns for using a decoration """

    def execute(self, game_state):
        item = self.item_use_state
        # check if item is in current room
        if not game_state.current_room.itemstate_set.filter(item=item).exists():
            print("UseDecoration error: %s is not in the room" % item)
            return False
        if self.item_change is not None:
            wrapper = game_state.current_room.itemstate_set.get(item=item)
            wrapper.item = self.item_change
            wrapper.save()
        return True
        
    def __unicode__(self):
        return u'use %s' % self.item_use_state.item

class UseKey(AbstractUseItem):
    """ Usage pattern for a key """

    on_door = models.ForeignKey("Door")
    
    def json(self, room_name):
        obj = super(UseKey, self).json(room_name)
        # return appropriate usePattern if the door is in current room
        # otherwise return None
        room = Room.objects.get(name=room_name)
        if self.on_door.room_a == room or self.on_door.room_b == room:
            dirs = ['north', 'east', 'west', 'south']
            for dir in dirs:
                if room.get_door(dir) == self.on_door:
                    obj['usePattern'] = obj['usePattern'].replace("DOOR", dir + "\s+door")
                    break
        else:
            return None
        return obj
    
    def execute(self, game_state):
        # check if key is in inventory
        item = self.item_use_state
        if not game_state.inventory.filter(pk=item.pk).exists():  # ItemUseState items
            print("UseKey error: %s is not in inventory" % item)
            return False
        # check door direction
        room = game_state.current_room.room
        door_match = game_state.doorstate_set.filter(
            models.Q(room_a=room) | models.Q(room_b=room)
            ).filter(
            door=self.on_door
            )
        if not door_match.exists():
            print("UseKey error: door isn't in current room")
            return False
            
        # unlock the door (DoorState)
        door_state = door_match[0]
        door_state.locked = False
        door_state.save()
        
        # key is always consumed
        game_state.inventory.remove(item)
        return True

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
