from django.core.management.base import BaseCommand, CommandError
import importlib
from django.core import serializers
from gameworld.models import Room, Door, FixedItem, ItemUseState, UsePickupableItem, UseDecoration

JSON_MAP_PATH = 'gameworld/maps/'

class MapBuilder(object):

    def __init__(self):
        self.rooms = {}


    def connectRooms(self, roomA, roomB, direction, locked=False):
        """
        connect two rooms with a door, direction refers to the
        placement of the door in roomA!
        """

        # Create door connecting the two rooms
        door = Door()
        door.room_a = self.rooms.get(roomA)
        door.room_b = self.rooms.get(roomB)
        door.locked  = locked
        door.name = 'Door'
        door.shortdesc = ''
        door.examine = ''
        door.save()

        reverse = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west':'east',
        }

        self.rooms[roomA].set_door(direction, door)
        self.rooms[roomB].set_door(reverse[direction], door)

        self.rooms[roomA].save()
        self.rooms[roomB].save()

    def makeRoom(self, name, title="", illuminated=True,
                 desc="You are in a dim room.", desc2=""):

        try:
            room = Room.objects.get(name=name)
            print("Warning: %s already exists... overwriting" % name)
        except:
            room = Room()
            room.name = name

        room.title = title
        room.illuminated = illuminated
        room.desc_header = desc
        room.desc_footer = desc2
        room.save()

        self.rooms[name] = room

    def addItem(self, room, name, fixed, hidden=False, default_state=0):
        """ make an Item/FixedItem and add to an existing room """
        try:
            r = self.rooms[room]
        except KeyError:
            print("Unable to add %s: room %s does not exist" % (name, room))
            return

        item = FixedItem()

        # check if item already exists in the room
        # since FixedItem is parent class of Item, it holds both
        samename = FixedItem.objects.filter(name=name)
        for match in samename:
            if r in match.found_in.all():
                print("Warning: %s already exists in room %s... overwriting"
                % (name, room))
                # don't assign item = match bc the type won't be modified
                # delete so duplicates don't show up
                match.delete()
        item.name = name
        item.pickupable = fixed
        item.default_state = default_state
        item.save()

        r.default_items.add(item)
        r.save()

        return item


    def addItemUseState(self, item, state, hidden, shortdesc="", examine=""):

        itemUseState = ItemUseState()
        itemUseState.item = item
        itemUseState.examine = examine
        itemUseState.state = state
        itemUseState.hidden = hidden

        if shortdesc == "":
            if name[0] in "aeio":
                itemUseState.short_desc = "an " + name
            else:
                itemUseState.short_desc = "a " + name
        else:
            itemUseState.short_desc = shortdesc

        itemUseState.save()

        return itemUseState


    def addItemUse(
            self,
            item_use_state,
            pickup=True,
            use_message="",
            use_pattern="",
            on_item=None,
            on_item_change=None,
            item_change=None,
            consumed=False
        ):

        if pickup:
            itemUse = UsePickupableItem()
            itemUse.on_item = on_item
            itemUse.on_item_change = on_item_change
            itemUse.item_change = item_change
            itemUse.consumed = consumed

        else:
            itemUse = UseDecoration()

        itemUse.item_use_state = item_use_state
        itemUse.use_message = use_message
        itemUse.use_pattern = use_pattern

        itemUse.save()


def clean_map():
    """ clear everything in gameworld """
    Room.objects.all().delete()
    Door.objects.all().delete()
    FixedItem.objects.all().delete()
    ItemUseState.objects.all().delete()

def save_map(module_name):
    """ backup builder-generated gameworld to a JSON file """
    all_objects = list(Room.objects.all()) + list(Door.objects.all()) \
                + list(FixedItem.objects.all())
    # TODO: include ItemUse classes
    data = serializers.serialize('json', all_objects)

    with open('%s%s.json' % (JSON_MAP_PATH, module_name), 'w') as writer:
        writer.write(data)

def load_map_from_json(filename):
    """ load entire gameworld from a JSON file
        (alternatively, use manage.py loaddata) """
    with open('%s%s' % (JSON_MAP_PATH, filename)) as reader:
        clean_map()
        data = reader.read()
        for obj in serializers.deserialize('json', data):
            obj.save()


class Command(BaseCommand):
    """ Use Django's custom manage.py commands to call MapBuilder in the right
        context (syntax: manage.py mapbuilder [options] <filename>) """
    help = 'Replaces the current map stored in gameworld with a new map.\n' \
           'Specify a Python script, or use --load-json to load the map from ' \
           'a JSON file instead.'
    missing_args_message = 'you need to specify a file (Python or JSON) to build from'

    def add_arguments(self, parser):
        parser.add_argument('--load-json', action='store_true',
                            dest='load_json', default=False,
            help='Load from JSON file instead of running Python script')
        parser.add_argument('script', nargs=1, metavar='<file>',
                            help='.py or .json file')

    def handle(self, *args, **options):
        for script in options['script']:
            # guess if we meant a script or JSON
            is_json = options['load_json'] or script.endswith('.json')
            if is_json:
                if '.json' not in script:
                    script = script + '.json'
                try:
                    load_map_from_json(script)
                except IOError as e:
                    raise CommandError('Unable to load %s\n(more info: %s)' % (script, e))
            else:
                if script.endswith('.py'):
                    script = script[:-3]
                try:
                    module = importlib.import_module('.%s' % script,
                        'gameworld.maps')
                except ImportError as e:
                    raise CommandError('module %s was not found!' % script)
                clean_map()
                module.main()
                save_map(script)

            print('Success: imported map from %s' % script)
