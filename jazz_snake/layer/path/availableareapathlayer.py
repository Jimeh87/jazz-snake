from jazz_snake.board.pointtype import PointType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle


class AvailableAreaPathLayer:
    LIFE_CYCLE = LayerLifeCycle.AREA_ANALYSIS

    def __init__(self, you_snake):
        self._you_snake_head = you_snake['head']
        self._you_snake_body = you_snake['body']

    def visit(self, game_board: GameBoard):
        cell_area_counter = self.CellAreaCounter(game_board)

        head_directions = game_board.get_neighbour_cell_points_with_direction(self._you_snake_head['x'],
                                                                              self._you_snake_head['y'])
        point_id = 0
        for head_direction in head_directions:
            point = head_direction['point']
            cell_count = len(cell_area_counter.count(point))
            score = game_board.get_total_cells() - cell_count + 10000
            path = {
                'direction': head_direction['direction'],
                'point_type': PointType.AVAILABLE_AREA,
                'point_id': 'area-' + str(point_id),
                'distance': cell_count,
                'points': [point],
                'scores': [score],
                'final_score': score
            }

            game_board.add_path(path)

            point_id = point_id + 1

    class CellAreaCounter:

        def __init__(self, game_board: GameBoard):
            self._game_board = game_board

        def count(self, cell: (), cells=None):
            if cells is None:
                cells = set()

            if cell in cells:
                return cells

            if not self._game_board.is_cell_safe(cell[0], cell[1]):
                return cells

            cells.add(cell)

            next_cells = [
                (cell[0], cell[1] + 1),
                (cell[0], cell[1] - 1),
                (cell[0] + 1, cell[1]),
                (cell[0] - 1, cell[1])
            ]

            for next_cell in next_cells:
                self.count(next_cell, cells)

            return cells
