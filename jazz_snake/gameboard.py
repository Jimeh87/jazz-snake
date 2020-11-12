class GameBoard:
    CELL_OPTIMAL = -1
    CELL_SAFE = 0
    CELL_LOW_DANGER = 1
    CELL_HIGH_DANGER = 2
    CELL_EXTREME_DANGER = 3
    CELL_SUICIDE_DANGER = 4

    def __init__(self, height, width):
        self._height = height
        self._width = width
        self._board = self.create_board(height, width)

        self.create_board(height, width)

    def create_board(self, height, width):
        return [[self.CELL_SAFE for y in range(height + 2)] for x in range(width + 2)]

    def get_height(self):
        return self._height

    def get_width(self):
        return self._width

    def get_cell(self, x, y):
        return self._board[x + 1][y + 1]

    def get_cell_above(self, x, y):
        return self.get_cell(x, y + 1)

    def get_cell_below(self, x, y):
        return self.get_cell(x, y - 1)

    def get_cell_left(self, x, y):
        return self.get_cell(x - 1, y)

    def get_cell_right(self, x, y):
        return self.get_cell(x + 1, y)

    def set_cell(self, x, y, value):
        self._board[x + 1][y + 1] = value

    def increment_cell(self, x, y, amount):
        self.set_cell(x, y, self.get_cell(x, y) + amount)

    def is_cell_safe(self, x, y):
        return self.get_cell(x, y) < self.CELL_LOW_DANGER

    def get_total_cells(self):
        return self._height * self._width

    def accept_layer(self, layer):
        layer.visit(self)

    def print(self):
        output = ''
        for y in reversed(range(-1, self.get_height() + 1)):
            for x in range(-1, self.get_width() + 1):
                cell = self.get_cell(x, y)
                padding = ''
                if cell > -1:
                    padding = ' '
                output += padding + str(cell)
            output += '\n'
        print(output)
