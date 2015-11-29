/* script.js */
var inventory, currentRoom, parser;
$(function()  {
	getRoom();
	getInventory();
	
	/*parser class*/
	parser = new Parser();

	/* TODO: use currentRoom's fields to update HTML 
	if it's not illuminated, the player can't do much. */
	
	
	/*
	currentRoom.updateDescription();
	displayResponse("How would you like to proceed?");
	$("#pinnedText").html(player.currentRoom.description);
	*/
	
});

// returns a room object with description fields, room contents,
// doors, etc.
function getRoom()  {
	$.get('/get_current_room/', function(data) {
		displayResponse("Got current room.");
		currentRoom = data;
	});
}

// returns a list of player's inventory items
function getInventory()  {
	
}

// tells the backend the player picked up an item
function postInventoryChange()  {
	
}

// tells the backend the player used an item
function postPlayerAction()  {
	
	// backend returns a string describing the result
	// room contents may be updated
}

// tells the backend the player went through a door
function postRoomChange(room)  {
	// if successful/unsuccessful
}

/* extraClasses.js */
// Room()

//Player()
	// changeRoom()
	
//Inventory()


/* parser.js */
function Parser()  {
	this.patterns = [
	{
		name: "take item",
		patt: /^\s*(get|grab|take|pick\s*up)\s+(.+)\s*$/,
		ind: 2,
		func: takeItem
	},
	{
		name: "go",
		patt: /^\s*(go|move|walk)\s+(east|west|south|north)\s*$/,
		ind: 2,
		func: goThroughDoor
	},
	{
		name: "go through",
		patt: /^\s*(go\s*through|enter|use|open)\s+(east|west|south|north)\s+door\s*$/,
		ind: 2,
		func: goThroughDoor
	},
	{
		name: "examine",
		patt: /^\s*(examine|check|look at)\s+(.+)\s*$/,
		ind: 2,
		func: examineItem
	}
	];
	// patterns from server will be added

	this.check = function(s)  {
		s = s.toLowerCase();
		for (i = 0; i < this.patterns.length; i++)  {
			var match = this.patterns[i].patt.exec(s);
			if (match == null)  continue;
			var value = match[this.patterns[i].ind];
			// execute corresponding function
			var f = this.patterns[i].func;
			f(value);
			return;
		}
		displayResponse("I don't know what you mean.");
		return;
	}
	//var patt = new RegExp("string", "i"); // returns /string/i
}

function goThroughDoor(dir)  {
	// check doors object
	displayResponse("You try to go through the " + doorDirection + " door.");
}

function takeItem(item)  {
	// check room items
	// possible results:
	// "There isn't any [item] here."
	// "You physically can't pick the [item] up, but you can examine it."
	// "You take the [item]."
	displayResponse("You try to take the " + item + ".");
}

function examineItem(item)  {
	// check room items AND inventory
	// possible results:
	// "What [item]?"
	// [display item examine text]
	displayResponse("You examine the " + item + ".");
}


/* item.js - Item classes & subclasses */
// a list of all the possible properties:
/*
 * name
 * description
 * enterRoomDescription
 * hidden bool
 * usePattern regex
 * inInv bool
 * useMessage
 * locked
 * room1
 * room2
*/

/* gameState.js - example gamestate changes */

/* functions.js - checkers */
// itemIsInRoomOrInv() - checks if item is in room, inventory, or both
// form handler for terminal
$("#commandForm").submit(function(event)  {
	event.preventDefault();
	parse();
 });
 
 // Function called upon submit button being pressed
function parse() {
	//clear form after submitting text
	var enteredCommand = commandForm.command.value;
	$("#commandUserInput").val('');

	if (enteredCommand != "")  {
		//echo command
		$("#terminalText").append("<p class=\"echo\">" + enteredCommand + "</p>");

		//parse command, print whether or not the command is valid
		parser.check(enteredCommand);
	}
}

function displayResponse(s)  {
	$("#terminalText").append("<p class=\"response\">" + s + "</p>");
	//scroll down chat window
	$("#terminalText").scrollTop($("#terminalText")[0].scrollHeight);
}

//function mapUpdate(currentRoom)
/*TODO: create an update_room function*/
 	/* this function should fetch the room the player
 	   is supposed to be in from the database and
 	   the room's inventory */

	/*TODO: create an update_player function*/
	/* this function should fetch the player's
 	   inventory from the database */

 	/*TODO: create an update_inventory_pickup function*/
 	/* this moves the item from the room inventory to the
 	   player inventory and updates the database with this
 	   new information*/

 	/* TODO: create a gamestate_change function */
 	/* this updates the gamestate in the database */
