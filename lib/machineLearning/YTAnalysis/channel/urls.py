from django.contrib import admin
from django.urls import path
from .import views
from channel.views import HomeView
from django.conf.urls import url

urlpatterns = [
    path('', HomeView.as_view(), name = 'home'),
    path('vidlist/', views.vidlist, name = 'vidlist'),
    path('chart/<str:video_id>/', views.chart, name = 'chart'),
    path('vidlist/<str:video_id>/', views.video_detail,name='video_detail'),
]
