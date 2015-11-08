/*
 * JS for player dashboard, turns the fresh bootstrap buttons
 * into links
 */
$(document).ready(function() {
    // Resume Game
    $('#resume-game').click(function() {
        location.href = '/play/'
    });

    // Start a new game
    $('#start-new-game').click(function() {
        location.href = '/new_game/'
    });
});
