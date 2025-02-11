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
    day = time[-2:]
    month = time[5:7]
    year = time[:4]
    test = Test.objects.get(user=user, date__day=day, date__month=month, date__year=year)
    tasks = TaskTest.objects.all().filter(test=test).order_by('number')
    return tasks