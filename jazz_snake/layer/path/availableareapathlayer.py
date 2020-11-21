from jazz_snake.board.gameboard import GameBoard, RelativePoint
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.stepdata import PointType


class AvailableAreaPathLayer:
    LIFE_CYCLE = LayerLifeCycle.AREA_ANALYSIS

    def __init__(self, you_snake):
        self._you_snake_head = you_snake['head']
        self._you_snake_body = you_snake['body']

    def visit(self, game_board: GameBoard):
        cell_area = self.CellArea(game_board)

        neighbour_points = RelativePoint.get_neighbour_points((self._you_snake_head['x'], self._you_snake_head['y']))
        point_id = 0
        for neighbour_point in neighbour_points:
            cell_count = len(cell_area.collect(neighbour_point))
            score = game_board.get_total_cells() - cell_count + 300
            path = {
                'point_type': PointType.AVAILABLE_AREA,
                'point_id': 'area-' + str(point_id),
                'distance': cell_count,
                'points': [neighbour_point],
                'scores': [score],
                'final_score': score
            }

            game_board.add_path(path)

            point_id = point_id + 1

    class CellArea:

        def __init__(self, game_board: GameBoard):
            self._game_board = game_board

        def collect(self, point: (), points=None):
            if points is None:
                points = set()

            if point in points:
                return points

            if not self._game_board.get_cell_death_threat(point).is_cell_safe():
                return points

            points.add(point)

            next_points = RelativePoint.get_neighbour_points(point)

            for next_point in next_points:
                self.collect(next_point, points)

            return points
