from gameworld.management.commands.mapbuilder import MapBuilder

def main():
    m = MapBuilder()

    # Make rooms
    m.makeRoom(
        'start',
        title='Attic',
        desc="You wake up in a dimly lit room, not entirely sure where you are \
        or how you got there. The paint on the walls is cracked and peeling, \
        yellowed stains stretching from the ceiling to the floor. \
        the curtains hang tattered, light from the sunset casting shadows across the floor.",
        desc2="You look around the room and notice the door to the East.."
    )


    # Add items
    window = m.addItem('start', 'window', pickupable=False).addState(
        shortdesc='There is a window to the South.', examine="The window faces South, It's dirty, and cracked, but you can look through it easily enough. The sun is setting over the forest below.")
    
    painting = m.addItem('start', 'painting', pickupable=False).addState(
        0, shortdesc="There's a painting on the North wall.", examine="The painting hangs crookedly and is extremely ugly, the colors are mottled and grotesque. You can't even understand the actual forms on the canvas. The left side of the frame is a quarter-inch away from the wall, but the right side is flush with it.").addState(
        1, shortdesc="There's a painting on the North wall.", examine="The painting hangs crookedly and is extremely ugly, the colors are mottled and grotesque. You can't even understand the actual forms on the canvas.")
    
    '''
    lighter = m.addItem('start', 'lighter', pickupable=True).addState(
        shortdesc="There's a lighter on the floor.", examine="It's a prosaic yellow BIC lighter.")
    '''
    
    key = m.addItem('start', 'key', pickupable=True).addState(
        0, hidden=True
        ).addState(
        1, shortdesc="There's a key taped to the back of the painting.", examine="It's small and worn.", hidden=False)
    
    painting.addItemUse(0, pickup=False, use_pattern="(look behind)|lift NAME", use_message="You lift the painting away from the wall.", change_self=1, on_item=key.getState(0), change_other=1)
    painting.addItemUse(1, pickup=False, use_pattern="(look behind)|lift NAME", use_message="There's nothing else behind the painting.")

    m.makeRoom('room2', 'Second floor', desc="You walk down the stairs and into the next room.", desc2="You cast your gaze around the room and take note of the four doors. The West door is the one you came from has a set of stairs beyond and leads to the attic. There are three other doors, one to the North, one to the South and one to the East. There's a cabinet in one of the corners with a vase full of long dead flowers on top. There's also a desk next to the North door, papers strewn across the floor.")

    door = m.connectRooms('start', 'room2', 'east', locked=True)

    # todo add key use
    key.addKeyUse(state=1, on_door=door)
