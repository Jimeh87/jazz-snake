from math import copysign

from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.simpledata import SimpleData


class DirectPathLayer:

    LIFE_CYCLE = LayerLifeCycle.PATHING

    def __init__(self, you_snake_head, food):
        self._you_snake_head = you_snake_head
        self._food = food

    def visit(self, game_board: GameBoard):
        bresenham_path = self.bresenham(self._you_snake_head['x'],
                                        self._you_snake_head['y'],
                                        self._food['x'],
                                        self._food['y'])

        steps, safe_path = self.safe_direct_snake_path(game_board, bresenham_path)

        for cell in safe_path:
            game_board.set_cell((cell['x'], cell['y']), CellDataType.DESIRED_PATH, SimpleData(steps))

    @staticmethod
    def safe_direct_snake_path(game_board: GameBoard, bresenham_path) -> (int, []):
        steps = 0
        path = []
        previous = None

        for current in bresenham_path:
            if previous is None:
                previous = current
                continue

            difference = (current['x'] + current['y']) - (previous['x'] + previous['y'])
            if abs(difference) == 2:
                increment = int(copysign(1, difference))
                options = [
                    {'x': previous['x'] + increment, 'y': previous['y']},
                    {'x': previous['x'], 'y': previous['y'] + increment}
                ]

                safe_options = []
                for option in options:
                    if game_board.get_cell_death_threat((option['x'], option['y'])).is_cell_safe():
                        safe_options.append(option)
                if len(safe_options) == 0:
                    return 0, []

                steps += 1
                path.extend(safe_options)

            if not game_board.get_cell_death_threat((current['x'], current['y'])).is_cell_safe():
                return 0, []

            steps += 1
            path.append(current)

        return steps, path

    @staticmethod
    def bresenham(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0

        x_sign = 1 if dx > 0 else -1
        y_sign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = x_sign, 0, 0, y_sign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, y_sign, x_sign, 0

        d = 2 * dy - dx
        y = 0

        path = []
        for x in range(dx + 1):
            path.append({'x': x0 + x * xx + y * yx, 'y': y0 + x * xy + y * yy})
            if d >= 0:
                y += 1
                d -= 2 * dx
            d += 2 * dy

        return path
