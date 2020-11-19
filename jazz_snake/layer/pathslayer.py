import random

from jazz_snake.board.PointType import PointType
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle


class PathsLayer:

    LIFE_CYCLE = LayerLifeCycle.PATHING

    def __init__(self, you_snake):
        self._you = you_snake

    def visit(self, game_board: GameBoard):
        head_point = (self._you['head']['x'], self._you['head']['y'])
        points_with_directions = game_board.get_neighbour_cell_points_with_direction(head_point)

        paths = []
        for point_with_direction in points_with_directions:
            direction = point_with_direction['direction']
            start_point = point_with_direction['point']

            possible_paths = game_board.get_cell(start_point[0], start_point[1], CellDataType.STEPS)

            for possible_path in possible_paths:
                if possible_path['point_type'] == PointType.SNAKE_HEAD:
                    # TODO: At some point this would be a good snake killing path
                    pass
                elif possible_path['point_type'] == PointType.SNAKE_TAIL:
                    pass

                elif possible_path['point_type'] == PointType.FOOD:
                    point_type = possible_path['point_type']
                    point_id = possible_path['point_id']
                    distance = possible_path['distance']
                    path = {
                        'direction': direction,
                        'point_type': point_type,
                        'point_id': point_id,
                        'distance': distance,
                        'points': [],
                        'scores': []
                    }

                    current_distance = 0
                    next_points = [start_point]
                    while next_points:
                        current_distance = current_distance + 1
                        random.shuffle(next_points)
                        current_point, score = self.get_point_with_lowest_score(next_points,
                                                                                current_distance,
                                                                                point_id,
                                                                                game_board)
                        path['scores'].append(score)
                        path['points'].append(current_point)

                        point_step = self.find_point_step(current_point, point_id, game_board)

                        next_points.clear()
                        for possible_next_point in point_step['nodes']:
                            possible_next_point_step = self.find_point_step(possible_next_point, point_id, game_board)
                            if possible_next_point_step['distance'] < point_step['distance']:
                                next_points.append(possible_next_point)

                    path['final_score'] = sum(path['scores']) / (distance + 1)
                    paths.append(path)

        game_board.add_paths(paths)

    def find_point_step(self, point: (), point_id, game_board: GameBoard):
        steps = game_board.get_cell(point[0], point[1], CellDataType.STEPS)
        for step in steps:
            if step['point_id'] == point_id:
                return step

        return None

    def get_point_with_lowest_score(self, points, current_distance, point_id, game_board):
        best_score = None
        best_point = None
        for point in points:
            score = self.score_point(point, current_distance, point_id, game_board)
            if best_score is None or score < best_score:
                best_score = score
                best_point = point

        return best_point, best_score

    def score_point(self, point, current_distance, point_id, game_board):
        score = 0

        point_step = self.find_point_step(point, point_id, game_board)

        death_threat_level = game_board.get_final_cell(point[0], point[1])[CellDataType.DEATH_THREAT_LEVEL]
        score = score + (death_threat_level * 100)

        steps = game_board.get_cell(point[0], point[1], CellDataType.STEPS)
        tail_found = False
        for step in steps:
            if step['point_id'] == point_id:
                continue

            if step['point_type'] == PointType.FOOD:
                # alternative food on path
                score = score - 1
            elif step['point_type'] == PointType.SNAKE_HEAD:
                if step['point_id'] != self._you['id']:
                    other_snake_distance = point_step['distance']
                    if other_snake_distance < current_distance:
                        score = score + 300
                    elif other_snake_distance == current_distance:
                        score = score + 200
                    else:
                        score = score - 1
            elif step['point_type'] == PointType.SNAKE_TAIL:
                if step['point_id'] == 'tail-' + self._you['id']:
                    tail_found = True

        if tail_found:
            score = score - 1
        else:
            score = score + 400

        return score * (1 / float(current_distance))
