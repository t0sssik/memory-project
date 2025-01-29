from datetime import datetime
from symtable import Class
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Test(models.Model): # Номер теста для юзера
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    correct_memory = models.FloatField(default=0)
    correct_attention = models.FloatField(default=0)
    correct_recognition = models.FloatField(default=0)
    correct_action = models.FloatField(default=0)
    correct_speech = models.FloatField(default=0)
    date = models.DateTimeField(default=datetime.now)

class Task(models.Model): #Банк заданий
    type = models.CharField(max_length=30) # Тип задания: Memory, Attention,
                                            # Recognition, Action, Speech, Extra
    difficulty = models.IntegerField() # Сложность от 1 до 3
    question = models.IntegerField() # Формулировка вопроса
    image = models.ImageField() # Изображение
    url = models.URLField() # Ссылка на изображения

class TaskTest(models.Model): # Для нахождения тасков каждого типа + Распределение по сложности для каждого типа
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    result = models.FloatField(default=0)