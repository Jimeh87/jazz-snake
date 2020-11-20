from enum import Enum


class PointType(Enum):
    SNAKE_HEAD = 'SNAKE_HEAD'
    FOOD = 'FOOD'
    SNAKE_TAIL = 'TAIL'
    AVAILABLE_AREA = 'AVAILABLE_AREA'
