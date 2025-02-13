from typing import Dict
import pandas as pd
from task_set import TASK_SET_SIZE


class UserStatistics:
    
    def __init__(self, user_data: dict) -> None:
        self.user_data = pd.DataFrame(user_data).tail(10)
        self.user_stat = self._get_user_stat()
        self.user_reference_difficulty = self._get_reference_difficulty()
        
        
    def _get_user_stat(self) -> Dict[str, float]:
        user_stat = {
            'MEMORY': self.user_data["result_memory"].sum() / self.user_data["max_memory"].sum(),
            'ATTENTION': self.user_data["result_attention"].sum() / self.user_data["max_attention"].sum(),
            'RECOGNITION': self.user_data["result_recognition"].sum() / self.user_data["max_recognition"].sum(),
            'ACTION': self.user_data["result_action"].sum() / self.user_data["max_action"].sum(),
            'SPEECH': self.user_data["result_speech"].sum() / self.user_data["max_speech"].sum()
        }

        return user_stat
    
    def _get_reference_difficulty(self) -> float:
        self.user_data["avg_difficulty"] = (self.user_data["easy"] + self.user_data["medium"] * 2 + self.user_data["hard"] * 3) / TASK_SET_SIZE
        user_score = (self.user_data["result_memory"] + 
                      self.user_data["result_attention"] + 
                      self.user_data["result_recognition"] + 
                      self.user_data["result_action"] + 
                      self.user_data["result_speech"])
        max_score = (self.user_data["max_memory"] + 
                      self.user_data["max_attention"] + 
                      self.user_data["max_recognition"] + 
                      self.user_data["max_action"] + 
                      self.user_data["max_speech"])
        self.user_data["avg_difficulty"] = self.user_data["avg_difficulty"] * (user_score / max_score)
        reference_difficulty = self.user_data["avg_difficulty"].mean()
        
        return reference_difficulty