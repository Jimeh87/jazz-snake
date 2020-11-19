from queue import Queue

from jazz_snake.board.PointType import PointType
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle


class StepsFromPointLayer:
    LIFE_CYCLE = LayerLifeCycle.AREA_ANALYSIS

    def __init__(self, start_cell: {}, point_type: PointType, point_id):
        self._start_point = (start_cell['x'], start_cell['y'])
        self._point_type = point_type
        self._point_id = point_id

    def visit(self, game_board: GameBoard):
        point_data = self.determine_steps(self._start_point, game_board)

        for point, data in point_data.items():
            steps_data = {
                'point_type': self._point_type,
                'point_id': self._point_id,
                'distance': data['distance'],
                'nodes': data['nodes']
            }
            game_board.set_cell(point[0], point[1], CellDataType.STEPS, steps_data)

    @staticmethod
    def determine_steps(start_point: (), game_board: GameBoard) -> dict:
        frontier = Queue()
        frontier.put(start_point)
        point_data = dict()
        point_data[start_point] = {
            'distance': 0,
            'nodes': []
        }

        while not frontier.empty():
            current_point = frontier.get()
            for next_point in game_board.get_neighbour_cell_points(current_point):
                if next_point not in point_data and game_board.is_cell_safe(next_point[0], next_point[1]):
                    frontier.put(next_point)
                    point_data[current_point]['nodes'].append(next_point)
                    point_data[next_point] = {
                        'distance': point_data[current_point]['distance'] + 1,
                        'nodes': [current_point]
                    }

        return point_data
