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
		name: "examine room",
		patt: /^\s*(examine\s+room)|look\s*$/,
		ind: 0,
		func: examineRoom
	},
	{
		name: "examine door",
		patt: /^\s*examine\s+(east|west|south|north)\s+door\s*$/,
		ind: 1,
		func: examineDoor
	},
	{
		name: "examine",
		patt: /^\s*examine\s+(.+)\s*$/,
		ind: 1,
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
			useItem(pattList[i]);
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
					type: items[i].type,
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

function useItem(item)  {
	if (item.type == "pickupableAndUsable")  {
		// item must be in inventory
		for (i = 0; i < manager.inventory.length; i++)  {
			if (item.name == manager.inventory[i].name)  {
				displayResponse(item.message);
				manager.postPlayerAction({
					ref: item.ref
				});
				return;
			}
		}
		displayResponse("You need to be holding the " + item.name);
	}
	else  {
		displayResponse(item.message);
		manager.postPlayerAction({
			ref: item.ref
		});
	}
}

function takeItem(item)  {
	var items = manager.roomItems;
	for (i = 0; i < items.length; i++)  {
		if (item == items[i].name.toLowerCase())  {
			if (items[i].type == "pickupableAndUsable")  {
				//displayResponse("You take the " + item + ".");
				manager.postTakeItem({ "name": item });  // prints the inventory
			}
			else  {
				displayResponse("You can't pick the " + item 
					+ " up, but you can examine it.");
			}
			return;
		}
	}
	items = manager.inventory;
	for (i = 0; i < items.length; i++)  {
		if (item == items[i].name.toLowerCase())  {
			displayResponse("You're already holding the " + item + ".");
			return;
		}
	}
	
	displayResponse("There isn't any " + item + " here.");
}

function examineItem(item)  {
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
		printItemList(manager.inventory, function(item)  { 
			var name = item.name;
			var article = "aeio".indexOf(name.charAt(0)) >= 0 ? "an " : "a ";
			return article + name;
		});
	}
	else  {
		displayResponse("Your inventory is empty.");
	}
}

function examineRoom(data)  {
	manager.printRoom();
}

function examineDoor(dir)  {
	var doors = manager.roomDoors;
	var d = doors[dir];
	if (d)  {
		if (d.locked)  {
			displayResponse("The " + dir + " door is locked.");
		}
		else  {
			displayResponse("The " + dir + " door is unlocked.");
		}
	}
	else  {
		displayResponse("There's no door, just a wall.");
	}
}
