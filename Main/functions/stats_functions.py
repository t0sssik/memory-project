from .test_functions import get_today_test, get_completion_status
from ..models import *
from datetime import timedelta

def get_previous_test(user):
    """
    Получает и возвращает данные за вчерашний тест
    :param user: Данные пользователя
    :return: Данные теста, если он есть, либо False
    """
    time = timezone.now() - timedelta(days=1)
    try:
        previous_test = Test.objects.get(user=user, date__day = time.date().day, date__month = time.date().month,
                                        date__year = time.date().year)
    except:
        previous_test = None
    else:
        previous_test = Test.objects.get(user=user, date__day=time.date().day, date__month=time.date().month,
                                         date__year=time.date().year)
    return previous_test

def update_stats(user):
    """
    Функция обновляет данные статистики после прохождения теста
    :param user: Данные о пользователе
    :return:
    """
    stats = Stats.objects.get(user=user)
    previous_test = get_previous_test(user)
    if previous_test is not None and previous_test.is_completed:
        streak = stats.streak + 1
        stats.streak = streak
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
    previous_test = get_previous_test(user)
    if not (previous_test is not None and previous_test.is_completed):
        if stat.streak > 0 and not get_completion_status(user):
            stat.streak = 0
    stat.save()
    return Stats.objects.get(user=user)