from gameworld.management.commands.mapbuilder import MapBuilder

def main():
    mapBuilder = MapBuilder()

    # Make rooms
    mapBuilder.makeRoom(
        'start',
        title='Attic',
        desc="You wake up in a dimly lit room, not entirely sure where you are or how you got there. The paint on the
        walls is cracked and peeling, yellowed stains stretching from the ceiling to the floor. There is a window to the
        South, the curtains hang tattered, light from the sunset casting shadows across the floor.",
        desc2="You look around the room and notice the door to the East. There's a painting on the North Wall, and a lighter on the floor."
    )


    # Add items
    mapBuilder.addItem('start', 'window', fixed=True, examine="The window faces South, It's dirty, and cracked, but you can look through it easily enough. The sun is setting over the forest below.")
    mapBuilder.addItem('start', 'painting', fixed=True, examine=" The painting hangs crookedly and is extremely ugly, the colors are mottled and grotesque. You can't even understand the actual forms on the canvas.")
    # TODO add "use painting"
    mapBuilder.addItem('start', 'key', fixed=False, examine="It's small and worn.", hidden=True)

    mapBuilder.makeRoom('room2', 'Second floor', desc="You walk down the stairs and into the next room.", desc2="You cast your gaze around the room and take note of the four doors. The West door is the one you came from has a set of stairs beyond and leads to the attic. There are three other doors, one to the North, one to the South and one to the East. There's a cabinet in one of the corners with a vase full of long dead flowers on top. There's also a desk next to the North door, papers strewn across the floor.")

    mapBuilder.connectRooms('start', 'room2', 'east', locked=True)


