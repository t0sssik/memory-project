from django.contrib.auth.models import User

def create_user(response):
    info = dict()
    info['first_name'] = response.get('first-name-reg')
    info['last_name'] = response.get('last-name-reg')
    info['email'] = response.get('email-reg')
    info['username'] = response.get('email-reg')
    info['password'] = response.get('password-reg')

    user = User.objects.create_user(**info)
    User.save(user)
    return info