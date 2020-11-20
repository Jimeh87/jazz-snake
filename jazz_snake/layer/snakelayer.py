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
        head_x = self._snake['head']['x']
        head_y = self._snake['head']['y']
        game_board.set_cell(
            head_x,
            head_y,
            CellDataType.DEATH_THREAT_LEVEL,
            DeathThreatLevel.SUICIDE
        )

        # TODO I don't think I need this anymore
        # if self._you['id'] != self._snake['id'] and self._you['length'] <= self._snake['length']:
        #     game_board.set_cell(head_x + 1, head_y, CellDataType.DEATH_THREAT_LEVEL, DeathThreatLevel.EXTREME)
        #     game_board.set_cell(head_x - 1, head_y, CellDataType.DEATH_THREAT_LEVEL, DeathThreatLevel.EXTREME)
        #     game_board.set_cell(head_x, head_y + 1, CellDataType.DEATH_THREAT_LEVEL, DeathThreatLevel.EXTREME)
        #     game_board.set_cell(head_x, head_y - 1, CellDataType.DEATH_THREAT_LEVEL, DeathThreatLevel.EXTREME)

        snake_body = self._snake['body']
        for i in range(self._snake['length'] - 2):
            game_board.set_cell(
                snake_body[i]['x'],
                snake_body[i]['y'],
                CellDataType.DEATH_THREAT_LEVEL,
                DeathThreatLevel.SUICIDE
            )
