var Item = function(name, description, enterRoomDescription, useMessage) {
	/*strings*/
	this.name = name;
	this.description = description;
	this.enterRoomDescription = enterRoomDescription;
	this.useMessage = useMessage;
	this.hidden = false;
	/*adds a new item into the room array when the item is created*/
}

var Pickupable = function(name, description, enterRoomDescription, useMessage) {
	Item.call(this, name, description, enterRoomDescription, useMessage);
}

var NonPickupable = function(name, description, enterRoomDescription, useMessage) {
	Item.call(this, name, description, enterRoomDescription, useMessage);
}

/*this item can be picked up and used if it is picked up, it's usePattern is just a regular
expression that is matched for the items use command.  it's needed so different items can
be used by typing different verbs.*/
var PickupableAndUsable = function(name, description, enterRoomDescription, useMessage, usePattern) {
	Pickupable.call(this, name, description, enterRoomDescription, useMessage);
	this.usePattern = usePattern;
	this.inInv = false;
}

/* TODO: create a key Item (for special error messages when trying to unlock a door with the wrong key)*/
var Key = function(name, description, enterRoomDescription, useMessage) {
	regx = /^\s*(use)\s+(\w+)\s*$/i;
	PickupableAndUsable.call(this, name, description, enterRoomDescription, useMessage, regx );
}
/*this item cannot be picked up but it can be used, it's usePattern is just a regular
expression that is matched for the items use command.  it's needed so different items can
be used by typing different verbs.*/
var NonPickupableAndUsable = function(name, description, enterRoomDescription, useMessage, usePattern) {
	NonPickupable.call(this, name, description, enterRoomDescription, useMessage);
	this.usePattern = usePattern;
}

/*this item can be examined but it can't be used or picked up*/
var Decoration = function(name, description, enterRoomDescription, useMessage) {
	NonPickupable.call(this, name, description, enterRoomDescription, useMessage);
}

/*doors are not items anymore but they still kind of work the same way*/
var Door = function(room, room2, name, description, enterRoomDescription, useMessage, locked) {
	this.name = name;
	this.description = description;
	this.enterRoomDescription = enterRoomDescription;
	this.useMessage = useMessage;
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
