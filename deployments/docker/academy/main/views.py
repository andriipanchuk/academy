from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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

