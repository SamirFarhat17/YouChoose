from django.contrib import admin
from django.urls import path
from .import views
from channel.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('vidlist/', views.vidlist, name = 'vidlist')
]
