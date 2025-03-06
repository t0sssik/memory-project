from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ..models import Stats

def _validate_user(request):
    """
    Функция проверяет данные пользователя на уникальность
    :param request: Запрос из браузера
    :return: True или False в зависимости от результата
    """
    _email = request.POST.get('email')

    try:
        User.objects.get(username=_email)
    except:
        return True
    else:
        return False

def create_user(request):
    """
    Функция обрабатывает запроси и создаёт объект User в модель User
    :param request: Запрос из браузера
    :return: True или False в случае успеха или неудачи
    """
    if _validate_user(request):
        info = dict()
        info['first_name'] = request.POST.get('first-name')
        info['last_name'] = request.POST.get('last-name')
        info['email'] = request.POST.get('email')
        info['username'] = request.POST.get('email')
        info['password'] = request.POST.get('password')

        user = User.objects.create_user(**info)
        User.save(user)
        create_stats(user)

        authenticate_user(request)
        return True
    else:
        return False

def authenticate_user(request):
    """
    Функция авторизует пользователя, если пользователь существует
    :param request: Запрос из браузера
    :return: True в случае успеха, иначе False
    """
    if not _validate_user(request):
        user = authenticate(request, username=request.POST.get('email'),
                            password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return True
        else:
            return False
    else:
        return False

def validate_register_email(request):
    """
    Функция проверяет данные пользователя на уникальность
    :param request: Запрос из браузера
    :return: True или False в зависимости от результата
    """
    username = request.GET.get('email')
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return response

def create_stats(user):
    """
    Создаёт данные о статистике пользователя в БД
    :param user: данные о пользователе
    :return: Данные сохранённые в модели Stats
    """
    stats = Stats.objects.create(user=user)
    return stats.save()

def change_password(request):
    user = User.objects.get(username=request.user.username)
    old_password = request.POST.get('old-pass')
    new_password = request.POST.get('new-pass')
    confirm_password = request.POST.get('new-pass-repeat')
    if user.check_password(old_password) and new_password == confirm_password:
        user.set_password(new_password)
        user.save()
        return True
    return False