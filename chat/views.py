from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from .models import Message, Block, ChatRoom
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404



@login_required
def chat_view(request):
    user = request.user
    # Fetch or create a chat room here
    room, created = ChatRoom.objects.get_or_create(name=f"{user.username}'s room")
    room.members.add(user)

    blocked_users = list(Block.objects.filter(user=user).values_list('blocked_user', flat=True))
    messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).exclude(sender__in=blocked_users).exclude(receiver__in=blocked_users).order_by('timestamp')

    other_users = User.objects.exclude(id=user.id).exclude(id__in=blocked_users)

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'other_users': other_users,
        'blocked_users': blocked_users,
        'room_id': room.id,
        'room' : room# Pass the room_id to the template context
    })




@login_required
def create_chat_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            chat_room = ChatRoom.objects.create(name=room_name)
            chat_room.members.add(request.user)  # Add the creator to the members of the chat room
            return redirect('chat')  # Redirect to the chat view after creation
        else:
            # Handle case where room name is not provided
            return render(request, 'chat/create_chat_room.html', {'error': 'Room name is required.'})

    return render(request, 'chat/create_chat_room.html')



@login_required
def send_message(request):
    if request.method == "POST":
        content = request.POST.get('content')
        receiver_username = request.POST.get('receiver')

        try:
            receiver = User.objects.get(username=receiver_username)
            # Kullanıcı bloklu mu kontrol et
            if Block.objects.filter(user=request.user, blocked_user=receiver).exists():
                return render(request, 'chat/send_message.html', {'error': 'Kullanıcıyı blokladınız.'})

            Message.objects.create(sender=request.user, receiver=receiver, content=content)
        except User.DoesNotExist:
            return render(request, 'chat/send_message.html', {'error': 'Kullanıcı bulunamadı.'})

        return redirect('chat')  # Mesaj gönderiminden sonra sohbet sayfasına yönlendirme

    return render(request, 'chat/send_message.html')


@login_required
def block_user(request, user_id):
    # Logic to block the user
    user_to_block = User.objects.get(id=user_id)
    Block.objects.create(user=request.user, blocked_user=user_to_block)

    # Assuming you want to redirect back to a specific chat room after blocking
    room_id = request.POST.get('room_id')  # Make sure room_id is included in your form or request
    if room_id:
        return redirect('chat_room', room_id=room_id)  # Redirect with room_id
    else:
        return redirect('chat')  # Fallback redirect


@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Giriş yapan kullanıcıyı hariç tut
    return render(request, 'chat/user_list.html', {'users': users})



def home_view(request):
    return render(request, 'home.html')  # 'home.html' şablonunu render eder


from django.contrib.auth.forms import UserCreationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Kullanıcıyı kaydet
            return redirect('login')  # Başarılı olursa giriş sayfasına yönlendir
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def invite_user(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)

    if request.method == 'POST':
        invitee_username = request.POST.get('invitee')
        # Davet edilen kullanıcının eklenmesi
        invitee = get_object_or_404(User, username=invitee_username)
        chat_room.user.add(invitee)  # Kullanıcıyı sohbet odasına ekle
        return redirect('chat_room', room_id=room_id)  # Kullanıcıyı sohbet odasına yönlendir

    return redirect('chat_room', room_id=room_id)


def chat_room(request, room_id):
    chat_room = get_object_or_404(ChatRoom, id=room_id)
    messages = Message.objects.filter(chat_room=chat_room).order_by('timestamp')

    if request.method == 'POST':
        # Mesaj gönderme işlemi
        content = request.POST.get('content')
        new_message = Message.objects.create(sender=request.user, content=content, chat_room=chat_room)
        new_message.save()
        return redirect('chat_room', room_id=room_id)

    return render(request, 'chat/chat_room.html', {'chat_room': chat_room, 'messages': messages})


@login_required
def block_user(request, user_id):
    Block.objects.get_or_create(user=request.user, blocked_user_id=user_id)
    return redirect('chat_room')

@login_required
def create_chat_room(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')

        # Ensure room_name is provided
        if not room_name:
            return render(request, 'chat/create_chat_room.html', {'error': 'Oda adı girin.'})

        chat_room = ChatRoom.objects.create(name=room_name)  # Create the chat room with the provided name
        chat_room.members.add(request.user)  # Add the creator to the members of the chat room
        return redirect('chat')  # Redirect to the chat view after creation

    return render(request, 'chat/create_chat_room.html')
