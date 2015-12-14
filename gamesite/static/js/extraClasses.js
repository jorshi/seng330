var Room = function(beginDescription, endDescription) {
	this.itemsInRoom = [];
	this.doorLayout = [];

	this.setUpDoors = function(doorArray) {
		this.doorLayout = doorArray;
	}
	// putting the items in the room
	this.setUpItems = function(itemArray) {
		this.itemsInRoom = itemArray;
	}

	//Building room description
	this.updateDescription = function() {
		this.description = beginDescription;
		for (i = 0; i < this.itemsInRoom.length; i++){
			this.description = this.description.concat(this.itemsInRoom[i].enterRoomDescription);
		}
		this.description = this.description.concat(endDescription);
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
	this.add = function(name) {
		this.itemsInInventory.push(name);
	}
	this.printInv = function() {
		for (var i = 0; i < this.itemsInInventory.length; i++) {
			displayResponse(this.itemsInInventory[i].name);
		}
	}
}

var MapNode = function(current, visited, x, y) {
	this.current = current;
	this.visited = visited;
	this.unvisitedButKnown = unvisitedButKnown;
	this.x = x;
	this.y = y;
}

var Map = function() {
	this.mapArray = [];

	this.printMap = function() {
		//$("#map").append("<TEXT>");
		for (var i = 0; i < mapArray.length; i++) {
			x = mapArray[i].x;
			y = mapArray[i].y;
			current = mapArray[i].current;
			visited = mapArray[i].visited;
			unvisitedButKnown = mapArray[i].unvisitedButKnown;
		}
	}
}