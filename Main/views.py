from django.shortcuts import render, redirect
from .functions import get_registration_info
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):
    return render(request, 'home.html')

def start(request):
    return render(request, 'start.html')

def main(request):
    return render(request, 'main.html')

def auth(response):
    if response.method == "POST":
        info = get_registration_info(response.POST)

    return render(response, "auth.html")