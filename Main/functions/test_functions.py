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
    test = Test.objects.get(user=user)
    tasks = TaskTest.objects.all().filter(test=test, test__date__day=day, test__date__month=month, test__date__year=year).order_by('number')
    return tasks