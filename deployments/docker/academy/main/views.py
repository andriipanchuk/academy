from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'main.html', {})


@login_required
def home(request):
    return render(request, 'home.html', {})


@login_required
def profile(request):
    u = User.objects.get(username=request.user.username)
    return render(request, 'profile.html', {})


@login_required
def settings(request):
    u = User.objects.get(username=request.user.username)
    return render(request, 'settings.html', {})

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