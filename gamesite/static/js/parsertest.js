    // Patterns (this is the one for picking up items)
     pattTakeItem = /^\s*(get|grab|take|pick\s*up)\s+(\w+)\s*$/i;

     pattUseItem = /^\s*(use)\s+(\w+)\s*$/i;

     pattGo = /^\s*(go|move|walk)\s+(\w*)\s*$/i;

     pattExamine = /^\s*(examine|check|look at)\s+(\w*)\s*$/i;

     pattDrop = /^\s*(discard|drop|throw away|throw out)\s+(\w*)\s*$/i;


	 
	// function that will check if an item is in a room (it will return that item if it is, else will return null)
	function itemIsInRoomOrInv(name, mode) {
		/* The mode specifies if your checking the inventory, room or both
		 "r" = room, "ri" = room and inventory and "i" = inventory */
		if (mode == "r" || mode == "ri") {
			for (var i = 0; i < itemsInRoom.length; i++) {
				if (name == itemsInRoom[i].name) return itemsInRoom[i];
			}
		}
		if (mode == "i" || mode == "ri") {
			for (var i = 0; i < itemsInInventory.length; i++) {
				if (name == itemsInInventory[i].name) return itemsInInventory[i];
			}
		}
		return null;
	}
	// print out the list of items in room (used for error checking)
	function printRoom(){
		for (var i = 0; i < itemsInRoom.length; i++) {
			alert(itemsInRoom[i].name);
		}	
	}
	
	//Array of all the items in the room (might want to put this in a room class later)
	var itemsInRoom = [];
	//Array of all the items in your Inventory (might want to make this its own class later)
	var itemsInInventory = [];
	
	
	function Item(name, description, useMessage, canBePickedUp, canBeUsed, needsToBeInInvForUse) {
		//strings
		this.name = name;
		this.description = description;
		this.useMessage = useMessage;
		// booleans
		this.canBePickedUp = canBePickedUp;
		this.canBeUsed = canBeUsed;
		this.needsToBeInInvForUse = needsToBeInInvForUse;
		inInv = false;
		//adds a new item into the room array when the item is created
		itemsInRoom.push(this);
	}


    // Parser Class
	function Parser() {}

	// Parser Method to check if a command is valid or not
	Parser.prototype.check = function(s) {
		
		if (pickUpCheck(s)) return true;					
		if (useItemCheck(s)) return true;
		if (examineCheck(s)) return true;		
		if (dropCheck(s)) return true;	

		// just for error checking	
		if (s == "printroom") {
			printRoom();
			return true
		}

		return false;	// Not a valid command




		
		// Parser Method to check for an item that is to be picked up
		function pickUpCheck(s){
			// this gets the group in the RE
			match = pattTakeItem.exec(s);
			if (match == null){
				return false;
			}

			// match[2] is string containing <item> that the user inputted
			itemToCheck = itemIsInRoomOrInv(match[2],"r");
			// checks if item is in the room
			if (itemToCheck != null){
				// item is in the room, so see if it can be picked up
				if (itemToCheck.canBePickedUp == true){
					$("body").append("You just picked up the " + itemToCheck.name + "<br>");
					// Now we have to remove the item from the room and put it into the inventory
					var index = itemsInRoom.indexOf(itemToCheck);
					// confusing looking but all it does is move the item from the room to the inventory
					itemsInInventory.push(itemsInRoom.splice(index, 1)[0]);
					itemToCheck.inInv = true;
					return true;
				} else {
					$("body").append("You can not pick up the " + itemToCheck.name + "<br>");
					return true;
				}
			} else {
				$("body").append("There is no " + match[2] + "<br>");
				return true;

			}

		}




		// Parser Method to drop an item
		function dropCheck(s){
			// this gets the group in the RE
			match = pattDrop.exec(s);
			if (match == null){
				return false;
			}
			// match[2] is string containing <item> that the user inputted
			itemToCheck = itemIsInRoomOrInv(match[2],"i");
			// checks if item is in the room
			if (itemToCheck != null){
				// item is in the room, so see if it can be picked up
				$("body").append("You dropped the " + itemToCheck.name + "<br>");
				// Now we have to remove the item from the room and put it into the inventory
				var index = itemsInInventory.indexOf(itemToCheck);
				// confusing looking but all it does is move the item from the Inventory to the room
				itemsInRoom.push(itemsInInventory.splice(index, 1)[0]);
				itemToCheck.inInv = false;
				return true;
			} else {
				$("body").append("There is no " + match[2] + " in your inventory" + "<br>");
				return true;

			}
		}




		// Parser Method to Examine an item
		function examineCheck(s){
			// this gets the group in the RE
			match = pattExamine.exec(s);
			if (match == null){
				return false;
			}
			// match[2] is string containing <item> that the user inputted
			itemToCheck = itemIsInRoomOrInv(match[2],"ri");
			// checks if item is in the room
			if (itemToCheck != null){
				// item is in the room, so see if it can be picked up
				$("body").append(itemToCheck.description + "<br>");
				return true;
			} else {
				$("body").append("There is no " + match[2] + "<br>");
				return true;

			}
		}




		// parser method to use an item
		function useItemCheck(s){
			//populate RE
			match = pattUseItem.exec(s);

			if (match == null){
				return false;
			}

			itemToCheck = itemIsInRoomOrInv(match[2],"ri");

			if(itemToCheck != null){
				// first check if the ifem can be used
				if (itemToCheck.canBeUsed == true) {
					// if the item doesent need to be in your inventory to be used
					if (itemToCheck.needsToBeInInvForUse == false) {
						// in case we want a custom message when the item is used
						if (itemToCheck.useMessage == null) {
							$("body").append("You just used the " + itemToCheck.name + "<br>");
							return true;
						} else {
							$("body").append(itemToCheck.useMessage + "<br>");
							return true;
						}
					// the item needs to be in your inventory to be used so check if in inventory
					} else if (itemToCheck.inInv == true) {
						// custom method for item use
						if (itemToCheck.useMessage == null) {
							$("body").append("You just used the " + itemToCheck.name + "<br>");
							return true;
						} else {
							$("body").append(itemToCheck.useMessage + "<br>");
							return true;
						}
					// item isnt in your inventory and needs to be there to be used
					} else {
						$("body").append("You need to pick it up first" + "<br>");
						return true;
					}
				} else {
						// the item cant be used so give tell the player
						$("body").append("You can not use the " + itemToCheck.name + "<br>");
						return true;
				}
			} else {
				// if their wasn't an item in the room
				$("body").append("There is no " + match[2] + "<br>");
				return true;
			}
		}


		function goCheck(s){
		//create RE group
			match = pattGo.exec(s);
			match[2].toLowerCase();

			console.log(match)
		
			var direction = match[2];

			//temporary movement logic
			if (direction == 'north'){
				$("body").append("You went north." + "<br>");
			}
			else if (direction == 'east'){
				$("body").append("You went east." + "<br>");
			}
			else if (direction == 'south'){
				$("body").append("You went south." + "<br>");
			}
			else if (direction == 'west'){
				$("body").append("You went west." + "<br>");
			}

			else{
				$("body").append("Invalid direction specified." + "<br>");
			}
		}
	}

    // Called once when document loads
    $(function()  {
        // Instantiate some test items
        var key = new Item("key", "Unlocks somthing.", null, true, false, true);
        var door = new Item("door", "its shut.", "you try to open the door but it's locked.", false, true, false);
        var clock = new Item("clock", "It's a clock, It appears to be broken.", null, false, false, false);
        var gun = new Item("gun", "It doesn't appear to be loaded.", "You try to fire the gun but you can't.", true, true, true);
        // parser class
        var parser = new Parser();
    });

	// Function called upon submit button being pressed
	function parse(){
		//clear form after submitting text
		var enteredCommand = commandForm.command.value;
		document.getElementById("commandForm").reset();

		//parse command, print whether or not the command is valid
		if (!parser.check(enteredCommand)){
			$("body").append(enteredCommand + " is an "+ "invalid command." + "<br>");
		}
	}
