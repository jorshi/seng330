function GameManager()  {
	this.currentRoom;
	this.inventory;
	
	// returns a room object with description fields, room contents,
	// doors, etc.
	this.getRoom = function()  {
		$.get('/get_current_room/', function(data) {
			manager.currentRoom = data;
			$("#pinnedText").html(data.title);
			printRoom(data);
			
			parser.addRoomItems(data.items);
			
			$("#commandUserInput").focus();
		}, "json");
	}
	
	
}

/* script.js */
var parser, manager;

$(function()  {
	manager = new GameManager();
	parser = new Parser();
	manager.getRoom();
	//getInventory();
	
});



// print the room description & its contents to the terminal
function printRoom(room)  {
	// TODO if it's not illuminated, the player can't see anything
	
	// TODO make special functions to list the items
	displayResponse(room.desc_header);
	for (i = 0; i < room.items.length; i++)  {
		displayResponse(" * " + room.items[i].enterRoomDescription);
	}
	displayResponse(room.desc_footer);
}

// returns a list of player's inventory items
function getInventory()  {
	
}

// tells the backend the player picked up an item
function postInventoryChange()  {
	
}

// tells the backend the player used an item
function postPlayerAction(data)  {
	displayResponse("POSTing action " + data.ref);
	// TODO add a handler
	$.post('/post_player_action/', data);
	
	// backend returns a string describing the result
	// room contents may be updated
	// player inventory may be updated
	// (these all should be pushed here)
}

// tells the backend the player went through a door
function postRoomChange(room)  {
	// if successful/unsuccessful
}


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
	this.roomItemPatterns = [];
	

	this.check = function(s)  {
		s = s.toLowerCase();
		
		var pattList = this.patterns;
		for (i = 0; i < pattList.length; i++)  {
			var match = pattList[i].patt.exec(s);
			if (match == null)  continue;
			var value = match[pattList[i].ind];
			// execute corresponding function
			var f = pattList[i].func;
			f(value);
			return;
		}
		// TODO check roomItemPatterns
		// (calls postPlayerAction with the reference number
		// and prints out message)
		pattList = this.roomItemPatterns;
		for (i = 0; i < pattList.length; i++)  {
			var match = pattList[i].patt.exec(s);
			if (match == null)  continue;
			displayResponse(pattList[i].message);
			postPlayerAction({
				name: pattList[i].name,
				ref: pattList[i].ref
				});
			return;
		}
		
		displayResponse("I don't know what you mean.");
		return;
	}
	//var patt = new RegExp("string", "i"); // returns /string/i
	
	// patterns from server will be added
	this.addRoomItems = function(items)  {
		for (i = 0; i < items.length; i++)  {
			for (j = 0; j < items[i].useCases.length; j++)  {
				var useCase = items[i].useCases[j];
				this.roomItemPatterns.push({
					name: items[i].name,
					patt: new RegExp(useCase.usePattern, ""),
					message: useCase.useMessage,
					ref: useCase.ref
				});
			}
		}
	}
}

function goThroughDoor(dir)  {
	// check doors object
	displayResponse("You try to go through the " + dir + " door.");
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
	// TODO: check room items AND inventory
	var items = manager.currentRoom.items;
	for (i = 0; i < items.length; i++)  {
		if (item == items[i].name.toLowerCase())  {
			displayResponse(items[i].examineDescription);
			return;
		}
	}
	displayResponse("What " + item + "?");
}



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

	