from .task_type import TaskType
from .task_difficulty import TaskDifficulty


class Task:

    def __init__(self, task_type: TaskType, difficulty: TaskDifficulty, avg_time: float=3) -> None:
        self.task_type = task_type
        self.difficulty = difficulty
        self.avg_time = avg_time
        
        
    def __str__(self) -> str:
        
        return f"{self.task_type.name}/{self.difficulty.name}/{self.avg_time}"
