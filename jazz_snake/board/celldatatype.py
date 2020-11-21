from enum import Enum, unique
from typing import Type

from jazz_snake.board.deaththreatdata import DeathThreatDataAggregate
from jazz_snake.board.gameboarddata import GameBoardDataAggregate
from jazz_snake.board.simpledata import SimpleDataAggregate
from jazz_snake.board.stepdata import StepDataAggregate


@unique
class CellDataType(Enum):
    YOUR_HEAD = ('your_head', SimpleDataAggregate)
    DEATH_THREAT_LEVEL = ('death_threat', DeathThreatDataAggregate)
    STEP = ('steps', StepDataAggregate)
    FOOD = ('food', SimpleDataAggregate)
    DESIRED_PATH = ('desired_path', SimpleDataAggregate)

    def __init__(self, name, data_aggregate_type: Type[GameBoardDataAggregate]):
        self._name = name
        self.data_aggregate_type = data_aggregate_type
