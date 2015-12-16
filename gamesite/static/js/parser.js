// MAX: 
/* create key item and edge cases */

/*Patterns*/
pattTakeItem = /^\s*(get|grab|take|pick\s*up)\s+(.+)\s*$/i;
pattGo = /^\s*(go|move|walk)\s+(\w+)\s*$/i;
pattExamine = /^\s*(examine|check|look at)\s+(.+)\s*$/i;
pattUseOn = /^\s*(use)\s+(.+)\s+(on|with)\s+(.+)\s*$/i;
pattUseOnDoor = /^\s*(use)\s+(\w+)\s+(on|with)\s+(east|west|south|north)\s+door\s*$/i;
/*door related patterns*/
pattGoThrough = /^\s*(go through|enter|use|open)\s+(east|west|south|north)\s+door\s*$/i;
pattGoThroughNonDirection = /^\s*(go through|enter|use|open)\s+door\s*$/i;
pattFindDoor = /^\s*(north|south|east|west)\s+/i;
/*Patterns for use Items*/
pattGenericUse = /^\s*(use|fire|shoot|open|extinguish|stamp\s+out|put\s+out|look\s+behind|lift)\s+(.+)\s*$/i;
pattUseItem = /^\s*(use)\s+(.+)\s*$/i; /*Generic*/
pattShootItem = /^\s*(use|fire|shoot)\s+(.+)\s*$/i; /*shootable*/
pattOpenItem = /^\s*(use|open)\s+(.+)\s*$/i; /*openable*/
pattUnlightItem = /^\s*(extinguish|stamp\s+out|put\s+out)\s+(.+)\s*$/i; /*openable*/


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
		if (this.useItemOnDoorCheck(s)) return true;
		if (this.useItemOnCheck(s)) return true;
		if (this.useItemCheck(s)) return true;		

		if (s == "print inventory") {
			player.inv.printInv();
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
		/*case 2: item is unpickupable*/
		if (cantBePickedUp(itemToCheck)) return true;
		/*cases passed item can be picked up!*/
		moveToInventory(itemToCheck);

		updateRoomDescription();	
		$("#pinnedText").html(player.currentRoom.description);

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
		/*case 2: item can't be used*/
		if (cantBeUsed(itemToCheck,match[1])) return true;
		/*case 3: improper use of RE*/
		if (wrongVerbInputed(itemToCheck, match[1],s)) return true;
		/*case 4: item is useable but is not in your inventory*/
		if (notInInventory(itemToCheck)) return true;
		/*the item can be used so display use message*/

		displayResponse(itemToCheck.useMessage);
		changeItemState(itemToCheck);
		//gameState(s);
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
		if (doesNotExist(itemToGetUsedOn,match[4])) return true;
		/*case 2: item can't be used on that item*/
		if (cantBeUsedOn(itemToUse,itemToGetUsedOn)) return true;
		/*case 3: item is useable but is not in your inventory*/
		if (notInInventory(itemToUse)) return true;
		/*case 4: you try to use an item on itself*/
		if (useOnSelf(itemToUse,itemToGetUsedOn)) return true;
		/*the item can be used so display use message*/
		displayResponse(itemToUse.useMessage);

		changeStateOfItemUsedOn(itemToUse,itemToGetUsedOn);
		//gameState(s);
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
		/*case 2: there is no door on the wall*/
		doorToCheck = getDoor(doorDirection);
		if (doesNotExist(doorToCheck,doorDirection+" door")) return true;
		/*case 3: item is useable but is not in your inventory*/
		if (notInInventory(itemToUse)) return true;
		/*case 4: item isnt a key*/
		if (itemIsNotKey(itemToUse,doorToCheck)) return true;
		
		/*case 5: you try to use a key on an unlocked door*/
		if (doorAlreadyUnlocked(doorToCheck,doorDirection)) return true;
		/*TODO: case 6: you try to use the wrong key on the wrong door*/
		/*the item can be used so display use message*/
		displayResponse(itemToUse.useMessage);
		//gameState(s);
		changeStateOfItemUsedOn(itemToUse,doorToCheck);
		return true;
	}

	this.goThroughCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattGoThroughNonDirection.exec(s);
		if (match != null) {
			displayResponse("You need to specify a direction.");
			return true;
		}
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
		displayResponse("You went through the "+doorDirection+" door.");
		updateRoomDescription();
		$("#pinnedText").html(player.currentRoom.description);
		//mapUpdate(player.currentRoom);

		return true;
	}

	/*EDGE CASE FUNCTIONS*/
	doesNotExist = function(item, name) {
		if (name == 'door') {
			displayResponse("You need to specify a direction.");
			return true;
		}
		if (item == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no "+name+".");
			return true;
		}
	}

	cantBePickedUp = function(item) {
		if (item instanceof NonPickupable) {
			displayResponse("You cannot pick up the " + item.name+".");
			return true;
		}
	}

	cantBeUsed = function(item, verb) {
		if (!(item instanceof NonPickupableAndUsable) && !(item instanceof PickupableAndUsable)) {
			displayResponse("You cannot "+verb+" the " + item.name+ ".");
			return true;
		}
	}

	wrongVerbInputed = function(item, verb, s) {
		if (item.usePattern.exec(s) == null) {
			displayResponse("You cannot "+verb+" the " + item.name+ ".");
			return true;
		}
	}

	notInInventory = function(item) {
		if ((item instanceof Pickupable) && (item.inInv == false)) {
			displayResponse("The "+item.name+" is not in your inventory.");
			return true;
		}
	}

	cantBeUsedOn = function(itemToUse,itemToGetUsedOn) {
		if (!(itemToUse instanceof PickupableAndUsable) || (!(itemToGetUsedOn instanceof Door) && !(itemToGetUsedOn instanceof PickupableAndUsable) && !(itemToGetUsedOn instanceof NonPickupableAndUsable))) {
			displayResponse("You cannot use the " + itemToUse.name + " on the"+itemToGetUsedOn.name+".");
			return true;
		}
		if (!(itemToUse.usedOn == itemToGetUsedOn.name)) {
			displayResponse("You cannot use the " + itemToUse.name + " on the"+itemToGetUsedOn.name+".");
			return true;
		}
	}

	useOnSelf = function(itemToUse,itemToGetUsedOn) {
		if (itemToUse.name == itemToGetUsedOn.name) {
			displayResponse("You cannot use the "+itemToUse.name+" on itself.");
			return true;
		}
	}

	itemIsNotKey = function(item, itemToGetUsedOn) {
		if (!(item instanceof PickupableAndUsable)) {
			displayResponse("You cannot use the " + item.name + " on that.");
			return true;
		}
		if (!(item.usedOn == itemToGetUsedOn.name)) {
			displayResponse("You cannot use the " + item.name + " on the"+itemToGetUsedOn.name+".");
			return true;
		}
	}

	doorAlreadyUnlocked = function(doorToCheck, doorDirection) {
		if (doorToCheck.locked == false) {
			displayResponse("The "+doorDirection+" door is unlocked already.");
			return true;
		}
	}

	doorIsLocked = function(doorToCheck, doorDirection) {
		if (doorToCheck.locked) {
			displayResponse("You try to go through the "+doorDirection+" door, but it's locked.");
			return true;
		}
	}


	/*OTHER FUNCTIONS*/
	moveToInventory = function(item) {
		/*now we know item must be pickupable*/
		displayResponse("You just picked up the " + item.name+".");
		/*Now we have to remove the item from the room and put it into the inventory*/
		$.post('/post_take_item/', {"name" : item.name}, function(serverdata)  {
			getState(serverdata);
		}, 'json');


	}

	updateRoomDescription = function() {
		player.currentRoom.updateDescription();
	}

	moveRoom = function(doorToCheck) {
		$.post('/post_change_room/', {'room' : doorToCheck.nextRoomName}, function(serverdata)  {
			getState(serverdata);
			displayResponse("How would you like to proceed?");
		}, 'json');
	}
	changeItemState = function(itemToCheck) {
		$.post('/post_player_action/', {'name':itemToCheck.name}, function(serverdata)  {
			getState(serverdata);
		}, 'json');
	}
	changeStateOfItemUsedOn = function(itemToCheck,itemToCheck2) {
		$.post('/post_player_action/', {'name':itemToCheck.name, 'name2':itemToCheck2.name}, function(serverdata)  {
			getState(serverdata);
		}, 'json');
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