"""
View class for handling player sites, including login and registration
"""

from django.shortcuts import render
from player.forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.forms.util import ErrorList
import django.contrib.auth


@csrf_protect
def register(request):
    """
    Register and new user & player, or render the registration form

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


def player_dashboard(request):
    """
    Player dashboard - home page. Return a welcome page
    if the user is not logged in

    Args:
        request - request object
    """

    if request.user.is_authenticated():
        return render(request, 'player_dashboard.html', {'user': request.user})
    else:
        return render(request, 'welcome.html')
