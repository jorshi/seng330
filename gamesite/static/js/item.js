var Item = function(name, description, enterRoomDescription) {
	/*strings*/
	this.name = name;
	this.description = description;
	this.enterRoomDescription = enterRoomDescription;
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
var PickupableAndUsable = function(name, description, enterRoomDescription, useMessage, usePattern, inInv) {
	Pickupable.call(this, name, description, enterRoomDescription, inInv);
	this.usePattern = usePattern;
	this.useMessage = useMessage;

	this.newItemState = function(name, description, enterRoomDescription, useMessage, usePattern, inInv) {
		this.name = name;
		this.description = description;
		this.enterRoomDescription = enterRoomDescription;
		this.inInv = inInv;
		this.usePattern = usePattern;
		this.useMessage = useMessage;		
	}

}

var PickupableAndNonUseable = function(name, description, enterRoomDescription, inInv) {
	Pickupable.call(this, name, description, enterRoomDescription, inInv);
}



/* TODO: create a key Item (for special error messages when trying to unlock a door with the wrong key)*/
var Key = function(name, description, enterRoomDescription, doorToOpen) {
	regx = /^\s*(use)\s+(\w+)\s*$/i;
	PickupableAndUsable.call(this, name, description, enterRoomDescription, "You need to use it on something.", regx, inInv);
}
/*this item cannot be picked up but it can be used, it's usePattern is just a regular
expression that is matched for the items use command.  it's needed so different items can
be used by typing different verbs.*/
var NonPickupableAndUsable = function(name, description, enterRoomDescription, useMessage, usePattern) {
	NonPickupable.call(this, name, description, enterRoomDescription);
	this.usePattern = usePattern;
	this.useMessage = useMessage;

	this.newItemState = function(name, description, enterRoomDescription, useMessage, usePattern) {
		this.name = name;
		this.description = description;
		this.enterRoomDescription = enterRoomDescription;
		this.usePattern = usePattern;
		this.useMessage = useMessage;		
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

PickupableAndNonUseable.prototype = Object.create(Pickupable.prototype); 
PickupableAndNonUseable.prototype.constructor = PickupableAndNonUseable; 

Key.prototype = Object.create(PickupableAndUsable.prototype); 
Key.prototype.constructor = Key; 

NonPickupableAndUsable.prototype = Object.create(NonPickupable.prototype); 
NonPickupableAndUsable.prototype.constructor = NonPickupableAndUsable; 

Decoration.prototype = Object.create(NonPickupable.prototype); 
Decoration.prototype.constructor = Decoration; 
