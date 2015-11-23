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


    # Add items
    item = mapBuilder.addItem('start', 'Fireplace', True)
    itemState = mapBuilder.addItemUseState(item, 0, "Fieplace is lit", "Yo I'm on fire")
    mapBuilder.addItemUse(itemState, False, use_pattern="regexxx")
    itemState = mapBuilder.addItemUseState(item, 1, "Fireplace is not lit", "Yo I'm not lit")
