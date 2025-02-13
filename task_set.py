from typing import List, Dict
from task import Task
from task_type import TaskType
from task_difficulty import TaskDifficulty
from collections import Counter
import random


TASK_SET_SIZE = 20
TYPES_COUNT = 5


class TaskSet:

    def __init__(self, tasks: List[Task], user_statistics: Dict[str, float], reference_difficulty: float) -> None:
        self.tasks = tasks
        self.tasks_counter = self._count_types_of_tasks()
        self.avg_difficulty = self._count_avg_difficulty()
        self.fitness = self._calculate_fitness(user_statistics, reference_difficulty)
    
    
    def _count_types_of_tasks(self) -> dict:
        counter = {
            'MEMORY': 0,
            'ATTENTION':0,
            'RECOGNITION':0,
            'ACTION':0,
            'SPEECH':0
        }
        
        for task in self.tasks:
            task_type = task.task_type.name
            if task_type == "EXTRA":
                continue
            counter[task_type] += 1
            
        return counter
    
    
    def _count_avg_difficulty(self) -> float:
        
        return sum([task.difficulty.value for task in self.tasks]) / TASK_SET_SIZE
    
    
    # def _count_avg_duration(self) -> float:
        
    #     return sum([task.avg_time for task in self.tasks])
    
    
    def _calculate_fitness(self, user_statistics: Dict[str, float], reference_difficulty: float) -> float:
        a = 1
        b = 1
        '''
        TODO: добавить аргумент с реальными коэффициентами альфа, бета
        '''
        f1 = self._calculate_mean_absolute_error_of_tasks_distribution(user_statistics) # -> min
        f2 = self._calculate_mean_absolute_error_of_difficulty(reference_difficulty) # -> min
        
        return a*f1 + b*f2
    
    
    def _calculate_mean_absolute_error_of_tasks_distribution(self, user_statistics: Dict[str, float]) -> float:
        mae = 0
        sum_stat = sum(user_statistics.values())
        sorted_stat = [(k, v) for k,v in user_statistics.items()]
        sorted_stat.sort(key=lambda x: x[1])
        reference_distribution = dict()
        for i, stat in enumerate(sorted_stat):
            # (TASK_SET_SIZE - 5) учитывает, что для каждого типа есть хотя бы 1 задание (20 - 5 = 15)
            # в конце +1 чтобы вернуть сумму до 20
            reference_distribution[stat[0]] = ((sorted_stat[TYPES_COUNT - i - 1][1] * (TASK_SET_SIZE - 5)) / sum_stat) + 1
        for k in reference_distribution.keys():
            mae += abs(reference_distribution[k] - self.tasks_counter[k])
        
        return mae
    
    
    def _calculate_mean_absolute_error_of_difficulty(self, reference_difficulty: float) -> float:
        mae = abs(reference_difficulty - self.avg_difficulty)
        
        return mae
    
    
    def mutate(self) -> None:
        '''
        TODO: реаизовать мутацию
        '''
        pass
    
    
    def to_list(self) -> list:
        tasks = []
        for task in self.tasks:
            tasks.append((task.task_type.name, task.difficulty.value))
        
        return tasks