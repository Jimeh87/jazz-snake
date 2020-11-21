import random
from typing import Type

from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.stepdata import StepData, PointType
from jazz_snake.layer.path.pathscorer import PathScorer


class PathFollower:

    def __init__(self,
                 game_board: GameBoard,
                 point_type: PointType,
                 point_id,
                 distance,
                 you,
                 path_scorer_class: Type[PathScorer]):
        self._game_board = game_board
        self._point_type = point_type
        self._point_id = point_id
        self._distance = distance
        self._you_snake_id = you['id']
        self._you_snake_health = you['health']
        self._path_scorer_class = path_scorer_class

    def score_path(self, start_point):
        path = {
            'point_type': self._point_type,
            'point_id': self._point_id,
            'distance': self._distance,
            'points': [],
            'scores': [],
            'final_score': None
        }

        next_points = [start_point]
        while next_points:
            random.shuffle(next_points)
            current_point, score = self.get_point_with_lowest_score(next_points)
            path['scores'].append(score)
            path['points'].append(current_point)

            path_step = self.find_path_step(current_point)

            next_points.clear()
            for possible_next_point in path_step.nodes:
                possible_next_path_step = self.find_path_step(possible_next_point)
                if possible_next_path_step.distance != 0 and possible_next_path_step.distance < path_step.distance:
                    next_points.append(possible_next_point)

        path['final_score'] = self._path_scorer_class.calculate_final_score(self._distance, path['scores'])

        # flip orders of scores and points because they are created backwards
        path['points'].reverse()
        path['scores'].reverse()

        return path

    def find_path_step(self, point: ()) -> StepData:
        return self._game_board.get_cell_steps(point).get(self._point_type, self._point_id)

    def get_point_with_lowest_score(self, points):
        best_score = None
        best_point = None
        for point in points:
            score = self.score_point(point)
            if best_score is None or score < best_score:
                best_score = score
                best_point = point

        return best_point, best_score

    def score_point(self, point):
        return self._path_scorer_class(point=point,
                                       path_step=self.find_path_step(point),
                                       game_board=self._game_board,
                                       you_snake_id=self._you_snake_id,
                                       you_snake_health=self._you_snake_health).score_path()
