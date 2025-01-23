from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .functions import *
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return render(request, 'home.html')

def start(request):
    return render(request, 'start.html')

def main(request):
    return render(request, 'main.html')

def auth(request):
    if request.method == 'POST':
        if request.POST.get('button') == 'register':
            if create_user(request):
                return redirect('/')
        elif request.POST.get('button') == 'auth':
            if authenticate_user(request):
                return redirect('/')
    return render(request, 'auth.html')

def logout_view(request):
    logout(request)
    return redirect('/')