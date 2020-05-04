from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UpdateInfo


# Create your views here.

def index(request):
    login_form = AuthenticationForm()
    return render(request, 'main.html', {'login_form': login_form})


@login_required
def home(request):

    login_form = AuthenticationForm()

    user = User.objects.get(username=request.user.username)
    if not user.first_name or not user.last_name:
        return redirect('update_info')
    users = User.objects.all()
    return render(request, 'home.html', {'login_form': login_form, 'users': users})

@login_required
def update_info(request):
    login_form = AuthenticationForm()
    user = User.objects.get(username=request.user.username)
    
    if request.method == 'POST':
        form = UpdateInfo(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
    
    form = UpdateInfo()
    if user.first_name or user.last_name:
        return redirect('home')

    return render(request, 'update_info.html', {'form': form, 'login_form': login_form})


@login_required
def profile(request):
    login_form = AuthenticationForm()
    user = User.objects.get(username=request.user.username)
    return render(request, 'profile.html', {'login_form': login_form})


def commin_soon(request):
    return render(request, 'commin-soon.html', {})


def debug(request):
    login_form = AuthenticationForm()
    return render(request, 'debug.html', {'login_form': login_form})

@login_required
def settings(request):
    login_form = AuthenticationForm()
    user = User.objects.get(username=request.user.username)
    return render(request, 'settings.html', {'login_form': login_form})

def disabled(request):
    return render(request, 'disabled.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})