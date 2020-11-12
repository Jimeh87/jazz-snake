from jazz_snake.gameboard import GameBoard


class FoodLayer:

    def __init__(self, food: []):
        self._food = food

    def visit(self, game_board: GameBoard):
        # TODO: mark all food
        game_board.set_cell(self._food[0]['x'], self._food[0]['y'], game_board.CELL_OPTIMAL)
