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
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            return HttpResponseRedirect('/home/')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

@csrf_protect
def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = django.contrib.auth.authenticate(username=username, password=password)
            if user != None:
                django.contrib.auth.login(request, user)
                return HttpResponseRedirect('/home/', {'user': user})
            else:
                form.add_error(None, 'Invalid username or password')
        else:
            form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form':form})


def player_logout(request):
    django.contrib.auth.logout(request)
    return render(request, 'logout_success.html')

@login_required
def home(request):
    return render(request, 'home.html', {'user': request.user})
