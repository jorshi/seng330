from mapbuilder import MapBuilder

def main():
    mapBuilder = MapBuilder()
    mapBuilder.cleanMap()

    # Make rooms
    mapBuilder.makeRoom('Kitchen')
    mapBuilder.makeRoom('Living Room')
    mapBuilder.makeRoom('Den')
    mapBuilder.makeRoom('Entrance Hall')

    # Connect Rooms
    mapBuilder.connectRooms('Kitchen', 'Living Room', 'east')
