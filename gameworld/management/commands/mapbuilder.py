from django.core.management.base import BaseCommand, CommandError
import importlib
from gameworld.models import Room, Door

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
        door.created_in = self.rooms[roomA]
        door.name = 'Door'
        door.examine = "Door between %s and %s" % (roomA, roomB)
        door.save()

        direction_map = {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west':'east',
        }
        
        self.rooms[roomA].doors[direction] = door
        self.rooms[roomB].doors[direction_map[direction]] = door
        self.rooms[roomA].save()
        self.rooms[roomB].save()

    def makeRoom(self, title, illuminated=True):

        try:
            room = Room.objects.get(title=title)
        except:
            room = Room()
            room.title = title

        room.illuminated = illuminated
        room.save()
        
        self.rooms[title] = room

    def cleanMap(self):
        rooms = Room.objects.all().delete()
        doors = Door.objects.all().delete()

class Command(BaseCommand):
    help = 'Replaces the current map stored in gameworld with a new map'
    
    def add_arguments(self, parser):
        parser.add_argument('script', nargs=1)
        
    def handle(self, *args, **options):
        for script in options['script']:
            try:
                module = importlib.import_module('.%s' % script, 
                    'gameworld.management.commands')
                module.main()
            except ImportError:
                raise CommandError('%s was not found!' % script)
            print('Success: imported map from %s' % script)
            
