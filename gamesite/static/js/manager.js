function GameManager()  {
	this.currentRoom;
	this.roomItems;
	this.roomDoors;
	this.inventory;
	
	// returns a room object with description fields, room contents,
	// doors, etc.
	this.getRoom = function()  {
		$.get('/get_current_room/', function(data) {
			console.log(data)
			manager.updateSelf(data);
			manager.printRoom();
			manager.updateTitle();
			
			parser.addRoomItems(manager.roomItems); // TODO also inventory items
			
			$("#commandUserInput").focus();
		}, "json");
	}
	
	this.updateSelf = function(data)  {
		this.currentRoom = data.room;
		this.roomItems = this.currentRoom.items;
		this.roomDoors = this.currentRoom.doors;
		this.inventory = data.inventory;
		
	}
	
	// print the room description & its contents to the terminal
	this.printRoom = function()  {
		var room = this.currentRoom;
		// TODO if it's not illuminated, the player can't see anything
	
		// TODO make special functions to list the items
		displayResponse(room.desc_header);
		for (i = 0; i < room.items.length; i++)  {
			displayResponse(" * " + room.items[i].enterRoomDescription);
		}
		displayResponse(room.desc_footer);
	}
	
	this.updateTitle = function()  {
		$("#pinnedText").html(this.currentRoom.title);

	}

	this.postChangeRoom = function(data)  {
		$.post('/post_change_room/', data, function(serverdata)  {
			manager.updateSelf(serverdata);
			
			manager.printRoom();
			manager.updateTitle();
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
	
}
