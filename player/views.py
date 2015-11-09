"""
View class for handling player sites, including login and registration
"""

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.forms.util import ErrorList
import django.contrib.auth as auth
from django.shortcuts import render, redirect
from player.forms import RegistrationForm, LoginForm
from player.models import Player
from gameworld.models import Room
from gamestate.models import GameState

@csrf_protect
def login_register(request, tab='login'):
    """
    Render combined login/registration form
    """
    loginform = LoginForm()
    regform = RegistrationForm()
    
    if request.method == 'POST':
        if tab == 'login':
            return _login(request)
        if tab == 'register':
            return _register(request)
    
    return render(request, 'login_and_register.html', {
        'loginform': loginform, 
        'registerform': regform, 
        'tab': tab 
        })

def _register(request):
    """
    Register a new user & player, or render the registration form

    """
    
    form = RegistrationForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        user = User.objects.create_user(
            username=username,
            password=form.cleaned_data['password1'],
        )

        # Create a new player object for user
        player = Player()
        player.user = user
        player.save()

        # render the form (on login tab) with username filled in, and display a success message
        loginform = LoginForm({'username': username})
        return render(request, 'login_and_register.html', {
            'registerform': form,
            'loginform': loginform,
            'tab': 'login',
            'success': True
            })

    loginform = LoginForm()
    return render(request, 'login_and_register.html', {
        'registerform': form,
        'loginform': loginform,
        'tab': 'register'
        })


def _login(request):
    """
    Log a player in or return the login form

    Args:
        request - request object
    """

    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')

    form.add_error(None, 'Invalid username or password')

    registerform = RegistrationForm()
    return render(request, 'login_and_register.html', {
            'registerform': registerform,
            'loginform': form,
            'tab': 'login'
            })


def player_logout(request):
    """
    Log the current user out

    Args:
        request - request object
    """

    auth.logout(request)
    return redirect('home')


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

def qunit_tests(request):
    """
    QUNIT TESTS
    """

    return render(request, 'qunit_tests.html');
