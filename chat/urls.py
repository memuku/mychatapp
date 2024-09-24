from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import send_message , user_list
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:room_id>/', views.chat_view, name='chat_view'),
    path('chat/chat_room/<int:room_id>/invite/', views.invite_user, name='invite_user'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('send/', views.send_message, name='send_message'),
    path('users/', user_list, name='user_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('chat_room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('create_chat_room/', views.create_chat_room, name='create_chat_room'),
    path('chat/chat_room/<int:room_id>/invite/', views.invite_user, name='invite_user'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('register/', views.register, name='register')
]
