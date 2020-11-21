from queue import Queue

from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard, RelativePoint
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.stepdata import PointType, StepData


class StepsFromPointLayer:
    LIFE_CYCLE = LayerLifeCycle.AREA_ANALYSIS

    def __init__(self, start_cell: {}, point_type: PointType, point_id):
        self._start_point = (start_cell['x'], start_cell['y'])
        self._point_type = point_type
        self._point_id = point_id

    def visit(self, game_board: GameBoard):
        point_data = self.determine_steps(self._start_point, game_board)

        for point, data in point_data.items():
            game_board.set_cell(point, CellDataType.STEP, StepData(self._point_type,
                                                                   self._point_id,
                                                                   data['distance'],
                                                                   data['nodes']))

    def determine_steps(self, start_point: (), game_board: GameBoard) -> dict:
        frontier = Queue()
        frontier.put(start_point)
        point_data = dict()
        point_data[start_point] = {
            'distance': 0,
            'nodes': []
        }

        while not frontier.empty():
            current_point = frontier.get()
            for next_point in RelativePoint.get_neighbour_points(current_point):
                next_distance = point_data[current_point]['distance'] + 1
                # TODO hack to keep snake tail calc working. snake tail goes backwards to death threat future stuff doesn't work
                cell_safe_distance = None if self._point_type == PointType.SNAKE_TAIL else next_distance
                if next_point not in point_data \
                        and game_board.get_cell_death_threat(next_point).is_cell_safe(cell_safe_distance):
                    frontier.put(next_point)
                    point_data[current_point]['nodes'].append(next_point)
                    point_data[next_point] = {
                        'distance': next_distance,
                        'nodes': [current_point]
                    }

        return point_data
