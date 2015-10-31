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
}