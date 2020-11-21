from abc import abstractmethod

from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.goaltype import GoalType
from jazz_snake.board.stepdata import StepData, PointType


class PathScorer:

    def __init__(self, point: (), path_step: StepData, game_board: GameBoard, you_snake_id, you_snake_health):
        self.point = point
        self.path_step = path_step
        self.game_board = game_board
        self.you_snake_id = you_snake_id
        self.you_snake_health = you_snake_health

    def is_head_attack_goal_on_point(self):
        for goal in self.game_board.get_goals():
            if goal['type'] == GoalType.HEAD_ATTACK and goal['point'] == self.point:
                return True
        return False

    def get_death_threat_level(self):
        # FIXME: hack to keep snake tail checks working which is traversed backwards
        distance = None if self.path_step.point_type == PointType.SNAKE_TAIL else self.path_step.distance
        return self.game_board.get_cell_death_threat(self.point).get_death_threat_level(distance)

    def get_steps(self) -> [StepData]:
        return self.game_board.get_cell_steps(self.point).steps_data

    def has_your_tail_in_path(self):
        return any(self.is_your_tail_step(step) for step in self.get_steps())

    def is_your_tail_step(self, step: StepData):
        # TODO Should probably make sure path to tail is safe as well
        return step.point_type == PointType.SNAKE_TAIL and step.point_id == 'tail-' + self.you_snake_id

    @staticmethod
    @abstractmethod
    def can_score_path(step: StepData, goal_type: GoalType, you_snake_id):
        pass

    @staticmethod
    @abstractmethod
    def calculate_final_score(distance, scores):
        pass

    @abstractmethod
    def score_path(self):
        pass
