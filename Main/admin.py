from unittest import TestResult

from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Task)
admin.site.register(Test)
admin.site.register(TaskTest)
