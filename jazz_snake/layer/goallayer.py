from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.goaltype import GoalType
from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.simpledata import SimpleData
from jazz_snake.board.stepdata import PointType


class GoalLayer:
    LIFE_CYCLE = LayerLifeCycle.GOALS

    def __init__(self, game_data):
        self._food = game_data['board']['food']
        self._you = game_data['you']
        self._snakes = game_data['board']['snakes']

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

        for snake in self._snakes:
            if snake['length'] < self._you['length']:
                points = self.find_lowest_overlapping_points(game_board, self._you['id'], snake['id'])
                for point in points:
                    game_board.add_goal({
                        'type': GoalType.HEAD_ATTACK,
                        'point': point
                    })

    def find_lowest_overlapping_points(self, game_board: GameBoard, snake1_id, snake2_id):
        lowest_distance = game_board.get_width() * game_board.get_height()
        points = []
        for x in range(game_board.get_width()):
            for y in range(game_board.get_height()):
                snake1_step = game_board.get_cell_steps((x, y)).get(PointType.SNAKE_HEAD, snake1_id)
                snake2_step = game_board.get_cell_steps((x, y)).get(PointType.SNAKE_HEAD, snake2_id)
                if snake1_step is not None and snake2_step is not None and snake1_step.distance == snake2_step.distance:
                    if snake1_step.distance == lowest_distance:
                        lowest_distance = snake1_step.distance
                        points.append((x, y))
                    elif snake1_step.distance < lowest_distance:
                        lowest_distance = snake1_step.distance
                        points = [(x, y)]

        return points


