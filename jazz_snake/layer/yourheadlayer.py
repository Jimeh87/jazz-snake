from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.simpledata import SimpleData


class YourHeadLayer:
    LIFE_CYCLE = LayerLifeCycle.DEBUG

    def __init__(self, you):
        self._you = you

    def visit(self, game_board: GameBoard):
        your_head = self._you['head']
        game_board.set_cell((your_head['x'], your_head['y']), CellDataType.YOUR_HEAD, SimpleData(True))
