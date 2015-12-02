function GameManager()  {
	this.currentRoom;
	this.roomItems;
	this.roomDoors;
	this.inventory;
	
	// returns a room object with description fields, room contents,
	// doors, etc.
	this.getRoom = function()  {
		$.get('/get_current_room/', function(data) {
			console.log(data)
			manager.updateSelf(data);
			manager.printRoom();
			manager.updateTitle();
			
			parser.addRoomItems(manager.roomItems); // TODO also inventory items
			
			$("#commandUserInput").focus();
		}, "json");
	}
	
	this.updateSelf = function(data)  {
		this.currentRoom = data.room;
		this.roomItems = this.currentRoom.items;
		this.roomDoors = this.currentRoom.doors;
		this.inventory = data.inventory;
		
	}
	
	// print the room description & its contents to the terminal
	this.printRoom = function()  {
		var room = this.currentRoom;
		// TODO if it's not illuminated, the player can't see anything
	
		// TODO make special functions to list the items
		displayResponse(room.desc_header);
		for (i = 0; i < room.items.length; i++)  {
			displayResponse(" * " + room.items[i].enterRoomDescription);
		}
		displayResponse(room.desc_footer);
	}
	
	this.updateTitle = function()  {
		$("#pinnedText").html(this.currentRoom.title);

	}

	this.postChangeRoom = function(data)  {
		$.post('/post_change_room/', data, function(serverdata)  {
			manager.updateSelf(serverdata);
			
			manager.printRoom();
			manager.updateTitle();
		}, 'json');
	}
	// tells the backend the player used an item
	this.postPlayerAction = function(data)  {
		// TODO add a handler
		$.post('/post_player_action/', data);
		
		// backend returns a string describing the result
		// room contents may be updated
		// player inventory may be updated
		// (these all should be pushed here)
	}
	
}

/* script.js */
var parser, manager, csrftoken;

$(function()  {
	csrftoken = getCookie('csrftoken');
	
	manager = new GameManager();
	parser = new Parser();
	manager.getRoom();
	
});

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



/* functions.js - checkers */
// itemIsInRoomOrInv() - checks if item is in room, inventory, or both
// form handler for terminal
$("#commandForm").submit(function(event)  {
	event.preventDefault();
	parse();
 });
 
 // Function called upon submit button being pressed
function parse() {
	//clear form after submitting text
	var enteredCommand = commandForm.command.value;
	$("#commandUserInput").val('');

	if (enteredCommand != "")  {
		//echo command
		$("#terminalText").append("<p class=\"echo\">" + enteredCommand + "</p>");

		//parse command, print whether or not the command is valid
		parser.check(enteredCommand);
	}
}

function displayResponse(s)  {
	$("#terminalText").append("<p class=\"response\">" + s + "</p>");
	//scroll down chat window
	$("#terminalText").scrollTop($("#terminalText")[0].scrollHeight);
}

//function mapUpdate(currentRoom)

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
