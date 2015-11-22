QUnit.test('MSample Test', function(assert) {
   assert.strictEqual(3, 3, 'check if 3==3');
});

QUnit.test('Player tests', function(assert) {
	assert.strictEqual(player.inv.itemsInInventory.length, 0, "Player Inventory test");
	assert.strictEqual(player.currentRoom, room1, "Player Room test");
});

QUnit.test('Room tests', function(assert) {
   assert.strictEqual(room1.description, "Room 1: there is a key on the ground (called 'key1'), there is a door on the south wall, there is a clock on the wall, there is a gun on the floor, end", 'room description match test');
   player.inv.itemsInInventory.push(room1.itemsInRoom.splice(0, 1)[0]);
   room1.updateDescription();
   assert.strictEqual(room1.description, "Room 1: there is a door on the south wall, there is a clock on the wall, there is a gun on the floor, end", 'room description match test remove item');
   room2.updateDescription();
   assert.strictEqual(room2.description, "Room 2: there is a key on the ground (called 'key2'), there is a door on the south wall, there is a door on the east wall, end", 'room2 description match test');
   room3.updateDescription();
   assert.strictEqual(room3.description, "Room 3: there is a door on the east wall, end", 'room3 description match test');
});

QUnit.test('Parser Test', function(assert) {
   assert.strictEqual(parser.check("drop key1"), true, 'drop test');
   assert.strictEqual(parser.check("examine door"), true, 'examine test');
   assert.strictEqual(parser.check("grab gun"), true, 'pickup test');
   assert.strictEqual(parser.check("throw away gun"), true, 'drop test2');
   assert.strictEqual(parser.check("pickup gun"), true, 'pickup test2');
   assert.strictEqual(parser.check("use key1 on door"), true, 'use on test');
   assert.strictEqual(parser.check("go through south door"), true, 'go through test');
   assert.strictEqual(parser.check("pick     up   key2   "), true, 'pickup test3');
   assert.strictEqual(parser.check("    use key2 with door2"), true, 'use on test2');
   assert.strictEqual(parser.check("go through east door"), true, 'go through test2');
   assert.strictEqual(parser.check("aershdrth"), false, 'spam command test');
   assert.strictEqual(parser.check("\"\""), false, 'quotes command test');
   assert.strictEqual(parser.check(""), false, 'empty command test');
   assert.strictEqual(parser.check("pick up trash"), true, 'invalid item command test');
});


