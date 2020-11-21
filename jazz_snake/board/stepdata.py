from enum import Enum

from jazz_snake.board.gameboarddata import GameBoardData, GameBoardDataAggregate


class PointType(Enum):
    SNAKE_HEAD = 'SNAKE_HEAD'
    FOOD = 'FOOD'
    SNAKE_TAIL = 'TAIL'
    AVAILABLE_AREA = 'AVAILABLE_AREA'


class StepData(GameBoardData):

    def __init__(self, point_type: PointType, point_id, distance: int, nodes: [()]):
        self.point_type = point_type
        self.point_id = point_id
        self.distance = distance
        self.nodes = nodes

    def is_same_path(self, step_data):
        return self.is_on_path(step_data.point_type, step_data.point_id)

    def is_on_path(self, point_type: PointType, point_id):
        return point_type == self.point_type and point_id == self.point_id


class StepDataAggregate(GameBoardDataAggregate):

    def __init__(self):
        self.steps_data: [StepData] = []

    def add_data(self, data: GameBoardData):
        self.steps_data.append(data)

    def get(self, point_type: PointType, point_id):
        for step in self.steps_data:
            if step.is_on_path(point_type, point_id):
                return step

        return None

    def to_string(self) -> str:
        return ", ".join("type[{}] id[{}] distance[{}]".format(d.point_type, d.point_id, d.distance) for d in self.steps_data)
