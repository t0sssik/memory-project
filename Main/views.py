from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .functions import *
# Create your views here.

def home(request):
    return render(request, 'home.html')

def start(request):
    return render(request, 'start.html')

def main(request):
    return render(request, 'main.html')

def auth(request):
    if request.method == 'POST':
        if request.POST.get('button') == 'register':
            if create_user(request.POST):
                return redirect('/')
        elif request.POST.get('button') == 'auth':
            pass
    return render(request, 'auth.html')