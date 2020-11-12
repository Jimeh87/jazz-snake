from classes.gameboard import GameBoard


class SnakeLayer:

    def __init__(self, snake):
        self._snake = snake

    def visit(self, game_board: GameBoard):
        game_board.set_cell(self._snake['head']['x'], self._snake['head']['y'], game_board.CELL_SUICIDE_DANGER)
        snake_body = self._snake['body']
        for i in range(self._snake['length']):
            game_board.set_cell(snake_body[i]['x'], snake_body[i]['y'], game_board.CELL_SUICIDE_DANGER)
