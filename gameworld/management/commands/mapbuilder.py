from django.core.management.base import BaseCommand, CommandError
import importlib
from django.core import serializers
from gameworld.models import Room, Door

def clean_map():
    """ clear everything in gameworld """
    Room.objects.all().delete()
    Door.objects.all().delete()
    
def save_map(name):
    """ backup builder-generated gameworld to a JSON file """
    all_objects =   list(Room.objects.all()) + list(Door.objects.all())
    data = serializers.serialize('json', all_objects)
    
    with open('gameworld/maps/%s.json' % name, 'w') as writer:
        writer.write(data)
        writer.close
            
    
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

    def makeRoom(self, name, title="", illuminated=True, desc="You are in a dim room."):

        try:
            room = Room.objects.get(name=name)
        except:
            room = Room()
            room.name = name

        room.title = title
        room.illuminated = illuminated
        room.desc_header = desc
        room.save()
        
        self.rooms[name] = room

class Command(BaseCommand):
    help = 'Replaces the current map stored in gameworld with a new map'
    
    def add_arguments(self, parser):
        parser.add_argument('script', nargs=1)
        
    def handle(self, *args, **options):
        for script in options['script']:
            try:
                module = importlib.import_module('.%s' % script, 
                    'gameworld.management.commands')
            except ImportError:
                raise CommandError('%s was not found!' % script)
            clean_map()
            module.main()
            save_map(script)
            
            print('Success: imported map from %s' % script)
            
