pattState1Change = /^\s*(use)\s+(key)\s+(on|with)\s+(door)\s*$/i;

function gameState(s) {
	if (pattState1Change.exec(s)) {
		door1.locked = false;
		player.inv.remove(key);
		displayResponse("You unlock the door");
	}	
}