from ..models import *
from .test_functions import *
from datetime import timedelta

def create_empty_dict():
    """
    Функция возвращает подготовленный пустой словарь для обработки данных тестов
    :return: Пустой словарь data
    """
    data=dict()
    data['max_memory'] = []
    data['max_attention'] = []
    data['max_recognition'] = []
    data['max_speech'] = []
    data['max_action'] = []
    data['result_memory'] = []
    data['result_attention'] = []
    data['result_recognition'] = []
    data['result_speech'] = []
    data['result_action'] = []
    data['easy'] = []
    data['medium'] = []
    data['hard'] = []
    return data

def get_latest_test_data(tests):
    """
    Функция возвращает словарь с данными, где каждый элемент ключа является списком
    :param tests: QuerySet, состоящий из тестов.
    :return: Словарь списков
    """
    data = create_empty_dict()
    for test in tests:
        tasks = TaskTest.objects.all().filter(test=test).order_by('number')
        data['max_memory'].append(len(tasks.filter(task__type='memory')))
        data['max_attention'].append(len(tasks.filter(task__type='attention')))
        data['max_recognition'].append(len(tasks.filter(task__type='recognition')))
        data['max_speech'].append(len(tasks.filter(task__type='speech')))
        data['max_action'].append(len(tasks.filter(task__type='action')))
        data['result_memory'].append(test.correct_memory)
        data['result_attention'].append(test.correct_attention)
        data['result_recognition'].append(test.correct_recognition)
        data['result_speech'].append(test.correct_speech)
        data['result_action'].append(test.correct_action)
        data['easy'].append(len(tasks.filter(task__difficulty=1)))
        data['medium'].append(len(tasks.filter(task__difficulty=2)))
        data['hard'].append(len(tasks.filter(task__difficulty=3)))
    return data

def update_stat(user):
    stat = Stats.objects.get(user=user)
    stat.completed = Test.objects.all().filter(user=user, is_completed=True).count()
    stat.save()
    return

def check_streak(user):
    previous_day = timezone.now() + timedelta(days=-1)
    test = Test.objects.get(user=user, date=previous_day)
    stat = Stats.objects.get(user=user)

    if test is not None and test.is_completed:
        stat.streak += 1
        stat.best_streak = max(stat.best_streak, stat.streak)
    else:
        stat.best_streak = max(stat.best_streak, stat.streak)
        stat.streak = 0
    stat.save()
    return