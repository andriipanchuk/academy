from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('settings', views.settings, name='settings'),
    path('logout', auth_views.LogoutView, name='logout'),
]