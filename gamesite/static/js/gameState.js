pattState1Change = /^\s*(use)\s+(key1)\s+(on|with)\s+(south door)\s*$/i;
pattState2Change = /^\s*(use)\s+(key2)\s+(on|with)\s+(east door)\s*$/i;
pattState3Change = /^\s*(use)\s+(ammo)\s+(on|with)\s+(gun)\s*$/i;
pattState4Change = /^\s*(use)\s+(lighter)\s+(on|with)\s+(fireplace)\s*$/i;
pattState5Change = /^\s*(extinguish|stamp\s+out|put\s+out)\s+(fireplace)\s*$/i;

function gameState(s) {
	/* TODO: make this better (proper error messages)*/
	if (pattState1Change.exec(s)) {
		/* call a gamestate_change function */
		door1.locked = false;
		player.inv.remove(key1);
		displayResponse("You unlock the south door");
	} 
	if (pattState2Change.exec(s)) {
		door2.locked = false;
		player.inv.remove(key2);
		displayResponse("You unlock the east door");
	}		
	if (pattState3Change.exec(s)) {
		gun.stateChange(2);
		player.inv.remove(ammo);
		displayResponse("You load the gun");
	}	
	if (pattState4Change.exec(s)) {
		if (firePlace.description == "there is a fire burning in it") {
			displayResponse("It's already lit");
			return;
		}
		firePlace.stateChange(2);
		displayResponse("You light the fireplace");
		player.currentRoom.updateDescription();
	}	
	if (pattState5Change.exec(s)) {
		firePlace.stateChange(1);
		displayResponse("You put out the fireplace");
		player.currentRoom.updateDescription();
	}	
}