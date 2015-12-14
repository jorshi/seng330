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
        The curtains hang tattered, light from the sunset casting shadows across the floor.",
        desc2="You look around the room and notice the door to the East."
    )
    m.makeRoom('room2', 'Second floor', desc="You walk down the stairs and \
        into the next room.", desc2="You cast your gaze around the room and \
        take note of the four doors. The West door has a set of stairs beyond \
        and leads to the attic. There are three other doors, one to the North, \
        one to the South and one to the East.")
    m.makeRoom('northroom', 'A study', desc="You enter the North room.", 
        desc2="There are several tables pressed up against the walls. There are many books \
        that have been left negligently around the room that are wormeaten \
        and moldy. There's a wooden box on one of the tables.")
    # can't access this room yet - the door needs to lock behind you
    # haven't implemented that yet
    m.makeRoom('room3', 'A bedroom', desc="")
    # currently no access - illumination is not supported yet
    m.makeRoom('eastroom', 'Dark', desc="It's completely dark. You can't see a \
    thing apart from the door you just came from, not even the walls.")
    
    # Connect rooms
    door = m.connectRooms('start', 'room2', 'east', locked=False)
    northdoor = m.connectRooms('room2', 'northroom', 'north', locked=True)
    southdoor = m.connectRooms('room2', 'room3', 'south', locked=True)
    bluedoor = m.connectRooms('room2', 'eastroom', 'east', locked=True)
    
    
    
    # Add items
    
    # starting room (Attic)
    window = m.addItem('start', 'window', pickupable=False).addState(
        shortdesc='There is a window to the South.', examine="The window faces \
        South. It's dirty and cracked, but you can look through it easily enough. \
        The sun is setting over the forest below.")
    
    painting = m.addItem('start', 'painting', pickupable=False).addState(
        0, shortdesc="There's a painting on the North wall.", examine="The \
        painting hangs crookedly and is extremely ugly, the colors are mottled \
        and grotesque. You can't even understand the actual forms on the \
        canvas. The left side of the frame is a quarter-inch away from the \
        wall, but the right side is flush with it.").addState(
        1, shortdesc="There's a painting on the North wall.", examine="The \
        painting hangs crookedly and is extremely ugly, the colors are mottled \
        and grotesque. You can't even understand the actual forms on the \
        canvas. There's a key taped to the back of the painting.")
    
    m.addItem('start', 'lighter', pickupable=True).addState(
        shortdesc="There's a lighter on the floor.", examine="It's a plain lighter.")
    
    key = m.addItem('start', 'key', pickupable=True).addState(
        0, hidden=True
        ).addState(
        1, shortdesc="There's a key taped to the back of the painting.", 
        examine="It's small and worn.", hidden=False)
    
    painting.addItemUse(0, pickup=False, use_pattern="look behind|lift NAME", 
        use_message="You lift the painting away from the wall. There's a key taped to the back.", 
        change_self=1, on_item=key.getState(0), change_other=1)
    painting.addItemUse(1, pickup=False, use_pattern="look behind|lift NAME", 
        use_message="There's nothing else behind the painting.")

    
    # Room 2
    
    # get key to north door
    desk = m.addItem('room2', 'desk', pickupable=False).addState(
        0, shortdesc="There's a desk next to the North door.", 
        examine="The desk has three drawers: one on the left, one on the right, \
        and one in the very middle. The right drawer is jammed shut.").addState(
        1, shortdesc="There's a desk next to the North door.",
        examine="The desk has three drawers. The left drawer is open. The \
        right drawer is jammed shut.").addState(
        10, shortdesc="There's a desk next to the North door.", examine="The \
        desk has three drawers. The middle drawer is open. The right drawer \
        is jammed shut.").addState(
        11, shortdesc="There's a desk next to the North door.", examine="The \
        desk has three drawers. The left drawer and the middle drawer are open. \
        The right drawer is jammed shut.")
    redkey = m.addItem('room2', 'red key', pickupable=True).addState(
        0, hidden=True).addState(
        1, shortdesc="There's a red key in the middle drawer.",
        examine="It's painted red.")
    # UseDecoration object
    desk.addItemUse(0, pickup=False, use_pattern="open left drawer", 
        use_message="There's a spare light bulb in the drawer.", change_self=1)
    desk.addItemUse(0, pickup=False, use_pattern="open middle drawer", 
        use_message="There's another key inside, this one painted red.", change_self=10,
        on_item=redkey.getState(0), change_other=1)
    desk.addItemUse(10, pickup=False, use_pattern="open left drawer", 
        use_message="There's a spare light bulb in the drawer.", change_self=11)
    desk.addItemUse(1, pickup=False, use_pattern="open middle drawer", 
        use_message="There's another key inside, this one painted red.", change_self=11,
        on_item=redkey.getState(0), change_other=1)
       
    # get key to south door
    cabinet = m.addItem('room2', 'cabinet', pickupable=False).addState(
        0, shortdesc="There's a cabinet in the corner of the room.", 
        examine="A pair of doors is set in the front.").addState(
        1, shortdesc="There's a cabinet in the corner of the room.", 
        examine="The cabinet is open.")
    key2 = m.addItem('room2', 'rusty key', pickupable=True).addState(
        0, hidden=True
        ).addState(
        1, shortdesc="There's a rusty key inside the cabinet.", 
        examine="It looks like it fits that door to the south.", hidden=False)
    cabinet.addItemUse(0, pickup=False, use_pattern="open NAME( doors)?", 
        use_message="There's a rusty key inside.", change_self=1, 
        on_item=key2.getState(0), change_other=1)
    
    # get key to east door
    vase = m.addItem('room2', 'vase', pickupable=False).addState(
        0, shortdesc="A vase full of long-dead flowers sits on top of the cabinet.", 
        examine="There's no water in the vase, and upon picking it up, all the \
        flowers fall apart.").addState(
        1, shortdesc="A vase sits on top of the cabinet.", 
        examine="The vase is empty.")
    bluekey = m.addItem('room2', 'blue key', pickupable=True).addState(
        0, hidden=True
        ).addState(
        1, shortdesc="Another key, painted blue, was hidden inside the vase.", 
        examine="The East door looks like it might have been blue once.", hidden=False)
    vase.addItemUse(0, pickup=False, use_pattern="(tip|turn) over NAME", 
        use_message="A key, this one painted blue, falls out.", change_self=1, 
        on_item=bluekey.getState(0), change_other=1)
    
    
    
    # Match keys to doors
    
    # east door in starting room
    key.addKeyUse(state=1, on_door=door)
    # north door
    redkey.addKeyUse(state=1, on_door=northdoor)
    # south door - fake use-case - tell the player the key failed to unlock the door
    key2.addItemUse(1, pickup=True, use_pattern="(unlock|use NAME on) south door",
        use_message="The key sticks in the lock and, despite your best efforts, \
        breaks in half.", consumed=True)
    # east door
    bluekey.addKeyUse(state=1, on_door=bluedoor)
    
