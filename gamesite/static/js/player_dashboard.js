var playerDashboard = {

    resumeGame: function() {
        console.log('resume game');
    }
};

$(document).ready(function() {
    
    // Resume Game
    $('#resume-game').click(function() {
        playerDashboard.resumeGame();
    });

    // Start a new game
    $('#start-new-game').click(function() {
        location.href = '/new_game/'
    });
});
