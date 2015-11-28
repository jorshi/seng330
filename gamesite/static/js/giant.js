/* script.js */
var inventory, currentRoom, parser;
$(function()  {
	inventory = [];
	currentRoom = {};

	/*TODO: call an update_room function*/

	/*TODO: call an update_inventory function*/

	/*parser class*/
	parser = new Parser();

	currentRoom.updateDescription();
	displayResponse("How would you like to proceed?");
	$("#pinnedText").html(player.currentRoom.description);
});

/* extraClasses.js */

Room(beginDescription, endDescription) {
	
	//Building room description
	this.updateDescription = function() {
		
	}

}

//Player()
	// changeRoom()
	
//Inventory()


/* parser.js */
/*Patterns*/
pattTakeItem = /^\s*(get|grab|take|pick\s*up)\s+(\w+)\s*$/i;
pattGo = /^\s*(go|move|walk)\s+(\w*)\s*$/i;
pattExamine = /^\s*(examine|check|look at)\s+(\w*)\s*$/i;

/*door related patterns*/
pattGoThrough = /^\s*(go through|enter|use|open)\s+(east|west|south|north)\s+door\s*$/i;
pattFindDoor = /^\s*(north|south|east|west)\s+/i;

//var patt = new RegExp("string", "i"); // returns /string/i
