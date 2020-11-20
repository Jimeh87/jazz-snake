import random

from jazz_snake.board.pointtype import PointType
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard


class PathFollower:

    def __init__(self,
                 game_board: GameBoard,
                 point_type: PointType,
                 point_id, distance,
                 you_snake_id,
                 path_scorer_class):
        self._game_board = game_board
        self._point_type = point_type
        self._point_id = point_id
        self._distance = distance
        self._you_snake_id = you_snake_id
        self._path_scorer_class = path_scorer_class

    def score_path(self, direction, start_point):
        path = {
            'direction': direction,
            'point_type': self._point_type,
            'point_id': self._point_id,
            'distance': self._distance,
            'points': [],
            'scores': [],
            'final_score': None
        }

        current_distance = 0
        next_points = [start_point]
        while next_points:
            current_distance = current_distance + 1
            random.shuffle(next_points)
            current_point, score = self.get_point_with_lowest_score(next_points, current_distance)
            path['scores'].append(score)
            path['points'].append(current_point)

            path_step = self.find_path_step(current_point)

            next_points.clear()
            for possible_next_point in path_step['nodes']:
                possible_next_path_step = self.find_path_step(possible_next_point)
                if possible_next_path_step['distance'] < path_step['distance']:
                    next_points.append(possible_next_point)

        path['final_score'] = sum(path['scores']) / (self._distance + 1)

        return path

    def find_path_step(self, point: ()):
        steps = self._game_board.get_cell(point[0], point[1], CellDataType.STEPS)
        for step in steps:
            if step['point_id'] == self._point_id:
                return step

        return None

    def get_point_with_lowest_score(self, points, current_distance):
        best_score = None
        best_point = None
        for point in points:
            score = self.score_point(point, current_distance)
            if best_score is None or score < best_score:
                best_score = score
                best_point = point

        return best_point, best_score

    def score_point(self, point, current_distance):
        return self._path_scorer_class(point=point,
                                       current_distance=current_distance,
                                       path_step=self.find_path_step(point),
                                       game_board=self._game_board,
                                       you_snake_id=self._you_snake_id).score_path()
