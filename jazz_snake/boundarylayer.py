from classes.gameboard import GameBoard


class BoundaryLayer:

    def visit(self, game_board: GameBoard):
        for y in range(-1, game_board.get_height() + 1):
            game_board.set_cell(-1, y, game_board.CELL_SUICIDE_DANGER)
            game_board.set_cell(game_board.get_height(), y, game_board.CELL_SUICIDE_DANGER)

        for x in range(-1, game_board.get_width() + 1):
            game_board.set_cell(x, -1, game_board.CELL_SUICIDE_DANGER)
            game_board.set_cell(x, game_board.get_width(), game_board.CELL_SUICIDE_DANGER)
