from ..models import *
from datetime import timedelta
from .test_functions import get_completion_status

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

def update_stats(user):
    """
    Функция обновляет данные статистики после прохождения теста
    :param user: Данные о пользователе
    :return:
    """
    stats = Stats.objects.get(user=user)
    time = timezone.now().date() - timedelta(days=1)
    previous_test = Test.objects.filter(user=user, date = time)
    if previous_test.count() > 0 is not None and Test.objects.get(user=user, date=time).is_completed:
        streak = stats.streak + 1
        stats.best_streak = max(streak, stats.best_streak)
    else:
        stats.streak = 1
        stats.best_streak = max(stats.streak, stats.best_streak)
    stats.save()
    return

def check_stats(user):
    """
    Получает и проверяет данные о статистике пользователя
    :param user: Данные о пользователе
    :return: Возвращает данные о пользователе
    """
    stat = Stats.objects.get(user=user)
    stat.completed = Test.objects.all().filter(user=user, is_completed=True).count()
    stat.save()
    return Stats.objects.get(user=user)