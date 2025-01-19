from typing import List, Dict
from task import Task
from task_type import TaskType
from task_difficulty import TaskDifficulty
from user_statistics import UserStatistics
from collections import Counter
import random


TASK_SET_SIZE = 20
TYPES_COUNT = 5


class TaskSet:

    def __init__(self, tasks: List[Task]) -> None:
        self.tasks = tasks
        self.tasks_counter = self._count_types_of_tasks()
        self.avg_difficulty = self._count_avg_duration()
        
        
    def __str__(self) -> str:
        return f"{self.tasks} / ff: {self.fitness()}"
    
    
    def _count_types_of_tasks(self) -> dict:
        
        return dict(Counter(self.tasks))
    
    
    def _count_avg_difficulty(self) -> float:
        
        return sum([task.difficulty.value for task in self.tasks])
    
    
    def _count_avg_duration(self) -> float:
        
        return sum([task.avg_time for task in self.tasks])
    
    
    def fitness(self, user_statistics: Dict[str, float], reference_difficulty: float) -> float:
        a = 1
        b = 1
        g = 1
        '''
        TODO: добавить аргумент с реальными коэффициентами альфа, бета, гамма
        '''
        f1 = self._calculate_mean_absolute_error_of_tasks_distribution(user_statistics)
        f2 = self._calculate_mean_absolute_error_of_difficulty(reference_difficulty)
        f3 = self._calculate_f3()
        
        return a*f1 + b*f2 + g*f3
    
    
    def _calculate_mean_absolute_error_of_tasks_distribution(self, user_statistics: Dict[str, float]) -> float:
        mae = 0
        sum_stat = sum(user_statistics.values())
        sorted_stat = [(k, v) for k,v in user_statistics.items()].sort(key=lambda x: x[1])
        reference_distribution = dict()
        for i, stat in enumerate(sorted_stat):
            # (TASK_SET_SIZE - 5) учитывает, что для каждого типа есть хотя бы 1 задание (20 - 5 = 15)
            # в конце +1 чтобы вернуть сумму до 20
            reference_distribution[stat[0]] = ((sorted_stat[TYPES_COUNT - i - 1][1] * (TASK_SET_SIZE - 5)) / sum_stat) + 1
        for k in reference_distribution.keys():
            mae += abs(reference_distribution[k] - self.tasks_counter[k])
        
        return mae
    
    
    def _calculate_mean_absolute_error_of_difficulty(self, reference_difficulty: float) -> float:
        
        return abs(reference_difficulty - self.avg_difficulty)
    
    
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
        while size < TASK_SET_SIZE:
            rand_type = random.choice(list(TaskType))
            rand_difficulty = random.choice(list(TaskDifficulty))
            task = Task(rand_type, rand_difficulty)
            task_set.append(task)
            size += 1
        
        return TaskSet(task_set)