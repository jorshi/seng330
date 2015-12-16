$(document).ready(function()  {
        csrftoken = getCookie('csrftoken');
        
        /*TODO: call an update_room function*/
        $.get('/get_current_room/', function(data) {

            getState(data);
            displayResponse("How would you like to proceed?");

        });

});

function getState(data) {

            console.log(data);
            room = new Room(data.room.desc_header, data.room.desc_footer);
 
            //TODO make doors added to room on creation
            playerInventory = new Inventory();
            player = new Player(room, playerInventory);

            addItemsToPlayer(data.inventory);
 
            addItemsToRoom(data.room);

            parser = new Parser(player);
            player.currentRoom.updateDescription();
                
            
            $("#pinnedText").html(player.currentRoom.description);    
        }

function addItemsToPlayer(data) {

     for(i = 0; i < data.length; i++){
        jsitem = data[i];
        if (jsitem.type == "pickupableAndUsable") {
            tempRegex = new RegExp(jsitem.useCases[0].usePattern);
            tempItem = new PickupableAndUsable(jsitem.name, jsitem.examineDescription, jsitem.enterRoomDescription, jsitem.useCases[0].useMessage, tempRegex, true, jsitem.useCases[0].usedOn);
            player.inv.add(tempItem);
        } else if (jsitem.type == "pickupableAndNonUsable") {
            tempItem = new PickupableAndNonUseable(jsitem.name, jsitem.examineDescription, jsitem.enterRoomDescription, true);
            player.inv.add(tempItem);
        } 
     }
}


function addItemsToRoom(data){
            roomItemArray = [];


            for(i = 0; i < data.items.length; i++){
                jsitem = data.items[i];

                //TEMPORARY WORKAROUND, let's painting be picked up
                if (jsitem.type == "fixedAndUsable"){
                        tempRegex = new RegExp(jsitem.useCases[0].usePattern);
                        tempItem = new NonPickupableAndUsable(jsitem.name, jsitem.examineDescription, jsitem.enterRoomDescription, jsitem.useCases[0].useMessage, tempRegex);
                        room.itemsInRoom.push(tempItem);
                    } else if (jsitem.type == "pickupableAndUsable") {
                        tempRegex = new RegExp(jsitem.useCases[0].usePattern);
                        tempItem = new PickupableAndUsable(jsitem.name, jsitem.examineDescription, jsitem.enterRoomDescription, jsitem.useCases[0].useMessage, tempRegex, false, jsitem.useCases[0].usedOn);
                        room.itemsInRoom.push(tempItem);
                    } else if (jsitem.type == "decoration") {
                        tempItem = new Decoration(jsitem.name, jsitem.examineDescription, jsitem.enterRoomDescription);
                        room.itemsInRoom.push(tempItem);
                    } else if (jsitem.type == "key") {
                        tempItem = new Key(jsitem.name, jsitem.examineDescription, jsitem.enterRoomDescription, jsitem.doorToOpen);
                        room.itemsInRoom.push(tempItem);
                    //} else if (jsitem.type == "door") {
                    //    tempItem = new Door(jsitem.direction, jsitem.examineDescription, jsitem.enterRoomDescription, jsitem.locked, jsitem.roomName);
                    //    room.itemsInRoom.push(tempItem);
                    } else if (jsitem.type == "pickupableAndNonUsable") {
                        tempItem = new PickupableAndNonUseable(jsitem.name, jsitem.examineDescription, jsitem.enterRoomDescription, false);
                        room.itemsInRoom.push(tempItem);
                    } 
                    //Will need to loop through this
                }

            eastDoor = null;
            westDoor = null;
            southDoor = null;
            northDoor = null;
            if (data.doors.east != null) {
                eastDoor = new Door("east door","It's a door on the east wall.", "there is a door on the east wall, ", data.doors.east.locked, data.doors.east.next_room);
            }
            if (data.doors.west != null) {
                westDoor = new Door("west door", "It's a door on the west wall.", "there is a door on the west wall, ", data.doors.west.locked, data.doors.west.next_room);
            }
            if (data.doors.north != null) {
                northDoor = new Door("north door","It's a door on the north wall.", "there is a door on the north wall, ", data.doors.north.locked, data.doors.north.next_room);
            }
            if (data.doors.south != null) {
                southDoor = new Door("south door", "It's a door on the south wall.", "there is a door on the south wall, ", data.doors.south.locked, data.doors.south.next_room);
            }
            room.setUpDoors([northDoor,eastDoor,southDoor,westDoor]);

        }


// Django's xss protection https://docs.djangoproject.com/en/1.8/ref/csrf/
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
