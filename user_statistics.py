from typing import Dict, Tuple
from task_type import TaskType
from task_difficulty import TaskDifficulty


class UserStatistics:
    
    def __init__(self, current_statistics: Dict[str, float], last_test_result: Dict[str, float]) -> None:
        self.current_statistics = current_statistics
        self.last_test_result = last_test_result
        
        
    def _update_statistics(self) -> Dict[str, float]:
        pass