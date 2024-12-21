from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from .forms import *
from .models import Advertisement, Users
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def chatPage(request, username):
    target_user = get_object_or_404(Users, username=username)
    context = {
        'target_user': target_user
    }
    return render(request, "Chat/chatPage.html", context)

def HomePage(request):
    products = Advertisement.objects.all()
    return render(request, 'Market/product_list.html', {'products': products})

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
    product = get_object_or_404(Advertisement, slug=slug)
    return render(request, 'Market/product_detail.html', {'product': product})

@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()
            return redirect('home')
    else:
        form = AdvertisementForm()
    return render(request, 'Market/create_ad.html', {'form': form})