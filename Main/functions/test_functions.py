import datetime
import math
from datetime import timedelta
from collections import deque
from ..models import *
from django.utils import timezone

def get_start_info(data):
    """
    Функция возвращает структурированную информацию в виде словаря в странице старта первого теста
    :param data: Данные полученные с формы методом POST
    :return: Возвращает словарь с обработанной информацией
    """
    info = dict()
    info['education'] = data['education']
    info['problem'] = int(data['problems'])
    info['disease'] = int(data['disease'])
    return info

def get_today_test(user):
    """
    Функция возвращает ID теста на сегодня для пользователя
    :param user: ID Пользователя
    :return: ID теста
    """
    time = str(timezone.now())[:10]
    day = time[-2:]
    month = time[5:7]
    year = time[:4]
    try:
        test = Test.objects.get(user=user, date__day=day, date__month=month, date__year=year)
    except:
        return False
    else:
        return Test.objects.get(user=user, date__day=day, date__month=month, date__year=year)

def get_today_tasks(user):
    """
    Функция возвращает список заданий для пользователя на сегодня
    :param user: ID пользователя
    :return: QuerySet модели TaskTest
    """
    test = get_today_test(user)
    tasks = TaskTest.objects.all().filter(test=test).order_by('number')
    return tasks


def get_latest_tests(user):
    """
    Функция возвращает QuerySet из 10 последних или менее тестов
    :param user: ID пользователя
    :return: QuerySet тестов
    """
    tests = Test.objects.filter(user=user).order_by('-date')[:10]
    return tests

def update_test(user, data):
    test = get_today_test(user)
    tasks = get_today_tasks(user).order_by('number')
    for i in range(min(24,len(tasks))):
        task = tasks[i]
        task.result = float(data['answer' + str(i+1)])
        task.save()

        if task.task.type == 'memory':
            test.correct_memory += task.result
        elif task.task.type == 'attention':
            test.correct_attention += task.result
        elif task.task.type == 'recognition':
            test.correct_recognition += task.result
        elif task.task.type == 'speech':
            test.correct_speech += task.result
        elif task.task.type == 'action':
            test.correct_action += task.result
    test.is_completed = True
    test.save()
    return

def get_completion_status(user):
    test = get_today_test(user=user)
    if test is False:
        is_completed = False
    else:
        is_completed = test.is_completed
    return is_completed

def get_test_result(user):
    test = get_today_test(user)
    value = (test.correct_memory + test.correct_attention + test.correct_recognition + test.correct_speech
              + test.correct_action)
    result = math.trunc(value / 24 * 100)
    return result, value

def get_last_ten_days(user):
    data = deque()
    week_days = ["ПН", "ВТ",
                   "СР", "ЧТ",
                   "ПТ", "СБ",
                   "ВС"]
    for i in range(10):
        day = datetime.now() + timedelta(hours=3) - timedelta(days=i)
        test = Test.objects.all().filter(date__day=day.day, date__month=day.month, date__year=day.year).count()
        data.appendleft([week_days[day.weekday()], test])
    print(data)
    return data