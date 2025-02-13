from enum import Enum


class TaskType(Enum):

    MEMORY = 1
    ATTENTION = 2
    RECOGNITION = 3
    ACTION = 4
    SPEECH = 5
    EXTRA = 0