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
    mapBuilder.connectRooms('Entrance Hall', 'Kitchen', 'north')
    mapBuilder.connectRooms('Entrance Hall', 'Den', 'west')
    mapBuilder.connectRooms('Kitchen', 'Living Room', 'west')
