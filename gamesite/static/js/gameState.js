pattState1Change = /^\s*(use)\s+(key1)\s+(on|with)\s+(door)\s*$/i;
pattState2Change = /^\s*(use)\s+(key2)\s+(on|with)\s+(door2)\s*$/i;

function gameState(s) {
	if (pattState1Change.exec(s)) {
		door1.locked = false;
		player.inv.remove(key1);
		displayResponse("You unlock the door");
	} 
	if (pattState2Change.exec(s)) {
		door2.locked = false;
		player.inv.remove(key2);
		displayResponse("You unlock the door");
	}		
}