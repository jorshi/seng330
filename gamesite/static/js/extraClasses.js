var Room = function() {
	this.itemsInRoom = [];
	this.doorLayout = [];

	this.setUpDoors = function(doorArray) {
		this.doorLayout = doorArray;
	}
}

var Player = function(currentRoom, inv) {
	this.currentRoom = currentRoom;
	this.inv = inv;

	this.changeRoom = function(room) {
		this.currentRoom = room;
	}
}

var Inventory = function() {
	this.itemsInInventory = [];

	this.remove = function(name) {
		/*Now we have to remove the item from the room and put it into the inventory*/
		var index = this.itemsInInventory.indexOf(name);
		/*confusing looking but all it does is move the item from the Inventory to the room*/
		this.itemsInInventory.splice(index, 1)[0];
	}
}