var Item = function(name, description, enterRoomDescription) {
	/*strings*/
	this.name = name;
	this.description = description;
	this.enterRoomDescription = enterRoomDescription;
	this.hidden = false;
	/*adds a new item into the room array when the item is created*/
}

var Pickupable = function(name, description, enterRoomDescription, inInv) {
	this.inInv = inInv;
	Item.call(this, name, description, enterRoomDescription);
}

var NonPickupable = function(name, description, enterRoomDescription) {
	Item.call(this, name, description, enterRoomDescription);
}

/*this item can be picked up and used if it is picked up, it's usePattern is just a regular
expression that is matched for the items use command.  it's needed so different items can
be used by typing different verbs.*/
var PickupableAndUsable = function(name, description, enterRoomDescription, useMessage, usePattern, inInv, state) {
	Pickupable.call(this, name, description[state-1], enterRoomDescription[state-1], inInv);
	this.usePattern = usePattern[state-1];
	this.useMessage = useMessage[state-1];

	this.stateChange = function(newState) {
		this.usePattern = usePattern[newState-1];
		this.useMessage = useMessage[newState-1];
		this.description = description[newState-1];
		this.enterRoomDescription = enterRoomDescription[newState-1];
	}
}

var PickupableAndUsable = function(name, description, enterRoomDescription, inInv) {
	Pickupable.call(this, name, description, enterRoomDescription, inInv);
	
}



/* TODO: create a key Item (for special error messages when trying to unlock a door with the wrong key)*/
var Key = function(name, description, enterRoomDescription, doorToOpen) {
	regx = /^\s*(use)\s+(\w+)\s*$/i;
	PickupableAndUsable.call(this, name, [description], [enterRoomDescription], ["You need to use it on something."], [regx], 1);
}
/*this item cannot be picked up but it can be used, it's usePattern is just a regular
expression that is matched for the items use command.  it's needed so different items can
be used by typing different verbs.*/
var NonPickupableAndUsable = function(name, description, enterRoomDescription, useMessage, usePattern, state) {
	NonPickupable.call(this, name, description[state-1], enterRoomDescription[state-1]);
	this.usePattern = usePattern[state-1];
	this.useMessage = useMessage[state-1];

	this.stateChange = function(newState) {
		this.usePattern = usePattern[newState-1];
		this.useMessage = useMessage[newState-1];
		this.description = description[newState-1];
		this.enterRoomDescription = enterRoomDescription[newState-1];
	}
}

/*this item can be examined but it can't be used or picked up*/
var Decoration = function(name, description, enterRoomDescription) {
	NonPickupable.call(this, name, description, enterRoomDescription);
}

/*doors are not items anymore but they still kind of work the same way*/
var Door = function(room, room2, name, description, enterRoomDescription, locked) {
	this.name = name;
	this.description = description;
	this.enterRoomDescription = enterRoomDescription;
	this.locked = locked;
	this.room = room;
	this.room2 = room2;
}

Pickupable.prototype = Object.create(Item.prototype); 
Pickupable.prototype.constructor = Pickupable; 

NonPickupable.prototype = Object.create(Item.prototype); 
NonPickupable.prototype.constructor = NonPickupable; 

PickupableAndUsable.prototype = Object.create(Pickupable.prototype); 
PickupableAndUsable.prototype.constructor = PickupableAndUsable; 

Key.prototype = Object.create(PickupableAndUsable.prototype); 
Key.prototype.constructor = Key; 

NonPickupableAndUsable.prototype = Object.create(NonPickupable.prototype); 
NonPickupableAndUsable.prototype.constructor = NonPickupableAndUsable; 

Decoration.prototype = Object.create(NonPickupable.prototype); 
Decoration.prototype.constructor = Decoration; 
