from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from .functions.user_functions import *
from .functions.test_functions import *
from .functions.test_functions import get_today_test
from .functions.stats_functions import *
from alg.user_statistics import *
from alg.genetic_algorithm import *
import math

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)
            if request.POST.get("button") == 'start':
                return redirect(test)
        stats = Stats.objects.get(user=request.user)
        # Если пользователь не прошёл, то выдаётся первый тест
        if not Test.objects.all().filter(user=request.user, is_completed=True).exists():
            assign_first_test(request.user)
        is_completed = get_completion_status(user=request.user)
        if is_completed:
            result, value = get_test_result(user=request.user)
        else:
            result = 0
            value = 0
            if get_today_test(user=request.user) == False and Test.objects.filter(user=request.user).exists():
                ga = generate_test(request)
                generate_pdf(request.user)
        days = get_last_ten_days(user=request.user)
        # check_streak(user=request.user)
        context = {
            'stats': stats,
            'test': is_completed,
            'result': result,
            'value': value,
            'days': days,
            'test_url' : 'tests/' + str(get_today_test(user=request.user).id) + '.pdf',
        }
        return render(request, 'main.html', context)
    else:
        return render(request, 'home.html')

def first(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        info = get_start_info(request.POST)
        if request.POST.get("button") == 'start':
            return redirect('/test')
    return render(request, 'first.html')

def auth(request):
    if request.user.is_authenticated:
        return redirect('/')
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
        return redirect('/')
    else:
        if request.method == 'POST':
            result = request.session['result']
            if create_user(request):
                save_first_test(user=request.user, result=result)
                return redirect('/')
    return render(request, 'offer.html')

def test(request):
    user = request.user
    if not user.is_authenticated:
        tasks = get_first_test()
    else:
        tasks = get_today_tasks(user)
    if request.method == 'POST':
        if request.POST.get('button') == 'exit':
            if not user.is_authenticated:
                result = get_first_test_result(request.POST)
                request.session['result'] = result
                return redirect(end)
            else:
                update_test(user, request.POST)
                update_stat(user)
                return redirect('/test/end')
    return render(request, 'test.html', {'test': tasks})

def end(request):
    user = request.user
    if request.method == 'POST':
        if request.POST.get('button') == 'save':
            return redirect(offer)
    if user.is_authenticated:
        data = get_test_data(user)
    else:
        result = request.session['result']
        data = result
    context = {
        'memory': math.trunc(data['result_memory'] / max(1, data['max_memory']) * 100),
        'recognition': math.trunc(data['result_recognition'] / max(1, data['max_recognition']) * 100),
        'attention': math.trunc(data['result_attention'] / max(1, data['max_attention']) * 100),
        'action': math.trunc(data['result_action'] / max(1, data['max_action']) * 100),
        'speech': math.trunc(data['result_speech'] / max(1, data['max_speech']) * 100),
        'correct': data['result_memory'] + data['result_recognition'] + data['result_attention'] + data[
            'result_action'] + data['result_speech'],
        'proportion': math.trunc((data['result_memory'] + data['result_recognition'] + data['result_attention']
                                  + data['result_action'] + data['result_speech']) / 20 * 100),
    }
    return render(request, 'end.html', context)