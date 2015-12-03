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
		patt: /^\s*(go|move|walk)?\s+(east|west|south|north)\s*$/,
		ind: 2,
		func: goThroughDoor
	},
	{
		name: "go through",
		patt: /^\s*(go\s+through|enter|use|open)\s+(east|west|south|north)\s+door\s*$/,
		ind: 2,
		func: goThroughDoor
	},
	{
		name: "examine",
		patt: /^\s*(examine|check|look at)\s+(.+)\s*$/,
		ind: 2,
		func: examineItem
	},
	{
		name: "inventory",
		patt: /^\s*(check )?inventory\s*$/,
		ind: 0,
		func: displayInventory
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
		
		// iterate again b/c of slightly different function behaviour
		pattList = this.roomItemPatterns;
		for (i = 0; i < pattList.length; i++)  {
			var match = pattList[i].patt.exec(s);
			if (match == null)  continue;
			// execute action & tell server
			displayResponse(pattList[i].message);
			manager.postPlayerAction({
				ref: pattList[i].ref
				});
			return;
		}
		
		displayResponse("I don't know what you mean.");
		return;
	}
	//var patt = new RegExp("string", "i"); // returns /string/i
	
	// patterns from server will be added
	this.addItemUses = function(items)  {
		this.roomItemPatterns = [];  // clear patterns whenever room is updated
		
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
	var doors = manager.roomDoors;
	var d = doors[dir];
	if (d)  {
		if (d.locked)  {
			displayResponse("The " + dir + " door is locked.");
		}
		else  {
			manager.postChangeRoom({ 'room': d.next_room });
		}
	}
	else  {
		displayResponse("There's no door, just a wall.");
	}
}

function takeItem(item)  {
	// check room items
	// possible results:
	// "There isn't any [item] here."
	// "You physically can't pick the [item] up, but you can examine it."
	// "You take the [item]."
	var items = manager.roomItems;
	for (i = 0; i < items.length; i++)  {
		if (item == items[i].name.toLowerCase())  {
			if (item.type == "pickupableAndUsable")  {
				displayResponse("You take the " + item + ".");
				manager.postTakeItem({ "name": item });
			}
			else  {
				displayResponse("You can't physically pick the " + item 
					+ " up, but you can examine it.");
			}
			return;
		}
	}
	
	displayResponse("There isn't any " + item + " here.");
}

function examineItem(item)  {
	// TODO: check room items AND inventory
	var items = manager.roomItems.concat(manager.inventory);
	for (i = 0; i < items.length; i++)  {
		if (item == items[i].name.toLowerCase())  {
			displayResponse(items[i].examineDescription);
			return;
		}
	}
	displayResponse("What " + item + "?");
}

function displayInventory(data)  {  // dummy parameter
	var inventory = manager.inventory;
	if (inventory.length > 0)  {
		displayResponse("You have:");
		for (i = 0; i < inventory.length; i++)  {
			displayResponse(" * " + inventory[i].enterRoomDescription);
		}
	}
	else  {
		displayResponse("Your inventory is empty.");
	}
}
