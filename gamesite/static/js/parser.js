// MAX: 
/* make door traversals make sense (only have east door, north door ect.) */
/* get rid of drop command */
/* create key item and edge cases */

/*Patterns*/
pattTakeItem = /^\s*(get|grab|take|pick\s*up)\s+(\w+)\s*$/i;
pattGo = /^\s*(go|move|walk)\s+(\w*)\s*$/i;
pattExamine = /^\s*(examine|check|look at)\s+(\w*)\s*$/i;
pattDrop = /^\s*(discard|drop|throw away|throw out)\s+(\w*)\s*$/i;
pattUseOn = /^\s*(use)\s+(\w+)\s+(on|with)\s+(\w+)\s*$/i;
/*door related patterns*/
pattGoThrough = /^\s*(go through|enter|use|open)\s+(east|west|south|north)\s+(\w+)\s*$/i;
pattFindDoor = /^\s*(north|south|east|west)\s+/i;
/*Patterns for use Items*/
pattGenericUse = /^\s*(use|fire|shoot|open)\s+(\w+)\s*$/i;
pattUseItem = /^\s*(use)\s+(\w+)\s*$/i; /*Generic*/
pattShootItem = /^\s*(use|fire|shoot)\s+(\w+)\s*$/i; /*shootable*/
pattOpenItem = /^\s*(use|open)\s+(\w+)\s*$/i; /*openable*/

/*Parser Class*/
QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
  QUnit,log("test", "test","test");
});

QUnit.test('Parser()',function(assert) {
	ok(Parser("3"), 'this should not work');
})

QUnit.start();	

