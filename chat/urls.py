from django.contrib import admin
from django.urls import path, include, re_path
from . import views as chat_views, consumers

urlpatterns = [
    path('', chat_views.chat_home, name='chat-home'),
    path('<str:room_name>/', chat_views.chat_room, name='chat-room'),
    path('users/', chat_views.user_list, name='user-list'),
]