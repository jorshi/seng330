function GameManager()  {
	this.currentRoom;
	this.roomItems;
	this.roomDoors;
	this.inventory;
	
	this.updateRoom = function(data)  {
		this.updateSelf(data);
		this.printRoom();
		this.printTitle();
		$("#commandUserInput").focus();
	}
	
	this.updateSelf = function(data)  {
		this.currentRoom = data.room;
		this.roomItems = this.currentRoom.items;
		this.roomDoors = this.currentRoom.doors;
		this.inventory = data.inventory;
		parser.addItemUses(this.roomItems.concat(this.inventory));
	}
	
	// print the room description & its contents to the terminal
	this.printRoom = function()  {
		var room = this.currentRoom;
	
		displayResponse(room.desc_header);
		printItemList(room.items, function(item)  {
			return item.enterRoomDescription;
		});
		
		displayResponse(room.desc_footer);
	}
	
	// replace title with new one
	this.printTitle = function()  {
		$("#pinnedText").html(this.currentRoom.title);
	}

	
	// API functions
	
	// returns a room object with description fields, room contents,
	// doors, etc.
	// called on page load
	this.getRoom = function()  {
		$.get('/get_current_room/', function(data) {
			manager.updateRoom(data);
		}, "json");
	}
	
	this.postChangeRoom = function(data)  {
		$.post('/post_change_room/', data, function(serverdata)  {
			manager.updateRoom(serverdata);
		}, 'json');
	}
	// tells the backend the player used an item
	this.postPlayerAction = function(data)  {
		// TODO add a handler
		$.post('/post_player_action/', data);
		
		// backend returns a string describing the result
		// room contents may be updated
		// player inventory may be updated
		// (these all should be pushed here)
	}
	
	this.postTakeItem = function(data)  {
		$.post('/post_take_item/', data, function(serverdata)  {
			manager.updateSelf(serverdata);
			displayInventory(null);
		}, 'json');
	}
}
