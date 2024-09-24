from django.contrib import admin
from django.urls import path, include
from chat import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Anasayfa
    path('admin/', admin.site.urls),
    path('chat/', views.chat_view, name='chat'),
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('register/', views.register, name='register'),  # Kayıt sayfası
    path('chat/', include('chat.urls')),
]
