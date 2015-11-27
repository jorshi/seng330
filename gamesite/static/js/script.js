$(function()  {
 
        /*TODO: call an update_room function*/
        $.get('/get_current_room/', function(data) {
                console.log(data);
                console.log(data[0].fields.title);
                console.log(data[0].pk);
                room = new Room(data[0].fields.desc_header, data[0].fields.desc_footer);
 
                //TODO make doors added to room on creation
 
                playerInventory = new Inventory();
                player = new Player(room, playerInventory);
 
                parser = new Parser(player);
 
                player.currentRoom.updateDescription();
                displayResponse("How would you like to proceed?");
                $("#pinnedText").html(player.currentRoom.description);
        });
 
        /*rooms*//*
        room1 = new Room("Room 1: ", "end");
        room2 = new Room("Room 2: ", "end");
        room3 = new Room("Room 3: ", "end");
 
        /*player*//*
        playerInventory = new Inventory();
        player = new Player(room1, playerInventory);
 
        /*items*/
        // need to make it so keys are linked to doors in some way
        /*key1 = new Key("key1", "Unlocks somthing.", "there is a key on the ground (called 'key1'), ");
        key2 = new Key("key2", "Unlocks somthing.", "there is a key on the ground (called 'key2'), ");
 
        door1 = new Door(room1, room2, "door", "its shut.", "there is a door on the south wall, ", true);
        door2 = new Door(room2, room3, "door2", "its shut.", "there is a door on the east wall, ", true);
        clock = new Decoration("clock", "It's a clock, It appears to be broken.", "there is a clock on the wall, ");
        gun = new PickupableAndUsable("gun", ["It doesn't appear to be loaded.", "The gun is loaded"],
                                                                                 ["there is a gun on the floor, ","there is a loaded gun on the floor, "],
                                                                                 ["You try to fire the gun but you can't.", "You fire the gun, It makes a loud BANG"],
                                                                                 [pattShootItem,pattShootItem], 1);
        ammo = new PickupableAndUsable("ammo", ["Ammo for a gun"], ["there is a cartrige of ammo on the floor, "],
                                                                                   ["You need to use it with somthing"], [pattUseItem], 1);
 
        firePlace = new NonPickupableAndUsable("fireplace", ["It is not lit", "there is a fire burning in it"],
                                                                                                                ["there is an unlit fireplace on the west wall, ","there is a fireplace on the west wall with a fire burning in it, "],
                                                                                                                ["You need to light it with somthing","you try to put out the fire"],
                                                                                                                [pattUseItem,pattUnlightItem], 1);
        lighter = new PickupableAndUsable("lighter", ["used to make fires"], ["there is a lighter on the floor, "],
                                                                                   ["You flicker it on and off, prehaps you should use it on somthing?"],
                                                                                   [pattUseItem], 1);
 
        /*this array will be [north,east,south,west] null means no door
        might make this automatically happen in the constructor later*/
        /*room1.setUpDoors([null,null,door1,null]);
        room2.setUpDoors([door1,door2,null,null]);
        room3.setUpDoors([null,null,null,door2]);
 
        room1.setUpItems([key1,door1,clock,gun]);
        room2.setUpItems([key2,door1,door2,ammo,firePlace]);
        room3.setUpItems([door2,lighter]);
 
        /*parser class*/
       
});