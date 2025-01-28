from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from Main.functions.user_functions import *
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return render(request, 'home.html')

def start(request):
    return render(request, 'start.html')

def auth(request):
    if request.method == 'POST':
        if request.POST.get('button') == 'register':
            if create_user(request):
                return redirect('/')
        elif request.method == "POST":
            if authenticate_user(request):
                return JsonResponse({"is_ok": True})
            else:
                return JsonResponse({"is_ok": False})
    return render(request, 'auth.html')

def logout_view(request):
    logout(request)
    return redirect('/')