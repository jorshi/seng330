 var room1, room2, playerInventory, player, key, door1, clock, gun, parser;

$(function()  {
	/*rooms*/
	room1 = new Room();
	room2 = new Room();
	
	/*player*/
	playerInventory = new Inventory();
	player = new Player(room1, playerInventory);

	/*items*/
	key = new PickupableAndUsable(room1,"key", "Unlocks somthing.", "You need to use it on somthing.", pattUseItem);
	door1 = new Door(room1, room2,"door", "its shut.", "You try to open the door but it's locked.",false);
	clock = new Decoration(room1,"clock", "It's a clock, It appears to be broken.", null);
	gun = new PickupableAndUsable(room1,"gun", "It doesn't appear to be loaded.", "You try to fire the gun but you can't.", pattShootItem);

	/*this array will be [north,east,south,west] null means no door
	might make this automatically happen in the constructor later*/
	room1.setUpDoors([null,null,door1,null]);
	room2.setUpDoors([door1,null,null,null]);

	/*parser class*/
	parser = new Parser(player);
});