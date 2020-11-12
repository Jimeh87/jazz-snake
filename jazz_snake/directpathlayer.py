from math import copysign

from classes.gameboard import GameBoard


class DirectPathLayer:

    def __init__(self, you_snake_head, food):
        self._you_snake_head = you_snake_head
        self._food = food

    def visit(self, game_board: GameBoard):
        bresenham_path = self.bresenham(self._you_snake_head['x'],
                                        self._you_snake_head['y'],
                                        self._food['x'],
                                        self._food['y'])

        if len(bresenham_path) == 0:
            print("BRESENHAM_PATH_EMPTY: ",
                  self._you_snake_head['x'],
                  self._you_snake_head['y'],
                  self._food['x'],
                  self._food['y'])

        safe_path = self.safe_direct_snake_path(game_board, bresenham_path)
        print(f"b path: {bresenham_path}")
        print(f"s path: {safe_path}")
        for cell in safe_path:
            game_board.increment_cell(cell['x'], cell['y'], game_board.CELL_OPTIMAL)

    @staticmethod
    def safe_direct_snake_path(game_board: GameBoard, bresenham_path):
        path = []
        previous = None

        for current in bresenham_path:
            if previous is None:
                # Snake head which is part of the path
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
                    if game_board.is_cell_safe(option['x'], option['y']):
                        safe_options.append(option)
                if len(safe_options) == 0:

                    return []
                path.extend(safe_options)

            if not game_board.is_cell_safe(current['x'], current['y']):
                return []
            path.append(current)

        return path

    @staticmethod
    def bresenham(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0

        xsign = 1 if dx > 0 else -1
        ysign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

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
