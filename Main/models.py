from symtable import Class

from django.db import models

# Create your models here.

class User(models.Model):
    pass

class Test(models.Model): # Номер теста для юзера
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    correct_memory = models.FloatField(default=0)
    correct_attention = models.FloatField(default=0)
    correct_recognition = models.FloatField(default=0)
    correct_action = models.FloatField(default=0)
    correct_speech = models.FloatField(default=0)

class Task(models.Model): #Банк заданий
    type = models.CharField(max_length=30) # Тип задания: Memory, Attention,
                                            # Recognition, Action, Speech, Extra
    difficulty = models.IntegerField() # Сложность от 1 до 3
    question = models.IntegerField() # Формулировка вопроса
    image = models.CharField(max_length=200) # Ссылка на изображения

class TaskTest(models.Model): # Для нахождения тасков каждого типа + Распределение по сложности для каждого типа
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    result = models.FloatField(default=0)