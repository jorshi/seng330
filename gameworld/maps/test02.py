from gameworld.management.commands.mapbuilder import MapBuilder

def main():
    mapBuilder = MapBuilder()

    # Make rooms
    mapBuilder.makeRoom('Xvgpura')
    mapBuilder.makeRoom('Ragenapr Unyy')
    mapBuilder.makeRoom('Qra')
    mapBuilder.makeRoom('Yvivat Ebbz')

    # Connect Rooms
    mapBuilder.connectRooms('Xvgpura', 'Ragenapr Unyy', 'west')
