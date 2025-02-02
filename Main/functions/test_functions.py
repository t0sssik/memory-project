from django.contrib.auth.models import User
from ..models import *
from django.utils import timezone

def get_start_info(data):
    info = dict()
    info['education'] = data['education']
    info['problem'] = int(data['problems'])
    info['disease'] = int(data['disease'])
    return info

def get_today_test(user):
    time = str(timezone.now())[:10]
    test = Test.objects.get(user=user)
    tasks = TaskTest.objects.all().filter(test=test).order_by('task__number')
    return tasks