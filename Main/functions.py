from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def create_user(response):
    if _validate_user(response):
        info = dict()
        info['first_name'] = response.get('first-name-reg')
        info['last_name'] = response.get('last-name-reg')
        info['email'] = response.get('email-reg')
        info['username'] = response.get('email-reg')
        info['password'] = response.get('password-reg')

        user = User.objects.create_user(**info)
        User.save(user)
        return True
    else:
        return False

def _validate_user(response):
    email = response.get('email-reg')

    try:
        User.objects.get(username=email)
    except:
        return True
    else:
        return False