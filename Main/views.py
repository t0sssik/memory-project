from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from Main.functions.user_functions import *
from .functions.test_functions import *
# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return render(request, 'home.html')

def first(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    if request.method == "POST":
        info = get_start_info(request.POST)
    return render(request, 'first.html')

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

def offer(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        if request.method == 'POST':
            if create_user(request):
                return redirect('/')
    return render(request, 'offer.html')

def test(request):
    return render(request, 'test.html')