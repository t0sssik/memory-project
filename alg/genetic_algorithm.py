from .task_set import TaskSet
from .task_set import TASK_SET_SIZE
from .task import Task
from .task_difficulty import TaskDifficulty
from .task_type import TaskType
from typing import List, Tuple
from .logger import Logger
import random
import yaml
from pathlib import Path


class GeneticAlgorithm:
    
    def __init__(self,
                 user_stat,
                 reference_difficulty,
                 hparams_conf_path: str,
                 logger: bool=True) -> None:
        if logger:
            self.logger = Logger(hparams_conf_path)
        else:
            self.logger = None
        self.user_statistics = user_stat
        self.reference_difficulty = reference_difficulty
        
        with open(Path(hparams_conf_path), 'r') as f:
            hparams = yaml.load(f, Loader=yaml.SafeLoader)
            
        self.population_size = hparams['population_size']
        self.num_of_candidates = hparams['num_of_candidates']
        if self.num_of_candidates % 2 != 0 or self.num_of_candidates == 0:
            raise Exception('num_of_candidates should be even')
        self.mutation_rate = hparams['mutation_rate']
        self.generations = hparams['generations']
        self.candidates_selection_method = hparams['candidates_selection_method']
        
        self.population = self._create_initial_population()
        
    
    def _create_initial_population(self) -> List[TaskSet]:      
        population = []
        for _ in range(self.population_size):
            population.append(self._create_dummy_taskset())
        
        return population
    
    
    def _create_dummy_taskset(self) -> TaskSet:
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
        
        return TaskSet(task_set, self.user_statistics, self.reference_difficulty)
    
    
    def _sort_by_fitness(self) -> None:
        self.population.sort(key=lambda x: x.fitness)
        
        
    def _top_selection(self) -> List[TaskSet]:
        self._sort_by_fitness()
        
        return self.population[:self.num_of_candidates]
    
    
    def _roulette_selection(self) -> List[TaskSet]:
        total_fitness = sum(ts.fitness for ts in self.population)
        selection_probs = [ts.fitness / total_fitness for ts in self.population]
        
        return random.choices(self.population, weights=selection_probs, k=self.num_of_candidates)
    
    
    def _competition_selection(self) -> List[TaskSet]:
        '''
        TODO: реализовать метод отбора соревнованием
        '''
        pass
    
    
    def _crossover(self, selected_sets: Tuple[TaskSet, TaskSet]) -> List[TaskSet]:
        mask = [random.randint(0, 1) for _ in range(TASK_SET_SIZE)]
        child_1 = []
        child_2 = []
        for i, elem in enumerate(mask):
            if elem == 0:
                child_1.append(selected_sets[0].tasks[i])
                child_2.append(selected_sets[1].tasks[i])
            else:
                child_1.append(selected_sets[1].tasks[i])
                child_2.append(selected_sets[0].tasks[i])
        
        return [TaskSet(child_1, self.user_statistics, self.reference_difficulty), TaskSet(child_2, self.user_statistics, self.reference_difficulty)]

    
    def _select_candidates(self) -> List[TaskSet]:
        if self.candidates_selection_method == "top":
            return self._top_selection()
        elif self.candidates_selection_method == "roulette":
            return self._roulette_selection()
        else:
            raise ValueError(f"Unknown selection method: {self.candidates_selection_method}")
    
    
    def evolve(self) -> TaskSet:
        '''
        Основной цикл эволюции генетического алгоритма.
        '''
        for i in range(self.generations):
            self._sort_by_fitness()
            if self.logger:
                self.logger.add_data(
                    i,
                    self.population[0].fitness,
                    self.population[0].avg_difficulty,
                    self.population[0].tasks_counter,
                )
            
            self.population = self.population[:self.population_size] # После скрещиваний оставляем исходный размер популяции
            
            candidates = self._select_candidates() # Выбор кандидатов для скрещивания
            
            # Цикл скрещивания
            while candidates:
                parents = (candidates.pop(0), candidates.pop(0))
                children = self._crossover(parents)
                self.population.extend(children)
                
        self._sort_by_fitness()
        if self.logger:
            self.logger.add_data(
                i,
                self.population[0].fitness,
                self.population[0].avg_difficulty,
                self.population[0].tasks_counter,
            )
            self.logger.save_data()
            self.logger.show_progress_plot()
            self.logger.show_avg_difficulty_plot()
            self.logger.show_tasks_counter_plot()
        
        return self.population[0]
    
    
if __name__ == '__main__':
    test_user_stat = {
        'MEMORY': 0.9,
        'ATTENTION':0.9,
        'RECOGNITION':0.9,
        'ACTION':0.9,
        'SPEECH':0.9
    }
    test_ref_dif = 2.8
    
    ga = GeneticAlgorithm(
        user_stat=test_user_stat,
        reference_difficulty=test_ref_dif,
        hparams_conf_path="hparams.yaml"
    )
    best = ga.evolve()
    print(best.to_list())