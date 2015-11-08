from gameworld.management.commands.mapbuilder import MapBuilder

def main():
    mapBuilder = MapBuilder()

    # Make rooms
    mapBuilder.makeRoom('Kitchen')
    mapBuilder.makeRoom('Living Room')
    mapBuilder.makeRoom('Den')
    mapBuilder.makeRoom('Entrance Hall')

    # Connect Rooms
    mapBuilder.connectRooms('Kitchen', 'Living Room', 'east')
