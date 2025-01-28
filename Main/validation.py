from .functions.user_functions import *
from django.http import JsonResponse

def validate_email(request):
    response = validate_register_email(request)
    return JsonResponse(response)

def validate_login_data(request):
    if not authenticate_user(request):
        response = {
            'wrong_data': 'wrong_data'
        }
        return JsonResponse(response)