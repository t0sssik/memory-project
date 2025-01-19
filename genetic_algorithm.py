from task_set import TaskSet
from task_set import MAX_TASK_SET_SIZE
from task import Task
from task_difficulty import TaskDifficulty
from task_type import TaskType
from typing import List, Tuple
import random


class GeneticAlgorithm:
    
    def __init__(self,
                 user_stat,
                 population_size: int=100,
                 num_of_candidates: int=20,
                 mutation_rate: float=0.01,
                 generations: int=100) -> None:
        self.user_statistics = user_stat
        self.population_size = population_size
        self.num_of_candidates = num_of_candidates
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = self._create_initial_population()
    
    
    def _create_initial_population(self) -> List[TaskSet]:      
        population = []
        for _ in range(self.population_size):
            population.append(TaskSet.generate_viable_set())
        
        return population
    
    
    def _sort_by_fitness(self) -> None:
        self.population.sort(key=lambda x: x.fitness(self.user_statistics), reverse=True)
        
        
    def _top_selection(self) -> List[TaskSet]:
        self._sort_by_fitness()
        
        return self.population[:2]
    
    
    def _roulette_selection(self) -> List[TaskSet]:
        '''
        TODO: реализовать метод отбора рулеткой
        '''
        pass
    
    
    def _competition_selection(self) -> List[TaskSet]:
        '''
        TODO: реализовать метод отбора соревнованием
        '''
        pass
    
    
    # def _crossover(self, selected_sets: Tuple[TaskSet, TaskSet]) -> List[TaskSet]:
    #     mask = [random.randint(0, 1) for _ in range(MAX_TASK_SET_SIZE)]
    #     child_1 = []
    #     child_2 = []
    #     for i, elem in enumerate(mask):
    #         if elem == 0:
    #             child_1.append(selected_sets[0].tasks[i])
    #             child_2.append(selected_sets[1].tasks[i])
    #         else:
    #             child_1.append(selected_sets[1].tasks[i])
    #             child_2.append(selected_sets[0].tasks[i])
        
    #     return [TaskSet(child_1), TaskSet(child_2)]

    
    def evolve(self, selection_method: str='top') -> TaskSet:
        '''
        Основной цикл эволюции генетического алгоритма.
        '''
        '''
        TODO: реализовать выбор метода отбора кандидатов
        '''
        for _ in range(self.generations):
            self._sort_by_fitness()
            self.population = self.population[:self.population_size]
            candidates = self.population[:self.num_of_candidates]
            while candidates:
                parents = (candidates.pop(0), candidates.pop(0))
                children = self._crossover(parents)
                self.population.extend(children)
        self._sort_by_fitness()
        
        return self.population[0]
    
    
if __name__ == '__main__':
    ga = GeneticAlgorithm(population_size=20, num_of_candidates=4, generations=10)
    best = ga.evolve()
    print(best)