import gameworld.management.commands.mapbuilder as mapbuilder

def main():
    m = mapbuilder.MapBuilder()
    mapbuilder.clean_map()
    

    # Make rooms
    m.makeRoom(
        'start',
        title='Attic',
        desc="""You wake up in a dimly lit room, not entirely sure where you are or how you got there. The paint on the
        walls is cracked and peeling, yellowed stains stretching from the ceiling to the floor. There is a window to the
        South, the curtains hang tattered, light from the sunset casting shadows across the floor.""",
        desc2="""You look around the room and notice the door to the East. There's a painting on the North Wall, and a
        lighter on the floor."""
    )


    # Add items
    item = m.addItem('start', 'Fireplace', True)
    
    item.addState(1, hidden=False, shortdesc="Fireplace is lit", examine="Yo I'm on fire")
    item.addState(0, shortdesc="Fireplace is not lit", examine="Yo I'm not lit")
    item.addItemUse(0, False, use_pattern="light fire(place)?", use_message="The fireplace comes to life.", change_self=1)
    
