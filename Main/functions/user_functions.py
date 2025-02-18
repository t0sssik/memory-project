from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ..models import Stats

def _validate_user(request):
    _email = request.POST.get('email')

    try:
        User.objects.get(username=_email)
    except:
        return True
    else:
        return False

def create_user(request):
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
    username = request.GET.get('email')
    response = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return response

def create_stats(user):
    stats = Stats.objects.create(user=user)
    return stats.save()