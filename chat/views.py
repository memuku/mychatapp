from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import models
from .models import Message, Block
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404


@login_required
def chat_view(request):
    user = request.user
    # Kullanıcının blokladığı kullanıcıları al
    blocked_users = Block.objects.filter(user=user).values_list('blocked_user', flat=True)

    # Kullanıcıların mesajlarını al
    messages = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).exclude(sender__in=blocked_users).exclude(receiver__in=blocked_users).order_by('timestamp')

    # Bloklanmayan diğer kullanıcıları al
    other_users = User.objects.exclude(id=user.id).exclude(id__in=blocked_users)

    return render(request, 'chat/chat.html', {
        'messages': messages,
        'other_users': other_users,
        'blocked_users': blocked_users,
    })


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
    user_to_block = User.objects.get(id=user_id)
    Block.objects.get_or_create(user=request.user, blocked_user=user_to_block)
    return redirect('chat')


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
