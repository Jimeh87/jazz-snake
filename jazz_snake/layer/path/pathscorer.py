from abc import abstractmethod

from jazz_snake.board.pointtype import PointType
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard


class PathScorer:

    def __init__(self, point: (), current_distance, path_step, game_board: GameBoard, you_snake_id, you_snake_health):
        self.point = point
        self.current_distance = current_distance
        self.path_step = path_step
        self.game_board = game_board
        self.you_snake_id = you_snake_id
        self.you_snake_health = you_snake_health

    def get_death_threat_level(self):
        return self.game_board.get_final_cell(self.point[0], self.point[1])[CellDataType.DEATH_THREAT_LEVEL]

    def get_steps(self) -> []:
        return self.game_board.get_cell(self.point[0], self.point[1], CellDataType.STEPS)

    def has_your_tail_in_path(self):
        return any(self.is_your_tail_step(step) for step in self.get_steps())

    def is_your_tail_step(self, step):
        return step['point_type'] == PointType.SNAKE_TAIL and step['point_id'] == 'tail-' + self.you_snake_id

    @staticmethod
    @abstractmethod
    def can_score_path(step):
        pass

    @staticmethod
    @abstractmethod
    def calculate_final_score(distance, scores):
        pass

    @abstractmethod
    def score_path(self):
        pass
