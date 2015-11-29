import gameworld.management.commands.mapbuilder as mapbuilder

def main():
    mapBuilder = mapbuilder.MapBuilder()
    mapbuilder.clean_map()


    # Make rooms
    mapBuilder.makeRoom(
        'start',
        title='Attic',
        desc="""You wake up in a dimly lit room, not entirely sure where you are or how you got there. The paint on the
        walls is cracked and peeling, yellowed stains stretching from the ceiling to the floor. There is a window to the
        South, the curtains hang tattered, light from the sunset casting shadows across the floor.""",
        desc2="""You look around the room and notice the door to the East. There's a painting on the North Wall, and a
        lighter on the floor."""
    )

    mapBuilder.makeRoom(
        'kitchen',
        'Kitchen',
        desc="""You've entered the Kitchen. The fridge door is slightly ajar and smells like bologni.""",
        desc2="""Yup that is a smelly fridge.""",
    )

    doorA = mapBuilder.connectRooms(
        'start',
        'kitchen',
        'north',
    )

    # Add items
    item = mapBuilder.addItem('start', 'Fireplace', False)
    itemState = mapBuilder.addItemUseState(item, 0, False, "Fieplace is lit", "Yo I'm on fire")
    mapBuilder.addItemUse(itemState, False, use_pattern="regexxx")
    itemState = mapBuilder.addItemUseState(item, 1, False, "Fireplace is not lit", "Yo I'm not lit")

    item = mapBuilder.addItem('start', 'Matches', True)
    itemState = mapBuilder.addItemUseState(item, 0, False, "Match short description 1", "Examine matches 1")
    mapBuilder. addItemUse(itemState, use_pattern="matchRegex")

    key = mapBuilder.addItem('start', 'Tarnished Key', True)
    itemState = mapBuilder.addItemUseState(key, 0, False, "Tarnished Key", "You found a tarnished key")
    mapBuilder.addKeyUse(itemState, doorA)
