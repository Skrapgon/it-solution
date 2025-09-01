from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Пароли не совпадают')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь уже существует')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('/')
    return render(request, 'accounts/register.html')