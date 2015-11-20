// MAX: 
/* create key item and edge cases */

/*Patterns*/
pattTakeItem = /^\s*(get|grab|take|pick\s*up)\s+(\w+)\s*$/i;
pattGo = /^\s*(go|move|walk)\s+(\w*)\s*$/i;
pattExamine = /^\s*(examine|check|look at)\s+(\w*)\s*$/i;
pattDrop = /^\s*(discard|drop|throw away|throw out)\s+(\w*)\s*$/i;
pattUseOn = /^\s*(use)\s+(\w+)\s+(on|with)\s+(\w+)\s*$/i;
pattUseOnDoor = /^\s*(use)\s+(\w+)\s+(on|with)\s+(east|west|south|north)\s+door\s*$/i;
/*door related patterns*/
pattGoThrough = /^\s*(go through|enter|use|open)\s+(east|west|south|north)\s+door\s*$/i;
pattFindDoor = /^\s*(north|south|east|west)\s+/i;
/*Patterns for use Items*/
pattGenericUse = /^\s*(use|fire|shoot|open)\s+(\w+)\s*$/i;
pattUseItem = /^\s*(use)\s+(\w+)\s*$/i; /*Generic*/
pattShootItem = /^\s*(use|fire|shoot)\s+(\w+)\s*$/i; /*shootable*/
pattOpenItem = /^\s*(use|open)\s+(\w+)\s*$/i; /*openable*/


/*Parser Class*/

