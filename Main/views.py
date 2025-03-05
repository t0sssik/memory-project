from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from alg.user_statistics import *
from alg.genetic_algorithm import *
from .models import Test
from .functions.stats_functions import (assign_first_test, generate_pdf, get_start_info, get_first_test, save_first_test,
                                       get_today_tasks, get_first_test_result, update_test, update_stat, get_test_data)
from .functions.user_functions import create_user, authenticate_user
from .functions.context_functions import get_end_context, get_index_context


def index(request):
    """
    Главное представление, которое отображает лэндинг в случае неавторизованного пользователя, либо основную страницу,
    если пользователь вошёл в аккаунт
    :param request: Запрос от браузера
    :return: Отображает страницу по шаблону в зависимости от данных
    """
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("button") == 'start':
                return redirect(test)
        # Если пользователь не прошёл, то выдаётся первый тест
        if not Test.objects.all().filter(user=request.user, is_completed=True).exists():
            assign_first_test(request.user)
            generate_pdf(request.user)
        # check_streak(user=request.user)
        context = get_index_context(request)
        return render(request, 'main.html', context)
    else:
        return render(request, 'home.html')

def first(request):
    """
    Представление для формы данных для прохождения теста в первый раз
    :param request: Запрос от браузера
    :return: Отображает страницу анкеты первого тестирования, если пользователь не авторизован
    """
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        info = get_start_info(request.POST)
        if request.POST.get("button") == 'start':
            return redirect('/test')
    return render(request, 'first.html')

def auth(request):
    """
    Представление для страницы регистрации\авторизации неавторизованного пользователя
    :param request: Запрос от браузера
    :return: Отображает страницу с шаблоном регистрации\авторизации
    """
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
    """
    Представление, которое пользователю выйти из аккаунта (без отображения)
    :param request: Запрос браузера
    :return:
    """
    logout(request)
    return redirect('/')

def offer(request):
    """
    Представление со страницей предложения зарегистрироваться после прохождения первого теста
    :param request: Запрос из браузера
    :return: Отображает страницу по шаблону
    """
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
    """
    Представление с основным тестовым экраном для оценивания заданий
    :param request: Запрос браузера
    :return: Отображает страницу по шаблону и переадресует в случае необходимости
    """
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
    """
    Отображение для страницы статистики после оценки тестирования с результатами
    :param request: Запрос из браузера
    :return: Отображает страницу с графиками и результатами тестирования или переадресует в случае необходимости
    """
    user = request.user
    if request.method == 'POST':
        if request.POST.get('button') == 'save':
            return redirect(offer)
    if user.is_authenticated:
        data = get_test_data(user)
    else:
        result = request.session['result']
        data = result
    context = get_end_context(data)
    return render(request, 'end.html', context)