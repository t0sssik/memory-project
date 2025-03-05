from .functions.user_functions import *
from django.http import JsonResponse

def validate_email(request):
    """
    отображение необходимо для валидации пользователя при регистрации на фронт-энде с помощью Ajax
    :param request: запрос из браузера
    :return: Json-ответ с данными о попытке регистрации
    """
    response = validate_register_email(request)
    return JsonResponse(response)

def validate_login_data(request):
    """
    отображение необходимо для валидации пользователя при авторизации на фронт-энде с помощью Ajax
    :param request: запрос из браузера
    :return: Json-ответ с данными о попытке авторизации
    """
    if not authenticate_user(request):
        response = {
            'wrong_data': 'wrong_data'
        }
        return JsonResponse(response)