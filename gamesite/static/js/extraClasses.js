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

			//PLEASE FORGIVE THE FOLLOWING CODE
			if (this.itemsInRoom[i].enterRoomDescription == "there is a door on the south wall, " && player.currentRoom != room1){
				this.itemsInRoom[i].enterRoomDescription = "there is a door on the north wall, "
			}

			if (this.itemsInRoom[i].enterRoomDescription == "there is a door on the west wall, " && player.currentRoom == room2){
				this.itemsInRoom[i].enterRoomDescription = "there is a door on the east wall, "
			}
			if (this.itemsInRoom[i].enterRoomDescription == "there is a door on the north wall, " && player.currentRoom == room1){
				this.itemsInRoom[i].enterRoomDescription = "there is a door on the south wall, "
			}

			if (this.itemsInRoom[i].enterRoomDescription == "there is a door on the east wall, " && player.currentRoom == room3){
				this.itemsInRoom[i].enterRoomDescription = "there is a door on the west wall, "
			}
			
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
}