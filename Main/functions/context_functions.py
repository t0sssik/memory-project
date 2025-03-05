import math
from .stats_functions import check_stats
from .test_functions import (get_today_test, get_last_ten_days, get_completion_status, generate_test, generate_pdf,
                              get_test_result)
from ..models import Stats, Test


def get_end_context(data):
    """
    Функция возвращающая контекст для end представления
    :param data: Данные, полученные с результатами теста
    :return: Словарь с данными, необходимыми в шаблоне
    """
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
    return context

def get_index_context(request):
    """
    Возвращает контекст для index представления
    :param request: запрос, отправленный пользователям в представлении
    :return: Словарь с данными, необходимыми для шаблона
    """
    days = get_last_ten_days(user=request.user)
    is_completed = get_completion_status(user=request.user)
    stats = check_stats(user=request.user)

    if is_completed:
        result, value = get_test_result(user=request.user)
    else:
        result = 0
        value = 0
        if get_today_test(user=request.user) == False and Test.objects.filter(user=request.user).exists():
            ga = generate_test(request)
            generate_pdf(request.user)
    context = {
        'stats': stats,
        'test': is_completed,
        'result': result,
        'value': value,
        'days': days,
        'test_url': 'tests/' + str(get_today_test(user=request.user).id) + '.pdf',
    }
    return context