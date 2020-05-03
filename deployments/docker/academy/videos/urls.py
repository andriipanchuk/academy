from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('all', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<str:topic>', views.topics, name='topics'),
]