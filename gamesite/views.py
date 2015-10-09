from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

def home(request):
    return render_to_response('home.html')



def login(request):
	#encryption token for authenticated login
	c = {}
	c.update(csrf(request))
	return render_to_response('login.html', c)

def auth_view(request):
	#if no value given use empty string
	username = request.POST.get('username', '')
	password = request.POST.get('password','')
	user = auth.authenticate(username=username, password=password)

	#check if user is in database
	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/loggedin')
	else:
		return HttpResponseRedirect('/invalid')

def loggedin(request):
	return render_to_response('loggedin.html',{'full_name' : request.user.username})

def invalid_login(request):
	return render_to_response('invalid.html')

def logout(request):
	auth.logout(request)
	return render_to_response('logout.html')