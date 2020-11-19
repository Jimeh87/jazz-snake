from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard


class AreasLayer:

    LIFE_CYCLE = LayerLifeCycle.AREA_ANALYSIS

    def __init__(self, you_snake):
        self._you_snake_head = you_snake['head']
        self._you_snake_body = you_snake['body']

    def visit(self, game_board: GameBoard):
        cell_area_counter = self.CellAreaCounter(game_board)

        head_direction_points = list(map(
            lambda p: p['point'],
            game_board.get_neighbour_cell_points_with_direction(self._you_snake_head['x'], self._you_snake_head['y'])
        ))

        cell_areas = set()
        for head_direction_point in head_direction_points:
            cell_areas.add(frozenset(cell_area_counter.count(head_direction_point)))

        for cell_area in cell_areas:
            coverage = len(cell_area) / float(game_board.get_total_cells())

            for point in cell_area:
                game_board.set_cell(point[0], point[1], CellDataType.AVAILABLE_AREA, coverage)

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
