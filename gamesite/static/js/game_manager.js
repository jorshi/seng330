/*
 * Game Manager Class
 *
 * This class will contain functionality for handling
 * communications with the backend and updating the map
 * and objects within the map on the frontend
 */

var GameManager = function() {

    // Attributes
    self = this; // store reference to 'this'
    this.room = null;

    /*
     * Requests
     */

    // Make Request to get the player's current room
    this.load_current_room = function() {
        $.get('/get_current_room/', function(data) {
            self.load_room(data)
        });
    };


    // Make request to get the inventory for the current room
    this.get_room_inventory = function() {
        if (this.room !== null) {
            $.get('/get_inventory/?room=' + this.room.pk, function(data) {
                self.load_inventory(data);
            });
        }
    };


    // Make request to get the doors for the current room
    this.get_room_doors = function() {
        if (this.room !== null) {
            $.get('/get_doors/?room=' + this.room.pk, function(data) {
                self.load_doors(data);
            });
        }
    };


    /*
     * Callbacks
     */

    // Callback for the get current room request
    this.load_room = function(data) {

        // Extract the room information
        try {
            this.room = data[0];
            this.get_room_inventory();
            this.get_room_doors();
        } catch(err) {
            console.log("Failed to load map! : " + err);
        }
    };


    // Callback for the get room inventory request
    this.load_inventory = function(data) {
        console.log("Got Inventory!");

        // Do stuff with the item inventory for this room here
    };


    // Callback for the get room doors request
    this.load_doors = function(data) {
        console.log("Got Doors!");

        // Do stuff with the doors for this room here
    };
};
