from jazz_snake.gameboard import GameBoard


class AvailableMovesLayer:

    def __init__(self, you_snake):
        self._you_snake_head = you_snake['head']
        self._you_snake_body = you_snake['body']

    def visit(self, game_board: GameBoard):
        cell_area_counter = self.CellAreaCounter(game_board)

        head_direction_cells = [
            {'x': self._you_snake_head['x'], 'y': self._you_snake_head['y'] + 1},
            {'x': self._you_snake_head['x'], 'y': self._you_snake_head['y'] - 1},
            {'x': self._you_snake_head['x'] + 1, 'y': self._you_snake_head['y']},
            {'x': self._you_snake_head['x'] - 1, 'y': self._you_snake_head['y']}
        ]

        cell_areas = set()
        for head_direction_cell in head_direction_cells:
            cell_areas.add(frozenset(cell_area_counter.count((head_direction_cell['x'], head_direction_cell['y']))))

        for cell_area in cell_areas:
            coverage = len(cell_area) / float(game_board.get_total_cells())

            cell_safety = None
            if coverage < .1:
                cell_safety = GameBoard.CELL_EXTREME_DANGER
            elif coverage < .2:
                cell_safety = GameBoard.CELL_HIGH_DANGER
            elif coverage < .1:
                cell_safety = GameBoard.CELL_LOW_DANGER

            if cell_safety is not None:
                for cell in cell_area:
                    game_board.set_cell(cell[0], cell[1], cell_safety)

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
