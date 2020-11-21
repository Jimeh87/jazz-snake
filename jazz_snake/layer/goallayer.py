from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.goaltype import GoalType
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.simpledata import SimpleData


class GoalLayer:
    LIFE_CYCLE = LayerLifeCycle.GOALS

    def __init__(self, game_data):
        self._food = game_data['board']['food']
        self._you = game_data['you']

    def visit(self, game_board: GameBoard):
        for food_item in self._food:
            food_point = (food_item['x'], food_item['y'])
            game_board.add_goal({
                'type': GoalType.FOOD,
                'point': food_point
            })
            game_board.set_cell(food_point, CellDataType.FOOD, SimpleData(True))

        tail = self._you['body'][-1]
        game_board.add_goal({
            'type': GoalType.TAIL,
            'point': (tail['x'], tail['y'])
        })

        game_board.add_goal({
            'type': GoalType.CENTER,
            'point': (int(game_board.get_width() / 2), int(game_board.get_height() / 2))
        })
