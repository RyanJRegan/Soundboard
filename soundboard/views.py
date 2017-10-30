from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login, authenticate

def index(request):
    return render(request, "soundboard/index.html")

@csrf_protect
def login_user(request):
    if request.method != 'POST':
        return #TODO error message city
    authentication_form = AuthenticationForm(data=request.POST)
    if not authentication_form.is_valid():
        return render(request, "soundboard/login_or_signup.html", {'authentication_form': authentication_form})
    # authentication_form.save()
    username = authentication_form.cleaned_data.get('username')
    password = authentication_form.cleaned_data.get('password')
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('your_boards')

@login_required
def your_boards(request):
    return render(request, "soundboard/your_boards.html")

def signup(request):
   pass

def login_or_signup(request):
    authentication_form = AuthenticationForm()
    return render(request, "soundboard/login_or_signup.html", {'authentication_form': authentication_form})
