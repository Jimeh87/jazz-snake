from jazz_snake.board.gameboard import GameBoard
from jazz_snake.board.layerlifecycle import LayerLifeCycle


class SnakeListenerLayer:
    LIFE_CYCLE = LayerLifeCycle.DEBUG

    def __init__(self, snakes):
        self._snakes = snakes

    def visit(self, game_board: GameBoard):
        print("Snake shouts")
        print("============")
        for snake in self._snakes:
            print(f"{snake['name']}: {snake['shout']}")
