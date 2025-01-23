from django.shortcuts import render
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
            create_user(request.POST)
    return render(request, 'auth.html')