function Parser(player) {
	/*this.player = player;
	Parser Method to check if a command is valid or not*/
	this.check = function(s) {
		//scroll down chat window
		$('#terminalText').scrollTop(1000000);

		s = s.toLowerCase();
		if (this.pickUpCheck(s)) return true;
		if (this.examineCheck(s)) return true;
		if (this.goThroughCheck(s)) return true;
		if (this.useItemCheck(s)) return true;
		if (this.useItemOnCheck(s)) return true;
		if (this.useItemOnDoorCheck(s)) return true;

		if (s == "printroom") {
			printArray(player.currentRoom.itemsInRoom);
			return true;
		}
		return false;	
	}

	this.pickUpCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattTakeItem.exec(s);
		/*no match*/
		if (match == null) return false;
		/*match[2] is string containing <item> that the user inputted*/
		itemToCheck = itemIsInRoomOrInv(player.currentRoom, player.inv, match[2], "r");
		/*now that we have the item check edge cases:*/
		/*case 1: item doesent exist or is hidden*/
		if (doesNotExist(itemToCheck,match[2])) return true;
		if (isHidden(itemToCheck,match[2])) return true;
		/*case 2: item is unpickupable*/
		if (cantBePickedUp(itemToCheck)) return true;
		/*cases passed item can be picked up!*/
		moveToInventory(itemToCheck);
		updateRoomDescription();	
		return true;		
	}

	this.examineCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattExamine.exec(s);
		/*no match */
		if (match == null) return false;
		/*match[2] is string containing <item> that the user inputted*/
		itemToCheck = itemIsInRoomOrInv(player.currentRoom, player.inv, match[2], "ri");
		/*now that we have the item check edge cases:*/
		/*case 1: item doesent exist or is hidden*/
		if (doesNotExist(itemToCheck,match[2])) return true;
		if (isHidden(itemToCheck,match[2])) return true;
		/*It must exist so examine it*/
		displayResponse(itemToCheck.description);
		return true;
	}

	/*parser method to use an item*/
	this.useItemCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattGenericUse.exec(s);
		/*no match*/
		if (match == null) return false;
		/*match[2] is string containing <item> that the user inputted*/
		itemToCheck = itemIsInRoomOrInv(player.currentRoom, player.inv, match[2], "ri");
		/*now that we have the item check edge cases:*/
		/*case 1: item doesent exist or is hidden*/
		if (doesNotExist(itemToCheck,match[2])) return true;
		if (isHidden(itemToCheck,match[2])) return true;
		/*case 2: item can't be used*/
		if (cantBeUsed(itemToCheck,match[1])) return true;
		/*case 3: improper use of RE*/
		if (wrongVerbInputed(itemToCheck, match[1])) return true;
		/*case 4: item is useable but is not in your inventory*/
		if (notInInventory(itemToCheck)) return true;
		/*the item can be used so display use message*/
		displayResponse(itemToCheck.useMessage);
		gameState(s);
		return true;
	}

	/*parser method to use an item*/
	this.useItemOnCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattUseOn.exec(s);
		/*no match*/
		if (match == null) return false;
		/*match[2] is string containing <item> that the user inputted*/
		itemToUse = itemIsInRoomOrInv(player.currentRoom, player.inv, match[2], "ri");
		itemToGetUsedOn = itemIsInRoomOrInv(player.currentRoom, player.inv, match[4], "ri");
		/*now that we have the item check edge cases:*/
		/*case 1: item doesent exist*/
		if (doesNotExist(itemToUse,match[2])) return true;
		if (isHidden(itemToUse,match[2])) return true;
		if (doesNotExist(itemToGetUsedOn,match[2])) return true;
		if (isHidden(itemToGetUsedOn,match[2])) return true;
		/*case 2: item can't be used on that item*/
		if (cantBeUsedOn(itemToUse,itemToGetUsedOn)) return true;
		/*case 3: item is useable but is not in your inventory*/
		if (notInInventory(itemToUse)) return true;
		/*case 4: you try to use an item on itself*/
		if (useOnSelf(itemToUse,itemToGetUsedOn)) return true;
		/*the item can be used so display use message*/
		displayResponse("You try to use the " + itemToUse.name + " on the " + itemToGetUsedOn.name);
		gameState(s);
		return true;
	}

	/*parser method to use a key on a door*/
	this.useItemOnDoorCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattUseOnDoor.exec(s);
		/*no match*/
		if (match == null) return false;
		/*match[2] is string containing <item> that the user inputted
		  match[4] is the wall that the door is on (east,south, ect.)*/
		itemToUse = itemIsInRoomOrInv(player.currentRoom, player.inv, match[2], "ri");
		doorDirection = match[4];
		/*now that we have the item check edge cases:*/
		/*case 1: item doesent exist*/
		if (doesNotExist(itemToUse,match[2])) return true;
		if (isHidden(itemToUse,match[2])) return true;
		/*case 2: there is no door on the wall*/
		doorToCheck = getDoor(doorDirection);
		if (doesNotExist(doorToCheck,doorDirection+" door")) return true;
		/*case 3: item isnt a key*/
		if (itemIsNotKey(itemToUse)) return true;
		/*case 4: item is useable but is not in your inventory*/
		if (notInInventory(itemToUse)) return true;
		/*case 5: you try to use a key on an unlocked door*/
		if (doorAlreadyUnlocked(doorToCheck,doorDirection)) return true;
		/*TODO: case 6: you try to use the wrong key on the wrong door*/
		/*the item can be used so display use message*/
		displayResponse("You try to use the "+itemToUse.name+" on the "+doorDirection+"door");
		gameState(s);
		return true;
	}

	this.goThroughCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattGoThrough.exec(s);
		/*no match*/
		if (match == null) return false;
		doorDirection = match[2];
		/*now we have the item in the door array*/
		doorToCheck = getDoor(doorDirection);
		/*now that we have the door check edge cases:*/
		/*case 1: door doesent exist*/
		if (doesNotExist(doorToCheck,doorDirection+" door")) return true;
		/*case 2: the door is locked*/
		if (doorIsLocked(doorToCheck,doorDirection)) return true;
		/*now figure out the new room*/
		moveRoom(doorToCheck);
		/* TODO: call an update_room function*/
		displayResponse("you went through the "+doorDirection+" door");
		updateRoomDescription();
		$("#pinnedText").html(player.currentRoom.description);
		mapUpdate(player.currentRoom);
		return true;
	}

	/*EDGE CASE FUNCTIONS*/
	doesNotExist = function(item, name) {
		if (item == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no "+name);
			return true;
		}
	}

	isHidden = function(item, name) {
		if (item.hidden == true) {
			/*print out message saying item is not in room*/
			displayResponse("There is no "+name);
			return true;
		}
	}

	cantBePickedUp = function(item) {
		if (item instanceof NonPickupable) {
			displayResponse("You can not pick up the " + item.name);
			return true;
		}
	}

	cantBeUsed = function(item, verb) {
		if (!(item instanceof NonPickupableAndUsable) && !(item instanceof PickupableAndUsable)) {
			displayResponse("You can not "+verb+" the " + item.name);
			return true;
		}
	}

	wrongVerbInputed = function(item, verb) {
		if (item.usePattern.exec(s) == null) {
			displayResponse("You can not "+verb+" the " + item.name);
			return true;
		}
	}

	notInInventory = function(item) {
		if ((item instanceof PickupableAndUsable) && (item.inInv == false)) {
			displayResponse("The "+item.name+" is not in your inventory");
			return true;
		}
	}

	cantBeUsedOn = function(itemToUse,itemToGetUsedOn) {
		if (!(itemToUse instanceof PickupableAndUsable) || (!(itemToGetUsedOn instanceof Door) && !(itemToGetUsedOn instanceof PickupableAndUsable) && !(itemToGetUsedOn instanceof NonPickupableAndUsable))) {
			displayResponse("You can not use the " + itemToUse.name + " on that");
			return true;
		}
	}

	useOnSelf = function(itemToUse,itemToGetUsedOn) {
		if (itemToUse.name == itemToGetUsedOn.name) {
			displayResponse("You can not use the "+itemToUse.name+" on itself");
			return true;
		}
	}

	itemIsNotKey = function(item) {
		if (!(item instanceof Key)) {
			displayResponse("You can not use the " + item.name + " on that");
			return true;
		}
	}

	doorAlreadyUnlocked = function(doorToCheck, doorDirection) {
		if (doorToCheck.locked == false) {
			displayResponse("The "+doorDirection+" door is unlocked already");
			return true;
		}
	}

	doorIsLocked = function(doorToCheck, doorDirection) {
		if (doorToCheck.locked) {
			displayResponse("you try to go through the "+doorDirection+" door but its locked");
			return true;
		}
	}


	/*OTHER FUNCTIONS*/
	moveToInventory = function(item) {
		/*now we know item must be pickupable*/
		displayResponse("You just picked up the " + item.name);
		/*Now we have to remove the item from the room and put it into the inventory*/
		var index = player.currentRoom.itemsInRoom.indexOf(item);
		/*confusing looking but all it does is move the item from the room to the inventory*/

		/*TODO: call a update_inventory_pickup function*/
		player.inv.itemsInInventory.push(player.currentRoom.itemsInRoom.splice(index, 1)[0]);
		itemToCheck.inInv = true;
	}

	updateRoomDescription = function() {
		player.currentRoom.updateDescription();
	}

	moveRoom = function(doorToCheck) {
		if (doorToCheck.room == player.currentRoom) {
			player.changeRoom(doorToCheck.room2);
		} else {
			player.changeRoom(doorToCheck.room);
		}
	}

	getDoor = function(doorDirection) {
		if (doorDirection == "north") {
			return player.currentRoom.doorLayout[0];
		} else if (doorDirection == "east") {
			return player.currentRoom.doorLayout[1];
		} else if (doorDirection == "south") {
			return player.currentRoom.doorLayout[2];
		} else if (doorDirection == "west") {
			return player.currentRoom.doorLayout[3];
		}
	}

}