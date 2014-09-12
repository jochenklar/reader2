from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate as auth_authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from forms import LoginForm

def index(request):
    if request.user.is_authenticated():
        return render(request,'layout.html')
    else:
        return HttpResponseRedirect('/login/')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            values = form.cleaned_data
            user = auth_authenticate(username=values['username'], password=values['password'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect('/')
    else:
        form = LoginForm()

    return render(request,'layout.html',{'form': form, 'login': True})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')
