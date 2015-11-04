/*function that will check if an item is in a room (it will return that item if it is, else will return null)*/
function itemIsInRoomOrInv(room, inventory, name, mode) {
	/* The mode specifies if your checking the inventory, room or both
	 "r" = room, "ri" = room and inventory and "i" = inventory */
	if (mode == "r" || mode == "ri") {
		for (var i = 0; i < room.itemsInRoom.length; i++) {
			if (name == room.itemsInRoom[i].name) return room.itemsInRoom[i];
		}
	}
	if (mode == "i" || mode == "ri") {
		for (var i = 0; i < inventory.itemsInInventory.length; i++) {
			if (name == inventory.itemsInInventory[i].name) return inventory.itemsInInventory[i];
		}
	}
	return null;
}

/*this function is used for testing purposes, it will not actually be in the game*/
function printArray(a){
	for (var i = 0; i < a.length; i++) {
		alert(a[i].name);
	}	
}

 $("#commandForm").submit(function(event)  {
        event.preventDefault();
        parse();
 });

// Function called upon submit button being pressed
function parse() {
	//clear form after submitting text

	var enteredCommand = commandForm.command.value;
	$("#commandUserInput").val('');
        
        //echo command
        $("#terminalText").append("<p class=\"echo\">" + echoedCommand + "</p>");
	//parse command, print whether or not the command is valid
	if (!parser.check(enteredCommand)){
		displayResponse(enteredCommand + " is an "+ "invalid command.");
	}
        
        //return false;
}

 function displayResponse(s)  {
        $("#terminalText").append("<p class=\"response\">" + s + "</p>");
    }