from django.shortcuts import render, redirect
from django.http import JsonResponse
from Main.functions.user_functions import *
import json
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
            else:
                return render(request, 'auth.html')
    return render(request, 'auth.html')

def validate_email(request):
    username = request.GET.get('email')
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(response)

def logout_view(request):
    logout(request)
    return redirect('/')