/* script.js */
var parser, manager, csrftoken;

$(function()  {
	csrftoken = getCookie('csrftoken');
	
	manager = new GameManager();
	parser = new Parser();
	manager.getRoom();
	
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

