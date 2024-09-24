from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from django.contrib.auth.models import User

@login_required
def chat_view(request):
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Message.objects.create(user=request.user, content=content)
        return redirect('chat')

    messages = Message.objects.all()
    return render(request, 'chat/chat.html', {'messages': messages})
from django.shortcuts import render

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
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Giriş yapan kullanıcıyı hariç tut
    return render(request, 'chat/user_list.html', {'users': users})


@login_required
def send_message(request):
    if request.method == "POST":
        content = request.POST.get('content')
        receiver_username = request.POST.get('receiver')

        try:
            receiver = User.objects.get(username=receiver_username)
            Message.objects.create(sender=request.user, receiver=receiver, content=content)
        except User.DoesNotExist:
            # Hata durumu: Kullanıcı bulunamadı
            return render(request, 'chat/send_message.html', {'error': 'Kullanıcı bulunamadı.'})

        return redirect('chat')  # Mesaj gönderiminden sonra sohbet sayfasına yönlendirme

    return render(request, 'chat/send_message.html')

@login_required
def chat_view(request):
    received_messages = Message.objects.filter(receiver=request.user)
    return render(request, 'chat/chat.html', {'messages': received_messages})
