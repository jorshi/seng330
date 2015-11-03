 var room1, room2, room3, playerInventory, player, key1, key2, door1, door2, clock, gun, parser;

$(function()  {
	/*rooms*/
	room1 = new Room();
	room2 = new Room();
	room3 = new Room();

	/*player*/
	playerInventory = new Inventory();
	player = new Player(room1, playerInventory);

	/*items*/
	// need to make it so keys are linked to doors in some way
	key1 = new PickupableAndUsable(room1,"key1", "Unlocks somthing.", "You need to use it on somthing.", pattUseItem);
	key2 = new PickupableAndUsable(room2,"key2", "Unlocks somthing.", "You need to use it on somthing.", pattUseItem);

	door1 = new Door(room1, room2, "door", "its shut.", "You try to open the door but it's locked.", true);
	door2 = new Door(room2, room3, "door2", "its shut.", "You try to open the door but it's locked.", true);
	clock = new Decoration(room1,"clock", "It's a clock, It appears to be broken.", null);
	gun = new PickupableAndUsable(room1,"gun", "It doesn't appear to be loaded.", "You try to fire the gun but you can't.", pattShootItem);

	/*this array will be [north,east,south,west] null means no door
	might make this automatically happen in the constructor later*/
	room1.setUpDoors([null,null,door1,null]);
	room2.setUpDoors([door1,door2,null,null]);
	room3.setUpDoors([null,null,null,door2]);

	/*parser class*/
	parser = new Parser(player);
});