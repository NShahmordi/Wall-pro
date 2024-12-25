from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import *
from .models import Advertisement, Users, Message, Room, AdvertisementImage
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

@login_required
def chat_history(request):
    rooms = Room.objects.filter(user1=request.user) | Room.objects.filter(user2=request.user)
    return render(request, 'Chat/chat_history.html', {'rooms': rooms})

def HomePage(request):
    products = Advertisement.objects.all()
    return render(request, 'Market/product_list.html', {'Advertisments': products})

def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Congratulations!! Your account has been created"
                )
                HttpResponseRedirect("/login/")
        else:
            form = CustomUserCreationForm()
        return render(request, "main/signup.html", {"form": form})
    else:
        return HttpResponseRedirect("/")

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data["username"]
                upass = form.cleaned_data["password"]
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/")
        else:
            form = LoginForm()
        return render(request, "main/login.html", {"form": form})
    else:
        return HttpResponseRedirect("/")

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")

def product_detail(request, slug):
    advertisement = get_object_or_404(Advertisement, slug=slug)
    user1 = request.user
    user2 = advertisement.owner

    if user1.is_authenticated:
        room, created = Room.objects.get_or_create(user1=user1, user2=user2)
        chat_room_id = room.id
    else:
        chat_room_id = None

    context = {
        'advertisement': advertisement,
        'chat_room_id': chat_room_id,
    }
    return render(request, 'Market/product_detail.html', context)

@login_required
def create_or_get_room(request, user_id):
    user1 = request.user
    user2 = get_object_or_404(get_user_model(), id=user_id)
    room, created = Room.objects.get_or_create(user1=user1, user2=user2)
    return redirect('room_detail', room_id=room.id)


@login_required
def edit_ad(request, slug):
    ad = get_object_or_404(Advertisement, slug=slug)
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            advertisement = form.save()
            images = request.FILES.getlist('images')
            if images:
                AdvertisementImage.objects.filter(advertisement=advertisement).delete()
                for image in images:
                    AdvertisementImage.objects.create(advertisement=advertisement, image=image)
            return redirect('product_detail', slug=ad.slug)
    else:
        form = AdvertisementForm(instance=ad)
    return render(request, 'Market/edit_ad.html', {'form': form, 'ad': ad})

@login_required
def create_room(request, user_id):
    user1 = request.user
    user2 = get_object_or_404(settings.AUTH_USER_MODEL, id=user_id)
    room, created = Room.objects.get_or_create(user1=user1, user2=user2)
    return redirect('room_detail', room_id=room.id)

@login_required
def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room).order_by('timestamp')
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = room
            message.sender = request.user
            message.save()
            return redirect('room_detail', room_id=room.id)
    else:
        form = MessageForm()
    
    return render(request, 'Chat/chatPage.html', {'room': room, 'form': form, 'messages': messages})

@login_required
def create_advertisement(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            advertisement = form.save()
            for file in request.FILES.getlist('images'):
                AdvertisementImage.objects.create(advertisement=advertisement, image=file)
            return redirect('home')  # Replace with your success URL
    else:
        form = AdvertisementForm()
    return render(request, 'Market/create_ad.html', {'form': form})