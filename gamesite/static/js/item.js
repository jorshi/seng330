var Item = function(room, name, description, useMessage) {
	/*strings*/
	this.name = name;
	this.room = room;
	this.description = description;
	this.useMessage = useMessage;
	/*adds a new item into the room array when the item is created*/
	room.itemsInRoom.push(this);
}

var Pickupable = function(room, name, description, useMessage) {
	Item.call(this, room, name, description, useMessage);
}

var NonPickupable = function(room, name, description, useMessage) {
	Item.call(this, room, name, description, useMessage);
}

/*this item can be picked up and used if it is picked up, it's usePattern is just a regular
expression that is matched for the items use command.  it's needed so different items can
be used by typing different verbs.*/
var PickupableAndUsable = function(room, name, description, useMessage, usePattern) {
	Pickupable.call(this, room, name, description, useMessage);
	this.usePattern = usePattern;
	this.inInv = false;
}

/*this item cannot be picked up but it can be used, it's usePattern is just a regular
expression that is matched for the items use command.  it's needed so different items can
be used by typing different verbs.*/
var NonPickupableAndUsable = function(room, name, description, useMessage, usePattern) {
	NonPickupable.call(this, room, name, description, useMessage);
	this.usePattern = usePattern;
}

/*this item can be examined but it can't be used or picked up*/
var Decoration = function(room, name, description, useMessage) {
	NonPickupable.call(this, room, name, description, useMessage);
}

/*the main difference between a door and a NonPickupableAndUsable is that doors need
to have both rooms they connect to passed in them, they also have a boolean to say 
if they're locked or not*/
var Door = function(room, room2, name, description, useMessage, locked) {
	NonPickupable.call(this, room, name, description, useMessage);
	this.locked = locked;
	this.room2 = room2;
	room2.itemsInRoom.push(this);
}

Pickupable.prototype = Object.create(Item.prototype); 
Pickupable.prototype.constructor = Pickupable; 

NonPickupable.prototype = Object.create(Item.prototype); 
NonPickupable.prototype.constructor = NonPickupable; 

PickupableAndUsable.prototype = Object.create(Pickupable.prototype); 
PickupableAndUsable.prototype.constructor = PickupableAndUsable; 

NonPickupableAndUsable.prototype = Object.create(NonPickupable.prototype); 
NonPickupableAndUsable.prototype.constructor = NonPickupableAndUsable; 

Decoration.prototype = Object.create(NonPickupable.prototype); 
Decoration.prototype.constructor = Decoration; 

Door.prototype = Object.create(NonPickupable.prototype); 
Door.prototype.constructor = Door; 
