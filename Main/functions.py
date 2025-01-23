def get_registration_info(response):
    info = dict()
    info['name'] = response.get('name-reg')
    info['surname'] = response.get('surname-reg')
    info['email'] = response.get('login-reg')
    info['password'] = response.get('pass-reg')

    print(info)
    return info