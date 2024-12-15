from django.shortcuts import render, HttpResponseRedirect,redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "Chat/chatPage.html", context)
def HomePage(request):
    return render(request,'base.html')
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