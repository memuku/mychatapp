from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from twisted.mail.smtp import User

from .forms import RoomForm
from .models import Message, Room
from django.contrib.auth.models import User
from django.shortcuts import render
from chat import templates

@login_required()
def chat_home(request):

    form = RoomForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        room_name = form.cleaned_data['room_name']
        db_messages = Message.objects.filter(room=room_name)[:]
        messages.success(request, f"Joined: {room_name}")
        return render(request, 'chat/chatroom.html', {'room_name': room_name, 'title': room_name, 'db_messages': db_messages})

    return render(request, 'chat/index.html', {'form': form})



@login_required
def chat_room(request, room_name):
    db_messages = Message.objects.filter(room=room_name)[:]
    users = User.objects.all()

    messages.success(request, f"Joined: {room_name}")
    return render(request, 'chat/chatroom.html', {
        'room_name': room_name,
        'title': room_name,
        'db_messages': db_messages,
        'users': users,
    })
@login_required
def home_view(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/home.html', {'users': users})

def user_list(request):
    users = User.objects.all()  # Tüm kullanıcıları al
    return render(request, 'chat/user_list.html', {'users': users})