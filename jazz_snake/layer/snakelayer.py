from jazz_snake.board.layerlifecycle import LayerLifeCycle
from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.deaththreatlevel import DeathThreatLevel
from jazz_snake.board.gameboard import GameBoard


class SnakeLayer:

    LIFE_CYCLE = LayerLifeCycle.DEATH_THREAT_ANALYSIS

    def __init__(self, snake, you):
        self._snake = snake
        self._you = you

    def visit(self, game_board: GameBoard):
        # TODO More advanced stuff around danger for head
        game_board.set_cell(
            self._snake['head']['x'],
            self._snake['head']['y'],
            CellDataType.DEATH_THREAT_LEVEL,
            DeathThreatLevel.SUICIDE
        )

        snake_body = self._snake['body']
        for i in range(self._snake['length']):
            game_board.set_cell(
                snake_body[i]['x'],
                snake_body[i]['y'],
                CellDataType.DEATH_THREAT_LEVEL,
                DeathThreatLevel.SUICIDE
            )
