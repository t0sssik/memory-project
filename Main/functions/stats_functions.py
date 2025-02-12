from ..models import *
from .test_functions import *

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

def update_stat(user):
    stat = Stats.objects.get(user=user)
    stat.completed = Test.objects.all().filter(user=user, is_completed=True).count()
    stat.save()
    return