"""
View class for handling player sites, including login and registration
"""

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms.util import ErrorList
import django.contrib.auth
from django.shortcuts import render
from player.forms import RegistrationForm, LoginForm
from player.models import Player
from gamestate.models import GameState
from gameworld.models import Room

@csrf_protect
def register(request):
    """
    Register a new user & player, or render the registration form

    Args:
        request - request object
    """

    # if the HTTP method is POST, then create a new user
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )

            # Create a new player object for user
            player = Player()
            player.user = user
            player.save()

            return render(request, 'register/success.html')
    else:
        form = RegistrationForm()
    return render(request, 'register/register.html', {'form': form})


@csrf_protect
def login(request):
    """
    Log a player in or return the login form

    Args:
        request - request object
    """

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = django.contrib.auth.authenticate(username=username, password=password)
            if user != None:
                django.contrib.auth.login(request, user)
                return HttpResponseRedirect('/', {'user': user})
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})


def player_logout(request):
    """
    Log the current user out

    Args:
        request - request object
    """

    django.contrib.auth.logout(request)
    return render(request, 'logout_success.html')


def home(request):
    """
    Return a welcome page
    if the user is not logged in
    """
    if request.user.is_authenticated():
        return _dashboard(request)
    else:
        return render(request, 'welcome.html')
    # TODO: welcome.html has a big 'Start' button
    
def _dashboard(request):
    """
    Return game UI if player has existing game,
    otherwise create a new game then return game UI
    """
    
    # Get the player for this user, if they don't have one (maybe a superuser?) create one for them
    try:
        player = Player.objects.get(pk=request.user)
    except Player.DoesNotExist:
        player = Player()
        player.user = request.user
        player.save()
    
    # Check for an existing game for the player
    try:
        gamestate = player.gamestate
        return _terminal(request, gamestate)
    except GameState.DoesNotExist:
        return _create_game(request, player)
        
def _terminal(request, gamestate):
    """
    Resume an existing game for this player
    """
    return render(request, 'game_view.html', { 'user': request.user, 'gameState': gamestate })
    
def _create_game(request, player):
    """
    Start a new game for this player
    """

    # Erase users current game state if they are starting a new game
    try:
        gamestate = player.gamestate
        gamestate.delete()
    except GameState.DoesNotExist:
        pass

    gamestate = GameState()
    gamestate.player = player
    gamestate.current_room = Room.objects.get(name='start')
    # other stuff?
    gamestate.save()
    return _terminal(request, gamestate)
    
