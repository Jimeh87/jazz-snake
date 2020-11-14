from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard


class FoodLayer:
    LIFE_CYCLE = LayerLifeCycle.GOALS

    def __init__(self, food: []):
        self._food = food

    def visit(self, game_board: GameBoard):
        for food_item in self._food:
            game_board.set_cell(food_item['x'], food_item['y'], CellDataType.GOAL, True)
