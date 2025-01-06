from typing import List
from task import Task
from task_type import TaskType
from task_difficulty import TaskDifficulty
from user_statistics import UserStatistics
from collections import Counter
import random


MAX_TASK_SET_SIZE = 15


class TaskSet:

    def __init__(self, tasks: List[Task]) -> None:
        self.tasks = tasks
        self.tasks_counter = self._count_types_of_tasks()
        self.avg_duration = self._count_avg_duration()
        
        
    def __str__(self) -> str:
        return f"{self.tasks} / ff: {self.fitness()}"
    
    
    def _count_types_of_tasks(self) -> dict:
        
        return dict(Counter(self.tasks))
    
    
    def _count_avg_duration(self) -> float:
        
        return sum([task.avg_time for task in self.tasks])
    
    
    def fitness(self, user_statistics) -> float:
        a = 1
        b = 1
        g = 1
        '''
        TODO: добавить аргумент с реальными коэффициентами альфа, бета, гамма
        '''
        f1 = self._calculate_mean_absolute_error_of_tasks_distribution(user_statistics)
        f2 = self._calculate_f2()
        f3 = self._calculate_f3()
        
        #return a*f1 - (b*f2 + g*f3)
        return 5
    
    
    def _calculate_mean_absolute_error_of_tasks_distribution(self, user_statistics) -> float:
        '''
        TODO: свзяать с user_statistics
        '''
        pass
    
    
    def _calculate_f2(self) -> float:
        '''
        TODO: свзяать с user_statistics
        '''
        pass
    
    
    def _calculate_f3(self) -> float:
        '''
        TODO: свзяать с user_statistics
        '''
        pass
    
    
    def mutate(self) -> None:
        pass
    
    
    @staticmethod
    def generate_viable_set() -> 'TaskSet':
        task_set = []
        size = 0
        
        # добавляем по 1 заданию каждого типа.
        for task_type in list(TaskType):
            rand_difficulty = random.choice(list(TaskDifficulty))
            task = Task(task_type, rand_difficulty)
            task_set.append(task)
            size += 1
            
        # добавляем случайные задания, пока есть место    
        while size < MAX_TASK_SET_SIZE:
            rand_type = random.choice(list(TaskType))
            rand_difficulty = random.choice(list(TaskDifficulty))
            task = Task(rand_type, rand_difficulty)
            task_set.append(task)
            size += 1
        
        return TaskSet(task_set)