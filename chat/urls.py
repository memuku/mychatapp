from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import send_message , user_list

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('send/', send_message, name='send_message'),
    path('users/', user_list, name='user_list'),
    path('register/', views.register, name='register')
]