function Parser(player) {
	/*this.player = player;
	Parser Method to check if a command is valid or not*/
	this.check = function(s) {

		s = s.toLowerCase();
		if (this.pickUpCheck(s)) return true;
		if (this.examineCheck(s)) return true;
		if (this.goThroughCheck(s)) return true;
		if (this.useItemCheck(s)) return true;
		if (this.useItemOnCheck(s)) return true;
		if (this.dropCheck(s)) return true;

		if (s == "printroom") {
			printArray(player.currentRoom.itemsInRoom);
			return true;
		}
		return false;	
	}

	this.pickUpCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattTakeItem.exec(s);
		/*no match */
		if (match == null) return false;
		/*match[2] is string containing <item> that the user inputted*/
		itemToCheck = itemIsInRoomOrInv(player.currentRoom, player.inv, match[2], "r");

		/*now that we have the item check edge cases:*/

		/*case 1: item doesent exist*/
		if (itemToCheck == null)  {
			/*print out message saying item is not in room*/
			displayResponse("There is no " + match[2]);
			return true;
		}

		/*case 2: item is unpickupable*/
		if (itemToCheck instanceof NonPickupable) {
			displayResponse("You can not pick up the " + itemToCheck.name);
			return true;
		}

		/*now we know item must be pickupable*/
		displayResponse("You just picked up the " + itemToCheck.name);
		/*Now we have to remove the item from the room and put it into the inventory*/
		var index = player.currentRoom.itemsInRoom.indexOf(itemToCheck);
		/*confusing looking but all it does is move the item from the room to the inventory*/

		/*TODO: call a update_inventory_pickup function*/
		player.inv.itemsInInventory.push(player.currentRoom.itemsInRoom.splice(index, 1)[0]);


		itemToCheck.inInv = true;
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

		/*case 1: item doesent exist*/
		if (itemToCheck == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no " + match[2]);
			return true;
		}

		/*It must exist so examine it*/
		displayResponse(itemToCheck.description);
		return true;
	}

	/*TODO: remove this functionality */
	this.dropCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattDrop.exec(s);
		/*no match */
		if (match == null) return false;
		/*match[2] is string containing <item> that the user inputted*/
		itemToCheck = itemIsInRoomOrInv(player.currentRoom, player.inv, match[2], "i");

		/*now that we have the item check edge cases:*/

		/*case 1: item doesent exist*/
		if (itemToCheck == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no " + match[2] + " in your inventory");
			return true;
		}

		/*item is in the room, so see if it can be picked up*/
		displayResponse("You dropped the " + itemToCheck.name);
		/*Now we have to remove the item from the room and put it into the inventory*/
		var index = player.inv.itemsInInventory.indexOf(itemToCheck);
		/*confusing looking but all it does is move the item from the Inventory to the room*/
		player.currentRoom.itemsInRoom.push(player.inv.itemsInInventory.splice(index, 1)[0]);
		itemToCheck.inInv = false;
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

		/*case 1: item doesent exist*/
		if (itemToCheck == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no " + match[2]);
			return true;
		}

		/*case 2: item can't be used*/
		if (!(itemToCheck instanceof NonPickupableAndUsable) && !(itemToCheck instanceof PickupableAndUsable)) {
			displayResponse("You can not "+match[1]+" the " + itemToCheck.name);
			return true;
		}

		/*case 3: improper use of RE*/
		if (itemToCheck.usePattern.exec(s) == null) {
			displayResponse("You can not "+match[1]+" the " + itemToCheck.name);
			return true;
		}

		/*case 4: item is useable but is not in your inventory*/
		if ((itemToCheck instanceof PickupableAndUsable) && (itemToCheck.inInv == false)) {
			displayResponse("The "+match[2]+" is not in your inventory");
			return true;
		}

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
		if (itemToUse == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no " + match[2]);
			return true;
		}
		if (itemToGetUsedOn == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no " + match[4]);
			return true;
		}

		/*case 2: item can't be used*/
		if (!(itemToUse instanceof PickupableAndUsable) || (!(itemToGetUsedOn instanceof Door) && !(itemToGetUsedOn instanceof PickupableAndUsable) && !(itemToGetUsedOn instanceof NonPickupableAndUsable))) {
			displayResponse("You can not use the " + itemToUse.name + " on that");
			return true;
		}

		/*case 3: item is useable but is not in your inventory*/
		if ((itemToUse instanceof PickupableAndUsable) && (itemToUse.inInv == false)) {
			displayResponse("The "+itemToUse.name+" is not in your inventory");
			return true;
		}

		/*case 4: you try to use an item on itself*/
		if (itemToUse.name == itemToGetUsedOn.name) {
			displayResponse("You can not use the "+itemToUse.name+" on itself");
			return true;
		}
		/*TODO: case 5: you try to use a key on an unlocked door*/
		/*TODO: case 6: you try to use the wrong key on the wrong door*/

		/*the item can be used so display use message*/
		displayResponse("You try to use the " + itemToUse.name + " on the " + itemToGetUsedOn.name);
		gameState(s);
		return true;
	}

	this.goThroughCheck = function(s) {
		/*this gets the group in the RE*/
		match = pattGoThrough.exec(s);
		/*no match*/
		if (match == null) return false;

		/*now figure out if the door exists*/
		if (!(match[3] == "door")) {
			/*print out message saying item is not in room*/
			displayResponse(match[3] + " is not a door");
			return true;
		}

		/*now we have the item in the door array*/
		if (match[2] == "north") {
			itemToCheck = player.currentRoom.doorLayout[0];
		} else if (match[2] == "east") {
			itemToCheck = player.currentRoom.doorLayout[1];
		} else if (match[2] == "south") {
			itemToCheck = player.currentRoom.doorLayout[2];
		} else if (match[2] == "west") {
			itemToCheck = player.currentRoom.doorLayout[3];
		}


		/*now that we have the door check edge cases:*/

		/*case 1: door doesent exist*/
		if (itemToCheck == null) {
			/*print out message saying item is not in room*/
			displayResponse("There is no "+match[2]+" "+match[3]);
			return true;
		}

		/*case 2: the door is locked*/
		if (itemToCheck.locked) {
			displayResponse("you try to go through the "+match[2]+" "+match[3]+" but its locked");
			return true;
		}

		/*now figure out the new room*/
		if (itemToCheck.room == player.currentRoom) {
			player.changeRoom(itemToCheck.room2);

		} else {
			player.changeRoom(itemToCheck.room);
		}
		/* TODO: call an update_room function*/
		displayResponse("you went through the "+match[2]+" "+match[3]);
		player.currentRoom.updateDescription();
		displayResponse(player.currentRoom.description);
		return true;
	}
}