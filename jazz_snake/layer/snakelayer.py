from jazz_snake.board.celldatatype import CellDataType
from jazz_snake.board.deaththreatdata import DeathThreatData, DeathThreatLevel
from jazz_snake.board.gameboard import GameBoard, RelativePoint
from jazz_snake.board.layerlifecycle import LayerLifeCycle


class SnakeLayer:
    LIFE_CYCLE = LayerLifeCycle.DEATH_THREAT_ANALYSIS

    def __init__(self, snake, you):
        self._snake = snake
        self._you = you

    def visit(self, game_board: GameBoard):
        head_x = self._snake['head']['x']
        head_y = self._snake['head']['y']
        game_board.set_cell((head_x, head_y),
                            CellDataType.DEATH_THREAT_LEVEL,
                            DeathThreatData(DeathThreatLevel.SUICIDE))

        if self._you['id'] != self._snake['id'] and self._you['length'] <= self._snake['length']:
            for head_direction in RelativePoint.get_neighbour_points((head_x, head_y)):
                game_board.set_cell(head_direction,
                                    CellDataType.DEATH_THREAT_LEVEL,
                                    DeathThreatData(DeathThreatLevel.SUICIDE, 1))

        snake_body = self._snake['body']
        for i in range(self._snake['length'] - 1):
            game_board.set_cell((snake_body[i]['x'], snake_body[i]['y']),
                                CellDataType.DEATH_THREAT_LEVEL,
                                DeathThreatData(DeathThreatLevel.SUICIDE, self._snake['length'] - i))
