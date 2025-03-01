import datetime
import math
from datetime import timedelta
from collections import deque

from reportlab.pdfgen.textobject import PDFTextObject

from ..models import *
from ..models import Task as TaskModel
from django.utils import timezone
from alg.genetic_algorithm import *
from alg.user_statistics import *
from .stats_functions import get_latest_test_data
import random
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph

pdfmetrics.registerFont(TTFont('CoFoSans', 'Main/static/fonts/CoFoSans-Regular.ttf'))

PAGE_WIDTH = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]


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
    time = str(datetime.now() + timedelta(hours=3))[:10]
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
        test = Test.objects.all().filter(date__day=day.day, date__month=day.month, date__year=day.year, user=user)
        if test.count()>0:
            is_completed = Test.objects.get(date__day=day.day, date__month=day.month, date__year=day.year, user=user).is_completed
        else:
            is_completed = False
        data.appendleft([week_days[day.weekday()], is_completed])
    return data

def generate_test(request):
    tests = get_latest_tests(user=request.user)
    data = get_latest_test_data(tests)
    user_stats = UserStatistics(data)
    user_stat = user_stats.user_stat
    user_ref_diff = user_stats.user_reference_difficulty
    ga = GeneticAlgorithm(user_stat, user_ref_diff, hparams_conf_path='alg/hparams.yaml')
    best = ga.evolve().to_list()
    user = request.user
    date = datetime.now() + timedelta(hours=3)
    test = Test.objects.create(user=user, date=date, is_completed=False)
    test.save()
    number = 0
    for cell in best:
        number = number + 1
        task = TaskModel.objects.all().filter(type=cell[0].lower(), difficulty=cell[1])
        random_task = random.choice(task)
        count = 0
        while TaskTest.objects.filter(task=random_task, test=test).exists():
            if count > len(task):
                break
            random_task = random.choice(task)
            count += 1
        TaskTest.objects.create(task=random_task, test=test, number=number)
    return best


def get_test_data(user):
    """
    Функция возвращает данные о сегодняшнем тесте в виде словаря
    :param user: ID пользователя
    :return: Словарь с данными
    """
    data = dict()
    test = get_today_test(user)
    tasks = get_today_tasks(user)
    data = get_max_values(data, tasks)
    data = get_current_values(data, test)
    data = get_difficulty_values(data, tasks)
    return data

def get_max_values(data, tasks):
    """
    Функция возвращает данные в виде словаря о максимально возможных баллах по видам заданий
    :param data: Словарь для добавления данных
    :param tasks: Список заданий в виде QuerySet
    :return: Словарь с новыми данными
    """
    data['max_memory'] = len(tasks.filter(task__type='memory'))
    data['max_attention'] = len(tasks.filter(task__type='attention'))
    data['max_recognition'] = len(tasks.filter(task__type='recognition'))
    data['max_speech'] = len(tasks.filter(task__type='speech'))
    data['max_action'] = len(tasks.filter(task__type='action'))
    return data

def get_current_values(data, test):
    """
    Функция возвращает полученные пользователем результаты
    :param data: Словарь с данными
    :param test: ID теста
    :return: Обновлённый словарь с данными
    """
    data['result_memory'] = test.correct_memory
    data['result_attention'] = test.correct_attention
    data['result_recognition'] = test.correct_recognition
    data['result_speech'] = test.correct_speech
    data['result_action'] = test.correct_action
    return data

def get_difficulty_values(data, tasks):
    """
    Функция возвращает словарь с обновлёнными данными о количестве заданий разного уровня сложности
    :param data: Словарь с данными
    :param tasks: Список заданий в виде QuerySet
    :return: Словарь с обновлёнными данными
    """
    data['easy'] = len(tasks.filter(task__difficulty=1))
    data['medium'] = len(tasks.filter(task__difficulty=2))
    data['hard'] = len(tasks.filter(task__difficulty=3))
    return data

def get_first_test():
    user = User.objects.get(username='Anon')
    test = Test.objects.get(user=user)
    tasks = TaskTest.objects.all().filter(test=test).order_by('number')
    return tasks

def get_first_test_result(request):
    result = dict()
    tasks = request
    user = User.objects.get(username='Anon')
    task_types = TaskTest.objects.all().filter(test__user=user)
    result['result_recognition'] = 0
    result['result_memory'] = 0
    result['result_speech'] = 0
    result['result_attention'] = 0
    result['result_action'] = 0
    result['max_recognition'] = task_types.filter(task__type='recognition').count()
    result['max_memory'] = task_types.filter(task__type='memory').count()
    result['max_speech'] = task_types.filter(task__type='speech').count()
    result['max_attention'] = task_types.filter(task__type='attention').count()
    result['max_action'] = task_types.filter(task__type='action').count()
    for i in range(20):
        task = tasks.get('answer'+str(i+1))
        task_type = task_types.get(number=i+1).task.type

        if task_type == 'memory':
            result['result_memory'] += float(task)
        elif task_type == 'attention':
            result['result_attention'] += float(task)
        elif task_type == 'recognition':
            result['result_recognition'] += float(task)
        elif task_type == 'speech':
            result['result_speech'] += float(task)
        elif task_type == 'action':
            result['result_action'] += float(task)

    return result

def save_first_test(user, result):
    test = Test.objects.create(user=user, date=datetime.now() + timedelta(hours=3), is_completed=True)
    test.correct_memory = result['result_memory']
    test.correct_attention = result['result_attention']
    test.correct_recognition = result['result_recognition']
    test.correct_speech = result['result_speech']
    test.correct_action = result['result_action']
    test.save()
    anon_user = User.objects.get(username='Anon')
    anon_tasks = get_first_test()
    for anon_task in anon_tasks:
        TaskTest.objects.create(test=test, number=anon_task.number, task=anon_task.task)

    return True

def assign_first_test(user):
    test = Test.objects.create(user=user, date=datetime.now() + timedelta(hours=3), is_completed=False)
    anon_user = User.objects.get(username='Anon')
    anon_tasks = get_first_test()
    for anon_task in anon_tasks:
        TaskTest.objects.create(test=test, number=anon_task.number, task=anon_task.task)
    return True

def generate_pdf(user):
    tasks = get_today_tasks(user)
    c = canvas.Canvas('Hello.pdf')
    c.translate(1 * cm, -1 * cm)
    c.setFont('CoFoSans', 16)
    count = 0
    y = PAGE_HEIGHT
    for task in tasks:
        count += 1
        text_object = c.beginText(0, y)
        if len(task.task.question) > 78:
            text_object.textLines(str(task.number) + ') ' + task.task.test_question[:66] + '\n' +
                                  task.task.test_question[66:len(task.task.test_question)])
        else:
            text_object.textLines(str(task.number) + ') ' + task.task.test_question)
        c.drawText(text_object)
        c.drawImage('Main/static/tasks/task' + str(task.task.id) + '.png', 0, y-255, width=400, height=230)
        y -= 275
        if count % 3 == 0 and count != len(tasks):
            c.showPage()
            c.setFont('CoFoSans', 16)
            c.translate(1 * cm, -1 * cm)
            y = PAGE_HEIGHT
    c.showPage()
    c.save()